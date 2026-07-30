import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { DashboardPage } from "./pages/DashboardPage";
import { LibraryProvider } from "./state/library";
import { SessionProvider } from "./state/session";

const ChartInputPage = lazy(() =>
  import("./pages/ChartInputPage").then((m) => ({ default: m.ChartInputPage })),
);
const ChartViewerPage = lazy(() =>
  import("./pages/ChartViewerPage").then((m) => ({ default: m.ChartViewerPage })),
);
const AnalysisViewerPage = lazy(() =>
  import("./pages/AnalysisViewerPage").then((m) => ({
    default: m.AnalysisViewerPage,
  })),
);
const InterpretationViewerPage = lazy(() =>
  import("./pages/InterpretationViewerPage").then((m) => ({
    default: m.InterpretationViewerPage,
  })),
);
const LuckViewerPage = lazy(() =>
  import("./pages/LuckViewerPage").then((m) => ({ default: m.LuckViewerPage })),
);
const ChartsPage = lazy(() =>
  import("./pages/ChartsPage").then((m) => ({ default: m.ChartsPage })),
);
const CustomerHistoryPage = lazy(() =>
  import("./pages/CustomerHistoryPage").then((m) => ({
    default: m.CustomerHistoryPage,
  })),
);
const TimelinePage = lazy(() =>
  import("./pages/TimelinePage").then((m) => ({ default: m.TimelinePage })),
);
const DataPage = lazy(() =>
  import("./pages/DataPage").then((m) => ({ default: m.DataPage })),
);
const SettingsPage = lazy(() =>
  import("./pages/SettingsPage").then((m) => ({ default: m.SettingsPage })),
);
const ProfilePage = lazy(() =>
  import("./pages/ProfilePage").then((m) => ({ default: m.ProfilePage })),
);

function RouteFallback() {
  return (
    <div className="mx-auto max-w-3xl py-16 text-center text-sm text-[var(--muted)]" role="status">
      Loading workspace…
    </div>
  );
}

export default function App() {
  return (
    <SessionProvider>
      <LibraryProvider>
        <AppShell>
          <Suspense fallback={<RouteFallback />}>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/charts" element={<ChartsPage />} />
              <Route path="/history" element={<CustomerHistoryPage />} />
              <Route path="/timeline" element={<TimelinePage />} />
              <Route path="/data" element={<DataPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/chart/input" element={<ChartInputPage />} />
              <Route path="/chart" element={<ChartViewerPage />} />
              <Route path="/analysis" element={<AnalysisViewerPage />} />
              <Route
                path="/interpretation"
                element={<InterpretationViewerPage />}
              />
              <Route path="/luck" element={<LuckViewerPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Suspense>
        </AppShell>
      </LibraryProvider>
    </SessionProvider>
  );
}
