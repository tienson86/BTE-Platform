import { lazy, Suspense, useCallback, useEffect, useRef, useState } from "react";
import { PortalShell } from "./chrome/PortalShell";
import { parsePortalHash, portalHref, type PortalRoute } from "./chrome/routes";
import type { ReportMode } from "./components/CommercialRail";
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
  type WizardAnalyzeStatus,
  type WizardDraft,
} from "./pages/AnalysisWizard";
import { DashboardPage, HomePage } from "./pages/HomeDashboard";
import {
  CompletionPage,
  KnowledgeArticlePage,
  OnboardingPage,
  PremiumPage,
  ShareSheet,
} from "./pages/JourneyPages";
import { KnowledgeCenterPage, ResultListPage } from "./pages/ResultsKnowledge";
import { PvLoading } from "./components/states";
import { apiErrorUserMessage, isApiError } from "../../api";
import type { AnalyzeService } from "../../services";
import { getAnalyzeService } from "../../services";
import {
  resolveAnalysisId,
  type PortalAnalysisSession,
} from "./analysisSession";
import { draftToAnalyzeRequest } from "./wizardAnalyzeRequest";
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

const VALIDATION_ERROR_VI =
  "Thông tin ngày sinh chưa đủ hoặc không hợp lệ. Vui lòng kiểm tra lại.";
const UNKNOWN_ERROR_VI = "Không tạo được phân tích. Vui lòng thử lại.";

export type PortalAppProps = {
  initialRoute?: PortalRoute;
  /** Optional AnalyzeService injection for tests. */
  analyzeService?: AnalyzeService;
};

