import { InformationBox, SectionHeader, SectionSurface } from "../shared";
import type { MetricExplanationViewModel } from "../../view_models/metrics";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type MetricExplanationProps = {
  data: MetricExplanationViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Narrative explanation for metrics — primary over charts. */
export function MetricExplanation({
  data,
  status = "ready",
  className,
}: MetricExplanationProps) {
  const title = data.title ?? "Metric Explanation";

  return (
    <section className={cx("cui-biz-metric-explanation", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading metric explanation",
          emptyTitle: "No metric explanation available",
          unavailableTitle: "Metric explanation unavailable",
          errorTitle: "Unable to load metric explanation",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {data.paragraphs.map((paragraph, index) => (
            <InformationBox key={`metric-explanation-${index}`}>
              {paragraph}
            </InformationBox>
          ))}
        </SectionSurface>,
      )}
    </section>
  );
}
