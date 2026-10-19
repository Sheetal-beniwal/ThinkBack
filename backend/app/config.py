import os

from dotenv import load_dotenv

load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# ── JWT settings (read from environment; never hardcoded) ─────────────────────
# JWT_SECRET_KEY  : a long, random secret used to sign tokens.
#                   Generate with: python -c "import secrets; print(secrets.token_hex(32))"
# ACCESS_TOKEN_EXPIRE_MINUTES : how long a token stays valid (default 60 min).
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)
JWT_ALGORITHM: str = "HS256"