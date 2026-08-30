/**
 * Mobile visual order. DOM source order stays DASHBOARD_CARDS.
 */

import type { DashboardCardId } from "../types";

export const MOBILE_VISUAL_ORDER: Record<DashboardCardId, number> = {
  overview: 1,
  "action-plan": 2,
  interpretation: 3,
  luck: 4,
  "five-elements": 5,
  pattern: 6,
  bazi: 7,
  "ten-gods": 8,
  shensha: 9,
};

export const MOBILE_EVIDENCE_CARDS: readonly DashboardCardId[] = [
  "five-elements",
  "pattern",
  "bazi",
  "ten-gods",
  "shensha",
];

/**
 * Data attributes for mobile visual priority. Desktop layout ignores these.
 */
export function mobileCardDom(id: DashboardCardId): {
  readonly "data-mobile-order": string;
  readonly "data-mobile-evidence"?: "true";
  readonly "data-mobile-expanded"?: "true";
  readonly "data-mobile-hero"?: "true";
} {
  const order = String(MOBILE_VISUAL_ORDER[id]);
  if (id === "overview") {
    return { "data-mobile-order": order, "data-mobile-hero": "true" };
  }
  if (id === "action-plan") {
    return { "data-mobile-order": order, "data-mobile-expanded": "true" };
  }
  if (MOBILE_EVIDENCE_CARDS.includes(id)) {
    return { "data-mobile-order": order, "data-mobile-evidence": "true" };
  }
  return { "data-mobile-order": order };
}
