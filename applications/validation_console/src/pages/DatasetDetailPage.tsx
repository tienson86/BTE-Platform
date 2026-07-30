import { useCallback, useEffect, useState, type FormEvent } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import type {
  CompareResponse,
  CoverageReport,
  GoldenDataset,
  RegressionReport,
  Statistics,
  WorkflowAction,
} from "../api/types";
import { StatusBadge } from "../components/StatusBadge";

type Panel =
  | "cases"
  | "compare"
  | "regression"
  | "statistics"
  | "coverage"
  | "history";

export function DatasetDetailPage() {
  const { datasetId = "" } = useParams();
  const [dataset, setDataset] = useState<GoldenDataset | null>(null);
  const [panel, setPanel] = useState<Panel>("cases");
  const [compare, setCompare] = useState<CompareResponse | null>(null);
  const [report, setReport] = useState<RegressionReport | null>(null);
  const [stats, setStats] = useState<Statistics | null>(null);
  const [coverage, setCoverage] = useState<CoverageReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const [caseId, setCaseId] = useState("");
  const [caseDesc, setCaseDesc] = useState("");
  const [caseExpected, setCaseExpected] = useState('{"result":"ok"}');
  const [caseActual, setCaseActual] = useState('{"result":"ok"}');
  const [caseTags, setCaseTags] = useState("canonical");
  const [caseGoal, setCaseGoal] = useState("canonical");

  const load = useCallback(async () => {
    const data = await api.getDataset(datasetId);
    setDataset(data);
  }, [datasetId]);

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

  const editable =
    dataset?.status === "draft" || dataset?.status === "rejected";

  const addCase = (e: FormEvent) => {
    e.preventDefault();
    void run(async () => {
      const expected = JSON.parse(caseExpected) as Record<string, unknown>;
      const actual = JSON.parse(caseActual) as Record<string, unknown>;
      const updated = await api.addCase(datasetId, {
        case_id: caseId,
        description: caseDesc,
        input_fixture: { source: "console" },
        expected_output: expected,
        actual_output: actual,
        tags: caseTags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
        coverage_goal: caseGoal,
      });
      setDataset(updated);
      setMessage(`Added case ${caseId}`);
      setCaseId("");
      setCaseDesc("");
    });
  };

  const openCompare = () =>
    run(async () => {
      setPanel("compare");
      setCompare(await api.compare(datasetId));
    });

  const openRegression = () =>
    run(async () => {
      setPanel("regression");
      const result = await api.regression(datasetId);
      setReport(result);
      await load();
      setMessage(
        `Regression: ${result.passed}/${result.total} passed, ${result.failed} failed`,
      );
    });

  const openStats = () =>
    run(async () => {
      setPanel("statistics");
      setStats(await api.statistics(datasetId));
    });

  const openCoverage = () =>
    run(async () => {
      setPanel("coverage");
      setCoverage(await api.coverage(datasetId));
    });

  const workflow = (action: WorkflowAction) =>
    run(async () => {
      const updated = await api.workflow(
        datasetId,
        action,
        action === "submit" ? "editor" : "reviewer",
        action,
      );
      setDataset(updated);
      setMessage(`Workflow: ${action} → ${updated.status}`);
    });

  if (!dataset && !error) {
    return <p className="text-sm text-[var(--muted)]">Loading…</p>;
  }
  if (!dataset) {
    return (
      <p className="text-sm text-[var(--danger)]" role="alert">
        {error}
      </p>
    );
  }

  const panels: Array<{ id: Panel; label: string; onClick: () => void }> = [
    { id: "cases", label: "Cases", onClick: () => setPanel("cases") },
    { id: "compare", label: "Compare", onClick: openCompare },
    { id: "regression", label: "Regression", onClick: openRegression },
    { id: "statistics", label: "Statistics", onClick: openStats },
    { id: "coverage", label: "Coverage", onClick: openCoverage },
    {
      id: "history",
      label: "History",
      onClick: () => setPanel("history"),
    },
  ];

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs text-[var(--muted)]">
            <Link to="/datasets" className="hover:text-[var(--accent)]">
              Datasets
            </Link>{" "}
            / {dataset.module}
          </p>
          <h2 className="font-display mt-1 text-2xl">{dataset.name}</h2>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
            <StatusBadge status={dataset.status} />
            <span>v{dataset.version}</span>
            <span>{dataset.case_count} cases</span>
            <span>{dataset.dataset_id}</span>
          </div>
          {dataset.description ? (
            <p className="mt-2 text-sm text-[var(--muted)]">
              {dataset.description}
            </p>
          ) : null}
        </div>
        <div className="flex flex-wrap gap-2">
          {(dataset.status === "draft" || dataset.status === "rejected") && (
            <button
              type="button"
              disabled={busy}
              onClick={() => workflow("submit")}
              className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
            >
              Submit review
            </button>
          )}
          {dataset.status === "review" && (
            <>
              <button
                type="button"
                disabled={busy}
                onClick={() => workflow("approve")}
                className="rounded-md bg-[var(--accent)] px-3 py-1.5 text-xs text-white"
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
          )}
          {dataset.status === "approved" && (
            <button
              type="button"
              disabled={busy}
              onClick={() => workflow("release")}
              className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs"
            >
              Release
            </button>
          )}
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
        <p className="text-sm text-[var(--pass)]">{message}</p>
      ) : null}
      {error ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}

      {panel === "cases" ? (
        <div className="space-y-6">
          <ul className="surface divide-y divide-[var(--line)] rounded-xl">
            {dataset.cases.map((c) => (
              <li key={c.case_id} className="px-4 py-3 text-sm">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="font-medium">{c.case_id}</p>
                  <p className="text-xs text-[var(--muted)]">
                    {c.coverage_goal || "unspecified"} ·{" "}
                    {c.actual_output ? "has actual" : "no actual"}
                  </p>
                </div>
                <p className="mt-1 text-[var(--muted)]">{c.description}</p>
                <p className="mt-1 text-xs text-[var(--muted)]">
                  tags: {c.tags.join(", ") || "—"}
                </p>
              </li>
            ))}
            {dataset.cases.length === 0 ? (
              <li className="px-4 py-8 text-sm text-[var(--muted)]">
                No cases yet.
              </li>
            ) : null}
          </ul>

          {editable ? (
            <form
              onSubmit={addCase}
              className="surface grid gap-3 rounded-xl p-5 md:grid-cols-2"
            >
              <h3 className="font-display text-lg md:col-span-2">Add case</h3>
              <label className="space-y-1 text-xs">
                <span className="text-[var(--muted)]">Case ID</span>
                <input
                  required
                  className="w-full rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5 text-sm"
                  value={caseId}
                  onChange={(e) => setCaseId(e.target.value)}
                />
              </label>
              <label className="space-y-1 text-xs">
                <span className="text-[var(--muted)]">Coverage goal</span>
                <input
                  className="w-full rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5 text-sm"
                  value={caseGoal}
                  onChange={(e) => setCaseGoal(e.target.value)}
                />
              </label>
              <label className="space-y-1 text-xs md:col-span-2">
                <span className="text-[var(--muted)]">Description</span>
                <input
                  required
                  className="w-full rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5 text-sm"
                  value={caseDesc}
                  onChange={(e) => setCaseDesc(e.target.value)}
                />
              </label>
              <label className="space-y-1 text-xs">
                <span className="text-[var(--muted)]">Expected JSON</span>
                <textarea
                  className="min-h-24 w-full rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5 font-mono text-xs"
                  value={caseExpected}
                  onChange={(e) => setCaseExpected(e.target.value)}
                />
              </label>
              <label className="space-y-1 text-xs">
                <span className="text-[var(--muted)]">Actual JSON</span>
                <textarea
                  className="min-h-24 w-full rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5 font-mono text-xs"
                  value={caseActual}
                  onChange={(e) => setCaseActual(e.target.value)}
                />
              </label>
              <label className="space-y-1 text-xs md:col-span-2">
                <span className="text-[var(--muted)]">Tags (comma-separated)</span>
                <input
                  className="w-full rounded-md border border-[var(--line)] bg-transparent px-2 py-1.5 text-sm"
                  value={caseTags}
                  onChange={(e) => setCaseTags(e.target.value)}
                />
              </label>
              <button
                type="submit"
                disabled={busy}
                className="rounded-md bg-[var(--accent)] px-3 py-2 text-xs text-white disabled:opacity-60 md:col-span-2 md:w-fit"
              >
                Add case
              </button>
            </form>
          ) : null}
        </div>
      ) : null}

      {panel === "compare" && compare ? (
        <div className="surface space-y-4 rounded-xl p-5">
          <h3 className="font-display text-lg">Compare results</h3>
          <p className="text-sm text-[var(--muted)]">
            pass {compare.summary.passed} · fail {compare.summary.failed} · skip{" "}
            {compare.summary.skipped} · error {compare.summary.errors}
          </p>
          <ul className="space-y-3">
            {compare.results.map((r) => (
              <li
                key={r.case_id}
                className="rounded-md border border-[var(--line)] px-3 py-2 text-sm"
              >
                <div className="flex justify-between gap-2">
                  <span className="font-medium">{r.case_id}</span>
                  <span
                    className={
                      r.status === "pass"
                        ? "text-[var(--pass)]"
                        : r.status === "fail"
                          ? "text-[var(--danger)]"
                          : "text-[var(--muted)]"
                    }
                  >
                    {r.status}
                  </span>
                </div>
                <p className="text-xs text-[var(--muted)]">{r.message}</p>
                {r.differences.length > 0 ? (
                  <ul className="mt-2 space-y-1 font-mono text-xs">
                    {r.differences.slice(0, 8).map((d) => (
                      <li key={d.field}>
                        {d.field}: {JSON.stringify(d.expected)} →{" "}
                        {JSON.stringify(d.actual)}
                      </li>
                    ))}
                  </ul>
                ) : null}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {panel === "regression" && report ? (
        <div className="surface space-y-4 rounded-xl p-5">
          <h3 className="font-display text-lg">Regression report</h3>
          <p className="text-sm text-[var(--muted)]">
            {report.report_id} · {report.ran_at} · {report.actor}
          </p>
          <div className="grid gap-3 sm:grid-cols-4">
            {[
              ["Passed", report.passed],
              ["Failed", report.failed],
              ["Skipped", report.skipped],
              ["Errors", report.errors],
            ].map(([label, value]) => (
              <div
                key={String(label)}
                className="rounded-md border border-[var(--line)] p-3"
              >
                <p className="text-xs text-[var(--muted)]">{label}</p>
                <p className="font-display text-2xl">{value}</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {panel === "statistics" && stats ? (
        <div className="surface space-y-4 rounded-xl p-5">
          <h3 className="font-display text-lg">Statistics</h3>
          <dl className="grid gap-3 sm:grid-cols-2 text-sm">
            <div>
              <dt className="text-[var(--muted)]">Cases</dt>
              <dd className="font-medium">{stats.case_count}</dd>
            </div>
            <div>
              <dt className="text-[var(--muted)]">With actual</dt>
              <dd className="font-medium">{stats.with_actual}</dd>
            </div>
            <div>
              <dt className="text-[var(--muted)]">Without actual</dt>
              <dd className="font-medium">{stats.without_actual}</dd>
            </div>
            <div>
              <dt className="text-[var(--muted)]">Unique tags</dt>
              <dd className="font-medium">{stats.tag_count}</dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-[var(--muted)]">Tags</dt>
              <dd className="font-medium">
                {stats.unique_tags.join(", ") || "—"}
              </dd>
            </div>
            {stats.latest_regression ? (
              <div className="sm:col-span-2">
                <dt className="text-[var(--muted)]">Latest pass rate</dt>
                <dd className="font-medium">
                  {(stats.latest_regression.pass_rate * 100).toFixed(1)}%
                </dd>
              </div>
            ) : null}
          </dl>
        </div>
      ) : null}

      {panel === "coverage" && coverage ? (
        <div className="surface space-y-4 rounded-xl p-5">
          <h3 className="font-display text-lg">Coverage</h3>
          <p className="text-sm text-[var(--muted)]">
            Ratio {(coverage.coverage_ratio * 100).toFixed(0)}% ·{" "}
            {coverage.complete ? "complete" : "incomplete"}
          </p>
          <div>
            <p className="text-xs uppercase text-[var(--muted)]">
              Missing goals
            </p>
            <p className="mt-1 text-sm">
              {coverage.missing_goals.join(", ") || "None"}
            </p>
          </div>
          <ul className="space-y-2 text-sm">
            {coverage.goal_coverage.map((g) => (
              <li
                key={g.goal}
                className="flex justify-between border-b border-[var(--line)] py-2"
              >
                <span>{g.goal}</span>
                <span className="text-[var(--muted)]">{g.count}</span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {panel === "history" ? (
        <div className="surface rounded-xl p-5">
          <h3 className="font-display text-lg">History</h3>
          <ol className="mt-4 space-y-3">
            {dataset.history.map((h) => (
              <li
                key={h.event_id}
                className="border-b border-[var(--line)] pb-3 text-sm last:border-0"
              >
                <p className="font-medium">
                  {h.action} · {h.actor}
                </p>
                <p className="text-xs text-[var(--muted)]">{h.at}</p>
                <p className="mt-1 text-[var(--muted)]">{h.message}</p>
              </li>
            ))}
          </ol>
        </div>
      ) : null}
    </div>
  );
}
