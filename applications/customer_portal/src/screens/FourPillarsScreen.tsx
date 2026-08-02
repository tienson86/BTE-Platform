import type { ReactNode } from "react";
import {
  EmptyState,
  ErrorState,
  FooterNote,
  InformationBox,
  LoadingState,
  ReadingProgress,
  SectionContainer,
  SectionDivider,
  SectionHeader,
  UnavailableState,
} from "../components/shared";
import type { FourPillarsViewModel } from "../view_models/four_pillars";
import { cx } from "../utils";
import {
  ChartLegend,
  ChartMetadata,
  FourPillarsChart,
} from "../components/business";

export type FourPillarsScreenProps = {
  data: FourPillarsViewModel;
  readingProgress?: number;
  className?: string;
  children?: ReactNode;
};

/**
 * Four Pillars Screen — Pack 03 / Pack 06 WP-0005.
 * Reading order is fixed and must not be reordered.
 *
 * Section Title → Chart Overview → Four Pillars Grid → Metadata → Legend → Transition
 */
export function FourPillarsScreen({
  data,
  readingProgress,
  className,
}: FourPillarsScreenProps) {
  if (data.status !== "ready") {
    return (
      <SectionContainer
        className={cx("cui-biz-four-pillars", className)}
        aria-label="Four Pillars"
      >
        {data.status === "loading" ? (
          <LoadingState title="Loading four pillars" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="BaZi chart data is unavailable." />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Four pillars unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load four pillars"
            description={data.errorMessage}
          />
        ) : null}
      </SectionContainer>
    );
  }

  const title = data.title ?? "Four Pillars";

  return (
    <SectionContainer
      width="wide"
      gap="section"
      className={cx("cui-biz-four-pillars", className)}
      aria-label="Four Pillars"
    >
      {typeof readingProgress === "number" ? (
        <ReadingProgress value={readingProgress} />
      ) : null}

      {/* 1. Section Title */}
      <SectionHeader title={title} level={2} />
      <SectionDivider />

      {/* 2. Chart Overview */}
      {data.overview ? (
        <>
          <InformationBox title="Chart Overview">{data.overview}</InformationBox>
          <SectionDivider />
        </>
      ) : null}

      {/* 3–4. Four Pillars Grid (includes Hidden Stems / Na Yin / Life Stage per column) */}
      <FourPillarsChart pillars={data.pillars} />
      <SectionDivider />

      {/* 5. Metadata */}
      <ChartMetadata items={data.metadata} />
      <SectionDivider />

      {/* 6. Legend */}
      <ChartLegend items={data.legend} />

      {/* 7. Section Transition */}
      {data.transition ? (
        <>
          <SectionDivider />
          <FooterNote className="cui-biz-four-pillars-transition">
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
