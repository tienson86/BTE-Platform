/**
 * VisualizationZone — Priority 3 reference charts (after advice + evidence).
 */

import type { ReactNode } from "react";
import { LuckTimelineCard, RadarChartCard } from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Details beat — charts/tables as reference, not hero.
 */
export function VisualizationZone(): ReactNode {
  const model = useResultPageViewModel();
  const showRadar = model.radar.visible;
  const showTimeline = model.timeline.visible;

  if (!showRadar && !showTimeline) return null;

  return (
    <ResultRow
      rowId="06"
      zone="visualization"
      heightClass="AUTO"
      pattern="LP-004"
      aria-label="Visualization Zone"
      data-priority="3"
    >
      <ResultGrid>
        {showRadar ? (
          <ResultGridCell span={showTimeline ? 6 : 12}>
            <RadarChartCard model={model.radar} />
          </ResultGridCell>
        ) : null}
        {showTimeline ? (
          <ResultGridCell span={showRadar ? 6 : 12}>
            <LuckTimelineCard model={model.timeline} />
          </ResultGridCell>
        ) : null}
      </ResultGrid>
    </ResultRow>
  );
}
