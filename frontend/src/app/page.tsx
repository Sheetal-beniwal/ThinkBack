import SearchSection from "@/components/SearchSection";
import AskSection from "@/components/AskSection";
import {
  Sparkle,
  StarDot,
  WavyUnderline,
  HeartDoodle,
  PencilDoodle,
} from "@/components/ui/Doodles";

export default function Home() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      {/* ── Hero ───────────────────────────────────────────────────────── */}
      <section className="relative mb-14 flex flex-col items-center gap-5 text-center">

        {/* ── Floating doodle decorations ── */}

        {/* Top-left sparkle cluster */}
        <Sparkle className="absolute -left-4 top-0 h-6 w-6 rotate-12 text-pink-300 opacity-70 sm:-left-10" />
        <StarDot className="absolute left-4 top-10 h-3 w-3 text-rose-300 opacity-60 sm:left-0" />
        <StarDot className="absolute left-10 top-2 h-2 w-2 text-pink-400 opacity-50 sm:left-6" />

        {/* Top-right sparkle cluster */}
        <Sparkle className="absolute -right-4 top-2 h-5 w-5 -rotate-12 text-violet-300 opacity-60 sm:-right-10" />
        <StarDot className="absolute right-4 top-12 h-3 w-3 text-pink-300 opacity-70 sm:right-2" />
        <StarDot className="absolute right-12 top-1 h-2 w-2 text-rose-300 opacity-50" />

        {/* Bottom-left heart */}
        <HeartDoodle className="absolute bottom-8 left-0 h-5 w-5 text-rose-300 opacity-50 sm:-left-8" />

        {/* Bottom-right pencil */}
        <PencilDoodle className="absolute bottom-4 right-0 h-6 w-6 -rotate-12 text-pink-300 opacity-50 sm:-right-8" />

        {/* Extra scattered dots */}
        <StarDot className="absolute bottom-0 right-16 h-2.5 w-2.5 text-violet-300 opacity-40" />
        <StarDot className="absolute top-20 left-20 h-2 w-2 text-pink-200 opacity-60 hidden sm:block" />

        {/* ── Content ── */}
        <div className="inline-flex items-center gap-2 rounded-full border border-pink-200 bg-white px-4 py-1.5 text-xs font-semibold text-pink-500 shadow-sm shadow-pink-100">
          <Sparkle className="h-3 w-3" />
          Semantic search · RAG-powered answers
        </div>

        {/* Main heading with wavy underline on the keyword */}
        <h1 className="max-w-2xl text-4xl font-extrabold tracking-tight text-[#1E1B4B] sm:text-5xl">
          Find Your{" "}
          <span className="relative inline-block">
            <span className="bg-gradient-to-r from-pink-500 via-rose-400 to-pink-400 bg-clip-text text-transparent">
              Patterns.
            </span>
            {/* Wavy underline */}
            <WavyUnderline className="absolute -bottom-2 left-0 w-full text-pink-300 opacity-70" />
          </span>{" "}
          Solve Smarter.
        </h1>

        <p className="max-w-lg text-base font-medium text-slate-500">
          AI-powered revision for your solved LeetCode problems. Search
          semantically, find patterns, and get personalized insights.
        </p>

        {/* Small "you can do it!" doodle note */}
        <div className="flex items-center gap-1.5 rounded-2xl border border-pink-100 bg-pink-50 px-3 py-1.5 text-xs font-bold text-pink-400 rotate-[-1deg] shadow-sm">
          <HeartDoodle className="h-3 w-3 text-rose-400" />
          you can do it!
        </div>
      </section>

      {/* ── Main content ───────────────────────────────────────────────── */}
      <div className="flex flex-col gap-12">
        <SearchSection />

        {/* Divider */}
        <div className="flex items-center gap-4">
          <div className="h-px flex-1 bg-pink-100" />
          <span className="text-xs font-bold uppercase tracking-widest text-pink-300">
            Ask AI
          </span>
          <div className="h-px flex-1 bg-pink-100" />
        </div>

        <AskSection />
      </div>
    </div>
  );
}
