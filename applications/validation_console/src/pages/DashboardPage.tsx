import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { GoldenDataset } from "../api/types";
import { StatusBadge } from "../components/StatusBadge";

export function DashboardPage() {
  const [datasets, setDatasets] = useState<GoldenDataset[]>([]);
  const [queue, setQueue] = useState<GoldenDataset[]>([]);
  const [health, setHealth] = useState("…");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [list, approval, h] = await Promise.all([
          api.listDatasets(),
          api.approvalQueue(),
          api.health(),
        ]);
        if (cancelled) return;
        setDatasets(list);
        setQueue(approval);
        setHealth(h.status);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const caseTotal = datasets.reduce((sum, d) => sum + d.case_count, 0);

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <section className="surface rounded-2xl px-6 py-8">
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--muted)]">
          BTE Validation Console
        </p>
        <h2 className="font-display mt-2 text-3xl">Golden Dataset Manager</h2>
        <p className="mt-3 max-w-xl text-sm text-[var(--muted)]">
          Manage workspace golden datasets for create, import, compare,
          regression, approval, statistics, and coverage. Does not mutate
          published tests/golden_dataset fixtures.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/create"
            className="rounded-md bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white"
          >
            Create dataset
          </Link>
          <Link
            to="/import"
            className="rounded-md border border-[var(--line)] px-4 py-2 text-sm"
          >
            Import
          </Link>
          <Link
            to="/approval"
            className="rounded-md border border-[var(--line)] px-4 py-2 text-sm"
          >
            Approval ({queue.length})
          </Link>
        </div>
        <p className="mt-4 text-xs text-[var(--muted)]">API health: {health}</p>
        {error ? (
          <p className="mt-2 text-sm text-[var(--danger)]" role="alert">
            {error}
          </p>
        ) : null}
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        <div className="surface rounded-xl p-4">
          <p className="text-xs uppercase text-[var(--muted)]">Datasets</p>
          <p className="font-display mt-2 text-3xl">{datasets.length}</p>
        </div>
        <div className="surface rounded-xl p-4">
          <p className="text-xs uppercase text-[var(--muted)]">Cases</p>
          <p className="font-display mt-2 text-3xl">{caseTotal}</p>
        </div>
        <div className="surface rounded-xl p-4">
          <p className="text-xs uppercase text-[var(--muted)]">In review</p>
          <p className="font-display mt-2 text-3xl">{queue.length}</p>
        </div>
      </section>

      <section className="surface rounded-xl p-5">
        <h3 className="font-display text-lg">Recent datasets</h3>
        <ul className="mt-4 divide-y divide-[var(--line)]">
          {datasets.slice(0, 8).map((ds) => (
            <li
              key={ds.dataset_id}
              className="flex items-center justify-between gap-3 py-3"
            >
              <div className="min-w-0">
                <Link
                  to={`/datasets/${ds.dataset_id}`}
                  className="truncate text-sm font-medium hover:text-[var(--accent)]"
                >
                  {ds.name}
                </Link>
                <p className="text-xs text-[var(--muted)]">
                  {ds.module} · {ds.case_count} cases · v{ds.version}
                </p>
              </div>
              <StatusBadge status={ds.status} />
            </li>
          ))}
          {datasets.length === 0 && !error ? (
            <li className="py-6 text-sm text-[var(--muted)]">No datasets yet.</li>
          ) : null}
        </ul>
      </section>
    </div>
  );
}
