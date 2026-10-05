from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.db.qdrant import client, COLLECTION_NAME
from app.services.embedding_service import model

def extract_filters(query: str):

    query_lower = query.lower()

    difficulty = None
    pattern = None

    # Difficulty
    if "easy" in query_lower:
        difficulty = "Easy"

    elif "medium" in query_lower:
        difficulty = "Medium"

    elif "hard" in query_lower:
        difficulty = "Hard"

    # Patterns
    if "sliding window" in query_lower:
        pattern = "Sliding Window"

    elif "binary search" in query_lower:
        pattern = "Binary Search"

    elif "dijkstra" in query_lower:
        pattern = "Dijkstra"

    elif "dynamic programming" in query_lower or "dp" in query_lower:
        pattern = "Dynamic Programming"

    elif "two pointers" in query_lower:
        pattern = "Two Pointers"

    elif "bfs" in query_lower:
        pattern = "BFS"

    elif "dfs" in query_lower:
        pattern = "DFS"

    return difficulty, pattern


def search_problems(
    query: str,
    top_k: int = 5,
    difficulty: str | None = None,
    pattern: str | None = None
):

    query_embedding = list(model.embed([query]))[0].tolist()

    conditions = []

    if difficulty:
        conditions.append(
            FieldCondition(
                key="difficulty",
                match=MatchValue(value=difficulty)
            )
        )

    if pattern:
        conditions.append(
            FieldCondition(
                key="primary_pattern",
                match=MatchValue(value=pattern)
            )
        )  
    query_filter = None
    if conditions:
        query_filter = Filter(
            must=conditions
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=query_filter,
        limit=top_k,
        with_payload=True
    )

    return results.points