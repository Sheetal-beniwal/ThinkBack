from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_problem_text(problem):
    return f"""
Title: {problem["title"]}

Description:
{problem["description"]}

Tags:
{", ".join(problem["tags"])}

Primary Pattern:
{problem["primary_pattern"]}

Secondary Patterns:
{", ".join(problem["secondary_patterns"])}
"""


def create_embedding(problem):

    text = create_problem_text(problem)

    embedding = model.encode(text)

    return embedding.tolist()