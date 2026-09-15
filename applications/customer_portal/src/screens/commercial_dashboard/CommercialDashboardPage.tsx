/**
 * Commercial Dashboard page header + Identity + Life Consulting + canonical grid.
 */

import { useState, type ReactNode } from "react";
import type { CanonicalDesktopViewModel } from "../../adapters";
import {
  customerExportBlockMessage,
  customerExportErrorMessage,
  customerExportReady,
  downloadOfficialExport,
  type CustomerExportPayload,
} from "../../export/customerExport";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../../models";
import { resolveNarrativeProvider } from "../../resultState/narrativeProvider";
import { selectNarrativePresentation } from "../../resultState/narrativePresentationSelection";
import { ResultPageStatusGate } from "../result";
import { adaptIdentityHeader } from "./adapter";
import { adaptBaziCard } from "./baziAdapter";
import { BAZI_VISUAL_FIXTURE } from "./baziFixture";
import { adaptFiveElementsCard } from "./fiveElementsAdapter";
import { FIVE_ELEMENTS_VISUAL_FIXTURE } from "./fiveElementsFixture";
import { adaptTenGodsCard } from "./tenGodsAdapter";
import { TEN_GODS_VISUAL_FIXTURE } from "./tenGodsFixture";
import { adaptPatternCard } from "./patternAdapter";
import { PATTERN_VISUAL_FIXTURE } from "./patternFixture";
import { adaptShenShaCard } from "./shenShaAdapter";
import { SHENSHA_VISUAL_FIXTURE } from "./shenShaFixture";
import { adaptLuckCard } from "./luckAdapter";
import { LUCK_VISUAL_FIXTURE } from "./luckFixture";
import { adaptLifeConsulting } from "./lifeConsultingAdapter";
import { LIFE_CONSULTING_VISUAL_FIXTURE } from "./lifeConsultingFixture";
import { INTERPRETATION_VISUAL_FIXTURE } from "./interpretationFixture";
import { ACTION_PLAN_VISUAL_FIXTURE } from "./actionPlanFixture";
import { adaptActionPlanCard, adaptOptimizationPlan } from "./actionPlanAdapter";
import { OVERVIEW_VISUAL_FIXTURE } from "./overviewFixture";
import { adaptOverviewCard } from "./overviewAdapter";
import { adaptInterpretationCard } from "./interpretationAdapter";
import { adaptPack07Narrative } from "./narrativeComposerAdapter";
import { attachInterpretationDomains, attachOverviewDomains } from "./domainAdapter";
import { RESULT_PAGE_TITLE } from "./cards";
import { DashboardGrid } from "./DashboardGrid";
import { IdentityHeader } from "./IdentityHeader";
import { MobileActionBar } from "./mobile/MobileActionBar";
import { adaptBaziReportDocument } from "./reportDocumentAdapter";
import { ReportDocumentSection } from "./ReportDocumentSection";
import "./commercial-dashboard.css";
import "./mobile/mobileExperience.css";
import "./motion/motionExperience.css";
import "./finish.css";

export type CommercialDashboardPageProps = {
  readonly analysis?: AnalysisDataDto | null;
  readonly request?: AnalyzeChartRequest | null;
  readonly initialData?: CanonicalDesktopViewModel;
  readonly analysisId?: string | null;
  readonly resultSource?:
    | "current"
    | "history"
    | "empty"
    | "preview"
    | "contract"
    | "missing"
    | "corrupt";
  readonly reanalyzeHref?: string | null;
  readonly layoutMode?: "live" | "skeleton" | "visual";
  readonly previewFallback?: boolean;
  readonly narrativeProvider?: string;
  readonly exportPayload?: CustomerExportPayload | null;
};

function ResultPageHeader(): ReactNode {
  return (
    <div className="bte-cdash__page-header" data-page-header="result">
      <h1 className="bte-cdash__title">{RESULT_PAGE_TITLE}</h1>
      <a className="bte-cdash__quiet-link" href="/analyze">
        Phân tích lá số khác
      </a>
    </div>
  );
}

function gateAction(resultSource: CommercialDashboardPageProps["resultSource"], href?: string | null): ReactNode {
  if (resultSource === "missing") {
    return (
      <a className="rp-status-gate__cta" href="/history">
        Về lịch sử
      </a>
    );
  }
  if (resultSource === "contract" || resultSource === "corrupt") {
    return (
      <a className="rp-status-gate__cta" href={href || "/analyze"}>
        Phân tích lại
      </a>
    );
  }
  return undefined;
}

