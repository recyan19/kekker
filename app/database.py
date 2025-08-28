"""Database configuration and session management for FastAPI CRUD app."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


SQL_ALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:"
                            f"{settings.database_password}@"
                            f"{settings.database_hostname}:"
                            f"{settings.database_port}/"
                            f"{settings.database_name}"
)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
