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
import { ReportIdentity } from "./components/ReportIdentity";
import { SupportingAnalysisSection } from "./components/SupportingAnalysisSection";
import { REPORT_ANALYSIS_TITLE, REPORT_PREVIEW_BANNER } from "./copy";
import {
  PrintAppendix,
  PrintCover,
  PrintDivider,
  PrintFooter,
  PrintHeader,
  PrintSection,
} from "./print";
import { buildExecutiveReportView } from "./reportModel";
import "./executive-report.css";
import "./print/print.css";
import "../commercial_dashboard/mobile/mobileExperience.css";
import "../commercial_dashboard/motion/motionExperience.css";

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
      data-motion="v1"
      data-pdf-export="false"
      data-print-ready="true"
      data-narrative-source="presentation-v2"
    >
      <p className="bte-er__preview-banner">{REPORT_PREVIEW_BANNER}</p>
      <PrintHeader
        title={REPORT_ANALYSIS_TITLE}
        customer={model.cover.customerName}
        version={model.cover.reportVersion}
      />
      <div className="bte-er__sheet">
        <PrintCover model={model.cover} />
        <ReportIdentity rows={model.identityRows} />
        <PrintDivider />
        <PrintSection breakBefore>
          <ExecutiveSummarySection overview={presentation?.overview ?? null} />
        </PrintSection>
        <PrintSection keepTogether>
          <ChartSnapshotSection
            bazi={model.bazi}
            fiveElements={model.fiveElements}
            pattern={model.pattern}
            luck={model.luck}
          />
        </PrintSection>
        <PrintSection keepTogether>
          <KeyFindingsSection findings={model.findings} />
        </PrintSection>
        <PrintSection breakBefore>
          <InterpretationSection interpretation={presentation?.interpretation ?? null} />
        </PrintSection>
        <PrintSection breakBefore>
          <ActionPlanSection plan={presentation?.action_plan ?? null} />
        </PrintSection>
        <PrintSection keepTogether>
          <LuckSection luck={model.luck} />
        </PrintSection>
        <SupportingAnalysisSection
          bazi={model.bazi}
          fiveElements={model.fiveElements}
          tenGods={model.tenGods}
          pattern={model.pattern}
          shenSha={model.shenSha}
        />
        <PrintAppendix model={model.appendix} />
      </div>
      <PrintFooter version={model.cover.reportVersion} />
    </article>
  );
}
