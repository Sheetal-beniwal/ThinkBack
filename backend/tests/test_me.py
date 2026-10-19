"""Tests for GET /auth/me — JWT authentication verification.

Beginner-friendly explanation of what is being tested
------------------------------------------------------
``GET /auth/me`` is a *protected* endpoint: you can only call it if you hold
a valid JWT access token.  Think of it like a members-only room:

- If you show a valid, unexpired membership card (token) → you get in.
- If you show a fake card, a card for a different club (wrong signature),
  or a card that has expired → you are turned away with a 401 response.

This test file covers every way the membership check can fail, plus the
happy path where it succeeds.

Design (mirrors test_login.py):
- A minimal FastAPI app is built with ONLY the auth router, so no embedding
  model or Qdrant connection is ever loaded.
- An in-memory SQLite database (StaticPool) is used — Neon is never touched.
- JWT_SECRET_KEY is patched to a fixed test value at module level.
- get_db (the DB dependency) is overridden so all routes use the SQLite DB.
- The get_current_user dependency's _oauth2_scheme is also overridden in
  relevant tests by replacing get_db on the minimal_app directly.

Covered scenarios:
  ✓ Valid token            → 200 + correct user profile (id, email, created_at)
  ✓ Missing token          → 401 (Authorization header absent)
  ✓ Malformed token        → 401 (not a valid JWT structure)
  ✓ Expired token          → 401 (exp claim in the past)
  ✓ Invalid signature      → 401 (signed with a different secret)
  ✓ Nonexistent user sub   → 401 (user deleted after token was issued)
  ✓ Response never exposes password_hash
"""
import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# ── Test JWT secret (patched before any imports that read config) ──────────────
TEST_JWT_SECRET = "test-secret-not-used-in-production-ever"
TEST_JWT_ALGORITHM = "HS256"

os.environ.setdefault("JWT_SECRET_KEY", TEST_JWT_SECRET)

from app import config as app_config  # noqa: E402
app_config.JWT_SECRET_KEY = TEST_JWT_SECRET

# ── Now it's safe to import from the auth modules ─────────────────────────────
from app.db.database import Base  # noqa: E402
from app.models.user import User  # noqa: E402 — registers table with Base.metadata
from app.api.auth import router as auth_router, get_db  # noqa: E402
from app.dependencies.auth import get_current_user  # noqa: E402
from app.services.auth_service import create_access_token  # noqa: E402


# ── Minimal FastAPI app (auth router only) ────────────────────────────────────
minimal_app = FastAPI()
minimal_app.include_router(auth_router, prefix="/auth")


# ── In-memory SQLite with StaticPool ─────────────────────────────────────────
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


