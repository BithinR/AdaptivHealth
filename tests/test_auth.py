"""
Tests for authentication service: password hashing, JWT tokens, and security.
"""

import pytest
from datetime import timedelta


class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_hash_password_returns_hash(self, auth_service):
        """Hashing a password should return a non-empty string."""
        hashed = auth_service.hash_password("testPassword123")
        assert hashed is not None
        assert len(hashed) > 0
        assert hashed != "testPassword123"

    def test_verify_correct_password(self, auth_service):
        """Correct password should verify successfully."""
        password = "securePassword456"
        hashed = auth_service.hash_password(password)
        assert auth_service.verify_password(password, hashed) is True

    def test_verify_wrong_password(self, auth_service):
        """Wrong password should fail verification."""
        hashed = auth_service.hash_password("correctPassword")
        assert auth_service.verify_password("wrongPassword", hashed) is False

    def test_different_hashes_for_same_password(self, auth_service):
        """Same password should produce different hashes (salted)."""
        hash1 = auth_service.hash_password("samePassword")
        hash2 = auth_service.hash_password("samePassword")
        assert hash1 != hash2


class TestJWTTokens:
    """Tests for JWT token creation and decoding."""

    def test_create_access_token(self, auth_service):
        """Access token should be created with valid data."""
        token = auth_service.create_access_token(
            data={"sub": "1", "role": "patient"}
        )
        assert token is not None
        assert len(token) > 0

    def test_decode_access_token(self, auth_service):
        """Access token should decode back to original claims."""
        token = auth_service.create_access_token(
            data={"sub": "42", "role": "clinician"}
        )
        payload = auth_service.decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"
        assert payload["role"] == "clinician"
        assert payload["type"] == "access"

    def test_access_token_default_type(self, auth_service):
        """Access token should have type 'access' by default."""
        token = auth_service.create_access_token(data={"sub": "1"})
        payload = auth_service.decode_token(token)
        assert payload["type"] == "access"

    def test_access_token_preserves_custom_type(self, auth_service):
        """Access token should preserve a caller-provided type claim."""
        token = auth_service.create_access_token(
            data={"sub": "1", "type": "password_reset"}
        )
        payload = auth_service.decode_token(token)
        assert payload["type"] == "password_reset"

    def test_create_refresh_token(self, auth_service):
        """Refresh token should be created with type 'refresh'."""
        token = auth_service.create_refresh_token(data={"sub": "1"})
        payload = auth_service.decode_token(token)
        assert payload is not None
        assert payload["type"] == "refresh"

    def test_decode_invalid_token(self, auth_service):
        """Invalid token should return None."""
        payload = auth_service.decode_token("invalid.token.string")
        assert payload is None

    def test_password_reset_token_expiration(self, auth_service):
        """Password reset token with custom expiration should decode."""
        token = auth_service.create_access_token(
            data={"user_id": 5, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        payload = auth_service.decode_token(token)
        assert payload is not None
        assert payload["type"] == "password_reset"
        assert payload["user_id"] == 5
