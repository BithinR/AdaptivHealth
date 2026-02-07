"""
Test configuration and fixtures for AdaptivHealth backend tests.
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment variables before importing app modules
os.environ["SECRET_KEY"] = "test-secret-key-for-unit-tests-only-32chars!"
os.environ["DATABASE_URL"] = "sqlite:///./test_adaptiv_health.db"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "false"

from app.database import Base
from app.services.auth_service import AuthService


@pytest.fixture
def auth_service():
    """Provide a fresh AuthService instance."""
    return AuthService()


@pytest.fixture
def test_db():
    """Create a temporary test database."""
    engine = create_engine(
        "sqlite:///./test_adaptiv_health.db",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
