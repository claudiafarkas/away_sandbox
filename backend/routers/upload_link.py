import re
import json
import hashlib
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from data.postgres import engine
from services.link_processing_service import geocode_name
from utils.config import get_google_api_key

router = APIRouter(tags=["upload_link"])
logger = logging.getLogger(__name__)


class UploadLinkRequest(BaseModel):
    url: str
    caption: str | None = None


MOCK_SCENARIOS = [
    {
        "caption": "A beautiful day exploring the streets of Paris! Cafe hopping, museums, and golden-hour views.",
        "thumbnailUrl": "https://example.com/mock_thumbnail_paris.jpg",
        "videoUrl": "https://example.com/mock_video_paris.mp4",
        "locations": [
            {
                "name": "Eiffel Tower",
                "address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
                "city": "Paris",
                "country": "France",
                "lat": 48.8584,
                "lng": 2.2945,
            },
            {
                "name": "Louvre Museum",
                "address": "Rue de Rivoli, 75001 Paris, France",
                "city": "Paris",
                "country": "France",
                "lat": 48.8606,
                "lng": 2.3376,
            },
        ],
    },
    {
        "caption": "Street food crawl across Mexico City neighborhoods with a sunset walk through Roma Norte.",
        "thumbnailUrl": "https://example.com/mock_thumbnail_mexico.jpg",
        "videoUrl": "https://example.com/mock_video_mexico.mp4",
        "locations": [
            {
                "name": "Mexico City",
                "address": "Mexico City, CDMX, Mexico",
                "city": "Mexico City",
                "country": "Mexico",
                "lat": 19.4326,
                "lng": -99.1332,
            },
            {
                "name": "Roma Norte",
                "address": "Roma Norte, Cuauhtemoc, Mexico City, CDMX, Mexico",
                "city": "Mexico City",
                "country": "Mexico",
                "lat": 19.4146,
                "lng": -99.1678,
            },
        ],
    },
    {
        "caption": "A calm Kyoto itinerary: hidden temples, old lanes in Gion, and late ramen stops.",
        "thumbnailUrl": "https://example.com/mock_thumbnail_kyoto.jpg",
        "videoUrl": "https://example.com/mock_video_kyoto.mp4",
        "locations": [
            {
                "name": "Kyoto",
                "address": "Kyoto, Japan",
                "city": "Kyoto",
                "country": "Japan",
                "lat": 35.0116,
                "lng": 135.7681,
            },
            {
                "name": "Gion",
                "address": "Gionmachi, Higashiyama Ward, Kyoto, Japan",
                "city": "Kyoto",
                "country": "Japan",
                "lat": 35.0037,
                "lng": 135.7751,
            },
        ],
    },
]


def _pick_scenario(url: str) -> dict:
    seed = int(hashlib.sha256(url.encode("utf-8")).hexdigest(), 16)
    return MOCK_SCENARIOS[seed % len(MOCK_SCENARIOS)]


def _enrich_locations_with_geocoding(locations: list[dict]) -> list[dict]:
    api_key = get_google_api_key()
    if not api_key:
        return locations

    enriched: list[dict] = []
    for location in locations:
        geocoded = geocode_name(location["name"], api_key)
        if geocoded:
            enriched.append(
                {
                    "name": geocoded["name"],
                    "address": geocoded["address"],
                    "city": geocoded["city"],
                    "country": geocoded["country"],
                    "lat": geocoded["lat"],
                    "lng": geocoded["lng"],
                }
            )
        else:
            enriched.append(location)
    return enriched


def _store_ingestion_result(payload: dict) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS mocked_link_ingestions (
                    id BIGSERIAL PRIMARY KEY,
                    source_url TEXT NOT NULL,
                    caption TEXT NOT NULL,
                    video_url TEXT,
                    thumbnail_url TEXT,
                    payload JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )

        conn.execute(
            text(
                """
                INSERT INTO mocked_link_ingestions (source_url, caption, video_url, thumbnail_url, payload)
                VALUES (:source_url, :caption, :video_url, :thumbnail_url, CAST(:payload AS JSONB))
                """
            ),
            {
                "source_url": payload["sourceUrl"],
                "caption": payload["caption"],
                "video_url": payload["videoUrl"],
                "thumbnail_url": payload["thumbnailUrl"],
                "payload": json.dumps(payload),
            },
        )


def _is_valid_instagram_url(url: str) -> bool:
    pattern = re.compile(r"^https?://(www\.)?instagram\.com/(p|reel|tv)/[A-Za-z0-9_-]+/?")
    return bool(pattern.match(url.strip()))


@router.post("/upload_link")
def upload_link(req: UploadLinkRequest) -> dict:
    """
    Mock scraper endpoint for metadata-only ingestion.

    Body:
        url      - required Instagram link
        caption  - optional user-provided caption override

    Returns:
        structured mock payload to simulate upstream ingestion
    """
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="'url' is required")
    if not _is_valid_instagram_url(url):
        raise HTTPException(status_code=400, detail="Please provide a valid Instagram post/reel URL")

    scenario = _pick_scenario(url)
    caption = req.caption.strip() if req.caption and req.caption.strip() else scenario["caption"]
    enriched_locations = _enrich_locations_with_geocoding(scenario["locations"])

    payload = {
        "caption": caption,
        "sourceUrl": url,
        "videoUrl": scenario["videoUrl"],
        "thumbnailUrl": scenario["thumbnailUrl"],
        "locations": enriched_locations,
    }

    try:
        _store_ingestion_result(payload)
    except Exception as exc:
        logger.warning("Failed to store ingestion result in Postgres: %s", exc)

    return payload
