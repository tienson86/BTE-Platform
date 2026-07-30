import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, ApiError } from "../api/client";
import type {
  DiffResult,
  HistoryEntry,
  KnowledgeAsset,
  PreviewResult,
  ValidationResult,
  VersionSnapshot,
  WorkflowAction,
} from "../api/types";
import { ContentEditor } from "../components/ContentEditor";
import { ASSET_TYPE_LABELS, StatusBadge } from "../lib/assetHelpers";

type Panel = "edit" | "preview" | "validation" | "diff" | "history" | "versions";

export function EditorPage() {
  const { assetId = "" } = useParams();
  const [asset, setAsset] = useState<KnowledgeAsset | null>(null);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState<Record<string, unknown>>({});
  const [panel, setPanel] = useState<Panel>("edit");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [preview, setPreview] = useState<PreviewResult | null>(null);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [versions, setVersions] = useState<VersionSnapshot[]>([]);
  const [diff, setDiff] = useState<DiffResult | null>(null);
  const [fromVersion, setFromVersion] = useState("");
  const [toVersion, setToVersion] = useState("");

  const editable =
    asset?.status === "draft" || asset?.status === "rejected";

  const load = useCallback(async () => {
    const data = await api.getAsset(assetId);
    setAsset(data);
    setTitle(data.title);
    setContent(data.content);
    setHistory(data.history);
    setVersions(data.versions);
    if (data.versions.length > 0) {
      setFromVersion(data.versions[0].version);
      setToVersion("");
    }
  }, [assetId]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        await load();
        if (!cancelled) setError(null);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Load failed");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [load]);

  const run = async (fn: () => Promise<void>) => {
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      await fn();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Action failed");
    } finally {
      setBusy(false);
    }
  };

  const save = () =>
    run(async () => {
      const updated = await api.updateAsset(assetId, {
        title,
        content,
        note: "Editor save",
      });
      setAsset(updated);
      setHistory(updated.history);
      setVersions(updated.versions);
      setMessage(`Saved as v${updated.version}`);
    });

  const openPreview = () =>
    run(async () => {
      setPanel("preview");
      setPreview(await api.preview(assetId));
    });

  const openValidation = () =>
    run(async () => {
      setPanel("validation");
      setValidation(await api.validate(assetId));
    });

  const openHistory = () =>
    run(async () => {
      setPanel("history");
      setHistory(await api.history(assetId));
    });

  const openVersions = () =>
    run(async () => {
      setPanel("versions");
      setVersions(await api.versions(assetId));
    });

  const openDiff = () =>
    run(async () => {
      setPanel("diff");
      if (!fromVersion) return;
      setDiff(
        await api.diff(
          assetId,
          fromVersion,
          toVersion || undefined,
        ),
      );
    });

  const workflow = (action: WorkflowAction) =>
    run(async () => {
      try {
        const updated = await api.workflow(
          assetId,
          action,
          action === "submit" ? "editor" : "reviewer",
          action,
        );
        setAsset(updated);
        setHistory(updated.history);
        setVersions(updated.versions);
        setMessage(`Workflow: ${action} → ${updated.status}`);
      } catch (err) {
        if (err instanceof ApiError) throw err;
        throw err;
      }
    });

  if (!asset && !error) {
    return <p className="text-sm text-[var(--muted)]">Loading asset…</p>;
  }

  if (!asset) {
    return (
      <p className="text-sm text-[var(--danger)]" role="alert">
        {error}
      </p>
    );
  }

  const panels: Array<{ id: Panel; label: string; onClick: () => void }> = [
    { id: "edit", label: "Edit", onClick: () => setPanel("edit") },
    { id: "preview", label: "Preview", onClick: openPreview },
    { id: "validation", label: "Validation", onClick: openValidation },
    { id: "diff", label: "Diff", onClick: openDiff },
    { id: "history", label: "History", onClick: openHistory },
    { id: "versions", label: "Version", onClick: openVersions },
  ];

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs text-[var(--muted)]">
            <Link to="/library" className="hover:text-[var(--accent)]">
              Library
            </Link>{" "}
            / {ASSET_TYPE_LABELS[asset.asset_type]} Editor
          </p>
          <h2 className="font-display mt-1 text-2xl">{asset.title}</h2>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
            <StatusBadge status={asset.status} />
            <span>v{asset.version}</span>
            <span>{asset.asset_id}</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {editable ? (
            <button
              type="button"
              disabled={busy}
              onClick={save}
              className="rounded-md bg-[var(--accent)] px-3 py-1.5 text-xs font-medium text-white disabled:opacity-60"
            >
              Save
            </button>
          ) : null}
          {asset.status === "draft" || asset.status === "rejected" ? (
            <button
              type="button"
              disabled={busy}
              onClick={() => workflow("submit")}
              className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
            >
              Submit review
            </button>
          ) : null}
          {asset.status === "review" ? (
            <>
              <button
                type="button"
                disabled={busy}
                onClick={() => workflow("approve")}
                className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
              >
                Approve
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => workflow("reject")}
                className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs text-[var(--danger)]"
              >
                Reject
              </button>
            </>
          ) : null}
          {asset.status === "approved" ? (
            <button
              type="button"
              disabled={busy}
              onClick={() => workflow("release")}
              className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
            >
              Release
            </button>
          ) : null}
        </div>
      </div>

      <div className="flex flex-wrap gap-2 border-b border-[var(--line)] pb-2">
        {panels.map((p) => (
          <button
            key={p.id}
            type="button"
            onClick={p.onClick}
            className={`rounded-md px-3 py-1.5 text-xs ${
              panel === p.id
                ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                : "text-[var(--muted)]"
            }`}
          >
            {p.label}
          </button>
        ))}
      </div>

      {message ? (
        <p className="text-sm text-[var(--accent)]">{message}</p>
      ) : null}
      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}

      {panel === "edit" ? (
        <div className="surface space-y-5 rounded-xl p-5">
          <label className="block space-y-1.5">
            <span className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
              Title
            </span>
            <input
              className="w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2 text-sm"
              disabled={!editable}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>
          <ContentEditor
            assetType={asset.asset_type}
            content={content}
            onChange={setContent}
            disabled={!editable}
          />
          {!editable ? (
            <p className="text-xs text-[var(--muted)]">
              Read-only while status is {asset.status}. Reject or wait for a new
              draft cycle to edit.
            </p>
          ) : null}
        </div>
      ) : null}

      {panel === "preview" && preview ? (
        <div className="surface rounded-xl p-5">
          <h3 className="font-display text-lg">Preview</h3>
          <p className="mt-4 whitespace-pre-wrap text-sm leading-relaxed">
            {preview.preview_text}
          </p>
        </div>
      ) : null}

      {panel === "validation" && validation ? (
        <div className="surface rounded-xl p-5">
          <h3 className="font-display text-lg">
            Validation{" "}
            <span className="text-sm font-sans text-[var(--muted)]">
              {validation.valid ? "passed" : "failed"}
            </span>
          </h3>
          <ul className="mt-4 space-y-2">
            {validation.issues.length === 0 ? (
              <li className="text-sm text-[var(--muted)]">No issues.</li>
            ) : (
              validation.issues.map((issue) => (
                <li
                  key={`${issue.code}-${issue.path}`}
                  className={`rounded-md border border-[var(--line)] px-3 py-2 text-sm ${
                    issue.severity === "error"
                      ? "text-[var(--danger)]"
                      : issue.severity === "warning"
                        ? "text-[var(--warn)]"
                        : "text-[var(--muted)]"
                  }`}
                >
                  <span className="font-medium uppercase">{issue.severity}</span>{" "}
                  · {issue.message}
                  {issue.path ? (
                    <span className="text-[var(--muted)]"> ({issue.path})</span>
                  ) : null}
                </li>
              ))
            )}
          </ul>
        </div>
      ) : null}

      {panel === "diff" ? (
        <div className="surface space-y-4 rounded-xl p-5">
          <h3 className="font-display text-lg">Diff</h3>
          <div className="flex flex-wrap items-end gap-3">
            <label className="space-y-1 text-xs">
              <span className="text-[var(--muted)]">From</span>
              <select
                className="block rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5"
                value={fromVersion}
                onChange={(e) => setFromVersion(e.target.value)}
              >
                {versions.map((v) => (
                  <option key={v.version} value={v.version}>
                    {v.version}
                  </option>
                ))}
              </select>
            </label>
            <label className="space-y-1 text-xs">
              <span className="text-[var(--muted)]">To</span>
              <select
                className="block rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5"
                value={toVersion}
                onChange={(e) => setToVersion(e.target.value)}
              >
                <option value="">current</option>
                {versions.map((v) => (
                  <option key={v.version} value={v.version}>
                    {v.version}
                  </option>
                ))}
              </select>
            </label>
            <button
              type="button"
              onClick={openDiff}
              className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
            >
              Compare
            </button>
          </div>
          <pre className="overflow-auto rounded-md border border-[var(--line)] p-3 font-mono text-xs leading-5">
            {(diff?.lines ?? []).map((line, i) => (
              <div
                key={`${i}-${line.kind}`}
                className={
                  line.kind === "add"
                    ? "diff-add"
                    : line.kind === "remove"
                      ? "diff-remove"
                      : ""
                }
              >
                {line.kind === "add" ? "+" : line.kind === "remove" ? "-" : " "}
                {line.text}
              </div>
            ))}
          </pre>
        </div>
      ) : null}

      {panel === "history" ? (
        <div className="surface rounded-xl p-5">
          <h3 className="font-display text-lg">History</h3>
          <ol className="mt-4 space-y-3">
            {history.map((entry) => (
              <li
                key={entry.event_id}
                className="border-b border-[var(--line)] pb-3 text-sm last:border-0"
              >
                <p className="font-medium">
                  {entry.action} · {entry.actor}
                </p>
                <p className="text-xs text-[var(--muted)]">{entry.at}</p>
                <p className="mt-1 text-[var(--muted)]">{entry.message}</p>
              </li>
            ))}
          </ol>
        </div>
      ) : null}

      {panel === "versions" ? (
        <div className="surface rounded-xl p-5">
          <h3 className="font-display text-lg">Versions</h3>
          <ul className="mt-4 space-y-3">
            {[...versions].reverse().map((v) => (
              <li
                key={v.version}
                className="rounded-md border border-[var(--line)] px-3 py-2 text-sm"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-medium">v{v.version}</span>
                  <StatusBadge status={v.status} />
                </div>
                <p className="mt-1 text-xs text-[var(--muted)]">
                  {v.created_by} · {v.created_at}
                </p>
                <p className="mt-1 text-[var(--muted)]">{v.note || v.title}</p>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
