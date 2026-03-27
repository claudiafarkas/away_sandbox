import os


def get_settings() -> dict:
    # TODO: Replace with pydantic-settings based config model.
    return {
        "postgres_host": os.getenv("POSTGRES_HOST", "localhost"),
        "postgres_port": os.getenv("POSTGRES_PORT", "5432"),
        "postgres_user": os.getenv("POSTGRES_USER", "away"),
        "postgres_db": os.getenv("POSTGRES_DB", "away_sandbox"),
        "duckdb_path": os.getenv("DUCKDB_PATH", "./data/analytics.duckdb"),
    }
