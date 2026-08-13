/**
 * ResultPage body — Product Polish V1 consulting reading order.
 * Zones retained (PACK_06 contracts); composition order prioritizes advice.
 */

import { useEffect, type ReactNode } from "react";
import {
  AnalysisZone,
  ContextZone,
  InterpretationZone,
  KnowledgeZone,
  RecommendationZone,
  SummaryZone,
  VisualizationZone,
} from "./zones";
import { scrollToResultZone, type ResultZoneId } from "./presentation/scrollToZone";
import { useResultPageViewModel } from "./ResultPageContext";

const HASH_TO_ZONE: Record<string, ResultZoneId> = {
  context: "context",
  "ngu-canh": "context",
  summary: "summary",
  "tom-tat": "summary",
  recommendation: "recommendation",
  analysis: "analysis",
  "bat-tu": "analysis",
  "phan-tich": "analysis",
  "tu-tru": "analysis",
  "ngu-hanh": "analysis",
  "than-vuong": "analysis",
  "thap-than": "analysis",
  interpretation: "interpretation",
  "luan-giai": "interpretation",
  visualization: "visualization",
  "bieu-do": "visualization",
  knowledge: "knowledge",
  "kien-thuc": "knowledge",
  "tri-thuc": "knowledge",
};

function syncHashToZone(): void {
  const raw = window.location.hash.replace(/^#/, "");
  if (!raw || raw === "xuat") return;
  const zone = HASH_TO_ZONE[raw];
  if (zone) scrollToResultZone(zone);
}

/**
 * Reading flow: Identity → Summary → Recommendation → Strength/Evidence → Details.
 */
export function ResultPageBody(): ReactNode {
  const model = useResultPageViewModel();

  useEffect(() => {
    syncHashToZone();
    window.addEventListener("hashchange", syncHashToZone);
    return () => window.removeEventListener("hashchange", syncHashToZone);
  }, []);

  return (
    <div
      className="rp-result-page"
      data-architecture="zone-row-grid-card"
      data-blueprint="pack07"
      data-presentation="pack04"
      data-sprint="product-polish-v1"
      data-visual="v2"
      data-experience="consulting"
      data-analysis-id={model.analysisId}
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
