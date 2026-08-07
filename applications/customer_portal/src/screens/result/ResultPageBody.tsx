/**
 * ResultPage body — Zone architecture only (PACK_06 / PACK_07).
 * No direct card rendering. Sprint A: Phases 01–04.
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
 */
export function ResultPageBody(): ReactNode {
  return (
    <div
      className="rp-result-page"
      data-architecture="zone-row-grid-card"
      data-blueprint="pack07"
      data-presentation="pack04"
      data-sprint="A"
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
