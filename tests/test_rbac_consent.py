"""
Tests for RBAC enforcement, consent workflow, and admin password reset.

Verifies:
- Admin blocked from PHI endpoints
- Clinician consent checks
- Patient consent state machine
- Admin password reset for users
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("SECRET_KEY", "test-secret-key-thats-long-enough-32chars")
os.environ.setdefault("PHI_ENCRYPTION_KEY", "dGVzdC1lbmNyeXB0aW9uLWtleS0zMmJ5dGVzISEhISE=")
os.environ.setdefault("DEBUG", "true")

from app.database import Base, get_db
from app.main import app
from app.models.user import UserRole

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rbac_consent.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    # Re-apply the override in case another test file changed it
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def register_user(client, email, password, name, role=None):
    """Register a user and return the response data."""
    payload = {"email": email, "password": password, "name": name}
    if role:
        payload["role"] = role
    resp = client.post("/api/v1/register", json=payload)
    return resp.json()


def login_user(client, email, password):
    """Login and return the access token."""
    resp = client.post("/api/v1/login", data={"username": email, "password": password})
    assert resp.status_code == 200, f"Login failed: {resp.json()}"
    return resp.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


class TestAdminBlockedFromPHI:
    """Admin users must NOT access PHI endpoints (vitals, alerts/user, risk, recommendations)."""

    def test_admin_blocked_from_user_vitals(self, client):
        register_user(client, "admin@test.com", "Admin1234", "Admin", role="admin")
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        token = login_user(client, "admin@test.com", "Admin1234")

        resp = client.get("/api/v1/vitals/user/2/latest", headers=auth_header(token))
        assert resp.status_code == 403

    def test_admin_blocked_from_user_alerts(self, client):
        register_user(client, "admin@test.com", "Admin1234", "Admin", role="admin")
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        token = login_user(client, "admin@test.com", "Admin1234")

        resp = client.get("/api/v1/alerts/user/2", headers=auth_header(token))
        assert resp.status_code == 403

    def test_admin_blocked_from_alert_stats(self, client):
        register_user(client, "admin@test.com", "Admin1234", "Admin", role="admin")
        token = login_user(client, "admin@test.com", "Admin1234")

        resp = client.get("/api/v1/alerts/stats", headers=auth_header(token))
        assert resp.status_code == 403

    def test_admin_blocked_from_patient_activities(self, client):
        register_user(client, "admin@test.com", "Admin1234", "Admin", role="admin")
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        token = login_user(client, "admin@test.com", "Admin1234")

        resp = client.get("/api/v1/activities/user/2", headers=auth_header(token))
        assert resp.status_code == 403


class TestConsentWorkflow:
    """Patient consent state machine and clinician review."""

    def test_patient_can_request_disable(self, client):
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        token = login_user(client, "patient@test.com", "Patient1234")

        resp = client.post(
            "/api/v1/consent/disable",
            json={"reason": "I want privacy"},
            headers=auth_header(token)
        )
        assert resp.status_code == 200

        # Check status
        resp = client.get("/api/v1/consent/status", headers=auth_header(token))
        assert resp.json()["share_state"] == "SHARING_DISABLE_REQUESTED"

    def test_duplicate_disable_request_rejected(self, client):
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        token = login_user(client, "patient@test.com", "Patient1234")

        client.post("/api/v1/consent/disable", json={}, headers=auth_header(token))

        resp = client.post("/api/v1/consent/disable", json={}, headers=auth_header(token))
        assert resp.status_code == 400

    def test_clinician_can_approve_disable(self, client):
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        register_user(client, "doc@test.com", "Doctor1234", "Doctor", role="clinician")

        pat_token = login_user(client, "patient@test.com", "Patient1234")
        doc_token = login_user(client, "doc@test.com", "Doctor1234")

        # Patient requests disable
        client.post("/api/v1/consent/disable", json={}, headers=auth_header(pat_token))

        # Clinician sees pending
        resp = client.get("/api/v1/consent/pending", headers=auth_header(doc_token))
        assert resp.status_code == 200
        assert len(resp.json()["pending_requests"]) == 1

        # Clinician approves
        patient_id = resp.json()["pending_requests"][0]["user_id"]
        resp = client.post(
            f"/api/v1/consent/{patient_id}/review",
            json={"decision": "approve"},
            headers=auth_header(doc_token)
        )
        assert resp.status_code == 200

        # Patient status is now SHARING_OFF
        resp = client.get("/api/v1/consent/status", headers=auth_header(pat_token))
        assert resp.json()["share_state"] == "SHARING_OFF"

    def test_clinician_can_reject_disable(self, client):
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        register_user(client, "doc@test.com", "Doctor1234", "Doctor", role="clinician")

        pat_token = login_user(client, "patient@test.com", "Patient1234")
        doc_token = login_user(client, "doc@test.com", "Doctor1234")

        client.post("/api/v1/consent/disable", json={}, headers=auth_header(pat_token))

        resp = client.get("/api/v1/consent/pending", headers=auth_header(doc_token))
        patient_id = resp.json()["pending_requests"][0]["user_id"]

        resp = client.post(
            f"/api/v1/consent/{patient_id}/review",
            json={"decision": "reject", "reason": "Still under care"},
            headers=auth_header(doc_token)
        )
        assert resp.status_code == 200

        resp = client.get("/api/v1/consent/status", headers=auth_header(pat_token))
        assert resp.json()["share_state"] == "SHARING_ON"

    def test_patient_can_reenable_after_off(self, client):
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")
        register_user(client, "doc@test.com", "Doctor1234", "Doctor", role="clinician")

        pat_token = login_user(client, "patient@test.com", "Patient1234")
        doc_token = login_user(client, "doc@test.com", "Doctor1234")

        client.post("/api/v1/consent/disable", json={}, headers=auth_header(pat_token))

        resp = client.get("/api/v1/consent/pending", headers=auth_header(doc_token))
        patient_id = resp.json()["pending_requests"][0]["user_id"]
        client.post(
            f"/api/v1/consent/{patient_id}/review",
            json={"decision": "approve"},
            headers=auth_header(doc_token)
        )

        # Re-enable
        resp = client.post("/api/v1/consent/enable", headers=auth_header(pat_token))
        assert resp.status_code == 200

        resp = client.get("/api/v1/consent/status", headers=auth_header(pat_token))
        assert resp.json()["share_state"] == "SHARING_ON"


class TestAdminPasswordReset:
    """Admin can set temporary passwords for other users."""

    def test_admin_can_reset_user_password(self, client):
        register_user(client, "admin@test.com", "Admin1234", "Admin", role="admin")
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")

        admin_token = login_user(client, "admin@test.com", "Admin1234")

        # Reset patient password
        resp = client.post(
            "/api/v1/users/2/reset-password",
            json={"new_password": "NewTemp1234"},
            headers=auth_header(admin_token)
        )
        assert resp.status_code == 200

        # Patient can login with new password
        pat_token = login_user(client, "patient@test.com", "NewTemp1234")
        assert pat_token is not None

    def test_non_admin_cannot_reset_password(self, client):
        register_user(client, "doc@test.com", "Doctor1234", "Doctor", role="clinician")
        register_user(client, "patient@test.com", "Patient1234", "Patient", role="patient")

        doc_token = login_user(client, "doc@test.com", "Doctor1234")

        resp = client.post(
            "/api/v1/users/2/reset-password",
            json={"new_password": "NewTemp1234"},
            headers=auth_header(doc_token)
        )
        assert resp.status_code == 403
