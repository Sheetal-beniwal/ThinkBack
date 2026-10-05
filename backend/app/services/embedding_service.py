from fastembed import TextEmbedding

model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


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

    embedding = list(model.embed([text]))[0]

    return embedding.tolist()