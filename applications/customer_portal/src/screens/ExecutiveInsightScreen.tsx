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
import type { ExecutiveInsightViewModel } from "../view_models/executive_insight";
import { cx } from "../utils";
import {
  ExecutiveConclusion,
  ExecutiveInsightHero,
  InsightSection,
  InsightSummary,
  OpportunityPanel,
  RecommendationPanel,
  RiskPanel,
} from "../components/business";

export type ExecutiveInsightScreenProps = {
  data: ExecutiveInsightViewModel;
  readingProgress?: number;
  className?: string;
  children?: ReactNode;
};

/**
 * Executive Insight Screen — Pack 03 / Pack 06 WP-0006.
 * Reading order is fixed and must not be reordered.
 *
 * Section Title → Executive Conclusion → Key Insights → Opportunity → Risk → Recommendations → Transition
 */
export function ExecutiveInsightScreen({
  data,
  readingProgress,
  className,
}: ExecutiveInsightScreenProps) {
  if (data.status !== "ready") {
    return (
      <SectionContainer
        className={cx("cui-biz-executive-insight", className)}
        aria-label="Executive Insight"
      >
        {data.status === "loading" ? (
          <LoadingState title="Loading executive insight" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No executive insight available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Executive insight unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load executive insight"
            description={data.errorMessage}
          />
        ) : null}
      </SectionContainer>
    );
  }

  const title = data.title ?? "Executive Insight";

  return (
    <SectionContainer
      width="reading"
      gap="section"
      className={cx("cui-biz-executive-insight", className)}
      aria-label="Executive Insight"
    >
      {typeof readingProgress === "number" ? (
        <ReadingProgress value={readingProgress} />
      ) : null}

      {/* 1. Section Title / Header */}
      <ExecutiveInsightHero data={data.hero} title={title} />
      <SectionDivider />

      {/* 2. Executive Conclusion */}
      <ExecutiveConclusion data={data.conclusion} />
      <SectionDivider />

      {/* Optional overall summary */}
      {data.summary ? (
        <>
          <InsightSummary data={data.summary} />
          <SectionDivider />
        </>
      ) : null}

      {/* 3. Key Insights */}
      <div className="cui-biz-key-insights" aria-label="Key Insights">
        {data.insights.map((insight) => (
          <InsightSection key={insight.id} data={insight} />
        ))}
      </div>
      <SectionDivider />

      {/* 4. Opportunity */}
      <OpportunityPanel items={data.opportunities} />
      <SectionDivider />

      {/* 5. Risk */}
      <RiskPanel items={data.risks} />
      <SectionDivider />

      {/* 6. Recommendations — reuse frozen RecommendationPanel */}
      <RecommendationPanel data={data.recommendation} />

      {/* 7. Section Transition */}
      {data.transition ? (
        <>
          <SectionDivider />
          <FooterNote className="cui-biz-insight-transition">
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
