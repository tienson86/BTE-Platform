import { Link } from "react-router-dom";
import { useSession } from "../state/session";

export function ChartViewerPage() {
  const { chart } = useSession();

  if (!chart) {
    return (
      <EmptyState
        title="No chart yet"
        body="Create a chart first, then return to inspect stems, calendar, and luck."
        actionTo="/chart/input"
        actionLabel="Open Chart Input"
      />
    );
  }

  const stems = chart.chart.stems ?? {};
  const luck = (chart.chart.luck ?? {}) as {
    current_age?: number;
    da_yun_sequence?: Array<Record<string, unknown>>;
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <header className="fade-in">
        <h1 className="font-display text-3xl font-semibold md:text-4xl">
          Chart Viewer
        </h1>
        <p className="mt-2 font-mono text-sm text-[var(--muted)]">
          {chart.chart_id}
        </p>
      </header>

      <section className="fade-in surface grid gap-4 rounded-2xl p-5 sm:grid-cols-2">
        <Field label="Day Master" value={chart.chart.day_master} />
        <Field label="Gender" value={String(chart.chart.gender ?? "—")} />
        <Field
          label="Birth"
          value={[
            chart.calendar.year,
            chart.calendar.month,
            chart.calendar.day,
          ]
            .filter((v) => v != null)
            .join("-")}
        />
        <Field
          label="Time"
          value={`${chart.calendar.hour ?? 0}:${String(chart.calendar.minute ?? 0).padStart(2, "0")}`}
        />
        <Field label="Timezone" value={chart.calendar.timezone ?? "—"} />
        <Field
          label="Name"
          value={String(chart.metadata.full_name ?? "—")}
        />
      </section>

      <section className="surface rounded-2xl p-5">
        <h2 className="font-display text-2xl font-semibold">Stems</h2>
        <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4">
          {Object.entries(stems).map(([key, value]) => (
            <div
              key={key}
              className="rounded-xl border border-[var(--line)] px-3 py-3"
            >
              <p className="text-xs uppercase text-[var(--muted)]">{key}</p>
              <p className="mt-1 text-lg font-medium">{value}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="surface rounded-2xl p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="font-display text-2xl font-semibold">Luck preview</h2>
          <Link
            to="/luck"
            className="text-sm font-medium text-[var(--accent)] hover:underline"
          >
            Open Luck Viewer
          </Link>
        </div>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Current age: {luck.current_age ?? "—"} · Da Yun entries:{" "}
          {luck.da_yun_sequence?.length ?? 0}
        </p>
      </section>

      <Link
        to="/analysis"
        className="inline-flex rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white"
      >
        Run Analysis
      </Link>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wide text-[var(--muted)]">
        {label}
      </p>
      <p className="mt-1 text-base font-medium">{value || "—"}</p>
    </div>
  );
}

function EmptyState({
  title,
  body,
  actionTo,
  actionLabel,
}: {
  title: string;
  body: string;
  actionTo: string;
  actionLabel: string;
}) {
  return (
    <div className="mx-auto max-w-lg surface rounded-2xl p-8 text-center">
      <h1 className="font-display text-3xl font-semibold">{title}</h1>
      <p className="mt-3 text-sm text-[var(--muted)]">{body}</p>
      <Link
        to={actionTo}
        className="mt-6 inline-flex rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white"
      >
        {actionLabel}
      </Link>
    </div>
  );
}
