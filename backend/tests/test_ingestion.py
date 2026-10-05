from app.services.ingestion import load_problems


problems = load_problems()

print("Total problems:", len(problems))

for problem in problems[:3]:
    print(problem.title)