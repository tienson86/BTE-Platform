/**
 * ResultPage body — Product Polish V1 consulting reading order.
 * Zones retained (PACK_06 contracts); composition order prioritizes advice.
 */

import type { ReactNode } from "react";
import {
  AnalysisZone,
  ContextZone,
  InterpretationZone,
  KnowledgeZone,
  RecommendationZone,
  SummaryZone,
  VisualizationZone,
} from "./zones";

/**
 * Reading flow: Identity → Summary → Recommendation → Strength/Evidence → Details.
 */
export function ResultPageBody(): ReactNode {
  return (
    <div
      className="rp-result-page"
      data-architecture="zone-row-grid-card"
      data-blueprint="pack07"
      data-presentation="pack04"
      data-sprint="product-polish-v1"
      data-visual="v2"
      data-experience="consulting"
    >
      <ContextZone />
      <SummaryZone />
      <RecommendationZone />
      <AnalysisZone />
      <InterpretationZone />
      <VisualizationZone />
      <KnowledgeZone />
    </div>
  );
}
