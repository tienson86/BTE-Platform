import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { GoldenDataset } from "../api/types";
import { StatusBadge } from "../components/StatusBadge";

export function ApprovalQueuePage() {
  const [queue, setQueue] = useState<GoldenDataset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const refresh = async () => {
    setQueue(await api.approvalQueue());
  };

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        await refresh();
        if (!cancelled) setError(null);
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

  const act = async (id: string, action: "approve" | "reject") => {
    setBusyId(id);
    setError(null);
    setMessage(null);
    try {
      await api.workflow(id, action, "reviewer", action);
      await refresh();
      setMessage(`${action}d ${id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Workflow failed");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <h2 className="font-display text-2xl">Approval</h2>
        <p className="text-sm text-[var(--muted)]">
          draft → review → approved → released
        </p>
      </div>
      {message ? (
        <p className="text-sm text-[var(--pass)]">{message}</p>
      ) : null}
      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}
      <ul className="surface divide-y divide-[var(--line)] rounded-xl">
        {queue.map((ds) => (
          <li
            key={ds.dataset_id}
            className="flex flex-wrap items-center justify-between gap-3 px-4 py-4"
          >
            <div>
              <Link
                to={`/datasets/${ds.dataset_id}`}
                className="text-sm font-medium hover:text-[var(--accent)]"
              >
                {ds.name}
              </Link>
              <p className="text-xs text-[var(--muted)]">
                {ds.module} · {ds.case_count} cases · v{ds.version}
              </p>
              <div className="mt-1">
                <StatusBadge status={ds.status} />
              </div>
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={busyId === ds.dataset_id}
                onClick={() => act(ds.dataset_id, "approve")}
                className="rounded-md bg-[var(--accent)] px-3 py-1.5 text-xs text-white disabled:opacity-60"
              >
                Approve
              </button>
              <button
                type="button"
                disabled={busyId === ds.dataset_id}
                onClick={() => act(ds.dataset_id, "reject")}
                className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs text-[var(--danger)] disabled:opacity-60"
              >
                Reject
              </button>
            </div>
          </li>
        ))}
        {queue.length === 0 ? (
          <li className="px-4 py-10 text-center text-sm text-[var(--muted)]">
            Queue empty. Submit a draft dataset for review.
          </li>
        ) : null}
      </ul>
    </div>
  );
}
