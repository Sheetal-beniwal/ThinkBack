interface PatternBadgeProps {
  pattern: string;
}

export default function PatternBadge({ pattern }: PatternBadgeProps) {
  return (
    <span className="inline-flex items-center rounded-full border border-pink-200 bg-pink-50 px-2.5 py-0.5 text-[11px] font-bold text-pink-500">
      {pattern}
    </span>
  );
}
