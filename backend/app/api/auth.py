"""Authentication router.

Currently exposes:
  POST /auth/register  — create a new user account
  POST /auth/login     — verify credentials and return a JWT access token
  GET  /auth/me        — return the currently authenticated user's profile

Future endpoints (token refresh, etc.) will be added here.
The existing Qdrant/RAG routes in app/api/routes.py are not affected.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db  # re-exported for backward compat; also used by routes
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services.auth_service import DUMMY_HASH, create_access_token, verify_password
from app.services.user_service import register_user

router = APIRouter()


# ── Database session dependency ───────────────────────────────────────────────
# get_db is defined in app.db.database and imported above.
# It is re-exported from this module so that existing test files that import it
# as `from app.api.auth import get_db` continue to work without modification.


# ── Shared 401 response ───────────────────────────────────────────────────────
# A single, generic error is used for both "email not found" and "wrong
# password" cases so that an attacker cannot determine whether a particular
# email address is registered (prevents user-enumeration attacks).
_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password.",
    headers={"WWW-Authenticate": "Bearer"},
)


# ── POST /auth/register ───────────────────────────────────────────────────────
@router.post(
    "/register",
    response_model=UserResponse,          # FastAPI serialises the return value
    status_code=status.HTTP_201_CREATED,  # 201 = "resource was created"
    summary="Register a new user",
    description=(
        "Creates a new ThinkBack account. "
        "The password is hashed with bcrypt and never stored or returned in plaintext. "
        "Returns HTTP 409 if the email is already registered."
    ),
)
def register(
    data: UserCreate,               # FastAPI validates + deserialises the request body
    db: Session = Depends(get_db),  # FastAPI injects the session automatically
) -> UserResponse:
    """Register a new user and return a safe (hash-free) response."""
    try:
        user = register_user(db, data)
    except ValueError as exc:
        # register_user raises ValueError for duplicate emails.
        # We convert it to an HTTP 409 Conflict response here,
        # keeping the service layer free of HTTP concerns.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    # UserResponse is defined without a password_hash field, so
    # the hash is automatically excluded from the JSON response.
    return UserResponse.model_validate(user)


# ── POST /auth/login ──────────────────────────────────────────────────────────
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Log in and obtain a JWT access token",
    description=(
        "Verifies the submitted email and password against the stored bcrypt hash. "
        "Returns a signed JWT access token on success. "
        "Returns HTTP 401 with a generic message on any credential mismatch — "
        "the response never reveals whether the email exists."
    ),
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Verify credentials and issue a JWT access token.

    Login flow:
    1. Look up the user row by email.
    2. If no row exists → raise 401 (same message as wrong password).
    3. Use passlib constant-time verify to compare the submitted password
       against the stored bcrypt hash.
    4. If the hash does not match → raise 401.
    5. Call create_access_token with the user's UUID; JWT is signed with
       HS256 using JWT_SECRET_KEY from the environment.
    6. Return the opaque token string; no user data is included in the response.
    """
    # Step 1 — look up by email.
    user: User | None = db.query(User).filter(User.email == data.email).first()

    # Steps 2 & 4 — identical 401 for both missing email and wrong password
    # to prevent email-enumeration.  The bcrypt verify call is always executed
    # regardless of whether the user exists, so timing is similar for both cases.
    # DUMMY_HASH is a real bcrypt hash generated once at module load by passlib.
    stored_hash = user.password_hash if user else DUMMY_HASH
    password_ok = verify_password(data.password, stored_hash)

    if not user or not password_ok:
        raise _INVALID_CREDENTIALS

    # Step 5 — create the JWT.
    token = create_access_token(user.id)

    # Step 6 — return only the token; no PII in the response.
    return TokenResponse(access_token=token)


# ── GET /auth/me ──────────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated user",
    description=(
        "Reads the Bearer token from the Authorization header, verifies its "
        "signature and expiry, looks up the user in PostgreSQL, and returns "
        "their public profile. Never exposes the password hash. "
        "Returns HTTP 401 for any invalid, expired, or unrecognised token."
    ),
)
def me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Return the profile of the authenticated caller.

    ``get_current_user`` (injected by FastAPI via Depends) does all the
    token validation and DB lookup.  By the time this function runs, we know
    ``current_user`` is a real, active user — no extra checks needed here.
    """
    # UserResponse excludes password_hash by design — it is not a field on
    # the schema, so FastAPI will never serialise it into the response.
    return UserResponse.model_validate(current_user)
