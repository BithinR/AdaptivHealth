"""
Shared test fixtures for AdaptivHealth.
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set environment variables BEFORE importing app modules
os.environ.setdefault("SECRET_KEY", "test-secret-key-thats-long-enough-32chars")
os.environ.setdefault("PHI_ENCRYPTION_KEY", "dGVzdC1lbmNyeXB0aW9uLWtleS0zMmJ5dGVzISEhISE=")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_adaptivhealth.db")

from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient


# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test_adaptivhealth.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
