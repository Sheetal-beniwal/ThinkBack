"""User-problems router — tracks a user's LeetCode problem progress.

Endpoints:
  GET  /user-problems/   — list every UserProblem record (basic demo).
  POST /user-problems/   — create or update a progress record for the
                           authenticated user.

The POST endpoint is protected by ``get_current_user``, which requires a
valid ``Authorization: Bearer <JWT>`` header.  The ``user_id`` is always
extracted from the token — it is never accepted from the request body, so
one user cannot tamper with another user's data.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.user_problem import UserProblem
from app.schemas.user_problem import UserProblemCreate, UserProblemResponse

router = APIRouter()


# ── GET /user-problems/ ──────────────────────────────────────────────────────
@router.get("/", response_model=list[UserProblemResponse])
def get_user_problems(db: Session = Depends(get_db)):
    """Return all UserProblem records (basic demo)."""
    return db.query(UserProblem).all()


# ── POST /user-problems/ ─────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserProblemResponse,
    status_code=status.HTTP_200_OK,
    summary="Create or update problem progress",
    description=(
        "Records the authenticated user's progress on a LeetCode problem. "
        "If the user already has a record for the given problem, the status "
        "is updated in place. Otherwise a new record is created. "
        "The user_id is always taken from the JWT — it cannot be set via "
        "the request body."
    ),
)
def create_or_update_user_problem(
    data: UserProblemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProblemResponse:
    """Create or update a user's progress on a LeetCode problem.

    Steps:
    1. Look for an existing record matching (current_user.id, leetcode_problem_id).
    2a. If found → update the status and updated_at timestamp.
    2b. If not found → create a brand-new record.
    3. Commit, refresh, and return the record via UserProblemResponse.
    """
    # Step 1 — check for an existing record.
    existing: UserProblem | None = (
        db.query(UserProblem)
        .filter(
            UserProblem.user_id == current_user.id,
            UserProblem.leetcode_problem_id == data.leetcode_problem_id,
        )
        .first()
    )

    if existing:
        # Step 2a — update the existing record.
        existing.status = data.status.value
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return UserProblemResponse.model_validate(existing)

    # Step 2b — create a new record.
    new_record = UserProblem(
        user_id=current_user.id,
        leetcode_problem_id=data.leetcode_problem_id,
        status=data.status.value,
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return UserProblemResponse.model_validate(new_record)
