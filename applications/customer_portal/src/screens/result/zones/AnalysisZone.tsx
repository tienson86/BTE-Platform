/**
 * AnalysisZone — Row 03 / LP-003 (Gallery Pattern 03 Triple Analysis).
 * Three equal cards · Height XL · Equal width · No dynamic height.
 */

import type { ReactNode } from "react";
import {
  FiveElementsCard,
  StrengthAnalysisCard,
  TenGodsAnalysisCard,
} from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Core analysis evidence — 4+4+4 equal height.
 */
export function AnalysisZone(): ReactNode {
  const model = useResultPageViewModel();

  return (
    <ResultRow
      rowId="03"
      zone="analysis"
      heightClass="XL"
      pattern="LP-003"
      aria-label="Analysis Zone"
    >
      <ResultGrid>
        <ResultGridCell span={4}>
          <FiveElementsCard model={model.fiveElements} />
        </ResultGridCell>
        <ResultGridCell span={4}>
          <StrengthAnalysisCard model={model.strength} />
        </ResultGridCell>
        <ResultGridCell span={4}>
          <TenGodsAnalysisCard model={model.tenGods} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
