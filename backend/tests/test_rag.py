from app.services.rag_service import ask_question


query = "Maine kaunse sliding window problems solve kiye hain?"

answer = ask_question(query)

print("\nANSWER:\n")
print(answer)