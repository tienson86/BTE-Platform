/**
 * Executive consulting report preview. Layout only. Presentation + canonical chart.
 */

import type { ReactNode } from "react";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../../models";
import { ActionPlanSection } from "./components/ActionPlanSection";
import { ChartSnapshotSection } from "./components/ChartSnapshotSection";
import { ExecutiveSummarySection } from "./components/ExecutiveSummarySection";
import { InterpretationSection } from "./components/InterpretationSection";
import { KeyFindingsSection } from "./components/KeyFindingsSection";
import { LuckSection } from "./components/LuckSection";
import { ReportAppendix } from "./components/ReportAppendix";
import { ReportCover } from "./components/ReportCover";
import { ReportIdentity } from "./components/ReportIdentity";
import { ReportDivider } from "./components/ReportPrimitives";
import { SupportingAnalysisSection } from "./components/SupportingAnalysisSection";
import { REPORT_PREVIEW_BANNER } from "./copy";
import { buildExecutiveReportView } from "./reportModel";
import "./executive-report.css";

export type ExecutiveReportPageProps = {
  readonly analysis?: AnalysisDataDto | null;
  readonly request?: AnalyzeChartRequest | null;
};

/**
 * HTML report preview surface. Does not replace the production PDF path.
 */
export function ExecutiveReportPage({
  analysis,
  request,
}: ExecutiveReportPageProps): ReactNode {
  const model = buildExecutiveReportView(analysis, request);
  const presentation = model.presentation;
  return (
    <article
      className="bte-er"
      data-ui="executive-report"
      data-report="preview"
      data-pdf-export="false"
      data-narrative-source="presentation-v2"
    >
      <p className="bte-er__preview-banner">{REPORT_PREVIEW_BANNER}</p>
      <div className="bte-er__sheet">
        <ReportCover model={model.cover} />
        <ReportIdentity rows={model.identityRows} />
        <ReportDivider />
        <ExecutiveSummarySection overview={presentation?.overview ?? null} />
        <ChartSnapshotSection
          bazi={model.bazi}
          fiveElements={model.fiveElements}
          pattern={model.pattern}
          luck={model.luck}
        />
        <KeyFindingsSection findings={model.findings} />
        <InterpretationSection interpretation={presentation?.interpretation ?? null} />
        <ActionPlanSection plan={presentation?.action_plan ?? null} />
        <LuckSection luck={model.luck} />
        <SupportingAnalysisSection
          bazi={model.bazi}
          fiveElements={model.fiveElements}
          tenGods={model.tenGods}
          pattern={model.pattern}
          shenSha={model.shenSha}
        />
        <ReportAppendix model={model.appendix} />
      </div>
    </article>
  );
}
