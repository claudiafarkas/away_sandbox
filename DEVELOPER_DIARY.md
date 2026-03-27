# Developer Diary

This file is a running journal of what I learned, what I built, what broke, and what I want to improve while working on Away Sandbox.

---

## Entries

### March 27, 2026

#### What I worked on

- Built a mock Instagram ingestion flow for the Away Sandbox project.
- Added backend endpoints for mock parsing, saving imports, listing imports, and checking DB health.
- Connected the frontend Home page and Imported Videos page to the backend.

#### What I learned

- A mock ingestion flow is enough to test backend architecture, persistence, and UI behavior without relying on scraping.
- Returning a production-shaped mock payload makes frontend development much easier because the contract stays realistic.
- Postgres-backed persistence is more useful for this sandbox than purely local browser storage.

#### Technical notes

- Main ingestion endpoint: `/upload_link`
- Save imports endpoint: `/api/save_import`
- Imports listing endpoint: `/api/imports`
- DB health endpoint: `/api/db_health`
- Postgres runs through `docker compose up -d postgres`

#### Next steps

- Implement the rest of the leanring pipeline: **Airflow → Spark → dbt → RAG → geospatial.**
