import {
  InformationBox,
  LabelValueRow,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { ChartLegendItemViewModel } from "../../view_models/four_pillars";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ChartLegendProps = {
  items: ChartLegendItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Chart legend explaining structural labels. */
export function ChartLegend({
  items,
  title = "Chart Legend",
  status = "ready",
  className,
}: ChartLegendProps) {
  return (
    <section className={cx("cui-biz-chart-legend", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading chart legend",
          emptyTitle: "No legend available",
          unavailableTitle: "Chart legend unavailable",
          errorTitle: "Unable to load chart legend",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {items.length === 0 ? (
            <InformationBox>No legend entries.</InformationBox>
          ) : (
            items.map((item) => (
              <LabelValueRow
                key={item.id}
                label={item.label}
                value={item.description}
              />
            ))
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
