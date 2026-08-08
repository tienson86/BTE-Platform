/**
 * Recommendation / Interpretation / Knowledge zones — Product Polish V1.
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
 * RecommendationZone — Primary actions (after Exec / Career).
 */
export function RecommendationZone(): ReactNode {
  const { recommendations } = useResultPageViewModel();
  if (!recommendations.visible || recommendations.items.length === 0) {
    return null;
  }

  return (
    <ResultRow
      rowId="04"
      zone="recommendation"
      heightClass="AUTO"
      pattern="LP-005"
      aria-label="Recommendation Zone"
      data-priority="1"
      data-sprint="product-polish-v1"
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
 * InterpretationZone — Evidence (Priority 2).
 */
export function InterpretationZone(): ReactNode {
  const { interpretation } = useResultPageViewModel();
  if (!interpretation.visible || interpretation.blocks.length === 0) {
    return null;
  }

  return (
    <ResultRow
      rowId="05"
      zone="interpretation"
      heightClass="AUTO"
      pattern="LP-006"
      aria-label="Interpretation Zone"
      data-priority="2"
      data-sprint="product-polish-v1"
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
 * KnowledgeZone — Reference (Priority 3).
 */
export function KnowledgeZone(): ReactNode {
  const { knowledge } = useResultPageViewModel();
  if (!knowledge.visible || knowledge.sections.length === 0) {
    return null;
  }

  return (
    <ResultRow
      rowId="07"
      zone="knowledge"
      heightClass="AUTO"
      pattern="LP-007"
      aria-label="Knowledge Zone"
      data-priority="3"
      data-sprint="product-polish-v1"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <KnowledgeCard model={knowledge} />
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
