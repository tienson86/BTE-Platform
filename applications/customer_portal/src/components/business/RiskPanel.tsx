import {
  HighlightBox,
  SectionHeader,
  SectionSurface,
  StatusBadge,
  WarningBox,
} from "../shared";
import type { InsightRiskViewModel } from "../../view_models/executive_insight";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type RiskPanelProps = {
  items: InsightRiskViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Risk summary panel — presentation only. */
export function RiskPanel({
  items,
  title = "Risks",
  status = "ready",
  className,
}: RiskPanelProps) {
  return (
    <section className={cx("cui-biz-risk-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading risks",
          emptyTitle: "No risks available",
          unavailableTitle: "Risks unavailable",
          errorTitle: "Unable to load risks",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {items.length === 0 ? (
            <HighlightBox title={title}>Unavailable</HighlightBox>
          ) : (
            items.map((item) => (
              <div key={item.id} className="cui-biz-risk-item">
                {item.priorityLabel ? (
                  <StatusBadge status="warning">{item.priorityLabel}</StatusBadge>
                ) : null}
                <WarningBox title={item.title}>{item.body}</WarningBox>
              </div>
            ))
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
