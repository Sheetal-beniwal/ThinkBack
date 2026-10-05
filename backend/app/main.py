from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="ThinkBack",
    description="AI-powered DSA revision assistant",
    version="1.0.0"
)


app.include_router(router)