export function PortalApp({ initialRoute, analyzeService }: PortalAppProps) {
  const [route, setRoute] = useState<PortalRoute>(initialRoute ?? "home");
  const [search, setSearch] = useState("");
  const [toast, setToast] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [draft, setDraft] = useState<WizardDraft>(INITIAL_DRAFT);
  const [saved, setSaved] = useState(false);
  const [reportMode, setReportMode] = useState<ReportMode>("reading");
  const [shareOpen, setShareOpen] = useState(false);
  const [knowledgeReturn, setKnowledgeReturn] = useState<PortalRoute>("result");
  const [analyzeStatus, setAnalyzeStatus] = useState<WizardAnalyzeStatus>("idle");
  const [analyzeError, setAnalyzeError] = useState<string | null>(null);
  const [analysisSession, setAnalysisSession] = useState<PortalAnalysisSession | null>(
    null,
  );
  const submittingRef = useRef(false);

  useEffect(() => {
    if (initialRoute) return;
    const sync = () => setRoute(parsePortalHash(window.location.hash));
    sync();
    window.addEventListener("hashchange", sync);
    return () => window.removeEventListener("hashchange", sync);
  }, [initialRoute]);

  const onNavigate = useCallback(
    (next: PortalRoute) => {
      setRoute(next);
      setSidebarOpen(false);
      if (!initialRoute && typeof window !== "undefined") {
        window.location.hash = portalHref(next).slice(1);
      }
    },
    [initialRoute],
  );

  const onSearch = useCallback((value: string) => {
    setSearch(value);
    setToast(value.trim() ? "Đang lọc theo từ khóa trên trang hiện tại" : null);
  }, []);

  const openKnowledgeFromResult = useCallback(() => {
    setKnowledgeReturn("result");
    onNavigate("knowledge-article");
  }, [onNavigate]);

  const startAnalysis = useCallback(async () => {
    if (submittingRef.current || analyzeStatus === "loading") {
      return;
    }

    const request = draftToAnalyzeRequest(draft);
    if (!request) {
      setAnalyzeStatus("error");
      setAnalyzeError(VALIDATION_ERROR_VI);
      onNavigate("analyze-progress");
      return;
    }

    submittingRef.current = true;
    setAnalyzeStatus("loading");
    setAnalyzeError(null);
    onNavigate("analyze-progress");

    const service = analyzeService ?? getAnalyzeService();
    try {
      const response = await service.analyze(request);
      const analysisId = resolveAnalysisId(response.request_id);
      setAnalysisSession({
        analysis_id: analysisId,
        request_id: response.request_id ?? null,
        data: response.data,
      });
      setAnalyzeStatus("ready");
      onNavigate("result");
    } catch (error) {
      const message = isApiError(error)
        ? apiErrorUserMessage(error)
        : UNKNOWN_ERROR_VI;
      setAnalyzeStatus("error");
      setAnalyzeError(message);
      setAnalysisSession(null);
    } finally {
      submittingRef.current = false;
    }
  }, [analyzeService, analyzeStatus, draft, onNavigate]);

  let body;
  switch (route) {
    case "home":
      body = <HomePage onNavigate={onNavigate} />;
      break;
    case "onboarding":
      body = <OnboardingPage onNavigate={onNavigate} />;
      break;
    case "dashboard":
      body = <DashboardPage onNavigate={onNavigate} />;
      break;
    case "analyze":
      body = <NewAnalysisPage onNavigate={onNavigate} />;
      break;
    case "analyze-birth":
      body = (
        <BirthInformationPage
          draft={draft}
          onChange={(patch) => setDraft((prev) => ({ ...prev, ...patch }))}
          onNavigate={onNavigate}
        />
      );
      break;
    case "analyze-chart":
      body = (
        <ChartInputPage
          draft={draft}
          onChange={(patch) => setDraft((prev) => ({ ...prev, ...patch }))}
          onNavigate={onNavigate}
          onStartAnalysis={() => {
            void startAnalysis();
          }}
          analyzeStatus={analyzeStatus}
        />
      );
      break;
    case "analyze-progress":
      body = (
        <AnalysisProgressPage
          draft={draft}
          onNavigate={onNavigate}
          analyzeStatus={analyzeStatus}
          analyzeError={analyzeError}
          onRetry={() => {
            void startAnalysis();
          }}
        />
      );
      break;
    case "results":
      body = <ResultListPage onNavigate={onNavigate} />;
      break;
    case "result":
      body = (
        <Suspense fallback={<PvLoading label="Đang mở kết quả tư vấn" />}>
          <ResultViewerPage
            mode={reportMode}
            saved={saved}
            analysisId={analysisSession?.analysis_id ?? null}
            analysisResult={analysisSession?.data ?? null}
            onSave={() => {
              setSaved(true);
              setToast("Báo cáo đã được lưu trên thiết bị này");
              onNavigate("complete");
            }}
            onPdf={() => {
              setReportMode("print");
              setToast("Bạn có thể lưu thành PDF từ hộp thoại in");
            }}
            onPrint={() => {
              setReportMode("print");
              if (typeof window !== "undefined") window.print();
            }}
            onShare={() => {
              setReportMode("sharing");
              setShareOpen(true);
              setToast("Liên kết tư vấn đã sẵn sàng để sao chép");
            }}
            onKnowledge={openKnowledgeFromResult}
            onPremium={() => onNavigate("premium")}
          />
        </Suspense>
      );
      break;
    case "knowledge":
      body = <KnowledgeCenterPage onNavigate={onNavigate} />;
      break;
    case "knowledge-article":
      body = (
        <KnowledgeArticlePage
          onNavigate={onNavigate}
          onBackToResult={() => onNavigate(knowledgeReturn)}
        />
      );
      break;
    case "complete":
      body = <CompletionPage onNavigate={onNavigate} />;
      break;
    case "premium":
      body = <PremiumPage onNavigate={onNavigate} />;
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
      <div data-report-mode={reportMode}>{body}</div>
      <ShareSheet open={shareOpen} onClose={() => setShareOpen(false)} />
    </PortalShell>
  );
}

export default PortalApp;
