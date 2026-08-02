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
import type { MetricsViewModel } from "../view_models/metrics";
import { cx } from "../utils";
import {
  BalancePanel,
  ConfidencePanel,
  MetricExplanation,
  MetricSection,
  MetricsSummary,
} from "../components/business";

export type MetricsScreenProps = {
  data: MetricsViewModel;
  readingProgress?: number;
  className?: string;
  children?: ReactNode;
};

/**
 * Metrics Screen — Pack 03 / Pack 06 WP-0007.
 * Reading order is fixed and must not be reordered.
 *
 * Section Title → Executive Metrics Summary → Metric Explanation →
 * Supporting Indicators → Confidence → Transition
 */
export function MetricsScreen({
  data,
  readingProgress,
  className,
}: MetricsScreenProps) {
  if (data.status !== "ready") {
    return (
      <SectionContainer
        className={cx("cui-biz-metrics", className)}
        aria-label="Metrics"
      >
        {data.status === "loading" ? (
          <LoadingState title="Loading metrics" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No metrics available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Metrics unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load metrics"
            description={data.errorMessage}
          />
        ) : null}
      </SectionContainer>
    );
  }

  const title = data.title ?? data.hero?.headline ?? "Metrics";

  return (
    <SectionContainer
      width="reading"
      gap="section"
      className={cx("cui-biz-metrics", className)}
      aria-label="Metrics"
    >
      {typeof readingProgress === "number" ? (
        <ReadingProgress value={readingProgress} />
      ) : null}

      {/* 1. Section Title */}
      <SectionHeader
        title={title}
        subtitle={data.hero?.subtitle}
        level={2}
      />
      <SectionDivider />

      {/* 2. Executive Metrics Summary */}
      <MetricsSummary data={data.summary} />
      <SectionDivider />

      {/* 3. Metric Explanation */}
      {data.explanation ? (
        <>
          <MetricExplanation data={data.explanation} />
          <SectionDivider />
        </>
      ) : null}

      {/* 4. Supporting Indicators (Strength / Five Elements / Ten Gods / Balance) */}
      <div className="cui-biz-metrics-indicators" aria-label="Supporting Indicators">
        {data.sections.map((section) => (
          <MetricSection key={section.id} data={section} />
        ))}
        <BalancePanel data={data.balance} />
      </div>
      <SectionDivider />

      {/* 5. Confidence */}
      <ConfidencePanel data={data.confidence} />

      {/* 6. Section Transition */}
      {data.transition ? (
        <>
          <SectionDivider />
          <FooterNote className="cui-biz-metrics-transition">
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
