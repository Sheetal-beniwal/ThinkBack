import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration input. Never exposed in responses."""

    email: EmailStr
    password: str = Field(
        min_length=8,
        description="Must be at least 8 characters.",
    )


class UserResponse(BaseModel):
    """Safe public schema. password_hash is never included."""

    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Schema for POST /auth/login.

    The plaintext password is never stored, logged, or echoed.
    """

    email: EmailStr
    password: str = Field(min_length=1, description="Account password.")


class TokenResponse(BaseModel):
    """Response returned after a successful login.

    Only the opaque JWT and its type are included — no user data,
    no password, no internal IDs are ever embedded in this response.
    """

    access_token: str
    token_type: str = "bearer"
