/**
 * Reusable hand-drawn / doodle SVG components.
 * Keep all doodle assets here so they're easy to tweak or swap.
 */

// ─── 4-point sparkle star ────────────────────────────────────────────────────
export function Sparkle({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M12 2C12 2 13 8 15 10C17 12 23 12 23 12C23 12 17 13 15 15C13 17 12 23 12 23C12 23 11 17 9 15C7 13 1 12 1 12C1 12 7 11 9 10C11 8 12 2 12 2Z" />
    </svg>
  );
}

// ─── Tiny 4-point star (smaller variant) ─────────────────────────────────────
export function StarDot({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 12 12"
      className={className}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M6 0C6 0 6.6 3.8 7.8 5C9 6.2 12 6 12 6C12 6 9 6.5 7.8 7.8C6.6 9 6 12 6 12C6 12 5.4 9 4.2 7.8C3 6.5 0 6 0 6C0 6 3 5.8 4.2 5C5.4 3.8 6 0 6 0Z" />
    </svg>
  );
}

// ─── Hand-drawn squiggly arrow (for section headings) ────────────────────────
export function DoodleArrow({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 38 18"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {/* Squiggly line */}
      <path d="M2 9 C6 4, 10 14, 14 9 C18 4, 22 14, 26 9" />
      {/* Arrowhead */}
      <path d="M26 9 L32 9" />
      <path d="M28.5 6 L32 9 L28.5 12" />
    </svg>
  );
}

// ─── Wavy underline (for hero title highlight) ────────────────────────────────
export function WavyUnderline({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 180 10"
      preserveAspectRatio="none"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M0 6 C15 1, 30 9, 45 6 C60 1, 75 9, 90 6 C105 1, 120 9, 135 6 C150 1, 165 9, 180 6" />
    </svg>
  );
}

// ─── Small heart ─────────────────────────────────────────────────────────────
export function HeartDoodle({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M12 21C12 21 3 14 3 8.5C3 5.42 5.42 3 8.5 3C10.24 3 11.91 3.81 13 5.08C14.09 3.81 15.76 3 17.5 3C20.58 3 23 5.42 23 8.5C23 14 14 21 12 21Z" />
    </svg>
  );
}

// ─── Pencil / writing doodle ──────────────────────────────────────────────────
export function PencilDoodle({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
      <path d="m15 5 4 4" />
    </svg>
  );
}

