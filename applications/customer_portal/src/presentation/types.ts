/**
 * PACK_04 — UI Presentation types.
 * Preview models only; no business logic.
 */

/** Fixed-height card categories for Result surfaces. */
export type PresentationCardType =
  | "context"
  | "module"
  | "guidance"
  | "chart"
  | "metric"
  | "summary"
  | "list"
  | "preview";

/** Overflow strategy applied to a presentation slot. */
export type OverflowStrategy = "hidden" | "line-clamp" | "internal-scroll";

/** Typography roles allowed on PACK_04 surfaces. */
export type PresentationTypographyRole =
  | "title"
  | "subtitle"
  | "body"
  | "summary"
  | "caption"
  | "metric";

/** Line-clamp field roles. */
export type LineClampField =
  | "title"
  | "subtitle"
  | "summary"
  | "description"
  | "narrative";

/** Truncated text preview produced by the Presentation Adapter. */
export type PreviewText = {
  readonly text: string;
  readonly fullText: string;
  readonly hasMore: boolean;
  readonly lineClamp: number;
};

/** Truncated list preview produced by the Presentation Adapter. */
export type PreviewList<T> = {
  readonly items: readonly T[];
  readonly totalCount: number;
  readonly hasMore: boolean;
  readonly maxItems: number;
};

/** Generic preview block for narrative sections. */
export type PreviewBlock = {
  readonly title: PreviewText;
  readonly body: PreviewText;
  readonly hasMore: boolean;
};

/** Section keys on Canonical Desktop Result. */
export type ResultSectionId =
  | "s00"
  | "s01"
  | "s02"
  | "s03"
  | "s04"
  | "s05"
  | "s06"
  | "s07"
  | "s08"
  | "s09"
  | "s10"
  | "s11";
