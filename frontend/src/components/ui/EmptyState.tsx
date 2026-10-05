import { SearchX } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  description?: string;
}

export default function EmptyState({
  title = "No results found",
  description = "Try adjusting your query or removing filters.",
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center gap-4 py-16 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-pink-100 bg-pink-50">
        <SearchX className="h-6 w-6 text-pink-300" />
      </div>
      <div className="flex flex-col gap-1">
        <p className="text-sm font-bold text-slate-500">{title}</p>
        <p className="text-xs font-medium text-slate-400">{description}</p>
      </div>
    </div>
  );
}
