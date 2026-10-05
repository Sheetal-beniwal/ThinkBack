interface DifficultyBadgeProps {
  difficulty: "Easy" | "Medium" | "Hard";
}

const styles: Record<DifficultyBadgeProps["difficulty"], string> = {
  Easy:   "bg-emerald-50 text-emerald-600 border-emerald-200",
  Medium: "bg-amber-50  text-amber-600  border-amber-200",
  Hard:   "bg-rose-50   text-rose-600   border-rose-200",
};

export default function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-bold tracking-wide ${styles[difficulty]}`}
    >
      {difficulty}
    </span>
  );
}
