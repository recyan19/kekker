""" Tests for Users API """

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from app.database import Base, get_db


SQL_ALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:"
                            f"{settings.database_password}@"
                            f"{settings.database_hostname}:"
                            f"{settings.database_port}/"
                            f"{settings.database_name}_test"
)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    """ Database fixture """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):  # type: ignore pylint: disable=redefined-outer-name
    """ Client fixture"""
    def override_get_db():  # type: ignore
        try:
            yield session
        finally:
            session.close()  # type: ignore
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
