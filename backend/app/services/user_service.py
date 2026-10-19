"""User service: business logic for registration.

Responsibilities:
- Hash the plain-text password with bcrypt before storing it.
- Insert a new User row into PostgreSQL.
- Detect duplicate emails and raise a clean error the route can convert to HTTP 409.

This module never logs or returns a plaintext password or a password hash.
"""
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

# CryptContext tells passlib which algorithm to use.
# bcrypt is the industry standard for password hashing: it is slow by design
# (making brute-force attacks expensive) and automatically embeds a unique
# random salt in every hash so two identical passwords produce different hashes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return the bcrypt hash of a plain-text password.

    The result looks like: $2b$12$<22-char-salt><31-char-hash>
    This string is safe to store in the database.
    """
    return pwd_context.hash(plain_password)


def register_user(db: Session, data: UserCreate) -> User:
    """Create and persist a new User row.

    Args:
        db:   An active SQLAlchemy session (provided by the FastAPI dependency).
        data: Validated registration input (email + plain password).

    Returns:
        The newly created User ORM object (with id and created_at populated).

    Raises:
        ValueError: If the email address is already registered.
    """
    # Hash the password BEFORE touching the database.
    # The plain-text password is discarded after this line.
    hashed = hash_password(data.password)

    new_user = User(
        email=data.email,
        password_hash=hashed,
        # id and created_at have defaults defined on the model,
        # so we do not need to set them here.
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        # IntegrityError is raised by PostgreSQL when a UNIQUE constraint
        # is violated — i.e. the email already exists in the users table.
        db.rollback()  # undo the failed insert so the session stays usable
        raise ValueError(f"Email '{data.email}' is already registered.")

    db.refresh(new_user)  # reload from DB so id and created_at are populated
    return new_user
