
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yield a database session, then close it.

    Usage::

        from app.db.database import get_db

        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...

    The ``yield`` makes this a generator dependency:
    1. A fresh session is created before the route handler runs.
    2. The route receives and uses the session.
    3. The ``finally`` block closes the session even if an exception occurred,
       returning the connection to the pool and preventing leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_db_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("ThinkBack PostgreSQL connection successful!")
