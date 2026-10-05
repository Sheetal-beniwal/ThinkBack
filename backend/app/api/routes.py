from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import ask_question
from app.services.retrival_service import search_problems


router = APIRouter()


class AskRequest(BaseModel):
    query: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    difficulty: str | None = None
    pattern: str | None = None


@router.post("/ask")
def ask(request: AskRequest):

    answer = ask_question(request.query)

    return {
        "query": request.query,
        "answer": answer
    }


@router.post("/search")
def search(request: SearchRequest):

    results = search_problems(
        query=request.query,
        top_k=request.top_k,
        difficulty=request.difficulty,
        pattern=request.pattern
    )

    problems = []

    for result in results:

        problems.append({
            "score": result.score,
            "title": result.payload["title"],
            "difficulty": result.payload["difficulty"],
            "primary_pattern": result.payload["primary_pattern"],
            "url": result.payload["url"]
        })

    return {
        "results": problems
    }