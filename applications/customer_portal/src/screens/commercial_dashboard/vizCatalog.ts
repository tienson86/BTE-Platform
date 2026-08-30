/**
 * UI-15 visualization kinds. Presentation chrome only. No new data.
 */

import type { DashboardCardId } from "./types";

export type VisualizationKind =
  | "balance-bars"
  | "timeline"
  | "formation-flow"
  | "structure"
  | "relationship"
  | "grouped-chips";

export const VISUALIZATIONS: Partial<Record<DashboardCardId, VisualizationKind>> = {
  "five-elements": "balance-bars",
  luck: "timeline",
  pattern: "formation-flow",
  bazi: "structure",
  "ten-gods": "relationship",
  shensha: "grouped-chips",
};

/**
 * DOM attribute for the approved visualization kind.
 */
export function vizDom(id: DashboardCardId): { readonly "data-viz": VisualizationKind } | Record<string, never> {
  const kind = VISUALIZATIONS[id];
  if (!kind) return {};
  return { "data-viz": kind };
}
