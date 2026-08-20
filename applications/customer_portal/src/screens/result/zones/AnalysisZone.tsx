/**
 * AnalysisZone — primary analytical facts, then supporting cards.
 */

import type { ReactNode } from "react";
import {
  ChartDetailCard,
  ClimateSnapshotCard,
  CoreIndicatorsCard,
  FiveElementsCard,
  PatternSnapshotCard,
  ShenShaCard,
  StrengthAnalysisCard,
  TenGodsAnalysisCard,
} from "../cards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Primary: pillars, strength, pattern, useful god, điều hậu.
 * Secondary: five elements, ten gods, shensha.
 */
export function AnalysisZone(): ReactNode {
  const model = useResultPageViewModel();
  const primary: ReactNode[] = [];
  const secondary: ReactNode[] = [];

  if (model.chart.visible) {
    primary.push(
      <ResultGridCell key="chart" span={12}>
        <ChartDetailCard model={model.chart} />
      </ResultGridCell>,
    );
  }
  if (model.strength.visible) {
    primary.push(
      <ResultGridCell key="strength" span={model.pattern.visible ? 6 : 12}>
        <StrengthAnalysisCard model={model.strength} />
      </ResultGridCell>,
    );
  }
  if (model.pattern.visible) {
    primary.push(
      <ResultGridCell key="pattern" span={model.strength.visible ? 6 : 12}>
        <PatternSnapshotCard model={model.pattern} />
      </ResultGridCell>,
    );
  }
  if (model.indicators.visible) {
    primary.push(
      <ResultGridCell key="indicators" span={12}>
        <CoreIndicatorsCard model={model.indicators} />
      </ResultGridCell>,
    );
  }
  if (model.climate.visible) {
    primary.push(
      <ResultGridCell key="climate" span={12}>
        <ClimateSnapshotCard model={model.climate} />
      </ResultGridCell>,
    );
  }
  if (model.fiveElements.visible) {
    secondary.push(
      <ResultGridCell key="five-elements" span={6}>
        <FiveElementsCard model={model.fiveElements} />
      </ResultGridCell>,
    );
  }
  if (model.tenGods.visible) {
    secondary.push(
      <ResultGridCell key="ten-gods" span={6}>
        <TenGodsAnalysisCard model={model.tenGods} />
      </ResultGridCell>,
    );
  }
  if (model.shenSha.visible) {
    secondary.push(
      <ResultGridCell key="shensha" span={12}>
        <ShenShaCard model={model.shenSha} />
      </ResultGridCell>,
    );
  }

  const cards = [...primary, ...secondary];
  if (cards.length === 0) return null;

  return (
    <ResultRow
      rowId="03"
      zone="analysis"
      heightClass="AUTO"
      pattern="LP-003"
      aria-label="Analysis Zone"
      data-priority="1"
    >
      <ResultGrid>{cards}</ResultGrid>
    </ResultRow>
  );
}
