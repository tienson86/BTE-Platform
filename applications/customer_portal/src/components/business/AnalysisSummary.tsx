import { InformationBox, SectionHeader, SectionSurface } from "../shared";
import type { AnalysisSummaryViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type AnalysisSummaryProps = {
  data: AnalysisSummaryViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Explainable analysis summary narrative. */
export function AnalysisSummary({
  data,
  status = "ready",
  className,
}: AnalysisSummaryProps) {
  const title = data.title ?? "Analysis Summary";

  return (
    <section className={cx("cui-biz-analysis-summary", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading analysis summary",
          emptyTitle: "No analysis summary available",
          unavailableTitle: "Analysis summary unavailable",
          errorTitle: "Unable to load analysis summary",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {data.paragraphs.map((paragraph, index) => (
            <InformationBox key={`analysis-summary-${index}`}>{paragraph}</InformationBox>
          ))}
        </SectionSurface>,
      )}
    </section>
  );
}
