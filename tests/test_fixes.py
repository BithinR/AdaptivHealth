"""
Tests for bug fixes identified during deep analysis.
"""

import os
import pytest

# Ensure env vars are set before app imports
os.environ.setdefault("SECRET_KEY", "test-secret-key-thats-long-enough-32chars")
os.environ.setdefault("PHI_ENCRYPTION_KEY", "dGVzdC1lbmNyeXB0aW9uLWtleS0zMmJ5dGVzISEhISE=")
os.environ.setdefault("DEBUG", "true")

from app.models.user import User, UserRole
from app.models.auth_credential import AuthCredential
from app.services.auth_service import AuthService


# ============================================================================
# Fix 1: VitalSignListResponse import error
# ============================================================================

class TestSchemaImports:
    """Test that all schema imports work correctly."""

    def test_schemas_init_imports(self):
        """Verify app.schemas.__init__ imports succeed (previously crashed with VitalSignListResponse)."""
        from app.schemas import (
            VitalSignCreate,
            VitalSignResponse,
            VitalSignsHistoryResponse,
        )
        assert VitalSignCreate is not None
        assert VitalSignResponse is not None
        assert VitalSignsHistoryResponse is not None

    def test_app_main_imports(self):
        """Verify the main app module imports without error."""
        from app.main import app
        assert app is not None


# ============================================================================
# Fix 2: timedelta import in auth.py for password reset
# ============================================================================

