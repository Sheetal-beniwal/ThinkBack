from app.services.ingestion import load_problems
from app.services.pattern_service import (
    classify_all_problems,
    save_enriched_problems
)


problems = load_problems()

enriched_problems = classify_all_problems(problems)

save_enriched_problems(enriched_problems)