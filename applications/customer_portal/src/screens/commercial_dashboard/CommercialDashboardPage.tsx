/**
 * Commercial Dashboard page header + Identity Header + canonical grid.
 */

import type { ReactNode } from "react";
import type { CanonicalDesktopViewModel } from "../../adapters";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../../models";
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
import { adaptInterpretationCard } from "./interpretationAdapter";
import { INTERPRETATION_VISUAL_FIXTURE } from "./interpretationFixture";
import { adaptActionPlanCard } from "./actionPlanAdapter";
import { ACTION_PLAN_VISUAL_FIXTURE } from "./actionPlanFixture";
import { adaptOverviewCard } from "./overviewAdapter";
import { OVERVIEW_VISUAL_FIXTURE } from "./overviewFixture";
import { RESULT_PAGE_TITLE } from "./cards";
import { CanXuongDetail } from "./CanXuongDetail";
import { DashboardGrid } from "./DashboardGrid";
import { IdentityHeader } from "./IdentityHeader";
import "./commercial-dashboard.css";

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

/**
 * Canonical `/result` body for Commercial Dashboard V1.0 (UI-03).
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
}: CommercialDashboardPageProps): ReactNode {
  const harness = layoutMode === "skeleton" || layoutMode === "visual" || previewFallback;
  const status = initialData?.status;
  const showGate = !harness && ((status && status !== "ready") || (!analysis && resultSource !== "current"));

  if (showGate) {
    const gateStatus = status && status !== "ready" ? status : "empty";
    return (
      <div className="bte-cdash" data-dashboard="commercial-v1" data-canonical-result="ui03">
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
  const overview =
    layoutMode === "visual"
      ? OVERVIEW_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptOverviewCard(analysis);
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
  const interpretation =
    layoutMode === "visual"
      ? INTERPRETATION_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptInterpretationCard(analysis);
  const actionPlan =
    layoutMode === "visual"
      ? ACTION_PLAN_VISUAL_FIXTURE
      : layoutMode === "skeleton" || previewFallback
        ? null
        : adaptActionPlanCard(analysis);
  return (
    <div
      className="bte-cdash"
      data-dashboard="commercial-v1"
      data-canonical-result="ui03"
      data-layout={layoutMode === "skeleton" || previewFallback ? "skeleton" : layoutMode}
    >
      <ResultPageHeader />
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
      />
      <CanXuongDetail foundation={model.foundation} />
    </div>
  );
}
