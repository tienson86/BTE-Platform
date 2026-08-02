import { InformationBox, SectionHeader, SectionSurface } from "../shared";
import type { AppendixSummaryViewModel } from "../../view_models/appendix";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type AppendixSummaryProps = {
  data: AppendixSummaryViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Appendix overview — presentation narrative only. */
export function AppendixSummary({
  data,
  status = "ready",
  className,
}: AppendixSummaryProps) {
  const title = data.title ?? "Appendix Summary";

  return (
    <section className={cx("cui-biz-appendix-summary", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading appendix summary",
          emptyTitle: "No appendix summary available",
          unavailableTitle: "Appendix summary unavailable",
          errorTitle: "Unable to load appendix summary",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {data.paragraphs.map((paragraph, index) => (
            <InformationBox key={`appendix-summary-${index}`}>{paragraph}</InformationBox>
          ))}
        </SectionSurface>,
      )}
    </section>
  );
}
