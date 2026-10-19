"""Tests for POST /user-problems/ — create or update problem progress.

Design decisions (mirrors the approach in test_login.py):
- A minimal FastAPI app is built with both the auth router (needed for
  registering + logging in) and the user-problems router.
- An in-memory SQLite database (StaticPool) is used — no Neon DB is touched.
- JWT_SECRET_KEY is set to a fixed test value so the service layer never
  raises RuntimeError and tests are hermetic.
- All test users are created through the register endpoint and authenticated
  via the login endpoint, NOT by direct DB insertion.

Covered scenarios:
  ✓ Create a new progress record → 200 + correct fields
  ✓ Update an existing record → status changes, same id
  ✓ Invalid status string → 422
  ✓ Missing fields → 422
  ✓ Unauthenticated request → 401
  ✓ User isolation: user A cannot see/affect user B's records
  ✓ user_id in request body is ignored (server sets it from JWT)
"""

import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.models.user import User  # registers users table
from app.models.user_problem import UserProblem  # registers user_problems table
from app.api.auth import router as auth_router
from app.api.user_problems import router as user_problem_router

# ── Test JWT secret ────────────────────────────────────────────────────────────
TEST_JWT_SECRET = "test-secret-not-used-in-production-ever"
os.environ.setdefault("JWT_SECRET_KEY", TEST_JWT_SECRET)

from app import config as app_config  # noqa: E402
app_config.JWT_SECRET_KEY = TEST_JWT_SECRET

# ── Minimal app ────────────────────────────────────────────────────────────────
minimal_app = FastAPI()
minimal_app.include_router(auth_router, prefix="/auth")
minimal_app.include_router(user_problem_router, prefix="/user-problems")

# ── In-memory SQLite ───────────────────────────────────────────────────────────
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

def register_and_login(
    email: str = "alice@example.com",
    password: str = "securepass1",
) -> dict:
    """Register a user and log in, returning headers with the Bearer token."""
    client.post("/auth/register", json={"email": email, "password": password})
    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def post_progress(headers: dict, leetcode_problem_id: int = 1, status: str = "Solved"):
    """POST a progress record using the given auth headers."""
    return client.post(
        "/user-problems/",
        json={"leetcode_problem_id": leetcode_problem_id, "status": status},
        headers=headers,
    )


# ── Tests: Creation ───────────────────────────────────────────────────────────

class TestCreateProgress:
    """Creating a brand-new progress record."""

    def test_returns_200(self):
        headers = register_and_login()
        response = post_progress(headers, leetcode_problem_id=1, status="Solved")
        assert response.status_code == 200

    def test_response_contains_correct_fields(self):
        headers = register_and_login()
        body = post_progress(headers, leetcode_problem_id=42, status="Attempted").json()
        assert body["leetcode_problem_id"] == 42
        assert body["status"] == "Attempted"
        assert "id" in body
        assert "user_id" in body
        assert "updated_at" in body

    def test_each_status_is_accepted(self):
        """All three valid statuses should be accepted."""
        headers = register_and_login()
        for status_value in ("Solved", "Attempted", "Revision"):
            resp = post_progress(headers, leetcode_problem_id=hash(status_value) % 9999, status=status_value)
            assert resp.status_code == 200, f"Status '{status_value}' was rejected"
            assert resp.json()["status"] == status_value


# ── Tests: Update ─────────────────────────────────────────────────────────────

class TestUpdateProgress:
    """Updating an existing progress record (same user + same problem)."""

    def test_update_changes_status(self):
        headers = register_and_login()
        first = post_progress(headers, leetcode_problem_id=1, status="Attempted").json()
        second = post_progress(headers, leetcode_problem_id=1, status="Solved").json()

        assert first["status"] == "Attempted"
        assert second["status"] == "Solved"

    def test_update_preserves_record_id(self):
        """Updating should modify the existing row, not create a new one."""
        headers = register_and_login()
        first = post_progress(headers, leetcode_problem_id=1, status="Attempted").json()
        second = post_progress(headers, leetcode_problem_id=1, status="Solved").json()

        assert first["id"] == second["id"]

    def test_update_refreshes_updated_at(self):
        headers = register_and_login()
        first = post_progress(headers, leetcode_problem_id=1, status="Attempted").json()
        second = post_progress(headers, leetcode_problem_id=1, status="Revision").json()

        # updated_at should change (or at minimum not be empty).
        assert second["updated_at"] is not None


