import type { Problem } from "@/types";
import DifficultyBadge from "@/components/ui/DifficultyBadge";
import PatternBadge from "@/components/ui/PatternBadge";
import ScoreBar from "@/components/ui/ScoreBar";
import { StarDot } from "@/components/ui/Doodles";
import { ExternalLink } from "lucide-react";

interface ProblemCardProps {
  problem: Problem;
  rank: number;
}

export default function ProblemCard({ problem, rank }: ProblemCardProps) {
  return (
    <article className="group relative flex flex-col gap-4 rounded-2xl border border-pink-100 bg-white p-5 shadow-sm shadow-pink-50 transition-all duration-200 hover:border-pink-200 hover:shadow-md hover:shadow-pink-100 hover:-translate-y-0.5">
      {/* Rank badge */}
      <span className="absolute right-4 top-4 flex h-6 w-6 items-center justify-center rounded-full bg-pink-50 text-[10px] font-bold text-pink-400">
        #{rank}
      </span>

      {/* Tiny sparkle doodle — top-left corner decoration */}
      <StarDot className="absolute left-3 top-3 h-2 w-2 text-pink-200 opacity-60" />

      {/* Header */}
      <div className="flex flex-col gap-2.5 pr-8">
        <h3 className="text-sm font-bold leading-snug text-[#1E1B4B] group-hover:text-pink-600 transition-colors">
          {problem.title}
        </h3>
        <div className="flex flex-wrap items-center gap-1.5">
          <DifficultyBadge difficulty={problem.difficulty} />
          <PatternBadge pattern={problem.primary_pattern} />
        </div>
      </div>

      {/* Score */}
      <ScoreBar score={problem.score} />

      {/* CTA */}
      <a
        href={problem.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center justify-center gap-2 rounded-xl border border-pink-200 bg-pink-50 px-4 py-2.5 text-xs font-bold text-pink-500 transition-all duration-150 hover:bg-gradient-to-r hover:from-pink-500 hover:to-rose-400 hover:text-white hover:border-pink-500 hover:shadow-md hover:shadow-pink-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-pink-400"
      >
        Open on LeetCode
        <ExternalLink className="h-3.5 w-3.5" />
      </a>
    </article>
  );
}
