import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import type { AssetStatus, AssetType, KnowledgeAsset } from "../api/types";
import { ASSET_TYPE_LABELS, StatusBadge } from "../lib/assetHelpers";

const TYPES: Array<AssetType | "all"> = [
  "all",
  "rule",
  "sentence",
  "phrase",
  "terminology",
];

const STATUSES: Array<AssetStatus | "all"> = [
  "all",
  "draft",
  "review",
  "approved",
  "released",
  "rejected",
];

export function LibraryPage() {
  const [params, setParams] = useSearchParams();
  const typeFilter = (params.get("type") as AssetType | "all") || "all";
  const statusFilter = (params.get("status") as AssetStatus | "all") || "all";
  const [assets, setAssets] = useState<KnowledgeAsset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    (async () => {
      try {
        const list = await api.listAssets({
          asset_type: typeFilter === "all" ? undefined : typeFilter,
          status: statusFilter === "all" ? undefined : statusFilter,
        });
        if (!cancelled) {
          setAssets(list);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [typeFilter, statusFilter]);

  const setFilter = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (value === "all") next.delete(key);
    else next.set(key, value);
    setParams(next);
  };

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-2xl">Library</h2>
          <p className="text-sm text-[var(--muted)]">
            Browse editable knowledge assets
          </p>
        </div>
        <Link
          to="/create"
          className="rounded-md bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white"
        >
          New asset
        </Link>
      </div>

      <div className="flex flex-wrap gap-2">
        {TYPES.map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setFilter("type", t)}
            className={`rounded-md px-3 py-1.5 text-xs ${
              typeFilter === t
                ? "bg-[var(--accent)] text-white"
                : "border border-[var(--line)] text-[var(--muted)]"
            }`}
          >
            {t === "all" ? "All types" : ASSET_TYPE_LABELS[t]}
          </button>
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {STATUSES.map((s) => (
          <button
            key={s}
            type="button"
            onClick={() => setFilter("status", s)}
            className={`rounded-md px-3 py-1.5 text-xs ${
              statusFilter === s
                ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                : "border border-[var(--line)] text-[var(--muted)]"
            }`}
          >
            {s === "all" ? "All statuses" : s}
          </button>
        ))}
      </div>

      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}
      {loading ? (
        <p className="text-sm text-[var(--muted)]">Loading…</p>
      ) : (
        <ul className="surface divide-y divide-[var(--line)] rounded-xl">
          {assets.map((asset) => (
            <li key={asset.asset_id}>
              <Link
                to={`/editor/${asset.asset_id}`}
                className="flex items-center justify-between gap-4 px-4 py-3 hover:bg-[var(--accent-soft)]"
              >
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">{asset.title}</p>
                  <p className="text-xs text-[var(--muted)]">
                    {ASSET_TYPE_LABELS[asset.asset_type]} · {asset.asset_id} ·
                    v{asset.version}
                  </p>
                </div>
                <StatusBadge status={asset.status} />
              </Link>
            </li>
          ))}
          {assets.length === 0 ? (
            <li className="px-4 py-8 text-sm text-[var(--muted)]">
              No assets match these filters.
            </li>
          ) : null}
        </ul>
      )}
    </div>
  );
}