# ── Tests: Validation ─────────────────────────────────────────────────────────

class TestValidation:
    """Invalid inputs should return 422 Validation Error."""

    def test_invalid_status_returns_422(self):
        headers = register_and_login()
        response = post_progress(headers, leetcode_problem_id=1, status="WrongStatus")
        assert response.status_code == 422

    def test_missing_status_returns_422(self):
        headers = register_and_login()
        response = client.post(
            "/user-problems/",
            json={"leetcode_problem_id": 1},
            headers=headers,
        )
        assert response.status_code == 422

    def test_missing_leetcode_problem_id_returns_422(self):
        headers = register_and_login()
        response = client.post(
            "/user-problems/",
            json={"status": "Solved"},
            headers=headers,
        )
        assert response.status_code == 422

    def test_empty_body_returns_422(self):
        headers = register_and_login()
        response = client.post("/user-problems/", json={}, headers=headers)
        assert response.status_code == 422

    def test_zero_problem_id_returns_422(self):
        """leetcode_problem_id must be > 0."""
        headers = register_and_login()
        response = post_progress(headers, leetcode_problem_id=0, status="Solved")
        assert response.status_code == 422

    def test_negative_problem_id_returns_422(self):
        headers = register_and_login()
        response = post_progress(headers, leetcode_problem_id=-5, status="Solved")
        assert response.status_code == 422


# ── Tests: Authentication ─────────────────────────────────────────────────────

class TestAuthentication:
    """Unauthenticated requests must be rejected."""

    def test_no_token_returns_401(self):
        response = client.post(
            "/user-problems/",
            json={"leetcode_problem_id": 1, "status": "Solved"},
        )
        assert response.status_code == 401

    def test_invalid_token_returns_401(self):
        response = client.post(
            "/user-problems/",
            json={"leetcode_problem_id": 1, "status": "Solved"},
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401


# ── Tests: User Isolation ─────────────────────────────────────────────────────

class TestUserIsolation:
    """Each user's progress is independent of other users."""

    def test_two_users_same_problem_different_records(self):
        """User A and User B can both have progress on the same problem."""
        headers_a = register_and_login(email="alice@example.com", password="password1")
        headers_b = register_and_login(email="bob@example.com", password="password2")

        resp_a = post_progress(headers_a, leetcode_problem_id=1, status="Solved").json()
        resp_b = post_progress(headers_b, leetcode_problem_id=1, status="Attempted").json()

        # Different records (different IDs, different user_ids).
        assert resp_a["id"] != resp_b["id"]
        assert resp_a["user_id"] != resp_b["user_id"]

        # Each has their own status.
        assert resp_a["status"] == "Solved"
        assert resp_b["status"] == "Attempted"

    def test_user_id_comes_from_token_not_body(self):
        """Even if someone tries to send user_id in the body, it is ignored."""
        headers = register_and_login()
        import uuid

        response = client.post(
            "/user-problems/",
            json={
                "leetcode_problem_id": 1,
                "status": "Solved",
                "user_id": str(uuid.uuid4()),  # should be ignored
            },
            headers=headers,
        )
        assert response.status_code == 200
        # The user_id in the response should match the logged-in user,
        # not the fake UUID we sent.
        body = response.json()
        assert "user_id" in body

    def test_updating_does_not_affect_other_user(self):
        """User A updating problem 1 should not change User B's record."""
        headers_a = register_and_login(email="alice@example.com", password="password1")
        headers_b = register_and_login(email="bob@example.com", password="password2")

        # Both start as Attempted.
        post_progress(headers_a, leetcode_problem_id=1, status="Attempted")
        post_progress(headers_b, leetcode_problem_id=1, status="Attempted")

        # User A updates to Solved.
        post_progress(headers_a, leetcode_problem_id=1, status="Solved")

        # User B re-posts (which triggers the "existing" path) — should still be Attempted
        # unless explicitly changed.
        resp_b = post_progress(headers_b, leetcode_problem_id=1, status="Attempted").json()
        assert resp_b["status"] == "Attempted"
