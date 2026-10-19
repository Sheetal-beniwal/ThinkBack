"""Authentication service: credential verification and JWT creation/decoding.

Responsibilities:
- Verify a plaintext password against the stored bcrypt hash.
- Create a signed JWT access token.
- Decode and validate an incoming JWT access token.

Security invariants upheld here:
- Plaintext passwords are never stored, logged, or returned.
- The JWT secret is always read from an environment variable (via config.py).
- Token expiry is always set to a specific datetime, never omitted.
- The signing algorithm is HS256 (HMAC-SHA256) — symmetric, fast, widely supported.
- The algorithm used during *decoding* is always taken from config, never from the
  token's own header (prevents algorithm-confusion / alg:none attacks).
- The token subject (`sub`) carries the user's UUID as a string, not their email
  or any other personally-identifiable information.
"""
import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app import config

# Reuse the same CryptContext that registration uses so bcrypt parameters match.
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A pre-hashed sentinel used to perform a dummy bcrypt verify when a login
# attempt uses an email that does not exist in the database.  Doing the verify
# even for unknown emails keeps the response time similar to a real mismatch,
# which prevents timing-based email-enumeration attacks.
# We generate this once at module load (not per-request) so startup cost is paid
# only once and the hash is always structurally valid for the installed passlib.
DUMMY_HASH: str = _pwd_context.hash("thinkback-sentinel-do-not-use")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if *plain_password* matches the stored *hashed_password*.

    Uses passlib's constant-time comparison to prevent timing attacks.
    The plaintext password is never written to any variable after this call.

    Returns False (not raises) for malformed hashes so that the login route
    always produces a 401 rather than a 500.
    """
    try:
        return _pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Malformed hash stored in DB or dummy hash used for timing protection.
        # Treat as a non-match; never leak implementation details.
        return False


def create_access_token(user_id: uuid.UUID) -> str:
    """Return a signed JWT access token whose subject is *user_id*.

    Args:
        user_id: The UUID of the authenticated user.  Stored as ``sub`` in the
                 token payload so that downstream code can identify the caller
                 without knowing their email address.

    Returns:
        A compact, URL-safe JWT string.

    Raises:
        RuntimeError: If JWT_SECRET_KEY is empty (i.e. not set in the environment).
    """
    if not config.JWT_SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY is not set. "
            "Add it to your .env file and restart the server."
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: dict = {
        "sub": str(user_id),   # subject — who the token belongs to
        "exp": expire,         # expiry — python-jose converts datetime → Unix epoch
        "iat": datetime.now(timezone.utc),  # issued-at
    }

    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> uuid.UUID | None:
    """Validate *token* and return the user's UUID, or None on any failure.

    Security properties:
    - The algorithm is taken from ``config.JWT_ALGORITHM``, never from the
      token's own header.  This prevents algorithm-confusion attacks (e.g.
      setting ``alg: none`` in the header to bypass signature verification).
    - Expiry (``exp``) is checked automatically by python-jose.
    - The ``sub`` claim is validated to be a well-formed UUID; a token
      carrying a non-UUID subject is rejected.
    - Every failure mode (expired, wrong signature, missing claim, malformed
      UUID, missing secret) returns None so the caller can raise a uniform
      HTTP 401 without leaking which check failed.

    Args:
        token: The raw JWT string from the Authorization header.

    Returns:
        The user's UUID if the token is valid, ``None`` otherwise.
    """
    if not config.JWT_SECRET_KEY:
        # Server is misconfigured; treat every token as invalid rather than
        # accepting unsigned payloads or raising an unhandled 500.
        return None

    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            # IMPORTANT: algorithms must be an explicit allowlist.
            # python-jose would accept whatever the token header says if we
            # omitted this — that would allow an attacker to forge tokens with
            # alg=none or to perform RS256/HS256 confusion attacks.
            algorithms=[config.JWT_ALGORITHM],
        )
    except JWTError:
        # Covers: expired signature, wrong signature, missing claims,
        # malformed token, unsupported algorithm, etc.
        return None

    sub: str | None = payload.get("sub")
    if not sub:
        return None

    try:
        return uuid.UUID(sub)
    except ValueError:
        # sub is present but is not a valid UUID string.
        return None
