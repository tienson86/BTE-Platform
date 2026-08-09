import { lazy, Suspense, useCallback, useEffect, useState } from "react";
import { PortalShell } from "./chrome/PortalShell";
import { parsePortalHash, portalHref, type PortalRoute } from "./chrome/routes";
import {
  AboutPage,
  EmptyPage,
  ErrorPage,
  HelpPage,
  HistoryPage,
  LoadingPage,
  NotFoundPage,
  ProfilePage,
  SettingsPage,
} from "./pages/AccountSupport";
import {
  AnalysisProgressPage,
  BirthInformationPage,
  ChartInputPage,
  NewAnalysisPage,
  type WizardDraft,
} from "./pages/AnalysisWizard";
import { DashboardPage, HomePage } from "./pages/HomeDashboard";
import { KnowledgeCenterPage, ResultListPage } from "./pages/ResultsKnowledge";
import { PvLoading } from "./components/states";
import "./styles/portal.css";

const ResultViewerPage = lazy(() => import("./pages/ResultViewerPage"));

const INITIAL_DRAFT: WizardDraft = {
  name: "Nguyễn Văn An",
  place: "Hà Nội",
  year: "1990",
  month: "5",
  day: "15",
  hour: "10",
  minute: "30",
  gender: "male",
  calendar: "solar",
};

export type PortalAppProps = {
  initialRoute?: PortalRoute;
};

export function PortalApp({ initialRoute }: PortalAppProps) {
  const [route, setRoute] = useState<PortalRoute>(initialRoute ?? "home");
  const [search, setSearch] = useState("");
  const [toast, setToast] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [draft, setDraft] = useState<WizardDraft>(INITIAL_DRAFT);

  useEffect(() => {
    if (initialRoute) return;
    const sync = () => setRoute(parsePortalHash(window.location.hash));
    sync();
    window.addEventListener("hashchange", sync);
    return () => window.removeEventListener("hashchange", sync);
  }, [initialRoute]);

  const onNavigate = useCallback((next: PortalRoute) => {
    setRoute(next);
    setSidebarOpen(false);
    if (!initialRoute && typeof window !== "undefined") {
      window.location.hash = portalHref(next).slice(1);
    }
  }, [initialRoute]);

  const onSearch = useCallback((value: string) => {
    setSearch(value);
    if (value.trim()) {
      setToast("Đang lọc theo từ khóa trên trang hiện tại");
    } else {
      setToast(null);
    }
  }, []);

  let body;
  switch (route) {
    case "home":
      body = <HomePage onNavigate={onNavigate} />;
      break;
    case "dashboard":
      body = <DashboardPage onNavigate={onNavigate} />;
      break;
    case "analyze":
      body = <NewAnalysisPage onNavigate={onNavigate} />;
      break;
    case "analyze-birth":
      body = <BirthInformationPage draft={draft} onChange={(patch) => setDraft((prev) => ({ ...prev, ...patch }))} onNavigate={onNavigate} />;
      break;
    case "analyze-chart":
      body = <ChartInputPage draft={draft} onChange={(patch) => setDraft((prev) => ({ ...prev, ...patch }))} onNavigate={onNavigate} />;
      break;
    case "analyze-progress":
      body = <AnalysisProgressPage draft={draft} onNavigate={onNavigate} />;
      break;
    case "results":
      body = <ResultListPage onNavigate={onNavigate} />;
      break;
    case "result":
      body = (
        <Suspense fallback={<PvLoading label="Đang mở kết quả tư vấn" />}>
          <ResultViewerPage />
        </Suspense>
      );
      break;
    case "knowledge":
      body = <KnowledgeCenterPage onNavigate={onNavigate} />;
      break;
    case "profile":
      body = <ProfilePage />;
      break;
    case "history":
      body = <HistoryPage onNavigate={onNavigate} />;
      break;
    case "settings":
      body = <SettingsPage />;
      break;
    case "help":
      body = <HelpPage onNavigate={onNavigate} />;
      break;
    case "about":
      body = <AboutPage />;
      break;
    case "error":
      body = <ErrorPage onNavigate={onNavigate} />;
      break;
    case "loading":
      body = <LoadingPage />;
      break;
    case "empty":
      body = <EmptyPage onNavigate={onNavigate} />;
      break;
    default:
      body = <NotFoundPage onNavigate={onNavigate} />;
  }

  return (
    <PortalShell
      route={route}
      search={search}
      toast={toast}
      sidebarOpen={sidebarOpen}
      onSearch={onSearch}
      onNavigate={onNavigate}
      onToggleSidebar={() => setSidebarOpen((open) => !open)}
    >
      {body}
    </PortalShell>
  );
}

export default PortalApp;
