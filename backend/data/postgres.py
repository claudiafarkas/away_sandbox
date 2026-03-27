import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://away:away@localhost:5432/away_sandbox",
)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db_session():
    # TODO: Add context-managed session handling and retries.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