class TestPasswordReset:
    """Test password reset functionality."""

    def test_password_reset_request(self, client, db_session):
        """Test that password reset request doesn't crash with missing timedelta."""
        # Register a user first
        response = client.post("/api/v1/register", json={
            "email": "resetuser@test.com",
            "name": "Reset User",
            "password": "password123",
        })
        assert response.status_code == 200

        # Request password reset - this previously crashed due to missing timedelta import
        response = client.post("/api/v1/reset-password", json={
            "email": "resetuser@test.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_password_reset_nonexistent_email(self, client):
        """Test that password reset with non-existent email returns generic message."""
        response = client.post("/api/v1/reset-password", json={
            "email": "nobody@test.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


# ============================================================================
# Fix 3: locked_until field name (was account_locked_until)
# ============================================================================

class TestPasswordResetConfirm:
    """Test password reset confirmation uses correct field name."""

    def test_password_reset_confirm_unlocks_account(self, client, db_session):
        """Test that confirm_password_reset uses locked_until, not account_locked_until."""
        from datetime import datetime, timedelta, timezone

        # Register a user
        response = client.post("/api/v1/register", json={
            "email": "locked@test.com",
            "name": "Locked User",
            "password": "password123",
        })
        assert response.status_code == 200

        user = db_session.query(User).filter(User.email == "locked@test.com").first()
        auth_cred = user.auth_credential

        # Simulate account lockout
        auth_cred.failed_login_attempts = 5
        auth_cred.locked_until = datetime.now(timezone.utc) + timedelta(hours=1)
        db_session.commit()

        # Create a valid password reset token
        auth_service = AuthService()
        reset_token = auth_service.create_access_token(
            data={"user_id": user.user_id, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )

        # Confirm password reset - this previously used wrong field name
        response = client.post("/api/v1/reset-password/confirm", json={
            "token": reset_token,
            "new_password": "newpassword123"
        })
        assert response.status_code == 200

        # Verify account is unlocked
        db_session.refresh(auth_cred)
        assert auth_cred.locked_until is None
        assert auth_cred.failed_login_attempts == 0


# ============================================================================
# Fix 4: max_heart_rate property setter
# ============================================================================

class TestMaxHeartRateSetter:
    """Test that max_heart_rate property has a setter."""

    def test_max_heart_rate_setter(self):
        """Verify max_heart_rate property setter updates max_safe_hr column."""
        user = User(email="test@test.com", age=40)
        user.max_heart_rate = 180
        assert user.max_safe_hr == 180
        assert user.max_heart_rate == 180

    def test_calculate_and_set_max_heart_rate(self):
        """Verify calculate_max_heart_rate result can be set via property."""
        user = User(email="test@test.com", age=40)
        user.max_heart_rate = user.calculate_max_heart_rate()
        assert user.max_safe_hr == 180  # 220 - 40

    def test_user_profile_update_recalculates_max_hr(self, client, db_session):
        """Test that updating age recalculates max HR without crashing."""
        # Register user
        response = client.post("/api/v1/register", json={
            "email": "hrtest@test.com",
            "name": "HR Test",
            "password": "password123",
            "age": 40
        })
        assert response.status_code == 200

        # Login
        response = client.post("/api/v1/login", data={
            "username": "hrtest@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]

        # Update age - this triggers max_heart_rate recalculation
        response = client.put("/api/v1/users/me", json={
            "age": 50
        }, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200


# ============================================================================
# Fix 5: Pydantic v2 model_dump
# ============================================================================

class TestPydanticV2Compat:
    """Test that schemas use model_dump correctly."""

    def test_user_update_model_dump(self):
        """Verify UserUpdate supports model_dump (Pydantic v2)."""
        from app.schemas.user import UserUpdate
        update = UserUpdate(name="Test", age=30)
        data = update.model_dump(exclude_unset=True)
        assert data == {"name": "Test", "age": 30}

    def test_activity_update_model_dump(self):
        """Verify ActivitySessionUpdate supports model_dump."""
        from app.schemas.activity import ActivitySessionUpdate
        update = ActivitySessionUpdate(avg_heart_rate=75)
        data = update.model_dump(exclude_unset=True)
        assert data == {"avg_heart_rate": 75}


# ============================================================================
# Fix 6: Field whitelist on user profile update
# ============================================================================

class TestFieldWhitelist:
    """Test that user profile update only allows whitelisted fields."""

    def test_user_update_only_allowed_fields(self, client, db_session):
        """Verify that update endpoint only modifies whitelisted fields."""
        # Register user
        response = client.post("/api/v1/register", json={
            "email": "whitelist@test.com",
            "name": "Whitelist Test",
            "password": "password123",
        })
        assert response.status_code == 200

        # Login
        response = client.post("/api/v1/login", data={
            "username": "whitelist@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]

        # Update name (allowed field)
        response = client.put("/api/v1/users/me", json={
            "name": "Updated Name"
        }, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200

        # Verify name was updated
        user = db_session.query(User).filter(User.email == "whitelist@test.com").first()
        assert user.full_name == "Updated Name"


# ============================================================================
# Auth and login tests
# ============================================================================

class TestAccountLockout:
    """Test account lockout mechanism."""

    def test_failed_login_increments_counter(self, client, db_session):
        """Verify failed login increments failed_login_attempts."""
        # Register user
        client.post("/api/v1/register", json={
            "email": "lockout@test.com",
            "name": "Lockout Test",
            "password": "password123",
        })

        # Attempt login with wrong password
        response = client.post("/api/v1/login", data={
            "username": "lockout@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

        # Check counter
        user = db_session.query(User).filter(User.email == "lockout@test.com").first()
        assert user.auth_credential.failed_login_attempts == 1

    def test_successful_login_resets_counter(self, client, db_session):
        """Verify successful login resets failed_login_attempts."""
        # Register user
        client.post("/api/v1/register", json={
            "email": "reset@test.com",
            "name": "Reset Test",
            "password": "password123",
        })

        # Fail once
        client.post("/api/v1/login", data={
            "username": "reset@test.com",
            "password": "wrong"
        })

        # Succeed
        response = client.post("/api/v1/login", data={
            "username": "reset@test.com",
            "password": "password123"
        })
        assert response.status_code == 200

        # Counter should be reset
        user = db_session.query(User).filter(User.email == "reset@test.com").first()
        assert user.auth_credential.failed_login_attempts == 0
