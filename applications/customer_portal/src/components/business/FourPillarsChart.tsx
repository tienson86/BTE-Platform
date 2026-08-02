import { PropertyGrid, SectionHeader, SectionSurface } from "../shared";
import type { PillarViewModel } from "../../view_models/four_pillars";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { PillarColumn } from "./PillarColumn";
import { renderPresentationGate } from "./presentationGate";

export type FourPillarsChartProps = {
  pillars: PillarViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Four Pillars chart grid — equal visual weight, subtle Day emphasis. */
export function FourPillarsChart({
  pillars,
  title = "Four Pillars Chart",
  status = "ready",
  className,
}: FourPillarsChartProps) {
  return (
    <section className={cx("cui-biz-four-pillars-chart", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading four pillars chart",
          emptyTitle: "BaZi chart data is unavailable.",
          unavailableTitle: "Four pillars chart unavailable",
          errorTitle: "Unable to load four pillars chart",
        },
        <SectionSurface gap="block" variant="paper">
          <SectionHeader title={title} level={2} />
          <PropertyGrid columns={4} className="cui-biz-four-pillars-chart__grid">
            {pillars.map((pillar) => (
              <PillarColumn key={pillar.kind} data={pillar} />
            ))}
          </PropertyGrid>
        </SectionSurface>,
      )}
    </section>
  );
}
