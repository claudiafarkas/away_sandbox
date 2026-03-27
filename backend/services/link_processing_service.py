import os
import re

import requests

# spaCy model: try transformer first, fall back to small
try:
    import spacy
    try:
        _nlp = spacy.load("en_core_web_trf")
    except Exception:
        _nlp = spacy.load("en_core_web_sm")
except Exception as e:
    raise RuntimeError(
        "No spaCy model found. Run: python -m spacy download en_core_web_sm"
    ) from e


def extract_shortcode(url: str) -> str | None:
    """Extract Instagram shortcode from a reel/post/tv URL."""
    match = re.search(r"(?:/reel/|/p/|/tv/)([A-Za-z0-9_-]{5,})", url)
    return match.group(1) if match else None


def get_location_data(text: str) -> list[str]:
    """
    Extract likely place mentions from text using spaCy NER.
    Keeps only short GPE/LOC/FAC spans and groups near-adjacent entities.
    """
    doc = _nlp(text)
    ents = [
        e for e in doc.ents
        if e.label_ in ("GPE", "LOC", "FAC")
        and len(e.text.split()) <= 5
        and not any(char in e.text for char in "#|")
    ]
    ents = sorted(ents, key=lambda e: e.start_char)

    # Group entities that are within 5 characters of each other
    groups: list[list] = []
    for ent in ents:
        if not groups:
            groups.append([ent])
        else:
            prev = groups[-1][-1]
            if ent.start_char - prev.end_char <= 5:
                groups[-1].append(ent)
            else:
                groups.append([ent])

    spans: list[str] = []
    for grp in groups:
        start = grp[0].start_char
        end = grp[-1].end_char
        span_text = text[start:end].strip().strip(",")
        if span_text and span_text not in spans:
            spans.append(span_text)
    return spans


def geocode_name(name: str, api_key: str) -> dict | None:
    """Geocode a place name via Google Geocoding API."""
    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": name, "key": api_key},
            timeout=15,
        )
        data = resp.json()
    except requests.RequestException:
        return None

    if data.get("status") != "OK" or not data.get("results"):
        return None

    place = data["results"][0]
    full_address = place["formatted_address"]
    parts = [p.strip() for p in full_address.split(",")]
    country = parts[-1] if len(parts) >= 1 else ""
    city_raw = parts[-2] if len(parts) >= 2 else ""
    city = re.sub(r"^\d+\s*", "", city_raw)

    return {
        "name": name,
        "address": full_address,
        "city": city,
        "country": country,
        "lat": place["geometry"]["location"]["lat"],
        "lng": place["geometry"]["location"]["lng"],
    }


def dedupe_locations(locations: list[dict]) -> list[dict]:
    """Remove duplicate locations by (name, address) and filter '#' / '|' names."""
    filtered: list[dict] = []
    seen: set[tuple] = set()
    for loc in locations:
        name = loc["name"]
        if "#" in name or "|" in name:
            continue
        key = (name.lower(), loc["address"].lower())
        if key in seen:
            continue
        seen.add(key)
        filtered.append(loc)
    return filtered
