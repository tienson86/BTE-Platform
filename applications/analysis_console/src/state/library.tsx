import {
  createContext,
  startTransition,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { ChartData, CreateChartPayload } from "../api/types";
import { newId, readJson, writeJson } from "../lib/storage";
import {
  DEFAULT_PROFILE,
  DEFAULT_SETTINGS,
  type AppSettings,
  type CustomerRecord,
  type LibraryChart,
  type LibraryExportBundle,
  type TimelineEvent,
  type TimelineEventType,
  type UserProfile,
} from "./libraryTypes";

const CHARTS_KEY = "bte-console-library-charts";
const TIMELINE_KEY = "bte-console-library-timeline";
const CUSTOMERS_KEY = "bte-console-library-customers";
const PROFILE_KEY = "bte-console-user-profile";
const SETTINGS_KEY = "bte-console-settings";

type LibraryState = {
  charts: LibraryChart[];
  timeline: TimelineEvent[];
  customers: CustomerRecord[];
  profile: UserProfile;
  settings: AppSettings;
  upsertChartFromCreate: (
    payload: CreateChartPayload,
    remote: ChartData,
  ) => LibraryChart;
  openChart: (libraryId: string) => LibraryChart | null;
  toggleFavorite: (libraryId: string) => void;
  togglePinned: (libraryId: string) => void;
  removeChart: (libraryId: string) => void;
  recordEvent: (
    type: TimelineEventType,
    title: string,
    detail: string,
    refs?: { chart_id?: string | null; library_id?: string | null },
  ) => void;
  updateProfile: (patch: Partial<UserProfile>) => void;
  updateSettings: (patch: Partial<AppSettings>) => void;
  exportBundle: () => LibraryExportBundle;
  importBundle: (bundle: LibraryExportBundle, mode: "merge" | "replace") => void;
  recentCharts: LibraryChart[];
  favoriteCharts: LibraryChart[];
  pinnedCharts: LibraryChart[];
  searchCharts: (query: string) => LibraryChart[];
};

const LibraryContext = createContext<LibraryState | null>(null);

function rebuildCustomers(charts: LibraryChart[]): CustomerRecord[] {
  const map = new Map<string, CustomerRecord>();
  for (const chart of charts) {
    const name = chart.customer_name.trim() || "Unnamed customer";
    const key = name.toLowerCase();
    const existing = map.get(key);
    if (!existing) {
      map.set(key, {
        id: `cust_${key.replace(/\s+/g, "_")}`,
        name,
        chart_count: 1,
        library_ids: [chart.id],
        last_seen: chart.last_opened_at || chart.updated_at,
        notes: "",
      });
    } else {
      existing.chart_count += 1;
      existing.library_ids.push(chart.id);
      if (chart.last_opened_at > existing.last_seen) {
        existing.last_seen = chart.last_opened_at;
      }
    }
  }
  return Array.from(map.values()).sort((a, b) =>
    b.last_seen.localeCompare(a.last_seen),
  );
}

function sortByOpened(charts: LibraryChart[]): LibraryChart[] {
  return [...charts].sort((a, b) =>
    b.last_opened_at.localeCompare(a.last_opened_at),
  );
}

export function LibraryProvider({ children }: { children: ReactNode }) {
  const [charts, setCharts] = useState<LibraryChart[]>(() =>
    readJson(CHARTS_KEY, []),
  );
  const [timeline, setTimeline] = useState<TimelineEvent[]>(() =>
    readJson(TIMELINE_KEY, []),
  );
  const [customers, setCustomers] = useState<CustomerRecord[]>(() =>
    readJson(CUSTOMERS_KEY, []),
  );
  const [profile, setProfile] = useState<UserProfile>(() =>
    readJson(PROFILE_KEY, DEFAULT_PROFILE),
  );
  const [settings, setSettings] = useState<AppSettings>(() =>
    readJson(SETTINGS_KEY, DEFAULT_SETTINGS),
  );

  useEffect(() => writeJson(CHARTS_KEY, charts), [charts]);
  useEffect(() => writeJson(TIMELINE_KEY, timeline), [timeline]);
  useEffect(() => writeJson(CUSTOMERS_KEY, customers), [customers]);
  useEffect(() => writeJson(PROFILE_KEY, profile), [profile]);
  useEffect(() => writeJson(SETTINGS_KEY, settings), [settings]);

  const recordEvent = useCallback(
    (
      type: TimelineEventType,
      title: string,
      detail: string,
      refs?: { chart_id?: string | null; library_id?: string | null },
    ) => {
      const event: TimelineEvent = {
        id: newId("evt"),
        type,
        title,
        detail,
        at: new Date().toISOString(),
        chart_id: refs?.chart_id ?? null,
        library_id: refs?.library_id ?? null,
      };
      startTransition(() => {
        setTimeline((prev) => [event, ...prev].slice(0, 200));
      });
    },
    [],
  );

  const upsertChartFromCreate = useCallback(
    (payload: CreateChartPayload, remote: ChartData) => {
      const now = new Date().toISOString();
      const customer_name = payload.full_name?.trim() || "Unnamed customer";
      const entry: LibraryChart = {
        id: newId("lib"),
        chart_id: remote.chart_id,
        name: `${customer_name} · ${payload.day_master}`,
        customer_name,
        day_master: payload.day_master,
        gender: payload.gender ?? "",
        year: payload.year ?? null,
        month: payload.month ?? null,
        day: payload.day ?? null,
        favorite: false,
        pinned: false,
        created_at: now,
        updated_at: now,
        last_opened_at: now,
        tags: [],
        payload,
        remote,
      };
      startTransition(() => {
        setCharts((prev) => {
          const next = [entry, ...prev];
          setCustomers(rebuildCustomers(next));
          return next;
        });
      });
      recordEvent(
        "chart_created",
        "Chart created",
        entry.name,
        { chart_id: remote.chart_id, library_id: entry.id },
      );
      return entry;
    },
    [recordEvent],
  );

  const openChart = useCallback(
    (libraryId: string) => {
      const now = new Date().toISOString();
      const current = charts.find((item) => item.id === libraryId) ?? null;
      if (!current) return null;
      const updated = { ...current, last_opened_at: now, updated_at: now };
      setCharts((prev) =>
        prev.map((item) => (item.id === libraryId ? updated : item)),
      );
      recordEvent("chart_opened", "Chart opened", updated.name, {
        chart_id: updated.chart_id,
        library_id: updated.id,
      });
      return updated;
    },
    [charts, recordEvent],
  );

  const toggleFavorite = useCallback(
    (libraryId: string) => {
      setCharts((prev) =>
        prev.map((item) => {
          if (item.id !== libraryId) return item;
          const next = { ...item, favorite: !item.favorite, updated_at: new Date().toISOString() };
          recordEvent(
            "favorite",
            next.favorite ? "Added to favorites" : "Removed from favorites",
            next.name,
            { chart_id: next.chart_id, library_id: next.id },
          );
          return next;
        }),
      );
    },
    [recordEvent],
  );

  const togglePinned = useCallback(
    (libraryId: string) => {
      setCharts((prev) =>
        prev.map((item) => {
          if (item.id !== libraryId) return item;
          const next = { ...item, pinned: !item.pinned, updated_at: new Date().toISOString() };
          recordEvent(
            "pin",
            next.pinned ? "Pinned chart" : "Unpinned chart",
            next.name,
            { chart_id: next.chart_id, library_id: next.id },
          );
          return next;
        }),
      );
    },
    [recordEvent],
  );

  const removeChart = useCallback((libraryId: string) => {
    setCharts((prev) => {
      const next = prev.filter((item) => item.id !== libraryId);
      setCustomers(rebuildCustomers(next));
      return next;
    });
  }, []);

  const updateProfile = useCallback((patch: Partial<UserProfile>) => {
    setProfile((prev) => ({ ...prev, ...patch }));
  }, []);

  const updateSettings = useCallback((patch: Partial<AppSettings>) => {
    setSettings((prev) => ({ ...prev, ...patch }));
  }, []);

  const exportBundle = useCallback((): LibraryExportBundle => {
    const bundle: LibraryExportBundle = {
      version: "1.0.0",
      exported_at: new Date().toISOString(),
      charts,
      timeline,
      customers,
      profile,
      settings,
    };
    recordEvent("export", "Library exported", `${charts.length} charts`);
    return bundle;
  }, [charts, timeline, customers, profile, settings, recordEvent]);

  const importBundle = useCallback(
    (bundle: LibraryExportBundle, mode: "merge" | "replace") => {
      if (!bundle || bundle.version !== "1.0.0" || !Array.isArray(bundle.charts)) {
        throw new Error("Invalid import bundle");
      }
      startTransition(() => {
        if (mode === "replace") {
          setCharts(bundle.charts);
          setTimeline(bundle.timeline ?? []);
          setCustomers(bundle.customers ?? rebuildCustomers(bundle.charts));
          if (bundle.profile) setProfile(bundle.profile);
          if (bundle.settings) setSettings(bundle.settings);
        } else {
          setCharts((prev) => {
            const ids = new Set(prev.map((c) => c.id));
            const merged = [...prev];
            for (const chart of bundle.charts) {
              if (!ids.has(chart.id)) merged.push(chart);
            }
            setCustomers(rebuildCustomers(merged));
            return merged;
          });
          setTimeline((prev) => [...(bundle.timeline ?? []), ...prev].slice(0, 200));
        }
      });
      recordEvent(
        "import",
        "Library imported",
        `${bundle.charts.length} charts (${mode})`,
      );
    },
    [recordEvent],
  );

  const recentCharts = useMemo(() => sortByOpened(charts).slice(0, 12), [charts]);
  const favoriteCharts = useMemo(
    () => sortByOpened(charts.filter((c) => c.favorite)),
    [charts],
  );
  const pinnedCharts = useMemo(
    () => sortByOpened(charts.filter((c) => c.pinned)),
    [charts],
  );

  const searchCharts = useCallback(
    (query: string) => {
      const q = query.trim().toLowerCase();
      if (!q) return sortByOpened(charts);
      return sortByOpened(
        charts.filter((chart) => {
          const hay = [
            chart.name,
            chart.customer_name,
            chart.day_master,
            chart.chart_id ?? "",
            chart.tags.join(" "),
          ]
            .join(" ")
            .toLowerCase();
          return hay.includes(q);
        }),
      );
    },
    [charts],
  );

  const value = useMemo(
    () => ({
      charts,
      timeline,
      customers,
      profile,
      settings,
      upsertChartFromCreate,
      openChart,
      toggleFavorite,
      togglePinned,
      removeChart,
      recordEvent,
      updateProfile,
      updateSettings,
      exportBundle,
      importBundle,
      recentCharts,
      favoriteCharts,
      pinnedCharts,
      searchCharts,
    }),
    [
      charts,
      timeline,
      customers,
      profile,
      settings,
      upsertChartFromCreate,
      openChart,
      toggleFavorite,
      togglePinned,
      removeChart,
      recordEvent,
      updateProfile,
      updateSettings,
      exportBundle,
      importBundle,
      recentCharts,
      favoriteCharts,
      pinnedCharts,
      searchCharts,
    ],
  );

  return (
    <LibraryContext.Provider value={value}>{children}</LibraryContext.Provider>
  );
}

export function useLibrary() {
  const ctx = useContext(LibraryContext);
  if (!ctx) {
    throw new Error("useLibrary must be used within LibraryProvider");
  }
  return ctx;
}
