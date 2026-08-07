/**
 * Sprint B zones — LP-005 / LP-006 / LP-007.
 * Architecture frozen: same ResultRow / Grid / Cell contracts as Sprint A.
 */

import type { ReactNode } from "react";
import {
  InterpretationCard,
  KnowledgeCard,
  RecommendationCard,
} from "../cards/ContentCards";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * RecommendationZone — Row 05 / LP-005 · Height L.
 */
export function RecommendationZone(): ReactNode {
  const { recommendations } = useResultPageViewModel();

  return (
    <ResultRow
      rowId="05"
      zone="recommendation"
      heightClass="L"
      pattern="LP-005"
      aria-label="Recommendation Zone"
      data-sprint="B"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <RecommendationCard model={recommendations} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}

/**
 * InterpretationZone — Row 06 / LP-006 · AUTO height · Preview/Expand/Collapse.
 */
export function InterpretationZone(): ReactNode {
  const { interpretation } = useResultPageViewModel();

  return (
    <ResultRow
      rowId="06"
      zone="interpretation"
      heightClass="AUTO"
      pattern="LP-006"
      aria-label="Interpretation Zone"
      data-sprint="B"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <InterpretationCard model={interpretation} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}

/**
 * KnowledgeZone — Row 07 / LP-007 · AUTO height · Accordion · after Interpretation.
 */
export function KnowledgeZone(): ReactNode {
  const { knowledge } = useResultPageViewModel();

  return (
    <ResultRow
      rowId="07"
      zone="knowledge"
      heightClass="AUTO"
      pattern="LP-007"
      aria-label="Knowledge Zone"
      data-sprint="B"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <KnowledgeCard model={knowledge} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
