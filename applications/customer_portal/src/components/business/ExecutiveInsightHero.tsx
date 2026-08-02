import { SectionHeader, SectionSurface, StatusBadge } from "../shared";
import type { ExecutiveInsightHeroViewModel } from "../../view_models/executive_insight";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ExecutiveInsightHeroProps = {
  data?: ExecutiveInsightHeroViewModel;
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Executive Insight header — presentation only. */
export function ExecutiveInsightHero({
  data,
  title = "Executive Insight",
  status = "ready",
  className,
}: ExecutiveInsightHeroProps) {
  const headline = data?.headline ?? title;

  return (
    <section className={cx("cui-biz-insight-hero", className)} aria-label={headline}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading executive insight",
          emptyTitle: "No executive insight available",
          unavailableTitle: "Executive insight unavailable",
          errorTitle: "Unable to load executive insight",
        },
        <SectionSurface gap="paragraph" variant="paper">
          <SectionHeader
            title={headline}
            subtitle={data?.subtitle}
            level={2}
            actions={<StatusBadge status="info">Insight</StatusBadge>}
          />
        </SectionSurface>,
      )}
    </section>
  );
}
