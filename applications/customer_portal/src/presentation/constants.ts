/**
 * PACK_04 — Shared UI presentation constants.
 * Single source of truth for heights, clamps, overflow, spacing, typography.
 */

import type {
  LineClampField,
  OverflowStrategy,
  PresentationCardType,
  PresentationTypographyRole,
  ResultSectionId,
} from "./types";

/** Official PACK_04 height classes (px). */
export const HEIGHT_CLASS_PX = {
  XS: 160,
  S: 220,
  M: 320,
  L: 420,
  XL: 560,
} as const;

/** Fixed card heights (px) — maps legacy card types onto official classes. */
export const CARD_HEIGHT_PX = {
  context: HEIGHT_CLASS_PX.S,
  module: HEIGHT_CLASS_PX.M,
  guidance: HEIGHT_CLASS_PX.M,
  chart: HEIGHT_CLASS_PX.XL,
  metric: HEIGHT_CLASS_PX.XL,
  summary: HEIGHT_CLASS_PX.M,
  list: HEIGHT_CLASS_PX.XL,
  preview: HEIGHT_CLASS_PX.XL,
} as const satisfies Record<PresentationCardType, number>;

/** Canonical Result section → card type. */
export const CARD_TYPE_BY_SECTION = {
  s00: "context",
  s01: "module",
  s02: "module",
  s03: "chart",
  s04: "metric",
  s05: "preview",
  s06: "list",
  s07: "list",
  s08: "preview",
  s09: "guidance",
  s10: "summary",
  s11: "preview",
} as const satisfies Record<ResultSectionId, PresentationCardType>;

/** Default overflow strategy by card type. */
export const OVERFLOW_BY_CARD_TYPE = {
  context: { title: "hidden", body: "hidden" },
  module: { title: "line-clamp", body: "line-clamp" },
  guidance: { title: "line-clamp", body: "line-clamp" },
  chart: { title: "line-clamp", body: "hidden" },
  metric: { title: "line-clamp", body: "hidden" },
  summary: { title: "line-clamp", body: "hidden" },
  list: { title: "line-clamp", body: "internal-scroll" },
  preview: { title: "line-clamp", body: "line-clamp" },
} as const satisfies Record<
  PresentationCardType,
  { readonly title: OverflowStrategy; readonly body: OverflowStrategy }
>;

/** Line-clamp limits by field role. */
export const LINE_CLAMP = {
  title: 2,
  subtitle: 1,
  summary: 2,
  description: 3,
  narrative: 3,
} as const satisfies Record<LineClampField, number>;

/** Soft character budgets for adapter truncation (complements line-clamp). */
export const PREVIEW_CHAR_LIMIT = {
  title: 72,
  subtitle: 48,
  summary: 120,
  description: 180,
  narrative: 220,
} as const satisfies Record<LineClampField, number>;

/** Max preview list items by card type. */
export const PREVIEW_LIST_LIMIT = {
  context: 0,
  module: 3,
  guidance: 5,
  chart: 4,
  metric: 5,
  summary: 3,
  list: 6,
  preview: 2,
} as const satisfies Record<PresentationCardType, number>;

/** 8pt spacing scale (px). */
export const PRESENTATION_SPACE = {
  0: 0,
  1: 4,
  2: 8,
  3: 12,
  4: 16,
  5: 24,
  6: 32,
  7: 48,
  8: 64,
} as const;

/** Semantic spacing aliases for PACK_04 surfaces. */
export const PRESENTATION_SPACE_SEMANTIC = {
  inline: PRESENTATION_SPACE[2],
  list: PRESENTATION_SPACE[2],
  paragraph: PRESENTATION_SPACE[3],
  cardPadding: PRESENTATION_SPACE[4],
  sectionGap: PRESENTATION_SPACE[5],
  chapterGap: PRESENTATION_SPACE[6],
} as const;

/** Typography scale for PACK_04 Result cards. */
export const PRESENTATION_TYPE = {
  title: { fontSize: "16px", fontWeight: 700, lineHeight: 1.3 },
  subtitle: { fontSize: "14px", fontWeight: 600, lineHeight: 1.3 },
  body: { fontSize: "14px", fontWeight: 400, lineHeight: 1.5 },
  summary: { fontSize: "13px", fontWeight: 400, lineHeight: 1.4 },
  caption: { fontSize: "12px", fontWeight: 500, lineHeight: 1.35 },
  metric: { fontSize: "24px", fontWeight: 700, lineHeight: 1.15 },
} as const satisfies Record<
  PresentationTypographyRole,
  { readonly fontSize: string; readonly fontWeight: number; readonly lineHeight: number }
>;

/** Resolve fixed height for a Result section. */
export function cardHeightForSection(section: ResultSectionId): number {
  return CARD_HEIGHT_PX[CARD_TYPE_BY_SECTION[section]];
}

/** Resolve card type for a Result section. */
export function cardTypeForSection(section: ResultSectionId): PresentationCardType {
  return CARD_TYPE_BY_SECTION[section];
}
