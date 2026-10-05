import { AlertCircle } from "lucide-react";

interface ErrorAlertProps {
  message: string;
}

export default function ErrorAlert({ message }: ErrorAlertProps) {
  return (
    <div className="flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3.5">
      <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-rose-400" />
      <p className="text-sm font-semibold text-rose-600">{message}</p>
    </div>
  );
}
