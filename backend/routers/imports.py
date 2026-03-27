from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from data.postgres import engine

router = APIRouter(tags=["imports"])


class SaveImportLocation(BaseModel):
    city: str | None = None
    country: str | None = None
    lat: float | None = None
    lng: float | None = None


class SaveImportRequest(BaseModel):
    caption: str
    sourceUrl: str
    locations: list[SaveImportLocation] = []


def _ensure_imports_table() -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS imports (
                    id BIGSERIAL PRIMARY KEY,
                    caption TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    lat DOUBLE PRECISION,
                    lng DOUBLE PRECISION,
                    city TEXT,
                    country TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )


def _thumbnail_for_source(source_url: str) -> str:
    placeholders = [
        "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?auto=format&fit=crop&w=900&q=80",
    ]
    idx = abs(hash(source_url)) % len(placeholders)
    return placeholders[idx]


@router.post("/api/save_import")
def save_import(req: SaveImportRequest) -> dict[str, Any]:
    if not req.caption.strip():
        raise HTTPException(status_code=400, detail="caption is required")
    if not req.sourceUrl.strip():
        raise HTTPException(status_code=400, detail="sourceUrl is required")

    try:
        _ensure_imports_table()

        rows_to_insert = req.locations or [SaveImportLocation()]

        with engine.begin() as conn:
            for loc in rows_to_insert:
                conn.execute(
                    text(
                        """
                        INSERT INTO imports (caption, source_url, lat, lng, city, country)
                        VALUES (:caption, :source_url, :lat, :lng, :city, :country)
                        """
                    ),
                    {
                        "caption": req.caption,
                        "source_url": req.sourceUrl,
                        "lat": loc.lat,
                        "lng": loc.lng,
                        "city": loc.city,
                        "country": loc.country,
                    },
                )

        return {
            "saved": len(rows_to_insert),
            "sourceUrl": req.sourceUrl,
            "caption": req.caption,
            "createdAt": datetime.utcnow().isoformat() + "Z",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save import: {exc}")


@router.get("/api/imports")
def list_imports() -> dict[str, Any]:
    try:
        _ensure_imports_table()

        with engine.begin() as conn:
            rows = conn.execute(
                text(
                    """
                    SELECT id, caption, source_url, lat, lng, city, country, created_at
                    FROM imports
                    ORDER BY created_at DESC
                    """
                )
            ).mappings().all()

        grouped: dict[str, dict[str, Any]] = {}
        for row in rows:
            key = f"{row['source_url']}|{row['caption']}|{row['created_at']}"
            if key not in grouped:
                grouped[key] = {
                    "id": row["id"],
                    "caption": row["caption"],
                    "sourceUrl": row["source_url"],
                    "thumbnailUrl": _thumbnail_for_source(row["source_url"]),
                    "createdAt": row["created_at"].isoformat() if row["created_at"] else None,
                    "locations": [],
                }

            if row["city"] or row["country"] or row["lat"] is not None or row["lng"] is not None:
                grouped[key]["locations"].append(
                    {
                        "name": row["city"] or row["country"] or "Location",
                        "address": "",
                        "city": row["city"] or "",
                        "country": row["country"] or "",
                        "lat": row["lat"],
                        "lng": row["lng"],
                    }
                )

        return {"imports": list(grouped.values())}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to list imports: {exc}")


@router.get("/api/db_health")
def db_health() -> dict[str, Any]:
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
        return {"ok": True, "database": "postgres"}
    except Exception as exc:
        return {
            "ok": False,
            "database": "postgres",
            "detail": str(exc),
        }
