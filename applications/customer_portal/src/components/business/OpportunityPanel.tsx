import {
  HighlightBox,
  SectionHeader,
  SectionSurface,
  StatusBadge,
} from "../shared";
import type { InsightOpportunityViewModel } from "../../view_models/executive_insight";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type OpportunityPanelProps = {
  items: InsightOpportunityViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Opportunity summary panel — presentation only. */
export function OpportunityPanel({
  items,
  title = "Opportunities",
  status = "ready",
  className,
}: OpportunityPanelProps) {
  return (
    <section className={cx("cui-biz-opportunity-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading opportunities",
          emptyTitle: "No opportunities available",
          unavailableTitle: "Opportunities unavailable",
          errorTitle: "Unable to load opportunities",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {items.length === 0 ? (
            <HighlightBox title={title}>Unavailable</HighlightBox>
          ) : (
            items.map((item) => (
              <div key={item.id} className="cui-biz-opportunity-item">
                {item.priorityLabel ? (
                  <StatusBadge status="success">{item.priorityLabel}</StatusBadge>
                ) : null}
                <HighlightBox title={item.title}>{item.body}</HighlightBox>
              </div>
            ))
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
