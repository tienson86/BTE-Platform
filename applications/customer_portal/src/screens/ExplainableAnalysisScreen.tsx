import type { ReactNode } from "react";
import {
  EmptyState,
  ErrorState,
  FooterNote,
  LoadingState,
  ReadingProgress,
  SectionContainer,
  SectionDivider,
  SectionHeader,
  UnavailableState,
} from "../components/shared";
import type { ExplainableAnalysisViewModel } from "../view_models/explainable_analysis";
import { cx } from "../utils";
import {
  AnalysisSummary,
  ExplainableAnalysis,
} from "../components/business";

export type ExplainableAnalysisScreenProps = {
  data: ExplainableAnalysisViewModel;
  readingProgress?: number;
  className?: string;
  children?: ReactNode;
};

/**
 * Explainable Analysis Screen — Pack 03 / Pack 06 WP-0008.
 * Reading order is fixed and must not be reordered.
 *
 * Section Title → Summary → Analysis Blocks
 * (each block: Conclusion → Explanation → Evidence → Rule → Confidence → Knowledge → Recommendation)
 * → Transition
 */
export function ExplainableAnalysisScreen({
  data,
  readingProgress,
  className,
}: ExplainableAnalysisScreenProps) {
  if (data.status !== "ready") {
    return (
      <SectionContainer
        className={cx("cui-biz-explainable-analysis-screen", className)}
        aria-label="Explainable Analysis"
      >
        {data.status === "loading" ? (
          <LoadingState title="Loading explainable analysis" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No explainable analysis available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Explainable analysis unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load explainable analysis"
            description={data.errorMessage}
          />
        ) : null}
      </SectionContainer>
    );
  }

  const title = data.title ?? "Explainable Analysis";

  return (
    <SectionContainer
      width="reading"
      gap="section"
      className={cx("cui-biz-explainable-analysis-screen", className)}
      aria-label="Explainable Analysis"
    >
      {typeof readingProgress === "number" ? (
        <ReadingProgress value={readingProgress} />
      ) : null}

      {/* 1. Section Title */}
      <SectionHeader title={title} subtitle={data.subtitle} level={2} />
      <SectionDivider />

      {/* Optional overview */}
      {data.summary ? (
        <>
          <AnalysisSummary data={data.summary} />
          <SectionDivider />
        </>
      ) : null}

      {/* 2–N. Analysis blocks (explainability contract preserved inside) */}
      <ExplainableAnalysis blocks={data.blocks} title="Analysis Blocks" />

      {/* Transition */}
      {data.transition ? (
        <>
          <SectionDivider />
          <FooterNote className="cui-biz-explainable-transition">
            {data.transition.href ? (
              <a href={data.transition.href}>{data.transition.label}</a>
            ) : (
              data.transition.label
            )}
          </FooterNote>
        </>
      ) : null}
    </SectionContainer>
  );
}