// ─── Cute Pink Brain Character Doodle ──────────────────────────────────────────
export function BrainCharacterDoodle({ className = "" }: { className?: string }) {
  return (
    <div className={`relative flex flex-col items-center select-none ${className}`}>
      {/* Lightbulb above head */}
      <div className="relative mb-0.5 flex items-center justify-center">
        <svg viewBox="0 0 24 24" className="h-5 w-5 text-amber-400" fill="currentColor">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.87-3.13-7-7-7zm-2 17h4v1h-4v-1zm1 3h2v1h-2v-1z"/>
        </svg>
        {/* Glow rays */}
        <span className="absolute -top-1 -left-1 h-1 w-1 rounded-full bg-amber-300 animate-ping" />
        <span className="absolute -top-1 -right-1 h-1 w-1 rounded-full bg-amber-300 animate-ping" />
      </div>

      {/* Main Brain Character */}
      <div className="relative">
        <svg viewBox="0 0 100 80" className="h-16 w-20 text-pink-300">
          {/* Outer Brain Outline */}
          <path
            d="M 30,65 C 15,65 10,50 15,40 C 8,32 12,18 25,18 C 30,10 45,10 50,18 C 55,10 70,10 75,18 C 88,18 92,32 85,40 C 90,50 85,65 70,65 C 65,75 35,75 30,65 Z"
            fill="#FBCFE8"
            stroke="#F472B6"
            strokeWidth="3"
            strokeLinejoin="round"
          />
          {/* Inner Brain Folds */}
          <path
            d="M 30,30 C 35,25 45,35 50,30 C 55,25 65,35 70,30"
            fill="none"
            stroke="#EC4899"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          <path
            d="M 25,45 C 32,40 40,50 50,45 C 60,50 68,40 75,45"
            fill="none"
            stroke="#EC4899"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          {/* Eyes */}
          <circle cx="38" cy="45" r="3" fill="#1E1B4B" />
          <circle cx="62" cy="45" r="3" fill="#1E1B4B" />
          {/* Rosy Cheeks */}
          <circle cx="31" cy="49" r="3.5" fill="#F472B6" opacity="0.6" />
          <circle cx="69" cy="49" r="3.5" fill="#F472B6" opacity="0.6" />
          {/* Smile */}
          <path
            d="M 44,52 Q 50,57 56,52"
            fill="none"
            stroke="#1E1B4B"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          {/* Stick Arms */}
          <path d="M 12,48 Q 5,42 8,36" fill="none" stroke="#F472B6" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M 88,48 Q 95,42 92,36" fill="none" stroke="#F472B6" strokeWidth="2.5" strokeLinecap="round" />
          {/* Stick Feet */}
          <path d="M 40,70 L 38,77" fill="none" stroke="#F472B6" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M 60,70 L 62,77" fill="none" stroke="#F472B6" strokeWidth="2.5" strokeLinecap="round" />
        </svg>

        {/* Floating Heart */}
        <HeartDoodle className="absolute -top-1 -right-2 h-3.5 w-3.5 text-pink-400 rotate-12" />
        <HeartDoodle className="absolute top-6 -left-2 h-3 w-3 text-rose-400 -rotate-12" />
      </div>
    </div>
  );
}

// ─── Hero Mountain Landscape Illustration ────────────────────────────────────
export function HeroMountainIllustration({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 320 180"
      className={className}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="mtGradient1" x1="160" y1="40" x2="160" y2="180" gradientUnits="userSpaceOnUse">
          <stop stopColor="#F472B6" stopOpacity="0.35" />
          <stop offset="1" stopColor="#DDD6FE" stopOpacity="0.1" />
        </linearGradient>
        <linearGradient id="mtGradient2" x1="240" y1="20" x2="240" y2="180" gradientUnits="userSpaceOnUse">
          <stop stopColor="#EC4899" stopOpacity="0.45" />
          <stop offset="1" stopColor="#C084FC" stopOpacity="0.15" />
        </linearGradient>
      </defs>

      {/* Sun / Glow */}
      <circle cx="240" cy="40" r="28" fill="#FCE7F0" opacity="0.8" />
      <circle cx="240" cy="40" r="18" fill="#FBCFE8" opacity="0.9" />

      {/* Background Mountain */}
      <path d="M 70 180 L 160 70 L 250 180 Z" fill="url(#mtGradient1)" />

      {/* Foreground Mountain Peak */}
      <path d="M 150 180 L 240 30 L 320 180 Z" fill="url(#mtGradient2)" />

      {/* Peak Cap (Snow/Light) */}
      <path d="M 240 30 L 222 65 L 235 60 L 245 70 L 258 30 Z" fill="#FFFFFF" opacity="0.9" />

      {/* Pink Flag on Mountain Peak */}
      <path d="M 240 30 L 240 10" stroke="#DB2777" strokeWidth="2" strokeLinecap="round" />
      <path d="M 240 10 L 256 16 L 240 22 Z" fill="#EC4899" />

      {/* Floating Hearts */}
      <path d="M 268 45 C 268 45 264 41 264 38 C 264 36 265.5 34.5 267.5 34.5 C 268.5 34.5 269.5 35 270 36 C 270.5 35 271.5 34.5 272.5 34.5 C 274.5 34.5 276 36 276 38 C 276 41 272 45 272 45 Z" fill="#F472B6" />
      <circle cx="120" cy="90" r="3" fill="#F472B6" opacity="0.6" />
      <circle cx="90" cy="110" r="2" fill="#C084FC" opacity="0.5" />
    </svg>
  );
}

