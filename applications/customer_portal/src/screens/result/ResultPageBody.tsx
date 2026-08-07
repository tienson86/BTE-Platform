/**
 * ResultPage body — Zone architecture only (PACK_06 / PACK_07).
 * No direct card rendering. Architecture frozen (Sprint A).
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
 * Official Result Page composition — Zones → Rows → Grid → Cards.
 * Sprint A architecture frozen; Sprint B content; Sprint C quality.
 */
export function ResultPageBody(): ReactNode {
  return (
    <div
      className="rp-result-page"
      data-architecture="zone-row-grid-card"
      data-blueprint="pack07"
      data-presentation="pack04"
      data-sprint="D"
    >
      <ContextZone />
      <SummaryZone />
      <AnalysisZone />
      <VisualizationZone />
      <RecommendationZone />
      <InterpretationZone />
      <KnowledgeZone />
    </div>
  );
}
