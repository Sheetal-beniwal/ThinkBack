"""Alembic migration environment.

Uses the existing SQLAlchemy engine and Base defined in app.db.database so
that we never create a second engine or Base.  DATABASE_URL is read from the
.env file via app.db.database, keeping credentials out of alembic.ini.
"""
from logging.config import fileConfig

from alembic import context

# ── Re-use the existing engine and declarative Base ──────────────────────────
from app.db.database import Base, engine  # noqa: E402  (must come after imports)

# ── Import all ORM models so their tables appear in Base.metadata ─────────────
import app.models.user  # noqa: F401  ensures User table is registered
import app.models.user_problem  # noqa: F401  ensures UserProblem table is registered

# ── Alembic config object ─────────────────────────────────────────────────────
config = context.config

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Point autogenerate at the shared metadata
target_metadata = Base.metadata


# ── Offline migration (SQL script output, no live DB needed) ──────────────────
def run_migrations_offline() -> None:
    """Emit migration SQL without a live connection."""
    url = engine.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Render UUIDs as native PostgreSQL uuid type
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online migration (runs against the live Neon PostgreSQL database) ─────────
def run_migrations_online() -> None:
    """Run migrations against the live database connection."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
