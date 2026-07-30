import { useDeferredValue, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { ChartCard } from "../components/ChartCard";
import { EmptyState } from "../components/EmptyState";
import { PageHeader } from "../components/PageHeader";
import { SearchField } from "../components/SearchField";
import { useOpenLibraryChart } from "../hooks/useOpenLibraryChart";
import { useLibrary } from "../state/library";

const TABS = [
  { id: "all", label: "All" },
  { id: "recent", label: "Recent" },
  { id: "favorites", label: "Favorites" },
  { id: "pinned", label: "Pinned" },
  { id: "search", label: "Search" },
] as const;

type TabId = (typeof TABS)[number]["id"];

function isTabId(value: string | null): value is TabId {
  return TABS.some((tab) => tab.id === value);
}

export function ChartsPage() {
  const [params, setParams] = useSearchParams();
  const tabParam = params.get("tab");
  const tab: TabId = isTabId(tabParam) ? tabParam : "all";
  const [query, setQuery] = useState(params.get("q") ?? "");
  const deferredQuery = useDeferredValue(query);

  const {
    charts,
    recentCharts,
    favoriteCharts,
    pinnedCharts,
    searchCharts,
    toggleFavorite,
    togglePinned,
  } = useLibrary();
  const openLibraryChart = useOpenLibraryChart();

  const visible = useMemo(() => {
    switch (tab) {
      case "recent":
        return recentCharts;
      case "favorites":
        return favoriteCharts;
      case "pinned":
        return pinnedCharts;
      case "search":
        return searchCharts(deferredQuery);
      default:
        return charts;
    }
  }, [
    tab,
    charts,
    recentCharts,
    favoriteCharts,
    pinnedCharts,
    searchCharts,
    deferredQuery,
  ]);

  function setTab(next: TabId) {
    const nextParams = new URLSearchParams(params);
    nextParams.set("tab", next);
    if (next !== "search") nextParams.delete("q");
    setParams(nextParams);
  }

  return (
    <div className="mx-auto max-w-6xl">
      <PageHeader
        eyebrow="Library"
        title="Charts"
        description="Browse recent, favorite, and pinned charts. Search by name, Day Master, or chart id."
        actions={
          <Link
            to="/chart/input"
            className="rounded-xl bg-[var(--accent)] px-4 py-2.5 text-sm font-semibold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            New Chart
          </Link>
        }
      />

      <div
        role="tablist"
        aria-label="Chart filters"
        className="mb-5 flex flex-wrap gap-2"
      >
        {TABS.map((item) => (
          <button
            key={item.id}
            type="button"
            role="tab"
            aria-selected={tab === item.id}
            className={`rounded-xl px-3 py-2 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)] ${
              tab === item.id
                ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                : "border border-[var(--line)] text-[var(--muted)] hover:border-[var(--accent)]"
            }`}
            onClick={() => setTab(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>

      {tab === "search" ? (
        <div className="mb-5">
          <SearchField
            value={query}
            placeholder="Search name, Day Master, chart id…"
            onChange={(event) => {
              const value = event.target.value;
              setQuery(value);
              const nextParams = new URLSearchParams(params);
              nextParams.set("tab", "search");
              if (value) nextParams.set("q", value);
              else nextParams.delete("q");
              setParams(nextParams, { replace: true });
            }}
          />
          <p className="mt-2 text-xs text-[var(--muted)]" aria-live="polite">
            {visible.length} result{visible.length === 1 ? "" : "s"}
          </p>
        </div>
      ) : null}

      {visible.length === 0 ? (
        <EmptyState
          title="No charts in this view"
          body="Create a chart or switch filters to see library entries."
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
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {visible.map((item) => (
            <ChartCard
              key={item.id}
              chart={item}
              onOpen={openLibraryChart}
              onToggleFavorite={toggleFavorite}
              onTogglePinned={togglePinned}
            />
          ))}
        </div>
      )}
    </div>
  );
}
