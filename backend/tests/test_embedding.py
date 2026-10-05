import json

from app.services.embedding_service import create_embedding


with open("data/enriched_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)


problem = problems[0]

embedding = create_embedding(problem)

print("Problem:", problem["title"])
print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])