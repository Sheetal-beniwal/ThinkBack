import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";

const nunito = Nunito({
  subsets: ["latin"],
  variable: "--font-nunito",
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "LeetCode Pattern Finder",
  description:
    "AI-powered semantic search and revision assistant for your solved LeetCode problems. Find patterns, analyze your strengths, and prepare smarter.",
  keywords: ["LeetCode", "DSA", "pattern finder", "AI", "revision", "algorithms"],
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={nunito.variable}>
      <body className="min-h-screen bg-[#FFF5F7] text-[#1E1B4B] antialiased">
        {/* Subtle background decoration — soft pink blobs */}
        <div aria-hidden="true" className="pointer-events-none fixed inset-0 overflow-hidden">
          <div className="absolute -right-40 -top-40 h-[500px] w-[500px] rounded-full bg-pink-200/30 blur-3xl" />
          <div className="absolute -bottom-40 -left-40 h-[400px] w-[400px] rounded-full bg-rose-200/20 blur-3xl" />
        </div>

        <Header />
        <main className="relative">{children}</main>

        <footer className="mt-20 border-t border-pink-100 py-6 text-center text-xs text-slate-400 font-medium">
          LeetCode Pattern Finder · AI-powered DSA revision
        </footer>
      </body>
    </html>
  );
}
