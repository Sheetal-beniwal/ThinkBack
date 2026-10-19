"""Reusable FastAPI dependencies for authenticated routes.

``get_current_user`` is the single entry point for protecting any endpoint
that requires a logged-in user.  Import it and use it with ``Depends()``:

    from app.dependencies.auth import get_current_user

    @router.get("/protected")
    def protected(current_user: User = Depends(get_current_user)):
        return {"hello": current_user.email}

What happens inside (beginner-friendly explanation)
----------------------------------------------------
Think of ``get_current_user`` as a security guard that stands between the
client and every protected route:

1. The client must include a header like::

       Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

2. FastAPI's built-in ``HTTPBearer`` reads that header automatically and
   hands us an ``HTTPAuthorizationCredentials`` object containing the raw
   token string.  If the header is missing entirely we raise a 401.

   Why HTTPBearer instead of OAuth2PasswordBearer?
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   ``OAuth2PasswordBearer`` tells Swagger UI to render a username/password
   form that sends ``application/x-www-form-urlencoded`` data.  Our login
   endpoint accepts JSON, so that form would always produce a 422.
   ``HTTPBearer`` tells Swagger to render a simple "Bearer token" input
   field, which is exactly what our flow needs:
     1. Log in via POST /auth/login with a JSON body → receive a JWT.
     2. Paste the JWT into Swagger's "Authorize" popup → test protected
        routes interactively.

3. We pass the token to ``decode_access_token``, which:
   a. Checks the signature (nobody tampered with the payload).
   b. Checks the expiry (``exp`` claim).
   c. Ensures the algorithm is the one *we* configured — never whatever the
      token header claims.
   d. Extracts the ``sub`` claim and converts it to a UUID.
   If any of these checks fail, ``decode_access_token`` returns ``None``.

4. We look up the UUID in PostgreSQL.  If the user has been deleted since the
   token was issued, this also fails.

5. On every failure we raise HTTP 401 with a generic message — we never reveal
   *which* check failed.

6. On success we return the full ``User`` ORM object so the route can use any
   field it needs (e.g. for ``GET /auth/me`` we return the whole user).
"""
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.services.auth_service import decode_access_token

# HTTPBearer reads the "Authorization: Bearer <token>" header and returns an
# HTTPAuthorizationCredentials object with a `.credentials` attribute holding
# the raw token string.
#
# ``auto_error=False`` is set so that a MISSING Authorization header returns
# ``None`` instead of raising a 403.  We then raise our own 401 for
# consistency — all auth failures look the same to the client.
#
# In Swagger UI (OpenAPI docs) this renders a simple "Bearer token" input
# inside the Authorize popup, instead of the OAuth2 username/password form.
_http_bearer = HTTPBearer(auto_error=False)

# The single 401 response returned for every failure mode.
# Using one message for all failure types (expired, bad signature, user deleted,
# etc.) prevents information leakage — the client cannot tell which check failed.
_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_http_bearer),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency — validate the Bearer token and return the active user.

    Inject this into any route that requires authentication::

        current_user: User = Depends(get_current_user)

    Args:
        credentials: ``HTTPAuthorizationCredentials`` extracted from the
                     Authorization header by ``_http_bearer``.  ``None`` if
                     the header is absent (because ``auto_error=False``).
                     FastAPI injects this automatically.
        db:          Active SQLAlchemy session.  FastAPI injects this
                     automatically via the existing ``get_db`` dependency.

    Returns:
        The authenticated ``User`` ORM instance.

    Raises:
        HTTPException (401): For any missing, invalid, expired, malformed, or
                              unrecognised token, or if the user no longer
                              exists in the database.
    """
    # Step 0 — reject missing or empty tokens immediately.
    if credentials is None or not credentials.credentials:
        raise _CREDENTIALS_EXCEPTION

    token: str = credentials.credentials

    # Step 1 — decode the JWT and extract the user UUID.
    # Returns None for any failure (expired, bad sig, bad sub, etc.).
    user_id: uuid.UUID | None = decode_access_token(token)
    if user_id is None:
        raise _CREDENTIALS_EXCEPTION

    # Step 2 — fetch the user from PostgreSQL.
    # Even if the token is cryptographically valid, the user might have been
    # deleted after the token was issued.
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise _CREDENTIALS_EXCEPTION

    return user

