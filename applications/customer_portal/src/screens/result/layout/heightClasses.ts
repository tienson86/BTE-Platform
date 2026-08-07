/**
 * PACK_04 / PACK_02 — Official height classes (px).
 * Result Page Blueprint maps rows to these classes.
 */

export const HEIGHT_CLASS_PX = {
  XS: 160,
  S: 220,
  M: 320,
  L: 420,
  XL: 560,
} as const;

export type HeightClass = keyof typeof HEIGHT_CLASS_PX;

/** Blueprint row → height class (PACK_07). */
export const RESULT_ROW_HEIGHT: Record<
  "context" | "summary" | "analysis" | "visualization" | "recommendation",
  HeightClass
> = {
  context: "S",
  summary: "M",
  analysis: "XL",
  visualization: "XL",
  recommendation: "L",
};
