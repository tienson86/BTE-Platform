import { Link } from "react-router-dom";
import { useSession } from "../state/session";

const steps = [
  {
    title: "Chart Input",
    body: "Enter birth facts and Day Master to create a chart snapshot.",
    to: "/chart/input",
  },
  {
    title: "Analysis",
    body: "Run the Analysis Runtime across Strength through Summary.",
    to: "/analysis",
  },
  {
    title: "Interpretation",
    body: "Generate narrative sections from published AnalysisResult.",
    to: "/interpretation",
  },
  {
    title: "Luck & Report",
    body: "Inspect luck timeline and download the PDF report.",
    to: "/luck",
  },
];

export function DashboardPage() {
  const { chart, analysis, interpretation, report } = useSession();

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <section className="fade-in surface relative overflow-hidden rounded-[28px] px-6 py-10 md:px-10">
        <div className="pointer-events-none absolute -right-10 -top-16 h-48 w-48 rounded-full bg-[var(--accent-soft)] blur-2xl" />
        <p className="text-sm font-medium uppercase tracking-[0.18em] text-[var(--accent)]">
          BTE Platform
        </p>
        <h1 className="font-display mt-3 max-w-2xl text-4xl font-semibold leading-tight md:text-5xl">
          Analysis Console
        </h1>
        <p className="mt-4 max-w-xl text-base text-[var(--muted)] md:text-lg">
          Create a chart, run analysis, read interpretation, inspect luck, and
          download PDF — one responsive workspace.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            to="/chart/input"
            className="rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90"
          >
            Start Chart Input
          </Link>
          <Link
            to="/chart"
            className="rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold transition hover:border-[var(--accent)]"
          >
            Open Chart Viewer
          </Link>
        </div>
      </section>

      <section className="fade-in-delay grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          ["Chart", chart?.chart_id],
          ["Analysis", analysis?.analysis_id],
          ["Interpretation", interpretation?.interpretation_id],
          ["Report", report?.report_id],
        ].map(([label, value]) => (
          <div key={label} className="surface rounded-2xl p-4">
            <p className="text-xs uppercase tracking-wide text-[var(--muted)]">
              {label}
            </p>
            <p className="mt-2 truncate font-mono text-sm">{value ?? "Pending"}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        {steps.map((step) => (
          <Link
            key={step.title}
            to={step.to}
            className="surface block rounded-2xl p-5 transition hover:border-[var(--accent)]"
          >
            <h2 className="font-display text-2xl font-semibold">{step.title}</h2>
            <p className="mt-2 text-sm text-[var(--muted)]">{step.body}</p>
          </Link>
        ))}
      </section>
    </div>
  );
}
