"use client";

import { useState } from "react";
import { askAI } from "@/lib/api";
import ErrorAlert from "@/components/ui/ErrorAlert";
import { DoodleArrow, StarDot, HeartDoodle } from "@/components/ui/Doodles";
import { Sparkles, Send } from "lucide-react";

export default function AskSection() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAsk = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const data = await askAI({ query: query.trim() });
      setAnswer(data.answer);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not reach the AI service. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      void handleAsk();
    }
  };

  return (
    <section aria-labelledby="ask-heading" className="flex flex-col gap-6">
      {/* Section header */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex flex-col gap-1">
          <h2
            id="ask-heading"
            className="flex items-center gap-2 text-xl font-extrabold text-[#1E1B4B]"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-violet-400 to-pink-400 shadow-sm shadow-violet-200">
              <Sparkles className="h-4 w-4 text-white" />
            </span>
            Ask AI
            {/* Doodle accent */}
            <DoodleArrow className="h-5 w-8 text-violet-300 opacity-80" />
            <StarDot className="h-2.5 w-2.5 text-pink-300 opacity-70" />
          </h2>
          <p className="ml-10 text-sm font-medium text-slate-400">
            Ask anything about your solved problems — the AI answers from your personal data.
          </p>
        </div>

        {/* Small motivational doodle note — like the reference */}
        <div className="hidden shrink-0 rotate-2 flex-col items-center gap-1 rounded-2xl border border-pink-100 bg-pink-50 px-3 py-2 text-center shadow-sm sm:flex">
          <HeartDoodle className="h-4 w-4 text-rose-400" />
          <p className="text-[10px] font-bold leading-tight text-pink-400">
            small steps<br />build big progress
          </p>
        </div>
      </div>

      {/* Textarea card */}
      <div className="rounded-2xl border border-pink-100 bg-white p-5 shadow-sm shadow-pink-50">
        <form onSubmit={handleAsk} className="flex flex-col gap-3">
          <div className="relative rounded-xl border border-pink-100 bg-[#FFF8FB] focus-within:border-violet-300 focus-within:ring-3 focus-within:ring-violet-100 transition-all">
            <textarea
              id="ask-query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={4}
              placeholder="Which sliding window problems have I solved? What BFS patterns do I know?…"
              className="w-full resize-none rounded-xl bg-transparent px-4 pt-4 pb-14 text-sm font-medium text-[#1E1B4B] placeholder-slate-300 outline-none"
              aria-label="Ask AI input"
            />
            <div className="absolute bottom-3 right-3 flex items-center gap-2">
              <span className="hidden text-xs font-medium text-slate-300 sm:block">
                ⌘↵ to send
              </span>
              <button
                type="submit"
                disabled={!query.trim() || loading}
                className="flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-violet-500 to-pink-500 px-4 py-2 text-xs font-bold text-white shadow-md shadow-violet-200 transition-all hover:from-violet-600 hover:to-pink-600 hover:shadow-violet-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400 disabled:cursor-not-allowed disabled:opacity-40"
              >
                <Send className="h-3 w-3" />
                {loading ? "Thinking…" : "Ask AI"}
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Error */}
      {error && <ErrorAlert message={error} />}

      {/* Loading skeleton */}
      {loading && (
        <div className="flex flex-col gap-4 rounded-2xl border border-violet-100 bg-white p-5 shadow-sm shadow-violet-50">
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-violet-100 border-t-violet-400" />
            <span className="text-sm font-semibold text-slate-400">
              Thinking…
            </span>
          </div>
          <div className="space-y-2.5">
            <div className="h-3 w-3/4 animate-pulse rounded-full bg-pink-50" />
            <div className="h-3 w-full animate-pulse rounded-full bg-pink-50" />
            <div className="h-3 w-2/3 animate-pulse rounded-full bg-pink-50" />
          </div>
        </div>
      )}

      {/* Answer card */}
      {answer && !loading && (
        <div className="flex flex-col gap-4 rounded-2xl border border-violet-100 bg-white p-6 shadow-sm shadow-violet-50">
          {/* Answer header */}
          <div className="flex items-center gap-2 border-b border-pink-50 pb-4">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-violet-400 to-pink-400">
              <Sparkles className="h-3.5 w-3.5 text-white" />
            </div>
            <span className="text-xs font-extrabold uppercase tracking-widest text-violet-500">
              AI Answer
            </span>
          </div>
          {/* Answer body — preserves LLM newlines/formatting */}
          <pre className="whitespace-pre-wrap break-words font-sans text-sm font-medium leading-relaxed text-slate-600">
            {answer}
          </pre>
        </div>
      )}
    </section>
  );
}
