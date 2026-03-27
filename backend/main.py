import os

# Load .env in local development only; Cloud Run provides env vars directly
if os.getenv("ENV", "dev") == "dev":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.geospatial_insights import router as geospatial_insights_router
from routers.imports import router as imports_router
from routers.manual_geocode import router as manual_geocode_router
from routers.processed_data import router as processed_data_router
from routers.rag_itinerary import router as rag_itinerary_router
from routers.upload_link import router as upload_link_router

app = FastAPI(
    title="Away Sandbox API",
    version="0.1.0",
    description="Scaffolded API for Away Sandbox",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_link_router)
app.include_router(imports_router)
app.include_router(manual_geocode_router)
app.include_router(processed_data_router)
app.include_router(geospatial_insights_router)
app.include_router(rag_itinerary_router)


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "away-sandbox-backend"}
