# Away Sandbox

A scaffolded full-stack web sandbox for link ingestion, geospatial insight exploration, and AI itinerary experimentation.

## Project Structure

```text
away_sandbox/
├── frontend/                # Next.js + Tailwind frontend
├── backend/                 # FastAPI backend
│   ├── routers/             # API routers
│   ├── services/            # Business service placeholders
│   ├── data/                # Data access and analytics files
│   ├── models/              # Pydantic/domain model placeholders
│   └── utils/               # Utility/config helpers
├── docker-compose.yml
└── README.md
```

## Quick Start

### 1. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at `http://localhost:8000`.

### 3. Docker Compose

```bash
docker compose up --build
```

Services:
- Backend API: `http://localhost:8000`
- Postgres: `localhost:5432`
- pgAdmin: `http://localhost:5050`

## Environment Variables

Create a `.env` file at repository root (or export these values):

```env
POSTGRES_USER=away
POSTGRES_PASSWORD=away
POSTGRES_DB=away_sandbox
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql://away:away@postgres:5432/away_sandbox
DUCKDB_PATH=./data/analytics.duckdb
```

## Architecture Diagram (Placeholder)

```text
[ Next.js Frontend ]
         |
         v
[ FastAPI Backend ] ---> [ Postgres ]
         |
         v
      [ DuckDB ]
```

## Notes

- This repository currently contains scaffolding only.
- Business logic is intentionally not implemented yet.
- API route handlers contain TODO placeholders.
