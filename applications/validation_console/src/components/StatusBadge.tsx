import type { DatasetStatus } from "../api/types";

export function StatusBadge({ status }: { status: DatasetStatus }) {
  const tone =
    status === "released" || status === "approved"
      ? "text-[var(--pass)] bg-[rgba(31,122,82,0.14)]"
      : status === "review"
        ? "text-[var(--warn)] bg-[rgba(140,109,31,0.14)]"
        : status === "rejected"
          ? "text-[var(--danger)] bg-[rgba(161,61,50,0.14)]"
          : "text-[var(--accent)] bg-[var(--accent-soft)]";
  return (
    <span
      className={`inline-flex rounded px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide ${tone}`}
    >
      {status}
    </span>
  );
}
