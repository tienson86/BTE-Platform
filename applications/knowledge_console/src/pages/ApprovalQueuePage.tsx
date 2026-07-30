import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { KnowledgeAsset } from "../api/types";
import { ASSET_TYPE_LABELS, StatusBadge } from "../lib/assetHelpers";

export function ApprovalQueuePage() {
  const [queue, setQueue] = useState<KnowledgeAsset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const refresh = async () => {
    const data = await api.approvalQueue();
    setQueue(data);
  };

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        await refresh();
        if (!cancelled) setError(null);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load queue");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const act = async (assetId: string, action: "approve" | "reject") => {
    setBusyId(assetId);
    setError(null);
    setMessage(null);
    try {
      await api.workflow(assetId, action, "reviewer", action);
      await refresh();
      setMessage(`${action}d ${assetId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Workflow failed");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div>
        <h2 className="font-display text-2xl">Approval workflow</h2>
        <p className="text-sm text-[var(--muted)]">
          Review queue · draft → review → approved → released
        </p>
      </div>

      {message ? (
        <p className="text-sm text-[var(--accent)]">{message}</p>
      ) : null}
      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}

      <ul className="surface divide-y divide-[var(--line)] rounded-xl">
        {queue.map((asset) => (
          <li
            key={asset.asset_id}
            className="flex flex-wrap items-center justify-between gap-3 px-4 py-4"
          >
            <div className="min-w-0">
              <Link
                to={`/editor/${asset.asset_id}`}
                className="text-sm font-medium hover:text-[var(--accent)]"
              >
                {asset.title}
              </Link>
              <p className="text-xs text-[var(--muted)]">
                {ASSET_TYPE_LABELS[asset.asset_type]} · v{asset.version}
              </p>
              <div className="mt-1">
                <StatusBadge status={asset.status} />
              </div>
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={busyId === asset.asset_id}
                onClick={() => act(asset.asset_id, "approve")}
                className="rounded-md bg-[var(--accent)] px-3 py-1.5 text-xs text-white disabled:opacity-60"
              >
                Approve
              </button>
              <button
                type="button"
                disabled={busyId === asset.asset_id}
                onClick={() => act(asset.asset_id, "reject")}
                className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs text-[var(--danger)] disabled:opacity-60"
              >
                Reject
              </button>
            </div>
          </li>
        ))}
        {queue.length === 0 ? (
          <li className="px-4 py-10 text-center text-sm text-[var(--muted)]">
            Queue is empty. Submit a draft for review from the editor.
          </li>
        ) : null}
      </ul>
    </div>
  );
}
