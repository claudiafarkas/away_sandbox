# Away Sandbox

Away Sandbox is a full‑stack learning lab for mock social link ingestion, geospatial parsing output, and backend/data pipeline experimentation.

It serves as an experimental subtree of the main Away iOS app, allowing rapid prototyping of data engineering, ML engineering, and AI workflows without affecting the production mobile codebase.

## Learning Goals

This project exists to provide a safe, modular environment for practicing:

*Data Engineering*

* Building ingestion endpoints and structured persistence layers
* Designing schemas and transformations (Postgres + DuckDB)
* Experimenting with orchestration tools (Airflow)
* Running distributed or batch processing jobs (Spark)

*ML / AI Engineering*

* Extracting and enriching location metadata
* Preparing data for embeddings and vector search
* Building RAG‑style pipelines for itinerary generation
* Experimenting with geospatial clustering and analytics

*Backend Engineering*

* Designing clean FastAPI services
* Implementing modular routers and service layers
* Managing environment configs and containerized services
* Building production‑shaped API contracts

**The sandbox intentionally uses mock ingestion to focus on the engineering layers that matter for long‑term career growth.**

## Current Functionality

Implemented features in the current app:

- Mock Instagram link ingestion from the Home page
- Production-shaped parsed response payloads from backend
- Parsed location objects with name/address/city/country/lat/lng
- Save parsed imports to Postgres via API
- Load saved imports on Imported Videos page
- Backend DB health endpoint surfaced in frontend badges
- Manual caption input and sample JSON import support

## Tech Stack

- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Pydantic + SQLAlchemy
- Databases: Postgres (primary persistence), DuckDB (analytics sandbox)

## Project Structure

```text
away_sandbox/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                    # Home ingest + parse card + save action
│   │   └── imported-videos/page.tsx    # Saved imports view
│   └── lib/imported-videos.ts          # Shared frontend import types
├── backend/
│   ├── main.py                         # FastAPI app and router wiring
│   ├── routers/
│   │   ├── upload_link.py              # Mock parse payload endpoint
│   │   ├── imports.py                  # save/list/db_health endpoints
│   │   └── manual_geocode.py           # address geocoding endpoint
│   ├── data/postgres.py                # SQLAlchemy engine/session
│   └── services/link_processing_service.py
├── docker-compose.yml
└── README.md
```

## API Endpoints

**POST /upload_link:** Validates Instagram-style URL and returns mock parsed payload that matches the real backend contract:

```json
{
      "caption": "A beautiful day exploring the streets of Paris!",
      "sourceUrl": "https://www.instagram.com/reel/xyz123/",
      "videoUrl": "https://example.com/mock_video_paris.mp4",
      "thumbnailUrl": "https://example.com/mock_thumbnail_paris.jpg",
      "locations": [
            {
                  "name": "Eiffel Tower",
                  "address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
                  "city": "Paris",
                  "country": "France",
                  "lat": 48.8584,
                  "lng": 2.2945
            }
      ]
}
```

**POST /api/save_import:** Saves parsed results into Postgres table `imports`.

**GET /api/imports:** Returns saved imports grouped for frontend cards (with mock thumbnail and timestamp).

**GET /api/db_health:** Returns Postgres connectivity status:

```json
{ "ok": true, "database": "postgres" }
```

**POST /geocode_address:** Manual geocoding endpoint backed by Google Geocoding API.

## Database Schema

Table auto-created by backend when first saving/listing imports:

`imports (id, caption, source_url, lat, lng, city, country, created_at)`

## Local Setup

### 1. Start Postgres (required for save/list imports)

From repository root:

```bash
docker compose up -d postgres
```

Verify:

```bash
docker compose ps
```

### 2. Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --app-dir . --host 0.0.0.0 --port 8001
```

Backend URL: `http://127.0.0.1:8001`

### 3. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## Environment Variables

Use `backend/.env` for local backend settings:

```env
DATABASE_URL=postgresql://away:away@localhost:5432/away_sandbox
POSTGRES_USER=away
POSTGRES_PASSWORD=away
POSTGRES_DB=away_sandbox
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DUCKDB_PATH=./data/analytics.duckdb

# Optional for geocode enrichment endpoints
BACKEND_GOOGLE_API_KEY=your_google_maps_api_key
```

For frontend API base URL (optional), use `frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001
```

## User Flow

1. Paste Instagram link on Home page
2. Optionally provide manual caption
3. Click Ingest to receive parsed mock payload
4. Click Add to Imported Videos to persist in Postgres
5. Open Imported Videos page to view saved records

## Notes

- This project intentionally uses mock ingestion (no scraping providers).
- If Postgres is down, save/list endpoints will fail until DB is started.
- DB connectivity is shown in the frontend as a status badge.
