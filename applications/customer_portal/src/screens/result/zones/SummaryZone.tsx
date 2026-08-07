/**
 * SummaryZone — Row 02 / LP-001 (PACK_07 + Gallery Pattern 01).
 * Three equal cards · Height M · Preview only.
 */

import type { ReactNode } from "react";
import {
  CoreIndicatorsCard,
  DestinyDirectionCard,
  ExecutiveSummaryCard,
} from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Executive analytical summary — 4+4+4 equal height.
 */
export function SummaryZone(): ReactNode {
  const model = useResultPageViewModel();

  return (
    <ResultRow
      rowId="02"
      zone="summary"
      heightClass="M"
      pattern="LP-001"
      aria-label="Summary Zone"
    >
      <ResultGrid>
        <ResultGridCell span={4}>
          <ExecutiveSummaryCard model={model.executive} />
        </ResultGridCell>
        <ResultGridCell span={4}>
          <CoreIndicatorsCard model={model.indicators} />
        </ResultGridCell>
        <ResultGridCell span={4}>
          <DestinyDirectionCard model={model.destiny} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
