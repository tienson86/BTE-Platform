import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useLibrary } from "../state/library";
import { useSession } from "../state/session";

export function AnalysisViewerPage() {
  const {
    chart,
    analysis,
    setAnalysis,
    setInterpretation,
    setReport,
  } = useSession();
  const { recordEvent } = useLibrary();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    if (!chart) return;
    setBusy(true);
    setError(null);
    try {
      const result = await api.runAnalysis(chart.chart_id);
      setAnalysis(result);
      setInterpretation(null);
      setReport(null);
      recordEvent(
        "analysis_run",
        "Analysis completed",
        result.analysis_id,
        { chart_id: chart.chart_id },
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setBusy(false);
    }
  }

  if (!chart) {
    return (
      <Empty
        title="Chart required"
        body="Create a chart before running analysis."
        to="/chart/input"
      />
    );
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <header className="fade-in flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-semibold md:text-4xl">
            Analysis Viewer
          </h1>
          <p className="mt-2 text-sm text-[var(--muted)]">
            Chart {chart.chart_id}
          </p>
        </div>
        <button
          type="button"
          onClick={run}
          disabled={busy}
          className="rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white disabled:opacity-60"
        >
          {busy ? "Running…" : analysis ? "Re-run Analysis" : "Run Analysis"}
        </button>
      </header>

      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}

      {!analysis ? (
        <div className="surface rounded-2xl p-6 text-sm text-[var(--muted)]">
          No analysis yet. Run Analysis to populate Strength → Summary stages.
        </div>
      ) : (
        <>
          <section className="surface grid gap-4 rounded-2xl p-5 sm:grid-cols-3">
            <Metric label="Analysis ID" value={analysis.analysis_id} mono />
            <Metric
              label="Confidence"
              value={
                analysis.confidence?.score != null
                  ? `${analysis.confidence.score} (${analysis.confidence.level ?? "—"})`
                  : "—"
              }
            />
            <Metric
              label="Stages"
              value={String(analysis.stage_ids?.length ?? 0)}
            />
          </section>

          <section className="surface rounded-2xl p-5">
            <h2 className="font-display text-2xl font-semibold">Stage IDs</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {analysis.stage_ids.map((stageId) => (
                <span
                  key={stageId}
                  className="rounded-full bg-[var(--accent-soft)] px-3 py-1 text-xs font-medium text-[var(--accent)]"
                >
                  {stageId}
                </span>
              ))}
            </div>
          </section>

          <section className="surface rounded-2xl p-5">
            <h2 className="font-display text-2xl font-semibold">Summary</h2>
            <pre className="mt-4 overflow-x-auto rounded-xl border border-[var(--line)] p-4 text-xs leading-relaxed">
              {JSON.stringify(analysis.summary, null, 2)}
            </pre>
          </section>

          <Link
            to="/interpretation"
            className="inline-flex rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold hover:border-[var(--accent)]"
          >
            Continue to Interpretation
          </Link>
        </>
      )}
    </div>
  );
}

function Metric({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wide text-[var(--muted)]">
        {label}
      </p>
      <p className={`mt-1 text-sm ${mono ? "font-mono" : "font-medium"}`}>
        {value}
      </p>
    </div>
  );
}

function Empty({
  title,
  body,
  to,
}: {
  title: string;
  body: string;
  to: string;
}) {
  return (
    <div className="mx-auto max-w-lg surface rounded-2xl p-8 text-center">
      <h1 className="font-display text-3xl font-semibold">{title}</h1>
      <p className="mt-3 text-sm text-[var(--muted)]">{body}</p>
      <Link
        to={to}
        className="mt-6 inline-flex rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white"
      >
        Go
      </Link>
    </div>
  );
}
