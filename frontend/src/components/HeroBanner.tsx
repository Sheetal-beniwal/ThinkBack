"use client";

import { useState } from "react";
import { Search, ArrowRight } from "lucide-react";

interface HeroBannerProps {
  onSearch: (query: string) => void;
  loading?: boolean;
}

export default function HeroBanner({ onSearch, loading }: HeroBannerProps) {
  const [query, setQuery] = useState("");

  const suggestionTags = [
    "sliding window problems",
    "two pointer techniques",
    "binary search",
    "dynamic programming",
  ];

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleTagClick = (tag: string) => {
    setQuery(tag);
    onSearch(tag);
  };

  return (
    /* Hero card — warm cream on left → soft peach-lavender on right, exactly as in the reference */
    <div className="relative overflow-hidden rounded-3xl p-7 sm:p-9 border border-[#EFE3FB]"
      style={{ background: "linear-gradient(120deg, #FDF6FF 0%, #FCF0F9 40%, #F3E4FA 70%, #EDD5F5 100%)" }}
    >
      {/* ── Landscape Illustration on Bottom-Right ─────────────────────────── */}
      <div className="pointer-events-none absolute right-0 bottom-0 h-[200px] w-[380px] select-none overflow-hidden">
        <svg
          viewBox="0 0 380 200"
          className="w-full h-full"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* ── Sun / warm glow circle top-right ── */}
          <circle cx="310" cy="55" r="38" fill="#FDE7F5" opacity="0.55" />
          <circle cx="310" cy="55" r="24" fill="#F9CEEE" opacity="0.4" />

          {/* ── Far background hills (lightest) ── */}
          <ellipse cx="200" cy="190" rx="200" ry="70" fill="#F2D9F7" opacity="0.45" />

          {/* ── Left mid-ground hill ── */}
          <path
            d="M 0 200 Q 60 130 130 145 Q 180 155 200 200 Z"
            fill="#E8C5F2"
            opacity="0.55"
          />

          {/* ── Main right mountain / hill with rounded peak ── */}
          <path
            d="M 140 200 Q 200 100 260 75 Q 300 60 330 90 Q 360 115 380 200 Z"
            fill="#D9AEEA"
            opacity="0.75"
          />

          {/* ── Highlight on mountain face ── */}
          <path
            d="M 240 200 Q 265 115 285 88 Q 300 75 315 95 Q 335 120 340 200 Z"
            fill="#E8C8F5"
            opacity="0.6"
          />

          {/* ── Winding dotted path up the mountain ── */}
          {/* Dots going from bottom-center up to the peak */}
          <circle cx="252" cy="195" r="2.5" fill="#C084FC" opacity="0.55" />
          <circle cx="258" cy="183" r="2.5" fill="#C084FC" opacity="0.55" />
          <circle cx="262" cy="171" r="2.5" fill="#C084FC" opacity="0.55" />
          <circle cx="264" cy="158" r="2.5" fill="#C084FC" opacity="0.5" />
          <circle cx="265" cy="145" r="2.5" fill="#C084FC" opacity="0.5" />
          <circle cx="264" cy="132" r="2.5" fill="#C084FC" opacity="0.45" />
          <circle cx="262" cy="119" r="2" fill="#C084FC" opacity="0.4" />
          <circle cx="261" cy="107" r="2" fill="#C084FC" opacity="0.4" />

          {/* ── Flagpole ── */}
          <line x1="261" y1="72" x2="261" y2="102" stroke="#9D2CB3" strokeWidth="2" strokeLinecap="round" />

          {/* ── Flag (red/pink triangle pointing right) ── */}
          <path d="M 261 72 L 281 80 L 261 88 Z" fill="#EC4899" />

          {/* ── Small pink heart floating near flag ── */}
          <path
            d="M 290 76 C 290 76 286.5 72.5 286.5 70.2 C 286.5 68.4 287.8 67 289.5 67 C 290.3 67 291.1 67.4 291.6 68.1 C 292.1 67.4 292.9 67 293.7 67 C 295.4 67 296.7 68.4 296.7 70.2 C 296.7 72.5 293.2 76 293.2 76 Z"
            fill="#EC4899"
          />

          {/* ── Floating pink/purple dots in sky ── */}
          <circle cx="190" cy="100" r="3.5" fill="#EC4899" opacity="0.4" />
          <circle cx="170" cy="120" r="2.2" fill="#C084FC" opacity="0.35" />
          <circle cx="215" cy="85" r="1.8" fill="#F472B6" opacity="0.3" />
        </svg>
      </div>

      {/* ── Top-Right Handwritten Cursive Note ─────────────────────────────── */}
      <div className="absolute top-5 right-[220px] hidden sm:block z-10 text-right">
        <p className="font-handwriting text-[16px] font-semibold text-[#B060C0] leading-snug rotate-[-1deg]">
          You solved it before. <br />
          Now remember how. ♡
        </p>
      </div>

      {/* ── Main Content Area ───────────────────────────────────────────────── */}
      <div className="relative z-10 flex flex-col gap-3.5 max-w-[520px]">

        {/* Headings */}
        <div className="flex flex-col gap-0">
          <h1
            className="text-[34px] sm:text-[42px] tracking-tight text-[#1A0828] leading-tight"
            style={{ fontFamily: "var(--font-baloo2), system-ui, sans-serif", fontWeight: 800 }}
          >
            Find Your Patterns.
          </h1>
          <span
            className="text-[34px] sm:text-[42px] tracking-tight text-[#E0299A] leading-tight"
            style={{ fontFamily: "var(--font-baloo2), system-ui, sans-serif", fontWeight: 800 }}
          >
            Solve Smarter.
          </span>
        </div>

        {/* Subtitle */}
        <p className="text-[13px] font-semibold text-[#8A6A9A]">
          AI-powered revision for your solved LeetCode problems.
        </p>

        {/* Search Input Bar */}
        <form onSubmit={handleSubmit} className="mt-1.5 flex flex-col gap-3">
          <div className="flex items-center rounded-full bg-white px-2 py-1.5 shadow-[0_2px_16px_rgba(160,100,210,0.12)] border border-white">
            <Search className="ml-3 h-4 w-4 shrink-0 text-[#B4A0C8]" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe what you're looking for in plain English..."
              className="w-full bg-transparent px-3 py-2 text-[12px] font-medium text-[#1A0828] placeholder-[#B4A0C8] outline-none"
            />
            {/* Solid flat purple button — no gradient */}
            <button
              type="submit"
              disabled={!query.trim() || loading}
              className="flex shrink-0 items-center gap-1.5 rounded-full bg-[#9B51E0] px-6 py-2.5 text-[12px] font-bold text-white transition-colors hover:bg-[#8433CC] disabled:opacity-40"
            >
              {loading ? "Searching..." : "Search"}
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>

          {/* Suggested tags — plain underline-on-hover style matching reference */}
          <div className="flex flex-wrap items-center gap-x-3 gap-y-2 px-1">
            <span className="text-[12px] font-bold text-[#A090B8]">Try:</span>
            {suggestionTags.map((tag, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleTagClick(tag)}
                className="rounded-full border border-[#E4D5F5]/80 bg-white/70 px-3.5 py-1 text-[11px] font-semibold text-[#7A6296] transition-all hover:bg-white hover:border-[#C084FC] hover:text-[#7E22CE]"
              >
                {tag}
              </button>
            ))}
          </div>
        </form>
      </div>
    </div>
  );
}
