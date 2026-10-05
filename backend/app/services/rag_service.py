import os

from dotenv import load_dotenv
from groq import Groq
from app.services.retrival_service import (
    search_problems,
    extract_filters
)


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_context(results):

    context = ""

    for result in results:

        problem = result.payload

        context += f"""
Problem:
Title: {problem["title"]}
Difficulty: {problem["difficulty"]}
Primary Pattern: {problem["primary_pattern"]}
Secondary Patterns: {problem["secondary_patterns"]}
Description: {problem["description"]}
Reason: {problem["reason"]}

"""

    return context


def ask_question(query: str):

    difficulty, pattern = extract_filters(query)

    results = search_problems(
        query=query,
        top_k=5,
        difficulty=difficulty,
        pattern=pattern
    )

    context = build_context(results)

    prompt = f"""
You are a LeetCode DSA revision assistant.

Answer in English only.

Use ONLY the provided solved-problem context.

If the context does not contain enough information,
say so instead of inventing problems.

User question:
{query}

Relevant solved problems:
{context}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are a LeetCode DSA revision assistant.
Always respond in English.
Use concise and clear technical language.
Never invent problems that are not present in the context.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content