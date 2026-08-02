import {
  HighlightBox,
  MetricGroup,
  SectionHeader,
  SectionSurface,
  StatusBadge,
} from "../shared";
import type {
  ExecutiveHighlightViewModel,
  PresentationStatus,
} from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ExecutiveHighlightsProps = {
  items: ExecutiveHighlightViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Quick highlights (strength, opportunity, risk, etc.). */
export function ExecutiveHighlights({
  items,
  title = "Quick Highlights",
  status = "ready",
  className,
}: ExecutiveHighlightsProps) {
  return (
    <section className={cx("cui-biz-highlights", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading highlights",
          emptyTitle: "No highlights available",
          unavailableTitle: "Highlights unavailable",
          errorTitle: "Unable to load highlights",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          <MetricGroup columns={2}>
            {items.map((item) => (
              <div key={item.id} className="cui-biz-highlight-item">
                <StatusBadge status={item.tone ?? "neutral"}>{item.label}</StatusBadge>
                <HighlightBox title={item.label}>{item.value}</HighlightBox>
              </div>
            ))}
          </MetricGroup>
        </SectionSurface>,
      )}
    </section>
  );
}
