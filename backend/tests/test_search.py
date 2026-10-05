from app.services.retrival_service import search_problems


query = "sliding window problems"

results = search_problems(query, top_k=5,difficulty="Medium")


for result in results:

    print("\n-------------------")

    print("Score:", result.score)
    print("Title:", result.payload["title"])
    print("Pattern:", result.payload["primary_pattern"])
    print("Difficulty:", result.payload["difficulty"])