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
