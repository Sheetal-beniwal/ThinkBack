"use client";

import type { DifficultyFilter } from "@/types";
import { ChevronDown, LayoutGrid, SlidersHorizontal } from "lucide-react";

interface FilterBarProps {
  selectedDifficulty: DifficultyFilter;
  onDifficultyChange: (diff: DifficultyFilter) => void;
  selectedPattern: string;
  onPatternChange: (pattern: string) => void;
  sortBy: string;
  onSortByChange: (sort: string) => void;
}

export default function FilterBar({
  selectedDifficulty,
  onDifficultyChange,
  selectedPattern,
  onPatternChange,
  sortBy,
  onSortByChange,
}: FilterBarProps) {
  const difficulties: DifficultyFilter[] = ["All", "Easy", "Medium", "Hard"];
  const patternOptions = [
    "All Patterns",
    "Binary Search",
    "Two Pointers",
    "Sliding Window",
    "Dynamic Programming",
    "Breadth-First Search",
    "Depth-First Search",
  ];

  return (
    <div className="flex flex-wrap items-center justify-between gap-4 py-2">
      {/* Left side: Difficulty segmented control */}
      <div className="flex items-center gap-1">
        {difficulties.map((diff) => {
          const isActive = selectedDifficulty === diff;
          return (
            <button
              key={diff}
              type="button"
              onClick={() => onDifficultyChange(diff)}
              className={`rounded-full px-5 py-1.5 text-xs font-bold transition-all ${
                isActive
                  ? "bg-[#9333EA] text-white shadow-2xs"
                  : "text-slate-500 hover:text-slate-900 hover:bg-slate-100/60"
              }`}
            >
              {diff}
            </button>
          );
        })}
      </div>

      {/* Right side: Pattern & Sort by Dropdowns */}
      <div className="flex items-center gap-2.5">
        {/* Pattern Dropdown */}
        <div className="relative">
          <select
            value={selectedPattern || "All Patterns"}
            onChange={(e) => {
              const val = e.target.value;
              onPatternChange(val === "All Patterns" ? "" : val);
            }}
            aria-label="Filter by Pattern"
            className="appearance-none rounded-full border border-slate-200 bg-white py-1.5 pl-8 pr-7 text-xs font-bold text-slate-700 shadow-2xs outline-none transition-all focus:border-purple-300"
          >
            {patternOptions.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
          <LayoutGrid className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-purple-600" />
          <ChevronDown className="pointer-events-none absolute right-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400" />
        </div>

        {/* Sort by Dropdown */}
        <div className="relative">
          <select
            value={sortBy}
            onChange={(e) => onSortByChange(e.target.value)}
            aria-label="Sort options"
            className="appearance-none rounded-full border border-slate-200 bg-white py-1.5 pl-8 pr-7 text-xs font-bold text-slate-700 shadow-2xs outline-none transition-all focus:border-purple-300"
          >
            <option value="relevance">Relevance</option>
            <option value="acceptance">Acceptance Rate</option>
            <option value="submissions">Submissions</option>
          </select>
          <SlidersHorizontal className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-purple-600" />
          <ChevronDown className="pointer-events-none absolute right-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400" />
        </div>
      </div>
    </div>
  );
}
