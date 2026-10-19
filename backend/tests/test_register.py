"""Tests for POST /auth/register.

Why we build a minimal_app instead of importing app.main
---------------------------------------------------------
The main app imports the RAG router, which imports embedding_service.py,
which calls TextEmbedding() at module level — downloading and loading a
150 MB embedding model just to test registration.

Instead we build a bare FastAPI app that mounts ONLY the auth router.
This means:
  - Tests run in seconds, not minutes.
  - No embedding model is loaded.
  - No Qdrant connection is attempted.
  - No Neon database is contacted (we use in-memory SQLite).
  - All real auth code (hashing, DB writes, validation) is exercised.

The existing RAG tests are completely unaffected.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models.user import User  # must be imported so Base.metadata knows about the users table
from app.api.auth import router as auth_router, get_db


# ── Minimal FastAPI app containing only the auth router ───────────────────────
minimal_app = FastAPI()
minimal_app.include_router(auth_router, prefix="/auth")


# ── In-memory SQLite database (no network, no files, resets each test) ────────
# StaticPool: all calls to connect() return the SAME underlying connection.
# This is essential for in-memory SQLite — without it, each new connection
# opens a brand-new empty database, so the table created by create_all()
# is invisible to the session the route handler uses.
from sqlalchemy.pool import StaticPool

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


# Replace the production DB dependency for all tests in this file
minimal_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    """Create tables before each test, drop them after — keeps tests isolated."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# TestClient drives HTTP requests through the app in-process (no real server)
client = TestClient(minimal_app)


# ── Helper ─────────────────────────────────────────────────────────────────────
def register(email: str = "alice@example.com", password: str = "securepass1"):
    return client.post("/auth/register", json={"email": email, "password": password})


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_register_success():
    """A valid registration returns HTTP 201 with a safe user payload."""
    response = register()

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert "id" in body
    assert "created_at" in body


def test_register_response_excludes_password_hash():
    """The password and its hash must NEVER appear in the HTTP response."""
    body = register().json()

    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email_returns_409():
    """Registering the same email twice returns HTTP 409 Conflict."""
    register()                   # first attempt — succeeds
    response = register()        # second attempt — duplicate

    assert response.status_code == 409
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email_returns_422():
    """A badly-formed email is rejected by Pydantic before any DB work."""
    response = register(email="not-an-email")

    assert response.status_code == 422


def test_register_short_password_returns_422():
    """A password shorter than 8 characters is rejected by the schema."""
    response = register(password="short")

    assert response.status_code == 422


def test_register_missing_email_returns_422():
    """Omitting the email field produces a 422 validation error."""
    response = client.post("/auth/register", json={"password": "securepass1"})

    assert response.status_code == 422


def test_register_missing_password_returns_422():
    """Omitting the password field produces a 422 validation error."""
    response = client.post("/auth/register", json={"email": "bob@example.com"})

    assert response.status_code == 422


def test_register_password_is_stored_as_bcrypt_hash():
    """The database stores a bcrypt hash, never the plaintext password."""
    from app.models.user import User

    register(email="check@example.com", password="plaintextpw")

    db = TestingSessionLocal()
    try:
        user = db.query(User).filter_by(email="check@example.com").first()
        assert user is not None
        # Every bcrypt hash starts with $2b$ — confirming the algorithm was used
        assert user.password_hash.startswith("$2b$")
        assert user.password_hash != "plaintextpw"
    finally:
        db.close()


def test_different_users_get_unique_ids():
    """Each registered user receives a distinct UUID."""
    id1 = register(email="user1@example.com").json()["id"]
    id2 = register(email="user2@example.com").json()["id"]

    assert id1 != id2
