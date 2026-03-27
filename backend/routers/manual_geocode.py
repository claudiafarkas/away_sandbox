import os
import re

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["manual_geocode"])

GOOGLE_API_KEY = os.getenv("BACKEND_GOOGLE_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")


class ManualGeocodeRequest(BaseModel):
    address: str


@router.post("/geocode_address")
def geocode_address(req: ManualGeocodeRequest):
    address = (req.address or "").strip()
    if not address:
        raise HTTPException(status_code=400, detail="Missing 'address'")
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Google Maps API key not configured")

    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": address, "key": GOOGLE_API_KEY},
            timeout=15,
        )
        data = resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Geocoding request failed: {e}")

    status = data.get("status")
    results = data.get("results", [])
    if status != "OK" or not results:
        raise HTTPException(status_code=400, detail=f"Geocoding failed: {status}")

    place = results[0]
    loc = place["geometry"]["location"]
    formatted = place.get("formatted_address", address)

    parts = [p.strip() for p in formatted.split(",")]
    country = parts[-1] if len(parts) >= 1 else ""
    city_raw = parts[-2] if len(parts) >= 2 else ""
    city = re.sub(r"^\d+\s*", "", city_raw)

    return {
        "name": address,
        "address": formatted,
        "city": city,
        "country": country,
        "lat": loc["lat"],
        "lng": loc["lng"],
        "place_id": place.get("place_id"),
    }


# Compatibility alias
@router.post("/manual_geocode", include_in_schema=False)
def manual_geocode_alias(req: ManualGeocodeRequest):
    return geocode_address(req)
