import json

from app.db.qdrant import create_collection, insert_problem
from app.services.embedding_service import create_embedding


create_collection()


with open("data/enriched_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)


for problem in problems:

    embedding = create_embedding(problem)

    insert_problem(
        problem,
        embedding
    )

    print(f"Inserted: {problem['title']}")