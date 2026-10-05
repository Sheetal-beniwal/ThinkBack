import json
from pathlib import Path

from app.models.problem import Problem


def load_problems():
    file_path = Path("data/problems.json")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    problems = [Problem(**item) for item in data]

    return problems