/**
 * AnalysisZone — Strength first (P2), then supporting technical cards (P3).
 */

import type { ReactNode } from "react";
import {
  ChartDetailCard,
  CoreIndicatorsCard,
  FiveElementsCard,
  ShenShaCard,
  StrengthAnalysisCard,
  TenGodsAnalysisCard,
} from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Understanding beat — strength before technical apparatus.
 */
export function AnalysisZone(): ReactNode {
  const model = useResultPageViewModel();
  const cards: ReactNode[] = [];

  if (model.strength.visible) {
    cards.push(
      <ResultGridCell key="strength" span={4}>
        <StrengthAnalysisCard model={model.strength} />
      </ResultGridCell>,
    );
  }
  if (model.fiveElements.visible) {
    cards.push(
      <ResultGridCell key="five-elements" span={4}>
        <FiveElementsCard model={model.fiveElements} />
      </ResultGridCell>,
    );
  }
  if (model.tenGods.visible) {
    cards.push(
      <ResultGridCell key="ten-gods" span={4}>
        <TenGodsAnalysisCard model={model.tenGods} />
      </ResultGridCell>,
    );
  }
  if (model.indicators.visible) {
    cards.push(
      <ResultGridCell key="indicators" span={12}>
        <CoreIndicatorsCard model={model.indicators} />
      </ResultGridCell>,
    );
  }
  if (model.chart.visible) {
    cards.push(
      <ResultGridCell key="chart" span={12}>
        <ChartDetailCard model={model.chart} />
      </ResultGridCell>,
    );
  }
  if (model.shenSha.visible) {
    cards.push(
      <ResultGridCell key="shensha" span={12}>
        <ShenShaCard model={model.shenSha} />
      </ResultGridCell>,
    );
  }

  if (cards.length === 0) return null;

  return (
    <ResultRow
      rowId="03"
      zone="analysis"
      heightClass="AUTO"
      pattern="LP-003"
      aria-label="Analysis Zone"
      data-priority="2"
    >
      <ResultGrid>{cards}</ResultGrid>
    </ResultRow>
  );
}
