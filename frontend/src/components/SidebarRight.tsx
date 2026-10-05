"use client";

import { useState } from "react";
import { Sparkles, SunMoon, ArrowRight, LayoutGrid } from "lucide-react";
import { askAI } from "@/lib/api";
import ErrorAlert from "@/components/ui/ErrorAlert";

interface SidebarRightProps {
  onSelectQuery?: (query: string) => void;
  onSelectPattern?: (pattern: string) => void;
}

export default function SidebarRight({ onSelectQuery, onSelectPattern }: SidebarRightProps) {
  const [aiQuery, setAiQuery] = useState("");
  const [aiAnswer, setAiAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const popularQuestions = [
    "What sliding window problems have I solved?",
    "Show me all binary search problems",
    "Give me medium level graph problems",
    "What are my strongest patterns?",
    "Suggest problems I might have forgotten",
  ];

  const patterns = [
    { title: "Binary Search", count: "5 problems", bg: "bg-[#F0F7FF] border-[#DBEAFE] hover:bg-blue-100/60", titleColor: "text-[#1E40AF]", countColor: "text-[#60A5FA]" },
    { title: "Two Pointers", count: "4 problems", bg: "bg-[#F8FAFC] border-[#F1F5F9] hover:bg-slate-100/80", titleColor: "text-[#334155]", countColor: "text-[#64748B]" },
    { title: "Sliding Window", count: "3 problems", bg: "bg-[#FFF1F2] border-[#FFE4E6] hover:bg-rose-100/60", titleColor: "text-[#BE123C]", countColor: "text-[#FB7185]" },
    { title: "Dynamic Programming", count: "3 problems", bg: "bg-[#F0FDF4] border-[#DCFCE7] hover:bg-emerald-100/60", titleColor: "text-[#15803D]", countColor: "text-[#4ADE80]" },
  ];

  const handleAsk = async (queryText?: string) => {
    const q = queryText || aiQuery;
    if (!q.trim()) return;

    if (queryText) {
      setAiQuery(queryText);
    }

    setLoading(true);
    setError(null);
    setAiAnswer(null);

    try {
      const res = await askAI({ query: q.trim() });
      setAiAnswer(res.answer);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get AI answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <aside className="w-80 shrink-0 flex flex-col gap-6 py-6 px-4 min-h-screen sticky top-0 self-start">
      {/* Top Header Controls: Theme toggle & Avatar */}
      <div className="flex items-center justify-end gap-3 px-1">
        <button
          type="button"
          aria-label="Toggle theme"
          className="flex h-8 w-8 items-center justify-center rounded-full bg-white border border-[#F3E8EE] text-slate-500 hover:text-purple-600 shadow-2xs transition-all"
        >
          <SunMoon className="h-4 w-4" />
        </button>

        {/* User avatar circle */}
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-[#EC4899] to-[#DB2777] text-white font-extrabold text-xs shadow-2xs">
          S
        </div>
      </div>

      {/* ── Ask AI Card ────────────────────────────────────────────────── */}
      <div className="flex flex-col gap-4 rounded-3xl border border-[#F3E8EE] bg-white p-5 shadow-2xs">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-purple-600" />
            <h3 className="text-sm font-black text-[#1E1035]">Ask AI</h3>
          </div>
          <span className="rounded-full bg-[#FCE7F1] border border-[#FBCFE8] px-2.5 py-0.5 text-[10px] font-bold text-[#BE185D]">
            Beta
          </span>
        </div>

        <p className="text-[11px] font-medium text-slate-500 leading-relaxed">
          Ask questions about your solved problems. Get personalized insights using RAG.
        </p>

        {/* Query Input Box */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void handleAsk();
          }}
          className="relative flex flex-col"
        >
          <textarea
            value={aiQuery}
            onChange={(e) => setAiQuery(e.target.value)}
            placeholder="e.g. What sliding window problems have I solved?"
            rows={3}
            className="w-full resize-none rounded-2xl border border-[#E9DDF0] bg-[#FBF9FE] p-3.5 pr-10 text-xs font-medium text-[#1E1035] placeholder-slate-400 outline-none transition-all focus:border-purple-400 focus:bg-white"
          />
          <button
            type="submit"
            disabled={!aiQuery.trim() || loading}
            aria-label="Send query"
            className="absolute bottom-2.5 right-2.5 flex h-7 w-7 items-center justify-center rounded-full bg-gradient-to-br from-[#9333EA] to-[#EC4899] text-white shadow-2xs transition-all hover:scale-105 disabled:opacity-40 disabled:hover:scale-100"
          >
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </form>

        {/* AI Output Answer Area */}
        {loading && (
          <div className="flex items-center gap-2 py-2 text-xs font-semibold text-purple-600">
            <Sparkles className="h-3.5 w-3.5 animate-spin" />
            Thinking...
          </div>
        )}

        {error && <ErrorAlert message={error} />}

        {aiAnswer && !loading && (
          <div className="rounded-2xl bg-purple-50/70 p-3.5 border border-purple-100 text-xs text-slate-700 font-medium leading-relaxed max-h-48 overflow-y-auto">
            <span className="block font-bold text-purple-700 mb-1">AI Answer:</span>
            {aiAnswer}
          </div>
        )}

        {/* Popular Questions List */}
        <div className="flex flex-col gap-2 pt-1">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            Popular questions
          </span>
          <div className="flex flex-col gap-1.5">
            {popularQuestions.map((q, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setAiQuery(q);
                  onSelectQuery?.(q);
                  void handleAsk(q);
                }}
                className="text-left rounded-2xl bg-[#F8F5FC] border border-[#F0E6F7] px-3.5 py-2 text-[11px] font-medium text-[#4A3B69] transition-all hover:bg-[#F3E8FF] hover:border-purple-200 hover:text-[#7E22CE]"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ── Your Patterns Card ────────────────────────────────────────── */}
      <div className="flex flex-col gap-4 rounded-3xl border border-[#F3E8EE] bg-white p-5 shadow-2xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <LayoutGrid className="h-4 w-4 text-purple-600" />
            <h3 className="text-sm font-black text-[#1E1035]">Your Patterns</h3>
          </div>
          <button
            type="button"
            onClick={() => onSelectPattern?.("")}
            className="flex items-center gap-1 text-[11px] font-bold text-purple-600 hover:text-purple-700"
          >
            View all <ArrowRight className="h-3 w-3" />
          </button>
        </div>

        {/* 2x2 Grid of Patterns */}
        <div className="grid grid-cols-2 gap-2.5">
          {patterns.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => onSelectPattern?.(p.title)}
              className={`flex flex-col items-start p-3 rounded-2xl border transition-all text-left ${p.bg}`}
            >
              <span className={`text-xs font-black leading-tight ${p.titleColor}`}>
                {p.title}
              </span>
              <span className={`text-[10px] font-bold mt-1 ${p.countColor}`}>
                {p.count}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Bottom Doodle Note */}
      <div className="mt-2 text-center select-none">
        <p className="font-handwriting text-base font-bold text-[#DB2777] rotate-[-1deg]">
          ♡ Better recall &nbsp; Bigger goals ♡
        </p>
      </div>
    </aside>
  );
}
