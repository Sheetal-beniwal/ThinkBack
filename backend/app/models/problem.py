from pydantic import BaseModel
from typing import List


class Problem(BaseModel):
    problem_id: int
    title: str
    difficulty: str
    description: str
    tags: List[str]
    url: str