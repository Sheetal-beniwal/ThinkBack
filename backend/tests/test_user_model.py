"""Tests for the User SQLAlchemy model and Pydantic schemas.

These tests verify:
1. The User model class is correctly defined and maps to the 'users' table.
2. The UserCreate schema validates email and requires a password.
3. The UserResponse schema never exposes password_hash.
4. UserResponse works with SQLAlchemy ORM instances via from_attributes=True.
"""
import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


# ── ORM model tests ────────────────────────────────────────────────────────────

def test_user_table_name():
    assert User.__tablename__ == "users"


def test_user_columns_exist():
    columns = {col.name for col in User.__table__.columns}
    assert "id" in columns
    assert "email" in columns
    assert "password_hash" in columns
    assert "created_at" in columns


def test_user_email_is_unique_and_indexed():
    email_col = User.__table__.columns["email"]
    assert email_col.unique is True
    assert any(
        idx.name == "ix_users_email" for idx in User.__table__.indexes
    ), "Expected index 'ix_users_email' on the email column"


def test_user_id_is_primary_key():
    id_col = User.__table__.columns["id"]
    assert id_col.primary_key is True


# ── Pydantic schema tests ──────────────────────────────────────────────────────

def test_user_create_valid():
    data = UserCreate(email="test@example.com", password="s3cur3pass!")
    assert data.email == "test@example.com"
    assert data.password == "s3cur3pass!"


def test_user_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="abc123")


def test_user_create_requires_password():
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com")


def test_user_response_has_no_password_hash_field():
    """Ensure password_hash is NOT a field on UserResponse."""
    assert "password_hash" not in UserResponse.model_fields


def test_user_response_from_orm_instance():
    """UserResponse.model_validate works on an ORM-like object."""
    now = datetime.now(timezone.utc)
    fake_user = User(
        id=uuid.uuid4(),
        email="orm@example.com",
        password_hash="$2b$12$hashedvalue",
        created_at=now,
    )
    response = UserResponse.model_validate(fake_user)

    assert response.email == "orm@example.com"
    assert response.created_at == now
    # password_hash must NOT appear in the serialized output
    serialized = response.model_dump()
    assert "password_hash" not in serialized


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
