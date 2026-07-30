import { Link } from "react-router-dom";
import { EmptyState } from "../components/EmptyState";
import { PageHeader } from "../components/PageHeader";
import { useLibrary } from "../state/library";

export function CustomerHistoryPage() {
  const { customers, charts } = useLibrary();

  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader
        eyebrow="Customers"
        title="Customer History"
        description="Customers derived from chart library entries. Open related charts to continue analysis."
      />

      {customers.length === 0 ? (
        <EmptyState
          title="No customer history"
          body="Customer records appear after you create charts with a full name."
          action={
            <Link
              to="/chart/input"
              className="rounded-xl bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-white"
            >
              Create chart
            </Link>
          }
        />
      ) : (
        <ul className="space-y-3">
          {customers.map((customer) => {
            const related = charts.filter((chart) =>
              customer.library_ids.includes(chart.id),
            );
            return (
              <li key={customer.id} className="surface rounded-2xl p-5">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <h2 className="font-display text-2xl font-semibold">
                      {customer.name}
                    </h2>
                    <p className="mt-1 text-sm text-[var(--muted)]">
                      {customer.chart_count} chart
                      {customer.chart_count === 1 ? "" : "s"} · Last seen{" "}
                      {new Date(customer.last_seen).toLocaleString("vi-VN")}
                    </p>
                  </div>
                  <Link
                    to={`/charts?tab=search&q=${encodeURIComponent(customer.name)}`}
                    className="rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
                  >
                    Search charts
                  </Link>
                </div>
                <ul className="mt-4 space-y-2">
                  {related.slice(0, 5).map((chart) => (
                    <li
                      key={chart.id}
                      className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm"
                    >
                      <span>
                        {chart.day_master}
                        {chart.year ? ` · ${chart.year}` : ""}
                      </span>
                      <span className="font-mono text-xs text-[var(--muted)]">
                        {chart.chart_id ?? chart.id}
                      </span>
                    </li>
                  ))}
                </ul>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