# Override both the router-level and dependency-level get_db references.
# get_current_user uses get_db from app.db.database; auth routes use the
# re-exported get_db from app.api.auth.  Both point to the same function
# object, so a single override on minimal_app covers both.
minimal_app.dependency_overrides[get_db] = override_get_db


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_database():
    """Create tables before each test, drop after — full isolation."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(minimal_app)


# ── Helpers ───────────────────────────────────────────────────────────────────

_VALID_EMAIL = "alice@example.com"
_VALID_PASSWORD = "securepass1"


def register(email: str = _VALID_EMAIL, password: str = _VALID_PASSWORD) -> dict:
    """Register a user via the API and return the response body."""
    resp = client.post("/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 201, f"Registration failed: {resp.json()}"
    return resp.json()


def login(email: str = _VALID_EMAIL, password: str = _VALID_PASSWORD) -> str:
    """Log in and return the raw access token string."""
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login failed: {resp.json()}"
    return resp.json()["access_token"]


def get_me(token: str) -> "requests.Response":  # type: ignore[name-defined]
    """Call GET /auth/me with the given Bearer token."""
    return client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})


def forge_token(
    sub: str | None = None,
    secret: str = TEST_JWT_SECRET,
    algorithm: str = TEST_JWT_ALGORITHM,
    exp_delta_minutes: int = 60,
) -> str:
    """Build a JWT manually for testing edge cases."""
    payload: dict = {}
    if sub is not None:
        payload["sub"] = sub
    if exp_delta_minutes is not None:
        payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=exp_delta_minutes)
    return jwt.encode(payload, secret, algorithm=algorithm)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestMeSuccess:
    """Happy path: valid token → 200 + correct user profile."""

    def test_returns_200(self):
        register()
        token = login()
        response = get_me(token)
        assert response.status_code == 200

    def test_response_contains_correct_email(self):
        register()
        token = login()
        body = get_me(token).json()
        assert body["email"] == _VALID_EMAIL

    def test_response_contains_id(self):
        register()
        token = login()
        body = get_me(token).json()
        assert "id" in body
        # Must be a valid UUID string
        uuid.UUID(body["id"])

    def test_response_contains_created_at(self):
        register()
        token = login()
        body = get_me(token).json()
        assert "created_at" in body

    def test_id_matches_registered_user(self):
        """The ``id`` in /me must equal the ``id`` returned at registration."""
        reg_body = register()
        token = login()
        me_body = get_me(token).json()
        assert me_body["id"] == reg_body["id"]

    def test_response_never_exposes_password_hash(self):
        """The password hash must NEVER appear in the /me response."""
        register()
        token = login()
        body = get_me(token).json()
        assert "password" not in body
        assert "password_hash" not in body

    def test_correct_user_returned_for_each_account(self):
        """Each user's token should only return that user's profile."""
        reg1 = register(email="user1@example.com", password="password123")
        reg2 = register(email="user2@example.com", password="password456")

        token1 = login(email="user1@example.com", password="password123")
        token2 = login(email="user2@example.com", password="password456")

        assert get_me(token1).json()["id"] == reg1["id"]
        assert get_me(token2).json()["id"] == reg2["id"]


class TestMeMissingToken:
    """No Authorization header → 401."""

    def test_missing_header_returns_401(self):
        """
        FastAPI's OAuth2PasswordBearer raises 401 automatically when the
        Authorization header is absent — we don't even reach our code.
        """
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_empty_bearer_returns_401(self):
        """An Authorization header with no token value is also rejected."""
        response = client.get("/auth/me", headers={"Authorization": "Bearer "})
        assert response.status_code == 401


class TestMeMalformedToken:
    """Token string that is not a valid JWT → 401."""

    def test_random_string_returns_401(self):
        response = get_me("not.a.jwt.at.all")
        assert response.status_code == 401

    def test_empty_string_returns_401(self):
        response = get_me("")
        # Empty token: OAuth2PasswordBearer raises 401 before we run
        assert response.status_code == 401

    def test_truncated_jwt_returns_401(self):
        register()
        token = login()
        # Remove the last 10 characters — signature is now broken
        truncated = token[:-10]
        assert get_me(truncated).status_code == 401

    def test_token_with_no_sub_claim_returns_401(self):
        """A valid JWT that is missing the ``sub`` claim must be rejected."""
        # forge_token with sub=None produces a token with no sub
        token = forge_token(sub=None)
        assert get_me(token).status_code == 401

    def test_token_with_non_uuid_sub_returns_401(self):
        """A token whose ``sub`` is not a UUID must be rejected."""
        token = forge_token(sub="not-a-uuid")
        assert get_me(token).status_code == 401


class TestMeExpiredToken:
    """Token whose ``exp`` is in the past → 401."""

    def test_expired_token_returns_401(self):
        """
        We forge a token whose expiry is 1 minute in the PAST.
        python-jose's decode() checks ``exp`` automatically and raises
        JWTError, which ``decode_access_token`` converts to None → 401.
        """
        register()
        # exp_delta_minutes=-1 puts the expiry 1 minute ago
        expired_token = forge_token(
            sub=str(uuid.uuid4()),
            exp_delta_minutes=-1,
        )
        response = get_me(expired_token)
        assert response.status_code == 401

    def test_expired_token_same_error_as_missing_token(self):
        """Both failures should return 401 — client cannot distinguish them."""
        expired_token = forge_token(sub=str(uuid.uuid4()), exp_delta_minutes=-1)
        response_expired = get_me(expired_token)
        response_missing = client.get("/auth/me")
        assert response_expired.status_code == response_missing.status_code == 401


class TestMeInvalidSignature:
    """Token signed with a different secret → 401."""

    def test_wrong_secret_returns_401(self):
        """
        The signature is verified against ``config.JWT_SECRET_KEY``.
        A token signed with any other secret will fail the verify step
        inside ``decode_access_token``, which returns None → 401.
        """
        register()
        # Sign with a completely different secret
        tampered_token = forge_token(
            sub=str(uuid.uuid4()),
            secret="completely-wrong-secret",
        )
        response = get_me(tampered_token)
        assert response.status_code == 401

    def test_tampered_payload_returns_401(self):
        """Changing any byte of the payload invalidates the HMAC signature."""
        register()
        token = login()

        # A JWT has three base64-encoded parts: header.payload.signature
        # Flipping one character in the payload section corrupts it.
        parts = token.split(".")
        # Append a character to the payload section
        parts[1] = parts[1] + "X"
        tampered = ".".join(parts)

        assert get_me(tampered).status_code == 401


class TestMeNonexistentUser:
    """Token with a valid UUID sub that doesn't match any DB row → 401."""

    def test_deleted_user_sub_returns_401(self):
        """
        Simulate a user being deleted after their token was issued.
        The token is cryptographically valid, but the DB query returns None
        → get_current_user raises 401.
        """
        # Create a token for a UUID that does not exist in the DB
        ghost_id = uuid.uuid4()
        ghost_token = forge_token(sub=str(ghost_id))
        response = get_me(ghost_token)
        assert response.status_code == 401

    def test_error_message_is_generic(self):
        """
        The 401 detail must not reveal that the user was deleted or not found.
        The same generic message should appear for all 401 cases.
        """
        ghost_token = forge_token(sub=str(uuid.uuid4()))
        detail = get_me(ghost_token).json()["detail"].lower()
        assert "could not validate" in detail
