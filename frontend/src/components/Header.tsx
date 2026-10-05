import { BrainCircuit } from "lucide-react";
import Link from "next/link";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-pink-100 bg-white/80 backdrop-blur-xl shadow-sm shadow-pink-100/60">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3.5">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-pink-400 to-rose-400 shadow-md shadow-pink-200 transition-all group-hover:shadow-pink-300 group-hover:scale-105">
            <BrainCircuit className="h-5 w-5 text-white" />
          </div>
          <div className="flex flex-col leading-tight">
            <span className="text-sm font-bold tracking-tight text-[#1E1B4B]">
              ThinkBack
            </span>
            <span className="text-[10px] font-medium text-pink-400 leading-none">
              AI-powered revision
            </span>
          </div>
        </Link>

        {/* Right — nav placeholder for future auth */}
        <nav className="flex items-center gap-3" aria-label="Main navigation">
          <span className="hidden rounded-full border border-pink-200 bg-pink-50 px-3 py-1 text-xs font-semibold text-pink-500 sm:inline-block">
            ✦ AI-Powered
          </span>
        </nav>
      </div>
    </header>
  );
}
