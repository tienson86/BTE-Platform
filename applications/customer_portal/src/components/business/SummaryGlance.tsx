import { MetricGroup, MetricRow, SectionHeader, SectionSurface } from "../shared";
import type {
  ExecutiveGlanceItemViewModel,
  PresentationStatus,
} from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type SummaryGlanceProps = {
  items: ExecutiveGlanceItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Glance metrics for Executive Summary. */
export function SummaryGlance({
  items,
  title = "At a Glance",
  status = "ready",
  className,
}: SummaryGlanceProps) {
  return (
    <section className={cx("cui-biz-glance", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading glance metrics",
          emptyTitle: "No glance metrics available",
          unavailableTitle: "Glance metrics unavailable",
          errorTitle: "Unable to load glance metrics",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          <MetricGroup stacked>
            {items.map((item) => (
              <MetricRow
                key={item.id}
                label={item.label}
                value={item.value}
                hint={item.hint}
              />
            ))}
          </MetricGroup>
        </SectionSurface>,
      )}
    </section>
  );
}
