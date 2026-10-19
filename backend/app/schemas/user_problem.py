"""Pydantic schemas for the UserProblem feature.

Two schemas live here:

1. ``UserProblemCreate`` — validates the incoming request body for creating or
   updating a user's progress on a LeetCode problem.
2. ``UserProblemResponse`` — serialises a ``UserProblem`` ORM object into the
   JSON response returned to the client.

The ``ProblemStatus`` enum restricts accepted status values to a known set.
Any value outside this set triggers an automatic 422 Validation Error from
Pydantic — the route handler never even runs.
"""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ── Allowed statuses ──────────────────────────────────────────────────────────
class ProblemStatus(str, Enum):
    """The three valid states a user's problem progress can be in.

    Inheriting from ``str`` lets Pydantic compare incoming JSON strings
    directly (e.g. ``"Solved"``), and also means the value serialises back
    to a plain string in responses.
    """

    SOLVED = "Solved"
    ATTEMPTED = "Attempted"
    REVISION = "Revision"


# ── Request schema ────────────────────────────────────────────────────────────
class UserProblemCreate(BaseModel):
    """Request body for ``POST /user-problems/``.

    Only two fields are accepted from the client:
    - ``leetcode_problem_id``: the numeric LeetCode problem ID (must be ≥ 1).
    - ``status``: one of Solved, Attempted, or Revision.

    ``user_id`` is **not** accepted here — it is always set server-side from
    the authenticated user's JWT token.  This prevents users from writing
    progress records on behalf of other users.
    """

    leetcode_problem_id: int = Field(
        ...,
        gt=0,
        description="The numeric LeetCode problem ID (e.g. 1 for Two Sum).",
    )
    status: ProblemStatus = Field(
        ...,
        description='Progress status — must be "Solved", "Attempted", or "Revision".',
    )


# ── Response schema ───────────────────────────────────────────────────────────
class UserProblemResponse(BaseModel):
    """Pydantic schema for returning a UserProblem record.

    The fields map directly to the SQLAlchemy ``UserProblem`` ORM model. The
    ``model_config`` with ``from_attributes=True`` enables FastAPI to accept a
    SQLAlchemy model instance and automatically pull the attribute values.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    leetcode_problem_id: int
    status: str
    updated_at: datetime

    # Enable ORM mode so FastAPI can convert a ``UserProblem`` ORM object
    # into this schema without an explicit ``.dict()`` call.
    model_config = {"from_attributes": True}
