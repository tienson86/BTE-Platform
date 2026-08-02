/**
 * Consultation Report presentation ViewModels — WP-0009.
 * Report orchestration metadata + nested section ViewModels only.
 */

import type { PresentationStatus } from "./executive_summary";
import type { ExecutiveSummaryViewModel } from "./executive_summary";
import type { FourPillarsViewModel } from "./four_pillars";
import type { ExecutiveInsightViewModel } from "./executive_insight";
import type { MetricsViewModel } from "./metrics";
import type { ExplainableAnalysisViewModel } from "./explainable_analysis";

export type ReportSectionId =
  | "executive-summary"
  | "four-pillars"
  | "executive-insight"
  | "metrics"
  | "explainable-analysis";

export type ReportTocItemViewModel = {
  id: string;
  label: string;
  href: string;
  active?: boolean;
};

export type ReportSectionMetaViewModel = {
  id: ReportSectionId;
  title: string;
  href: string;
  transitionLabel?: string;
};

export type ReportHeaderViewModel = {
  title: string;
  subtitle?: string;
  clientLabel?: string;
  generatedLabel?: string;
};

export type ReportFooterViewModel = {
  note: string;
  copyright?: string;
};

export type ReportPrintViewModel = {
  headerTitle: string;
  footerNote: string;
};

export type ReportClosingViewModel = {
  title: string;
  body: string;
};

export type ConsultationReportReadyViewModel = {
  status: "ready";
  header: ReportHeaderViewModel;
  toc: ReportTocItemViewModel[];
  sections: ReportSectionMetaViewModel[];
  progress?: number;
  footer: ReportFooterViewModel;
  print: ReportPrintViewModel;
  closing?: ReportClosingViewModel;
  executiveSummary: ExecutiveSummaryViewModel;
  fourPillars: FourPillarsViewModel;
  executiveInsight: ExecutiveInsightViewModel;
  metrics: MetricsViewModel;
  explainableAnalysis: ExplainableAnalysisViewModel;
};

export type ConsultationReportPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type ConsultationReportErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type ConsultationReportViewModel =
  | ConsultationReportReadyViewModel
  | ConsultationReportPendingViewModel
  | ConsultationReportErrorViewModel;
