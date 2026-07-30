import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { KnowledgeAsset } from "../api/types";
import { ASSET_TYPE_LABELS, StatusBadge } from "../lib/assetHelpers";

export function DashboardPage() {
  const [assets, setAssets] = useState<KnowledgeAsset[]>([]);
  const [queue, setQueue] = useState<KnowledgeAsset[]>([]);
  const [health, setHealth] = useState<string>("…");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [list, approval, h] = await Promise.all([
          api.listAssets(),
          api.approvalQueue(),
          api.health(),
        ]);
        if (cancelled) return;
        setAssets(list);
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

  const counts = {
    rule: assets.filter((a) => a.asset_type === "rule").length,
    sentence: assets.filter((a) => a.asset_type === "sentence").length,
    phrase: assets.filter((a) => a.asset_type === "phrase").length,
    terminology: assets.filter((a) => a.asset_type === "terminology").length,
  };

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <section className="surface rounded-2xl px-6 py-8">
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--muted)]">
          BTE Knowledge Console
        </p>
        <h2 className="font-display mt-2 text-3xl text-[var(--fg)]">
          Knowledge Editor
        </h2>
        <p className="mt-3 max-w-xl text-sm text-[var(--muted)]">
          Draft, validate, preview, and approve rules, sentences, phrases, and
          terminology before release. Workspace is separate from golden
          knowledge.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/create"
            className="rounded-md bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white"
          >
            New asset
          </Link>
          <Link
            to="/approval"
            className="rounded-md border border-[var(--line)] px-4 py-2 text-sm text-[var(--fg)]"
          >
            Approval queue ({queue.length})
          </Link>
        </div>
        <p className="mt-4 text-xs text-[var(--muted)]">API health: {health}</p>
        {error ? (
          <p className="mt-2 text-sm text-[var(--danger)]" role="alert">
            {error}
          </p>
        ) : null}
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {(Object.keys(counts) as Array<keyof typeof counts>).map((key) => (
          <Link
            key={key}
            to={`/library?type=${key}`}
            className="surface rounded-xl p-4 transition hover:border-[var(--accent)]"
          >
            <p className="text-xs uppercase tracking-wide text-[var(--muted)]">
              {ASSET_TYPE_LABELS[key]}
            </p>
            <p className="font-display mt-2 text-3xl">{counts[key]}</p>
          </Link>
        ))}
      </section>

      <section className="surface rounded-xl p-5">
        <h3 className="font-display text-lg">Recent updates</h3>
        <ul className="mt-4 divide-y divide-[var(--line)]">
          {assets.slice(0, 8).map((asset) => (
            <li
              key={asset.asset_id}
              className="flex items-center justify-between gap-3 py-3"
            >
              <div className="min-w-0">
                <Link
                  to={`/editor/${asset.asset_id}`}
                  className="truncate text-sm font-medium text-[var(--fg)] hover:text-[var(--accent)]"
                >
                  {asset.title}
                </Link>
                <p className="text-xs text-[var(--muted)]">
                  {ASSET_TYPE_LABELS[asset.asset_type]} · v{asset.version}
                </p>
              </div>
              <StatusBadge status={asset.status} />
            </li>
          ))}
          {assets.length === 0 && !error ? (
            <li className="py-6 text-sm text-[var(--muted)]">No assets yet.</li>
          ) : null}
        </ul>
      </section>
    </div>
  );
}
