"use client";

import { useState } from "react";
import { searchProblems } from "@/lib/api";
import type { DifficultyFilter, Problem } from "@/types";
import ProblemCard from "@/components/ProblemCard";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import EmptyState from "@/components/ui/EmptyState";
import ErrorAlert from "@/components/ui/ErrorAlert";
import { DoodleArrow, StarDot } from "@/components/ui/Doodles";
import { Search, SlidersHorizontal } from "lucide-react";

// ─── Constants ────────────────────────────────────────────────────────────────

const DIFFICULTIES: DifficultyFilter[] = ["All", "Easy", "Medium", "Hard"];
const TOP_K_OPTIONS = [5, 10, 15, 20];

// ─── Component ────────────────────────────────────────────────────────────────

export default function SearchSection() {
  const [query, setQuery] = useState("");
  const [difficulty, setDifficulty] = useState<DifficultyFilter>("All");
  const [pattern, setPattern] = useState("");
  const [topK, setTopK] = useState(5);

  const [results, setResults] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setSearched(true);

    try {
      const data = await searchProblems({
        query: query.trim(),
        top_k: topK,
        difficulty: difficulty === "All" ? null : difficulty,
        pattern: pattern.trim() || null,
      });
      setResults(data.results);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong. Is the backend running?",
      );
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section aria-labelledby="search-heading" className="flex flex-col gap-6">
      {/* Section header */}
      <div className="flex flex-col gap-1">
        <h2
          id="search-heading"
          className="flex items-center gap-2 text-xl font-extrabold text-[#1E1B4B]"
        >
          <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-pink-400 to-rose-400 shadow-sm shadow-pink-200">
            <Search className="h-4 w-4 text-white" />
          </span>
          Semantic Search
          {/* Doodle accent — squiggly arrow like the reference */}
          <DoodleArrow className="h-5 w-8 text-pink-300 opacity-80" />
          <StarDot className="h-2.5 w-2.5 text-rose-300 opacity-70" />
        </h2>
        <p className="ml-10 text-sm font-medium text-slate-400">
          Describe what you&apos;re looking for in plain English.
        </p>
      </div>

      {/* Search card */}
      <div className="rounded-2xl border border-pink-100 bg-white p-5 shadow-sm shadow-pink-50">
        <form onSubmit={handleSearch} className="flex flex-col gap-4">
          {/* Query input row */}
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-pink-300" />
              <input
                id="search-query"
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. sliding window problems, two pointer techniques…"
                className="w-full rounded-xl border border-pink-100 bg-[#FFF8FB] py-3 pl-10 pr-4 text-sm font-medium text-[#1E1B4B] placeholder-slate-300 outline-none transition-all focus:border-pink-300 focus:ring-3 focus:ring-pink-100"
                aria-label="Search query"
              />
            </div>
            <button
              type="submit"
              disabled={!query.trim() || loading}
              className="shrink-0 rounded-xl bg-gradient-to-r from-pink-500 to-rose-400 px-6 py-3 text-sm font-bold text-white shadow-md shadow-pink-200 transition-all hover:from-pink-600 hover:to-rose-500 hover:shadow-pink-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-pink-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? "Searching…" : "✦ Search"}
            </button>
          </div>

          {/* Filters row */}
          <div className="flex flex-wrap items-center gap-2.5 border-t border-pink-50 pt-4">
            <span className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-400">
              <SlidersHorizontal className="h-3 w-3" />
              Filters
            </span>

            {/* Difficulty segmented control */}
            <div className="flex items-center gap-0.5 rounded-xl border border-pink-100 bg-pink-50 p-1">
              {DIFFICULTIES.map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => setDifficulty(d)}
                  className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                    difficulty === d
                      ? "bg-white text-pink-500 shadow-sm shadow-pink-100"
                      : "text-slate-400 hover:text-pink-400"
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>

            {/* Pattern filter */}
            <input
              id="pattern-filter"
              type="text"
              value={pattern}
              onChange={(e) => setPattern(e.target.value)}
              placeholder="Pattern (e.g. BFS)"
              className="rounded-xl border border-pink-100 bg-pink-50 px-3 py-2 text-xs font-medium text-[#1E1B4B] placeholder-slate-300 outline-none transition-all focus:border-pink-300 focus:ring-2 focus:ring-pink-100"
            />

            {/* Top K */}
            <div className="flex items-center gap-2 rounded-xl border border-pink-100 bg-pink-50 px-3 py-2">
              <label htmlFor="top-k" className="text-xs font-bold text-slate-400">
                Top
              </label>
              <select
                id="top-k"
                value={topK}
                onChange={(e) => setTopK(Number(e.target.value))}
                className="bg-transparent text-xs font-bold text-[#1E1B4B] outline-none"
              >
                {TOP_K_OPTIONS.map((k) => (
                  <option key={k} value={k}>
                    {k}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </form>
      </div>

      {/* Results area */}
      <div>
        {loading && <LoadingSpinner text="Finding your problems…" />}
        {error && !loading && <ErrorAlert message={error} />}
        {!loading && !error && searched && results.length === 0 && (
          <EmptyState
            title="No problems matched"
            description="Try a different query or remove the pattern/difficulty filter."
          />
        )}
        {!loading && results.length > 0 && (
          <>
            <p className="mb-4 text-xs font-bold uppercase tracking-wider text-slate-400">
              {results.length} result{results.length !== 1 ? "s" : ""} found
            </p>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {results.map((problem, i) => (
                <ProblemCard
                  key={`${problem.title}-${i}`}
                  problem={problem}
                  rank={i + 1}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </section>
  );
}
