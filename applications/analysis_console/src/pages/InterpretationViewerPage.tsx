import { useState } from "react";
import { Link } from "react-router-dom";
import { api, downloadPdfBase64 } from "../api/client";
import { useSession } from "../state/session";

export function InterpretationViewerPage() {
  const {
    analysis,
    interpretation,
    report,
    setInterpretation,
    setReport,
  } = useSession();
  const [busy, setBusy] = useState(false);
  const [pdfBusy, setPdfBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runInterpretation() {
    if (!analysis) return;
    setBusy(true);
    setError(null);
    try {
      const result = await api.runInterpretation(analysis.analysis_id);
      setInterpretation(result);
      setReport(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Interpretation failed");
    } finally {
      setBusy(false);
    }
  }

  async function downloadPdf() {
    if (!interpretation) return;
    setPdfBusy(true);
    setError(null);
    try {
      const result =
        report?.interpretation_id === interpretation.interpretation_id &&
        report.pdf_base64
          ? report
          : await api.generateReport(
              interpretation.interpretation_id,
              "BTE Analysis Report",
            );
      setReport(result);
      if (!result.pdf_base64) {
        throw new Error("PDF payload missing from report response");
      }
      downloadPdfBase64(
        result.pdf_base64,
        `${result.report_id || "bte-report"}.pdf`,
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "PDF download failed");
    } finally {
      setPdfBusy(false);
    }
  }

  if (!analysis) {
    return (
      <div className="mx-auto max-w-lg surface rounded-2xl p-8 text-center">
        <h1 className="font-display text-3xl font-semibold">
          Analysis required
        </h1>
        <p className="mt-3 text-sm text-[var(--muted)]">
          Run analysis before generating interpretation.
        </p>
        <Link
          to="/analysis"
          className="mt-6 inline-flex rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white"
        >
          Open Analysis
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <header className="fade-in flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-semibold md:text-4xl">
            Interpretation Viewer
          </h1>
          <p className="mt-2 text-sm text-[var(--muted)]">
            Analysis {analysis.analysis_id}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={runInterpretation}
            disabled={busy}
            className="rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white disabled:opacity-60"
          >
            {busy
              ? "Generating…"
              : interpretation
                ? "Re-run Interpretation"
                : "Generate Interpretation"}
          </button>
          <button
            type="button"
            onClick={downloadPdf}
            disabled={!interpretation || pdfBusy}
            className="rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold disabled:opacity-50 hover:border-[var(--accent)]"
          >
            {pdfBusy ? "Preparing PDF…" : "PDF Download"}
          </button>
        </div>
      </header>

      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}

      {!interpretation ? (
        <div className="surface rounded-2xl p-6 text-sm text-[var(--muted)]">
          No interpretation yet. Generate narrative sections from the published
          analysis result.
        </div>
      ) : (
        <>
          <section className="surface rounded-2xl p-5">
            <p className="text-xs uppercase tracking-wide text-[var(--muted)]">
              Overview
            </p>
            <p className="mt-3 text-base leading-relaxed">
              {interpretation.overview}
            </p>
            <p className="mt-4 font-mono text-xs text-[var(--muted)]">
              {interpretation.interpretation_id}
            </p>
          </section>

          <section className="space-y-4">
            {interpretation.sections.map((section) => (
              <article
                key={section.section_id}
                className="surface rounded-2xl p-5"
              >
                <h2 className="font-display text-2xl font-semibold">
                  {section.title}
                </h2>
                <p className="mt-3 text-sm leading-relaxed text-[var(--fg)]">
                  {section.body}
                </p>
              </article>
            ))}
          </section>

          <Link
            to="/luck"
            className="inline-flex text-sm font-medium text-[var(--accent)] hover:underline"
          >
            Inspect Luck Viewer →
          </Link>
        </>
      )}
    </div>
  );
}
