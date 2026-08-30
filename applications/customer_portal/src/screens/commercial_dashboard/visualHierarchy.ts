/**
 * UI-14 visual hierarchy. Presentation attributes only. No new data.
 */

import type { DashboardCardId } from "./types";

export type VisualLevel = 1 | 2 | 3 | 4;
export type VisualCardType = "hero" | "analysis" | "reference" | "status";

export const VISUAL_HIERARCHY: Record<
  DashboardCardId,
  { readonly level: VisualLevel; readonly type: VisualCardType }
> = {
  overview: { level: 1, type: "hero" },
  interpretation: { level: 2, type: "analysis" },
  "action-plan": { level: 2, type: "analysis" },
  bazi: { level: 3, type: "analysis" },
  "five-elements": { level: 3, type: "analysis" },
  "ten-gods": { level: 3, type: "analysis" },
  pattern: { level: 3, type: "analysis" },
  luck: { level: 3, type: "analysis" },
  shensha: { level: 3, type: "analysis" },
};

/**
 * DOM attributes for Visual System V2 card types. Copy-only metadata.
 */
export function visualCardDom(id: DashboardCardId): {
  readonly "data-visual-level": string;
  readonly "data-card-type": VisualCardType;
} {
  const meta = VISUAL_HIERARCHY[id];
  return {
    "data-visual-level": String(meta.level),
    "data-card-type": meta.type,
  };
}
