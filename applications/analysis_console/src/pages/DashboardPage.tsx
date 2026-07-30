import { Link } from "react-router-dom";
import { ChartCard } from "../components/ChartCard";
import { EmptyState } from "../components/EmptyState";
import { PageHeader } from "../components/PageHeader";
import { useOpenLibraryChart } from "../hooks/useOpenLibraryChart";
import { useLibrary } from "../state/library";
import { useSession } from "../state/session";

export function DashboardPage() {
  const {
    charts,
    recentCharts,
    favoriteCharts,
    pinnedCharts,
    timeline,
    customers,
    profile,
    toggleFavorite,
    togglePinned,
  } = useLibrary();
  const { chart, analysis, interpretation, report } = useSession();
  const openLibraryChart = useOpenLibraryChart();

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <section className="fade-in surface relative overflow-hidden rounded-[28px] px-6 py-10 md:px-10">
        <div className="pointer-events-none absolute -right-10 -top-16 h-48 w-48 rounded-full bg-[var(--accent-soft)] blur-2xl" />
        <p className="text-sm font-medium uppercase tracking-[0.18em] text-[var(--accent)]">
          Project Dashboard
        </p>
        <h1 className="font-display mt-3 max-w-2xl text-4xl font-semibold leading-tight md:text-5xl">
          Welcome, {profile.display_name}
        </h1>
        <p className="mt-4 max-w-xl text-base text-[var(--muted)] md:text-lg">
          Manage charts, favorites, pinned work, customer history, and analysis
          timeline in one responsive console.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            to="/chart/input"
            className="rounded-xl bg-[var(--accent)] px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            New Chart
          </Link>
          <Link
            to="/charts?tab=search"
            className="rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            Search Charts
          </Link>
          <Link
            to="/data"
            className="rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            Export / Import
          </Link>
        </div>
      </section>

      <section
        aria-label="Session status"
        className="fade-in-delay grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
      >
        {[
          ["Library", `${charts.length} charts`],
          ["Customers", `${customers.length}`],
          ["Active chart", chart?.chart_id ?? "None"],
          ["Pipeline", [analysis, interpretation, report].filter(Boolean).length + "/3"],
        ].map(([label, value]) => (
          <div key={label} className="surface rounded-2xl p-4">
            <p className="text-xs uppercase tracking-wide text-[var(--muted)]">
              {label}
            </p>
            <p className="mt-2 truncate font-mono text-sm">{value}</p>
          </div>
        ))}
      </section>

      <section aria-labelledby="pinned-heading" className="space-y-4">
        <div className="flex items-end justify-between gap-3">
          <h2 id="pinned-heading" className="font-display text-2xl font-semibold">
            Pinned Charts
          </h2>
          <Link to="/charts?tab=pinned" className="text-sm text-[var(--accent)]">
            View all
          </Link>
        </div>
        {pinnedCharts.length === 0 ? (
          <EmptyState
            title="No pinned charts"
            body="Pin important charts so they stay on your project dashboard."
            action={
              <Link to="/charts" className="text-sm font-semibold text-[var(--accent)]">
                Browse charts
              </Link>
            }
          />
        ) : (
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {pinnedCharts.slice(0, 3).map((item) => (
              <ChartCard
                key={item.id}
                chart={item}
                dense
                onOpen={openLibraryChart}
                onToggleFavorite={toggleFavorite}
                onTogglePinned={togglePinned}
              />
            ))}
          </div>
        )}
      </section>

      <div className="grid gap-8 lg:grid-cols-2">
        <section aria-labelledby="recent-heading" className="space-y-4">
          <div className="flex items-end justify-between gap-3">
            <h2 id="recent-heading" className="font-display text-2xl font-semibold">
              Recent Charts
            </h2>
            <Link to="/charts?tab=recent" className="text-sm text-[var(--accent)]">
              View all
            </Link>
          </div>
          {recentCharts.length === 0 ? (
            <EmptyState
              title="No recent charts"
              body="Create a chart to populate your project library."
              action={
                <Link
                  to="/chart/input"
                  className="rounded-xl bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-white"
                >
                  Chart Input
                </Link>
              }
            />
          ) : (
            <div className="grid gap-4">
              {recentCharts.slice(0, 4).map((item) => (
                <ChartCard
                  key={item.id}
                  chart={item}
                  dense
                  onOpen={openLibraryChart}
                  onToggleFavorite={toggleFavorite}
                  onTogglePinned={togglePinned}
                />
              ))}
            </div>
          )}
        </section>

        <section aria-labelledby="favorites-heading" className="space-y-4">
          <div className="flex items-end justify-between gap-3">
            <h2
              id="favorites-heading"
              className="font-display text-2xl font-semibold"
            >
              Favorite Charts
            </h2>
            <Link
              to="/charts?tab=favorites"
              className="text-sm text-[var(--accent)]"
            >
              View all
            </Link>
          </div>
          {favoriteCharts.length === 0 ? (
            <EmptyState
              title="No favorites yet"
              body="Mark charts with a star to keep them in favorites."
            />
          ) : (
            <div className="grid gap-4">
              {favoriteCharts.slice(0, 4).map((item) => (
                <ChartCard
                  key={item.id}
                  chart={item}
                  dense
                  onOpen={openLibraryChart}
                  onToggleFavorite={toggleFavorite}
                  onTogglePinned={togglePinned}
                />
              ))}
            </div>
          )}
        </section>
      </div>

      <section aria-labelledby="timeline-heading" className="space-y-4">
        <div className="flex items-end justify-between gap-3">
          <h2 id="timeline-heading" className="font-display text-2xl font-semibold">
            Analysis Timeline
          </h2>
          <Link to="/timeline" className="text-sm text-[var(--accent)]">
            Full timeline
          </Link>
        </div>
        <ol className="surface space-y-0 divide-y divide-[var(--line)] rounded-2xl">
          {timeline.slice(0, 6).map((event) => (
            <li key={event.id} className="px-5 py-4">
              <p className="text-sm font-medium">{event.title}</p>
              <p className="mt-1 text-sm text-[var(--muted)]">{event.detail}</p>
              <time
                className="mt-2 block text-xs text-[var(--muted)]"
                dateTime={event.at}
              >
                {new Date(event.at).toLocaleString("vi-VN")}
              </time>
            </li>
          ))}
          {timeline.length === 0 ? (
            <li className="px-5 py-8 text-sm text-[var(--muted)]">
              Timeline events appear as you create charts, run analysis, and
              export data.
            </li>
          ) : null}
        </ol>
      </section>
    </div>
  );
}
