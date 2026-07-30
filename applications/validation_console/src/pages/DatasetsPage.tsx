import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { GoldenDataset } from "../api/types";
import { StatusBadge } from "../components/StatusBadge";

export function DatasetsPage() {
  const [datasets, setDatasets] = useState<GoldenDataset[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const list = await api.listDatasets();
        if (!cancelled) setDatasets(list);
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

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-2xl">Datasets</h2>
          <p className="text-sm text-[var(--muted)]">Workspace golden datasets</p>
        </div>
        <div className="flex gap-2">
          <Link
            to="/create"
            className="rounded-md bg-[var(--accent)] px-3 py-1.5 text-xs text-white"
          >
            Create
          </Link>
          <Link
            to="/import"
            className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
          >
            Import
          </Link>
        </div>
      </div>
      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}
      <ul className="surface divide-y divide-[var(--line)] rounded-xl">
        {datasets.map((ds) => (
          <li key={ds.dataset_id}>
            <Link
              to={`/datasets/${ds.dataset_id}`}
              className="flex items-center justify-between gap-4 px-4 py-3 hover:bg-[var(--accent-soft)]"
            >
              <div>
                <p className="text-sm font-medium">{ds.name}</p>
                <p className="text-xs text-[var(--muted)]">
                  {ds.module} · {ds.case_count} cases · v{ds.version}
                </p>
              </div>
              <StatusBadge status={ds.status} />
            </Link>
          </li>
        ))}
        {datasets.length === 0 ? (
          <li className="px-4 py-8 text-sm text-[var(--muted)]">
            No datasets in workspace.
          </li>
        ) : null}
      </ul>
    </div>
  );
}
