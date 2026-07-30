import type { LibraryChart } from "../state/libraryTypes";

type ChartCardProps = {
  chart: LibraryChart;
  onOpen: (id: string) => void;
  onToggleFavorite: (id: string) => void;
  onTogglePinned: (id: string) => void;
  dense?: boolean;
};

function formatDate(value: string): string {
  try {
    return new Intl.DateTimeFormat("vi-VN", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

export function ChartCard({
  chart,
  onOpen,
  onToggleFavorite,
  onTogglePinned,
  dense = false,
}: ChartCardProps) {
  return (
    <article
      className={`surface rounded-2xl ${dense ? "p-4" : "p-5"} transition hover:border-[var(--accent)]`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="truncate font-display text-xl font-semibold">
            {chart.name}
          </h3>
          <p className="mt-1 text-sm text-[var(--muted)]">
            {chart.customer_name} · {chart.day_master}
            {chart.year ? ` · ${chart.year}` : ""}
          </p>
        </div>
        <div className="flex shrink-0 gap-1">
          <button
            type="button"
            className="rounded-lg border border-[var(--line)] px-2.5 py-1.5 text-xs font-medium transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
            aria-pressed={chart.favorite}
            aria-label={chart.favorite ? "Remove favorite" : "Add favorite"}
            onClick={() => onToggleFavorite(chart.id)}
          >
            {chart.favorite ? "★" : "☆"}
          </button>
          <button
            type="button"
            className="rounded-lg border border-[var(--line)] px-2.5 py-1.5 text-xs font-medium transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
            aria-pressed={chart.pinned}
            aria-label={chart.pinned ? "Unpin chart" : "Pin chart"}
            onClick={() => onTogglePinned(chart.id)}
          >
            {chart.pinned ? "Pinned" : "Pin"}
          </button>
        </div>
      </div>

      <dl className="mt-4 grid grid-cols-2 gap-2 text-xs text-[var(--muted)]">
        <div>
          <dt className="uppercase tracking-wide">Opened</dt>
          <dd className="mt-0.5 text-[var(--fg)]">
            {formatDate(chart.last_opened_at)}
          </dd>
        </div>
        <div>
          <dt className="uppercase tracking-wide">Chart ID</dt>
          <dd className="mt-0.5 truncate font-mono text-[var(--fg)]">
            {chart.chart_id ?? "local"}
          </dd>
        </div>
      </dl>

      <div className="mt-4">
        <button
          type="button"
          onClick={() => onOpen(chart.id)}
          className="rounded-xl bg-[var(--accent)] px-3 py-2 text-xs font-semibold text-white transition hover:opacity-90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
        >
          Open in viewer
        </button>
      </div>
    </article>
  );
}
