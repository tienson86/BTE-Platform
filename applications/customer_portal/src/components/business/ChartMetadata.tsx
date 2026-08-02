import {
  PropertyGrid,
  PropertyItem,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { ChartMetadataItemViewModel } from "../../view_models/four_pillars";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ChartMetadataProps = {
  items: ChartMetadataItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Chart metadata block — separated from the pillar grid. */
export function ChartMetadata({
  items,
  title = "Chart Metadata",
  status = "ready",
  className,
}: ChartMetadataProps) {
  return (
    <section className={cx("cui-biz-chart-metadata", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading chart metadata",
          emptyTitle: "No chart metadata available",
          unavailableTitle: "Chart metadata unavailable",
          errorTitle: "Unable to load chart metadata",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {items.length === 0 ? (
            <PropertyItem label="Metadata" value="Unavailable" />
          ) : (
            <PropertyGrid columns={2}>
              {items.map((item) => (
                <PropertyItem key={item.id} label={item.label} value={item.value} />
              ))}
            </PropertyGrid>
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
