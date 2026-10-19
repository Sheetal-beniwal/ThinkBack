from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.routes import router
from app.api.user_problems import router as user_problem_router

app = FastAPI(
    title="ThinkBack",
    description="AI-powered DSA revision assistant",
    version="1.0.0"
)

# Existing RAG/search routes — untouched
app.include_router(router)
app.include_router(user_problem_router, prefix="/user-problems", tags=["user-problems"])
# Auth routes: /auth/register (and future /auth/login, etc.)
app.include_router(auth_router, prefix="/auth", tags=["auth"])