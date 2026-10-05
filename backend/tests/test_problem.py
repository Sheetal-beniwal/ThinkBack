from app.models.problem import Problem


problem = Problem(
    problem_id=15,
    title="3Sum",
    difficulty="Medium",
    description="Find triplets whose sum is zero.",
    tags=["Array", "Two Pointers"],
    url="https://leetcode.com/problems/3sum/"
)

print(problem)