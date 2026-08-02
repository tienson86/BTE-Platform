import type { ReactNode } from "react";
import {
  EmptyState,
  ErrorState,
  FooterNote,
  LoadingState,
  ReadingProgress,
  SectionContainer,
  SectionDivider,
  UnavailableState,
} from "../components/shared";
import type { ExecutiveSummaryViewModel } from "../view_models/executive_summary";
import { cx } from "../utils";
import {
  ExecutiveHero,
  ExecutiveHighlights,
  ExecutiveOverview,
  RecommendationPanel,
  SummaryGlance,
} from "../components/business";

export type ExecutiveSummaryScreenProps = {
  data: ExecutiveSummaryViewModel;
  heroActions?: ReactNode;
  readingProgress?: number;
  className?: string;
};

/**
 * Executive Summary Screen — Pack 03 / Pack 06 WP-0004.
 * Reading order is fixed and must not be reordered.
 *
 * Hero → Primary Recommendation → Verdict/Overview → Glance → Highlights → Transition
 */
export function ExecutiveSummaryScreen({
  data,
  heroActions,
  readingProgress,
  className,
}: ExecutiveSummaryScreenProps) {
  if (data.status !== "ready") {
    return (
      <SectionContainer
        className={cx("cui-biz-executive-summary", className)}
        aria-label="Executive Summary"
      >
        {data.status === "loading" ? (
          <LoadingState title="Loading executive summary" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No executive summary available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Executive summary unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load executive summary"
            description={data.errorMessage}
          />
        ) : null}
      </SectionContainer>
    );
  }

  return (
    <SectionContainer
      width="reading"
      gap="section"
      className={cx("cui-biz-executive-summary", className)}
      aria-label="Executive Summary"
    >
      {typeof readingProgress === "number" ? (
        <ReadingProgress value={readingProgress} />
      ) : null}

      {/* 1. Hero */}
      <ExecutiveHero data={data.hero} actions={heroActions} />
      <SectionDivider />

      {/* 2. Primary Recommendation */}
      <RecommendationPanel data={data.recommendation} />
      <SectionDivider />

      {/* 3–4. Executive Verdict + Executive Summary */}
      <ExecutiveOverview overview={data.overview} verdict={data.hero.verdict} />
      <SectionDivider />

      {/* 5. Glance Information */}
      <SummaryGlance items={data.glance} />
      <SectionDivider />

      {/* 6. Quick Highlights */}
      <ExecutiveHighlights items={data.highlights} />

      {/* 7. Section Transition */}
      {data.transition ? (
        <>
          <SectionDivider />
          <FooterNote className="cui-biz-transition">
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
