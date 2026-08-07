/**
 * VisualizationZone — Row 04 / LP-004 (Gallery Pattern 04).
 * Radar + Timeline · 50/50 · Height XL · Fixed · Text summary required.
 */

import type { ReactNode } from "react";
import { LuckTimelineCard, RadarChartCard } from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Visualization support — 6+6 equal height, no resize.
 */
export function VisualizationZone(): ReactNode {
  const model = useResultPageViewModel();

  return (
    <ResultRow
      rowId="04"
      zone="visualization"
      heightClass="XL"
      pattern="LP-004"
      aria-label="Visualization Zone"
    >
      <ResultGrid>
        <ResultGridCell span={6}>
          <RadarChartCard model={model.radar} />
        </ResultGridCell>
        <ResultGridCell span={6}>
          <LuckTimelineCard model={model.timeline} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
