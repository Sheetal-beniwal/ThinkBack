import type { Metadata } from "next";
import { Nunito, Caveat, Baloo_2 } from "next/font/google";
import "./globals.css";

const nunito = Nunito({
  subsets: ["latin"],
  variable: "--font-nunito",
  weight: ["400", "500", "600", "700", "800", "900"],
  display: "swap",
});

const caveat = Caveat({
  subsets: ["latin"],
  variable: "--font-caveat",
  weight: ["400", "600", "700"],
  display: "swap",
});

const baloo2 = Baloo_2({
  subsets: ["latin"],
  variable: "--font-baloo2",
  weight: ["700", "800"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "ThinkBack - Your DSA Memory Hub",
  description:
    "AI-powered revision for your solved LeetCode problems. Find patterns, analyze your strengths, and prepare smarter.",
  keywords: ["ThinkBack", "LeetCode", "DSA", "pattern finder", "AI", "revision", "algorithms"],
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${nunito.variable} ${caveat.variable} ${baloo2.variable}`}>
      <body className="min-h-screen bg-[#FFF5F8] text-[#1E1B4B] antialiased selection:bg-pink-200 selection:text-pink-900">
        {children}
      </body>
    </html>
  );
}
