/**
 * SummaryZone — Row 02 consulting hero (Product Polish V1).
 * Executive Summary dominant · Career secondary · Indicators demoted (P3).
 */

import type { ReactNode } from "react";
import { DestinyDirectionCard, ExecutiveSummaryCard } from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * First-read consulting summary — Identity already shown; Exec + Career.
 */
export function SummaryZone(): ReactNode {
  const model = useResultPageViewModel();
  const showCareer = model.destiny.visible;

  return (
    <ResultRow
      rowId="02"
      zone="summary"
      heightClass="AUTO"
      pattern="LP-001"
      aria-label="Summary Zone"
      data-priority="1"
    >
      <ResultGrid>
        <ResultGridCell span={showCareer ? 8 : 12}>
          <ExecutiveSummaryCard model={model.executive} />
        </ResultGridCell>
        {showCareer ? (
          <ResultGridCell span={4}>
            <DestinyDirectionCard model={model.destiny} />
          </ResultGridCell>
        ) : null}
      </ResultGrid>
    </ResultRow>
  );
}
