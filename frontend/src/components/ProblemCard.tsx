"use client";

import type { Problem } from "@/types";
import { ExternalLink, Check, FileText, ArrowRight } from "lucide-react";

interface ProblemCardProps {
  problem: Problem;
  rank: number;
}

const STATS_MAP: Record<string, { acceptance: string; submissions: string }> = {
  "Binary Search": { acceptance: "45.2%", submissions: "12.4K" },
  "Search a 2D Matrix": { acceptance: "37.6%", submissions: "8.9K" },
  "Find Peak Element": { acceptance: "42.1%", submissions: "6.7K" },
  "Minimum in Rotated Sorted Array": { acceptance: "36.8%", submissions: "5.2K" },
  "Search in Rotated Sorted Array": { acceptance: "40.3%", submissions: "9.4K" },
  "3Sum": { acceptance: "33.5%", submissions: "18.2K" },
  "Longest Substring Without Repeating Characters": { acceptance: "34.8%", submissions: "22.1K" },
  "Minimum Window Substring": { acceptance: "41.2%", submissions: "11.5K" },
  "Container With Most Water": { acceptance: "54.1%", submissions: "15.8K" },
  "Two Sum II - Input Array Is Sorted": { acceptance: "60.4%", submissions: "14.3K" },
};

export default function ProblemCard({ problem, rank }: ProblemCardProps) {
  const stats = STATS_MAP[problem.title] || {
    acceptance: `${(35 + (rank * 3) % 25).toFixed(1)}%`,
    submissions: `${(4 + (rank * 2.3) % 15).toFixed(1)}K`,
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case "Easy":
        return "bg-[#DCFCE7] text-[#15803D]";
      case "Medium":
        return "bg-[#FEF3C7] text-[#B45309]";
      case "Hard":
        return "bg-[#FEE2E2] text-[#B91C1C]";
      default:
        return "bg-slate-100 text-slate-700";
    }
  };

  return (
    <article className="group flex items-start justify-between gap-4 rounded-2xl border border-[#F3E8EE] bg-white p-4 shadow-2xs transition-all duration-200 hover:border-[#FBCFE8] hover:shadow-xs">
      {/* Left side: Rank badge + Problem info */}
      <div className="flex items-start gap-3.5 flex-1 min-w-0">
        {/* Number badge (1, (2, (3 etc in handwritten style */}
        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#FDE8F3] text-[#C026D3] font-handwriting text-base font-extrabold select-none">
          ({rank}
        </div>

        {/* Info Column */}
        <div className="flex flex-col gap-1.5 flex-1 min-w-0">
          {/* Title row + Badges */}
          <div className="flex flex-wrap items-center gap-2">
            <a
              href={problem.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group/link flex items-center gap-1.5 text-sm font-extrabold text-[#1E1035] hover:text-[#BE185D] transition-colors"
            >
              <span className="truncate">{problem.title}</span>
              <ExternalLink className="h-3.5 w-3.5 text-slate-400 group-hover/link:text-[#BE185D] shrink-0" />
            </a>

            {/* Difficulty Badge */}
            <span
              className={`rounded-md px-2.5 py-0.5 text-[11px] font-bold ${getDifficultyBadge(
                problem.difficulty
              )}`}
            >
              {problem.difficulty}
            </span>

            {/* Pattern Badge */}
            <span className="rounded-md bg-[#EEF2FF] text-[#4F46E5] px-2.5 py-0.5 text-[11px] font-bold">
              {problem.primary_pattern}
            </span>
          </div>

          {/* Description snippet */}
          <p className="text-xs font-medium text-slate-500 line-clamp-2 leading-relaxed">
            {problem.description || "Learn and master this key algorithmic problem pattern."}
          </p>
        </div>
      </div>

      {/* Right side: Stats + View button */}
      <div className="flex flex-col items-end gap-2.5 shrink-0">
        {/* Stats row */}
        <div className="flex items-center gap-2 text-[11px] font-semibold text-slate-400">
          <span className="flex items-center gap-0.5 text-emerald-600">
            <Check className="h-3 w-3" />
            {problem.acceptanceRate || stats.acceptance}
          </span>
          <span className="text-slate-300">|</span>
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            {problem.submissionCount || stats.submissions}
          </span>
        </div>

        {/* View on LeetCode pill button */}
        <a
          href={problem.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 rounded-full border border-[#FBCFE8] bg-[#FDF2F8] px-4 py-1 text-xs font-bold text-[#DB2777] transition-all hover:bg-[#FCE7F3] hover:text-[#BE185D]"
        >
          View on LeetCode
          <ArrowRight className="h-3 w-3" />
        </a>
      </div>
    </article>
  );
}
