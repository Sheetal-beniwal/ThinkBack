interface LoadingSpinnerProps {
  text?: string;
}

export default function LoadingSpinner({ text = "Loading…" }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center gap-3 py-16 text-slate-400">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-pink-100 border-t-pink-400" />
      <p className="text-sm font-semibold">{text}</p>
    </div>
  );
}
