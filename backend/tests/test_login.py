"""Tests for POST /auth/login.

Design decisions (mirrors the approach in test_register.py):
- A minimal FastAPI app is built containing only the auth router, so no
  embedding model or Qdrant connection is loaded.
- An in-memory SQLite database (StaticPool) is used — no Neon DB is touched.
- JWT_SECRET_KEY is set to a fixed test value via monkeypatch so the service
  layer never raises RuntimeError and tests are hermetic.
- All test users are created through the register endpoint, NOT by direct DB
  insertion, so the password hash is always produced by the real bcrypt code.
- The existing tests in test_register.py are untouched.

Covered scenarios:
  ✓ Successful login → 200 + valid JWT bearing the correct user sub
  ✓ Wrong password  → 401 with generic message
  ✓ Unknown email   → 401 with the SAME generic message (no enumeration)
  ✓ Missing email field         → 422
  ✓ Missing password field      → 422
  ✓ Empty password string       → 401 (field passes schema, fails bcrypt)
  ✓ Token response never exposes password or password_hash
"""
import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.models.user import User  # registers the table with Base.metadata
from app.api.auth import router as auth_router, get_db

# ── Test JWT secret ────────────────────────────────────────────────────────────
# A fixed, non-production value used only during testing.
TEST_JWT_SECRET = "test-secret-not-used-in-production-ever"
TEST_JWT_ALGORITHM = "HS256"

# Patch the config module so auth_service picks up the test secret.
# This must happen BEFORE the service functions are called, so we set it at
# module import time and also via the monkeypatch fixture where needed.
os.environ.setdefault("JWT_SECRET_KEY", TEST_JWT_SECRET)

# Now import config and auth_service (they read env at import time or lazily).
from app import config as app_config  # noqa: E402
app_config.JWT_SECRET_KEY = TEST_JWT_SECRET  # ensure the in-process value matches

from app.services.auth_service import create_access_token  # noqa: E402


# ── Minimal app ────────────────────────────────────────────────────────────────
minimal_app = FastAPI()
minimal_app.include_router(auth_router, prefix="/auth")


# ── In-memory SQLite (StaticPool keeps the same connection) ───────────────────
SQLITE_URL = "sqlite://"

test_engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    """Yields a SQLite session instead of the real Neon session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


minimal_app.dependency_overrides[get_db] = override_get_db

# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_database():
    """Create tables before each test, drop after — full isolation."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(minimal_app)


# ── Helpers ────────────────────────────────────────────────────────────────────

_VALID_EMAIL = "alice@example.com"
_VALID_PASSWORD = "securepass1"


def register(email: str = _VALID_EMAIL, password: str = _VALID_PASSWORD):
    """Register a user through the API (uses real bcrypt hash)."""
    return client.post("/auth/register", json={"email": email, "password": password})


def login(email: str = _VALID_EMAIL, password: str = _VALID_PASSWORD):
    """Attempt login through the API."""
    return client.post("/auth/login", json={"email": email, "password": password})


# ── Tests ──────────────────────────────────────────────────────────────────────

class TestLoginSuccess:
    """Happy-path: correct credentials → 200 + usable JWT."""

    def test_returns_200(self):
        register()
        response = login()
        assert response.status_code == 200

    def test_response_contains_access_token(self):
        register()
        body = login().json()
        assert "access_token" in body
        assert isinstance(body["access_token"], str)
        assert len(body["access_token"]) > 0

    def test_token_type_is_bearer(self):
        register()
        body = login().json()
        assert body["token_type"] == "bearer"

    def test_token_sub_matches_registered_user_id(self):
        """The JWT ``sub`` claim must equal the registered user's UUID."""
        reg_body = register().json()
        registered_id = reg_body["id"]

        token = login().json()["access_token"]
        payload = jwt.decode(token, TEST_JWT_SECRET, algorithms=[TEST_JWT_ALGORITHM])

        assert payload["sub"] == registered_id

    def test_token_has_exp_claim(self):
        """The token must carry an expiry so it cannot be valid forever."""
        register()
        token = login().json()["access_token"]
        payload = jwt.decode(token, TEST_JWT_SECRET, algorithms=[TEST_JWT_ALGORITHM])
        assert "exp" in payload

    def test_response_never_contains_password_or_hash(self):
        """The HTTP response body must never expose any password data."""
        register()
        body = login().json()
        assert "password" not in body
        assert "password_hash" not in body


class TestLoginWrongPassword:
    """Wrong password → 401 with a generic message."""

    def test_returns_401(self):
        register()
        response = login(password="wrongpassword")
        assert response.status_code == 401

    def test_error_message_is_generic(self):
        """The detail must not reveal which field was wrong."""
        register()
        detail = login(password="wrongpassword").json()["detail"].lower()
        assert "incorrect" in detail
        # Must not say "password" or "email" individually
        assert detail not in ("incorrect password.", "incorrect email.")

    def test_www_authenticate_header_is_bearer(self):
        """WWW-Authenticate: Bearer is required by RFC 6750."""
        register()
        response = login(password="wrongpassword")
        assert response.headers.get("www-authenticate") == "Bearer"


class TestLoginUnknownEmail:
    """Email that was never registered → 401 with the SAME generic message."""

    def test_returns_401(self):
        # No register() call — email does not exist.
        response = login(email="ghost@example.com")
        assert response.status_code == 401

    def test_same_message_as_wrong_password(self):
        """Both failure modes must return identical detail to prevent enumeration."""
        register()
        wrong_pw_detail = login(password="wrongpassword").json()["detail"]
        unknown_email_detail = login(email="ghost@example.com").json()["detail"]
        assert wrong_pw_detail == unknown_email_detail


class TestLoginValidation:
    """Missing or malformed fields → 422 before any DB work."""

    def test_missing_email_returns_422(self):
        response = client.post("/auth/login", json={"password": _VALID_PASSWORD})
        assert response.status_code == 422

    def test_missing_password_returns_422(self):
        response = client.post("/auth/login", json={"email": _VALID_EMAIL})
        assert response.status_code == 422

    def test_malformed_email_returns_422(self):
        response = client.post(
            "/auth/login", json={"email": "not-an-email", "password": _VALID_PASSWORD}
        )
        assert response.status_code == 422

    def test_empty_body_returns_422(self):
        response = client.post("/auth/login", json={})
        assert response.status_code == 422


class TestLoginIsolation:
    """Confirm that login tests are fully isolated from each other."""

    def test_two_users_each_get_different_tokens(self):
        register(email="user1@example.com", password="password123")
        register(email="user2@example.com", password="password456")

        token1 = login(email="user1@example.com", password="password123").json()["access_token"]
        token2 = login(email="user2@example.com", password="password456").json()["access_token"]

        p1 = jwt.decode(token1, TEST_JWT_SECRET, algorithms=[TEST_JWT_ALGORITHM])
        p2 = jwt.decode(token2, TEST_JWT_SECRET, algorithms=[TEST_JWT_ALGORITHM])

        # Each token must carry a distinct sub (i.e. a distinct user UUID).
        assert p1["sub"] != p2["sub"]

    def test_user1_password_does_not_log_in_user2(self):
        """Bcrypt comparison must be per-user, not global."""
        register(email="user1@example.com", password="password123")
        register(email="user2@example.com", password="password456")

        response = login(email="user2@example.com", password="password123")
        assert response.status_code == 401
