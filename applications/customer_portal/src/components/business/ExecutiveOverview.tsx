import { InformationBox, SectionHeader, SectionSurface } from "../shared";
import type {
  ExecutiveOverviewViewModel,
  ExecutiveVerdictViewModel,
  PresentationStatus,
} from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ExecutiveOverviewProps = {
  overview: ExecutiveOverviewViewModel;
  verdict?: ExecutiveVerdictViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Executive summary narrative / verdict overview. */
export function ExecutiveOverview({
  overview,
  verdict,
  status = "ready",
  className,
}: ExecutiveOverviewProps) {
  const title = overview.title ?? "Executive Summary";

  return (
    <section className={cx("cui-biz-overview", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading overview",
          emptyTitle: "No overview available",
          unavailableTitle: "Overview unavailable",
          errorTitle: "Unable to load overview",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {verdict?.summary ? (
            <InformationBox title={verdict.label}>{verdict.summary}</InformationBox>
          ) : null}
          {overview.paragraphs.map((paragraph, index) => (
            <InformationBox key={`overview-${index}`}>{paragraph}</InformationBox>
          ))}
        </SectionSurface>,
      )}
    </section>
  );
}
