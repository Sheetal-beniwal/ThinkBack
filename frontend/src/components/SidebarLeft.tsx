"use client";

import Link from "next/link";
import { BrainCircuit, Home, Search, Sparkles, BarChart2, Edit3, LayoutGrid, CheckSquare, Layers } from "lucide-react";
import { BrainCharacterDoodle } from "@/components/ui/Doodles";

interface SidebarLeftProps {
  activeNav?: string;
  onNavClick?: (nav: string) => void;
}

export default function SidebarLeft({ activeNav = "home", onNavClick }: SidebarLeftProps) {
  const navItems = [
    { id: "home", label: "Home", icon: Home },
    { id: "search", label: "Search", icon: Search },
    { id: "ask", label: "Ask AI", icon: Sparkles },
    { id: "progress", label: "My Progress", icon: BarChart2 },
  ];

  const stats = [
    { label: "Solved Problems", value: "20", icon: Edit3 },
    { label: "Patterns", value: "8", icon: LayoutGrid },
    { label: "Easy", value: "3", icon: Layers },
    { label: "Medium", value: "15", icon: Layers },
    { label: "Hard", value: "2", icon: CheckSquare },
  ];

  return (
    <aside className="w-56 shrink-0 flex flex-col justify-between py-6 px-4 bg-white border-r border-[#F3E8EE] min-h-screen sticky top-0 self-start">
      <div className="flex flex-col gap-7">
        {/* Logo & Brand */}
        <Link href="/" className="flex items-center gap-2.5 px-2 group">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-[#FCE7F3] border border-[#FBCFE8] text-[#DB2777]">
            <BrainCircuit className="h-5 w-5 text-[#EC4899]" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-black tracking-tight text-[#1E1035]">
              ThinkBack
            </span>
            <span className="text-[10px] font-semibold text-[#EC4899] leading-tight">
              Your DSA Memory Hub
            </span>
          </div>
        </Link>

        {/* Main Navigation */}
        <nav className="flex flex-col gap-1.5" aria-label="Sidebar navigation">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeNav === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavClick?.(item.id)}
                className={`flex items-center gap-3 px-4 py-2.5 rounded-2xl text-xs font-bold transition-all ${
                  isActive
                    ? "bg-[#FCE7F1] text-[#BE185D] shadow-2xs"
                    : "text-slate-500 hover:bg-purple-50/60 hover:text-purple-600"
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? "text-[#BE185D]" : "text-slate-400"}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Quick Stats Section */}
        <div className="flex flex-col gap-3.5 pt-4 border-t border-[#F3E8EE]">
          <div className="flex items-center gap-2 px-2 text-xs font-black text-[#1E1035]">
            <LayoutGrid className="h-3.5 w-3.5 text-purple-500" />
            <span>Quick Stats</span>
          </div>

          <div className="flex flex-col gap-2.5 px-2">
            {stats.map((stat, i) => {
              const Icon = stat.icon;
              return (
                <div key={i} className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <Icon className="h-3.5 w-3.5 text-slate-400" />
                    <span className="font-extrabold text-[#1E1035] text-[11px]">
                      {stat.value}
                    </span>
                  </div>
                  <span className="text-[11px] font-medium text-slate-400">
                    {stat.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Bottom Cute Doodle Illustration */}
      <div className="mt-8 flex flex-col items-center gap-1.5 pt-4 text-center border-t border-[#F3E8EE]">
        <p className="font-handwriting text-base font-bold text-[#DB2777] leading-tight rotate-[-2deg]">
          Small steps <br /> big progress ♡
        </p>
        <BrainCharacterDoodle className="mt-1" />
      </div>
    </aside>
  );
}
