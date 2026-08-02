import {
  EmptyState,
  ErrorState,
  LoadingState,
  UnavailableState,
} from "../components/shared";
import type { ConsultationReportViewModel } from "../view_models/consultation_report";
import { cx } from "../utils";
import {
  ConsultationReport,
  ReportSection,
  SectionTransition,
} from "../components/business";
import { ReportContainer } from "../components/business/ReportContainer";
import { ExecutiveSummaryScreen } from "./ExecutiveSummaryScreen";
import { FourPillarsScreen } from "./FourPillarsScreen";
import { ExecutiveInsightScreen } from "./ExecutiveInsightScreen";
import { MetricsScreen } from "./MetricsScreen";
import { ExplainableAnalysisScreen } from "./ExplainableAnalysisScreen";

export type ConsultationReportScreenProps = {
  data: ConsultationReportViewModel;
  className?: string;
};

/**
 * Consultation Report Screen — Pack 03 / Pack 06 WP-0009.
 * Assembles frozen section screens into one commercial report.
 * Does not modify or reimplement section internals.
 *
 * Order: Executive Summary → Four Pillars → Executive Insight → Metrics →
 * Explainable Analysis → Report Closing
 */
export function ConsultationReportScreen({
  data,
  className,
}: ConsultationReportScreenProps) {
  if (data.status !== "ready") {
    return (
      <ReportContainer className={cx(className)}>
        {data.status === "loading" ? (
          <LoadingState title="Loading consultation report" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No consultation report available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Consultation report unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load consultation report"
            description={data.errorMessage}
          />
        ) : null}
      </ReportContainer>
    );
  }

  const sectionMeta = Object.fromEntries(
    data.sections.map((section) => [section.id, section]),
  );

  const executiveSummaryMeta = sectionMeta["executive-summary"];
  const fourPillarsMeta = sectionMeta["four-pillars"];
  const executiveInsightMeta = sectionMeta["executive-insight"];
  const metricsMeta = sectionMeta["metrics"];
  const explainableMeta = sectionMeta["explainable-analysis"];

  return (
    <ConsultationReport data={data} className={className}>
      <ReportSection
        id={executiveSummaryMeta?.id ?? "executive-summary"}
        title={executiveSummaryMeta?.title ?? "Executive Summary"}
      >
        <ExecutiveSummaryScreen data={data.executiveSummary} />
      </ReportSection>
      <SectionTransition
        label={
          executiveSummaryMeta?.transitionLabel ?? "Continue to Four Pillars"
        }
        href={fourPillarsMeta?.href}
      />

      <ReportSection
        id={fourPillarsMeta?.id ?? "four-pillars"}
        title={fourPillarsMeta?.title ?? "Four Pillars"}
      >
        <FourPillarsScreen data={data.fourPillars} />
      </ReportSection>
      <SectionTransition
        label={
          fourPillarsMeta?.transitionLabel ?? "Continue to Executive Insight"
        }
        href={executiveInsightMeta?.href}
      />

      <ReportSection
        id={executiveInsightMeta?.id ?? "executive-insight"}
        title={executiveInsightMeta?.title ?? "Executive Insight"}
      >
        <ExecutiveInsightScreen data={data.executiveInsight} />
      </ReportSection>
      <SectionTransition
        label={executiveInsightMeta?.transitionLabel ?? "Continue to Metrics"}
        href={metricsMeta?.href}
      />

      <ReportSection
        id={metricsMeta?.id ?? "metrics"}
        title={metricsMeta?.title ?? "Metrics"}
      >
        <MetricsScreen data={data.metrics} />
      </ReportSection>
      <SectionTransition
        label={
          metricsMeta?.transitionLabel ?? "Continue to Explainable Analysis"
        }
        href={explainableMeta?.href}
      />

      <ReportSection
        id={explainableMeta?.id ?? "explainable-analysis"}
        title={explainableMeta?.title ?? "Explainable Analysis"}
      >
        <ExplainableAnalysisScreen data={data.explainableAnalysis} />
      </ReportSection>
    </ConsultationReport>
  );
}
