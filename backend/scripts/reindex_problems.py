import json

from app.services.embedding_service import create_embedding
from app.db.qdrant import insert_problem


with open("data/enriched_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)


for problem in problems:
    embedding = create_embedding(problem)
    insert_problem(problem, embedding)
    print(f"Re-indexed: {problem['title']}")


print(f"Re-indexing complete: {len(problems)} problems")