import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class UserProblem(Base):
    """SQLAlchemy ORM model linking a ThinkBack user to a LeetCode problem.

    Each row records a user's interaction (e.g., solved, attempted, bookmarked) with a
    specific LeetCode problem. The combination of ``user_id`` and ``leetcode_problem_id``
    is enforced to be unique, so a user cannot have duplicate entries for the same
    LeetCode problem.
    """

    __tablename__ = "user_problems"
    __table_args__ = (
        UniqueConstraint("user_id", "leetcode_problem_id", name="uq_user_problem"),
    )

    # Primary key – a UUID generated automatically for each record.
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign key referencing the ``users`` table. ``users.id`` is also a UUID.
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # The LeetCode problem identifier (the numeric ID used by LeetCode).
    leetcode_problem_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Human‑readable status such as "Attempted", "Solved", "Revision".
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Timestamp of the last update – stored as UTC so it is independent of the server's timezone.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Optional relationship back to the ``User`` model for convenient access.
    user = relationship("User", backref="user_problems")

    def __repr__(self) -> str:
        return (
            f"<UserProblem id={self.id} user_id={self.user_id} "
            f"leetcode_problem_id={self.leetcode_problem_id} status={self.status}>"
        )

