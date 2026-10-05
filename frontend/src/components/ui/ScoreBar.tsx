interface ScoreBarProps {
  score: number; // 0–1
}

export default function ScoreBar({ score }: ScoreBarProps) {
  const pct = Math.round(score * 100);

  const gradient =
    pct >= 80
      ? "from-emerald-400 to-teal-300"
      : pct >= 60
        ? "from-pink-400 to-rose-300"
        : "from-slate-300 to-slate-200";

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 overflow-hidden rounded-full bg-pink-50 h-2">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${gradient}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="min-w-[3ch] text-right text-[11px] font-bold tabular-nums text-slate-400">
        {pct}%
      </span>
    </div>
  );
}
