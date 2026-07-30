import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { api, ApiError } from "../api/client";
import type { AssetType } from "../api/types";
import { ContentEditor } from "../components/ContentEditor";
import { ASSET_TYPE_LABELS, emptyContent } from "../lib/assetHelpers";

export function CreateAssetPage() {
  const navigate = useNavigate();
  const [assetType, setAssetType] = useState<AssetType>("rule");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState<Record<string, unknown>>(
    emptyContent("rule"),
  );
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const changeType = (next: AssetType) => {
    setAssetType(next);
    setContent(emptyContent(next));
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const asset = await api.createAsset({
        asset_type: assetType,
        title,
        content,
        actor: "editor",
      });
      navigate(`/editor/${asset.asset_id}`);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError(err instanceof Error ? err.message : "Create failed");
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h2 className="font-display text-2xl">New asset</h2>
        <p className="text-sm text-[var(--muted)]">
          Create a draft in the editor workspace
        </p>
      </div>

      <form onSubmit={onSubmit} className="surface space-y-6 rounded-xl p-6">
        <div className="flex flex-wrap gap-2">
          {(Object.keys(ASSET_TYPE_LABELS) as AssetType[]).map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => changeType(t)}
              className={`rounded-md px-3 py-1.5 text-xs ${
                assetType === t
                  ? "bg-[var(--accent)] text-white"
                  : "border border-[var(--line)] text-[var(--muted)]"
              }`}
            >
              {ASSET_TYPE_LABELS[t]} Editor
            </button>
          ))}
        </div>

        <label className="block space-y-1.5">
          <span className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
            Title
          </span>
          <input
            required
            className="w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2 text-sm"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </label>

        <ContentEditor
          assetType={assetType}
          content={content}
          onChange={setContent}
        />

        {error ? (
          <p className="text-sm text-[var(--danger)]" role="alert">
            {error}
          </p>
        ) : null}

        <button
          type="submit"
          disabled={saving}
          className="rounded-md bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
        >
          {saving ? "Creating…" : "Create draft"}
        </button>
      </form>
    </div>
  );
}
