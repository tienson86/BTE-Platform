import { InformationBox, SectionHeader, SectionSurface } from "../shared";
import type { InsightSummaryViewModel } from "../../view_models/executive_insight";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type InsightSummaryProps = {
  data: InsightSummaryViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Overall insight summary narrative. */
export function InsightSummary({
  data,
  status = "ready",
  className,
}: InsightSummaryProps) {
  const title = data.title ?? "Insight Summary";

  return (
    <section className={cx("cui-biz-insight-summary", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading insight summary",
          emptyTitle: "No insight summary available",
          unavailableTitle: "Insight summary unavailable",
          errorTitle: "Unable to load insight summary",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {data.paragraphs.map((paragraph, index) => (
            <InformationBox key={`insight-summary-${index}`}>{paragraph}</InformationBox>
          ))}
        </SectionSurface>,
      )}
    </section>
  );
}
