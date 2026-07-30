import { useRef, useState } from "react";
import { downloadTextFile } from "../lib/storage";
import { PageHeader } from "../components/PageHeader";
import { useLibrary } from "../state/library";
import type { LibraryExportBundle } from "../state/libraryTypes";
import { useSession } from "../state/session";

export function DataPage() {
  const fileRef = useRef<HTMLInputElement>(null);
  const { exportBundle, importBundle, charts, timeline } = useLibrary();
  const session = useSession();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<"merge" | "replace">("merge");

  function onExport() {
    setError(null);
    const bundle = exportBundle();
    downloadTextFile(
      JSON.stringify(bundle, null, 2),
      `bte-console-export-${new Date().toISOString().slice(0, 10)}.json`,
    );
    setMessage(`Exported ${bundle.charts.length} charts and ${bundle.timeline.length} timeline events.`);
  }

  function onExportSession() {
    setError(null);
    const payload = {
      version: "1.0.0",
      exported_at: new Date().toISOString(),
      session: {
        chart: session.chart,
        analysis: session.analysis,
        interpretation: session.interpretation,
        report: session.report
          ? { ...session.report, pdf_base64: session.report.pdf_base64 ? "[omitted]" : null }
          : null,
      },
    };
    downloadTextFile(
      JSON.stringify(payload, null, 2),
      `bte-session-export-${new Date().toISOString().slice(0, 10)}.json`,
    );
    setMessage("Active session exported (PDF bytes omitted).");
  }

  async function onImportFile(file: File) {
    setError(null);
    setMessage(null);
    try {
      const text = await file.text();
      const bundle = JSON.parse(text) as LibraryExportBundle;
      importBundle(bundle, mode);
      setMessage(`Imported ${bundle.charts?.length ?? 0} charts (${mode}).`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Import failed");
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <PageHeader
        eyebrow="Data"
        title="Export & Import"
        description="Backup your project library or restore charts, timeline, settings, and profile from a JSON bundle."
      />

      <section className="surface rounded-2xl p-6" aria-labelledby="export-heading">
        <h2 id="export-heading" className="font-display text-2xl font-semibold">
          Export
        </h2>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Library currently holds {charts.length} charts and {timeline.length}{" "}
          timeline events.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onExport}
            className="rounded-xl bg-[var(--accent)] px-4 py-2.5 text-sm font-semibold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            Export library JSON
          </button>
          <button
            type="button"
            onClick={onExportSession}
            className="rounded-xl border border-[var(--line)] px-4 py-2.5 text-sm font-semibold transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            Export active session
          </button>
        </div>
      </section>

      <section className="surface rounded-2xl p-6" aria-labelledby="import-heading">
        <h2 id="import-heading" className="font-display text-2xl font-semibold">
          Import
        </h2>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Choose merge to append missing charts, or replace to overwrite the
          local library.
        </p>
        <fieldset className="mt-4">
          <legend className="sr-only">Import mode</legend>
          <div className="flex flex-wrap gap-4 text-sm">
            <label className="inline-flex items-center gap-2">
              <input
                type="radio"
                name="import-mode"
                checked={mode === "merge"}
                onChange={() => setMode("merge")}
              />
              Merge
            </label>
            <label className="inline-flex items-center gap-2">
              <input
                type="radio"
                name="import-mode"
                checked={mode === "replace"}
                onChange={() => setMode("replace")}
              />
              Replace
            </label>
          </div>
        </fieldset>
        <input
          ref={fileRef}
          type="file"
          accept="application/json,.json"
          className="sr-only"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) void onImportFile(file);
            event.target.value = "";
          }}
        />
        <button
          type="button"
          className="mt-5 rounded-xl border border-[var(--line)] px-4 py-2.5 text-sm font-semibold transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          onClick={() => fileRef.current?.click()}
        >
          Choose JSON file
        </button>
      </section>

      {message ? (
        <p className="text-sm text-[var(--accent)]" role="status">
          {message}
        </p>
      ) : null}
      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
