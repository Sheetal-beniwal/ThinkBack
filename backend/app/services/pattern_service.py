import json
from pathlib import Path
import os

from dotenv import load_dotenv
from groq import Groq

from app.models.problem import Problem

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_pattern(problem: Problem):

    prompt = f"""
You are an expert DSA teacher.

Analyze this LeetCode problem and identify its algorithmic patterns.

Problem:
Title: {problem.title}

Description:
{problem.description}

Existing Tags:
{problem.tags}

Return ONLY valid JSON in this exact format:

{{
    "primary_pattern": "string",
    "secondary_patterns": ["string"],
    "reason": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You classify LeetCode problems by their core DSA patterns."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)

def classify_all_problems(problems: list[Problem]):

    enriched_problems = []

    for problem in problems:
        pattern = detect_pattern(problem)

        enriched_problem = {
            "problem_id": problem.problem_id,
            "title": problem.title,
            "difficulty": problem.difficulty,
            "description": problem.description,
            "tags": problem.tags,
            "url": problem.url,
            "primary_pattern": pattern["primary_pattern"],
            "secondary_patterns": pattern["secondary_patterns"],
            "reason": pattern["reason"]
        }

        enriched_problems.append(enriched_problem)

    return enriched_problems

def save_enriched_problems(problems):

    output_path = Path("data/enriched_problems.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(problems)} problems to {output_path}")