function ResultArchiveActions({
  payload,
  resultSource,
}: {
  readonly payload?: CustomerExportPayload | null;
  readonly resultSource: CommercialDashboardPageProps["resultSource"];
}): ReactNode {
  const [busy, setBusy] = useState<"pdf" | "docx" | null>(null);
  const [notice, setNotice] = useState("");
  const ready = customerExportReady(payload);
  const block = customerExportBlockMessage(payload);
  const savedLabel = resultSource === "history" ? "Đang xem hồ sơ đã lưu" : "Hồ sơ đã tự động lưu";

  async function onDownload(format: "pdf" | "docx"): Promise<void> {
    if (!payload) {
      setNotice(block);
      return;
    }
    setBusy(format);
    setNotice("");
    try {
      await downloadOfficialExport(payload, format);
    } catch (error) {
      setNotice(customerExportErrorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  return (
    <section className="bte-cdash__archive" aria-label="Lưu và xuất hồ sơ lá số">
      <div className="bte-cdash__archive-copy">
        <span className="bte-cdash__archive-status">{savedLabel}</span>
        <p>Quản lý lại lá số trong lịch sử, hoặc xuất bản luận giải thành tệp để gửi khách hàng.</p>
      </div>
      <div className="bte-cdash__archive-actions">
        <a className="bte-cdash__archive-btn" href="/history">
          Hồ sơ đã lưu
        </a>
        <button type="button" className="bte-cdash__archive-btn" onClick={() => window.print()}>
          In nhanh
        </button>
        <button
          type="button"
          className="bte-cdash__archive-btn bte-cdash__archive-btn--primary"
          disabled={!ready || busy !== null}
          onClick={() => void onDownload("pdf")}
        >
          {busy === "pdf" ? "Đang tạo PDF..." : "Tải PDF"}
        </button>
        <button
          type="button"
          className="bte-cdash__archive-btn bte-cdash__archive-btn--primary"
          disabled={!ready || busy !== null}
          onClick={() => void onDownload("docx")}
        >
          {busy === "docx" ? "Đang tạo DOCX..." : "Tải DOCX"}
        </button>
      </div>
      {notice || (!ready && block) ? (
        <p className="bte-cdash__archive-notice" role="status">
          {notice || block}
        </p>
      ) : null}
    </section>
  );
}

/**
 * Canonical `/result` body for Commercial Dashboard (UI-03 geometry, UI-14 visual hierarchy).
 */
export function CommercialDashboardPage({
  analysis = null,
  request = null,
  initialData,
  analysisId = null,
  resultSource = "current",
  reanalyzeHref = null,
  layoutMode = "live",
  previewFallback = false,
  narrativeProvider: _narrativeProvider,
  exportPayload = null,
}: CommercialDashboardPageProps): ReactNode {
  const harness = layoutMode === "skeleton" || layoutMode === "visual" || previewFallback;
  const requestedProvider = resolveNarrativeProvider();
  void _narrativeProvider;
  const status = initialData?.status;
  const showGate = !harness && ((status && status !== "ready") || (!analysis && resultSource !== "current"));

  if (showGate) {
    const gateStatus = status && status !== "ready" ? status : "empty";
    return (
      <div
        className="bte-cdash"
        data-dashboard="commercial-v1"
        data-canonical-result="ui03"
        data-visual="v2"
        data-ia="ui05a"
        data-mobile-experience="true"
        data-motion="v1"
        data-finish="v2"
        data-narrative-surface="production"
        data-narrative-provider={requestedProvider}
      >
        <ResultPageHeader />
        <ResultPageStatusGate
          status={gateStatus}
          message={initialData?.statusMessage}
          action={gateAction(resultSource, reanalyzeHref)}
        />
      </div>
    );
  }

  const model = adaptIdentityHeader(analysis, { request, analysisId });
  const bazi =
    layoutMode === "visual"
      ? BAZI_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptBaziCard(analysis);
  const fiveElements =
    layoutMode === "visual"
      ? FIVE_ELEMENTS_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptFiveElementsCard(analysis);
  const tenGods =
    layoutMode === "visual"
      ? TEN_GODS_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptTenGodsCard(analysis);
  const pattern =
    layoutMode === "visual"
      ? PATTERN_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptPatternCard(analysis);
  const shenSha =
    layoutMode === "visual"
      ? SHENSHA_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptShenShaCard(analysis);
  const luck =
    layoutMode === "visual"
      ? LUCK_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptLuckCard(analysis);
  const lifeConsulting =
    layoutMode === "visual"
      ? LIFE_CONSULTING_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptLifeConsulting(analysis, { request });
  const narrative = harness
    ? null
    : selectNarrativePresentation(analysis, requestedProvider);
  const overview =
    layoutMode === "visual"
      ? OVERVIEW_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : attachOverviewDomains(narrative?.overview ?? adaptOverviewCard(analysis), analysis);
  const pack07Narrative =
    layoutMode === "visual" || layoutMode === "skeleton" || previewFallback
      ? null
      : adaptPack07Narrative(analysis);
  const interpretation =
    layoutMode === "visual"
      ? INTERPRETATION_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : pack07Narrative
          ?? attachInterpretationDomains(
            narrative?.interpretation?.available
              ? narrative.interpretation
              : adaptInterpretationCard(analysis),
            analysis,
          );
  const consultingPlan = adaptActionPlanCard(analysis);
  const actionPlan =
    layoutMode === "visual"
      ? ACTION_PLAN_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptOptimizationPlan(analysis)
          ?? (narrative?.actionPlan?.available ? narrative.actionPlan : null)
          ?? consultingPlan;
  const reportDocument =
    layoutMode === "visual" || layoutMode === "skeleton" || previewFallback
      ? null
      : adaptBaziReportDocument(analysis);
  return (
    <div
      className="bte-cdash"
      data-dashboard="commercial-v1"
      data-canonical-result="ui03"
      data-visual="v2"
      data-ia="ui05a"
      data-mobile-experience="true"
      data-motion="v1"
      data-finish="v2"
      data-narrative-surface="production"
      data-narrative-provider={narrative?.selected ?? requestedProvider}
      data-narrative-fallback={narrative?.fallback ? "true" : "false"}
      data-presentation-version={narrative?.presentationVersion ?? ""}
      data-layout={layoutMode === "skeleton" || previewFallback ? "skeleton" : layoutMode}
    >
      <ResultPageHeader />
      <ResultArchiveActions payload={exportPayload} resultSource={resultSource} />
      <IdentityHeader model={model} />
      <DashboardGrid
        overview={overview}
        bazi={bazi}
        fiveElements={fiveElements}
        tenGods={tenGods}
        pattern={pattern}
        shenSha={shenSha}
        luck={luck}
        interpretation={interpretation}
        actionPlan={actionPlan}
        lifeConsulting={lifeConsulting}
      />
      {reportDocument ? <ReportDocumentSection model={reportDocument} /> : null}
      <MobileActionBar />
    </div>
  );
}
