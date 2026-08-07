/**
 * PACK_04 — Presentation layer barrel.
 */

export {
  CARD_HEIGHT_PX,
  CARD_TYPE_BY_SECTION,
  HEIGHT_CLASS_PX,
  LINE_CLAMP,
  OVERFLOW_BY_CARD_TYPE,
  PREVIEW_CHAR_LIMIT,
  PREVIEW_LIST_LIMIT,
  PRESENTATION_SPACE,
  PRESENTATION_SPACE_SEMANTIC,
  PRESENTATION_TYPE,
  cardHeightForSection,
  cardTypeForSection,
} from "./constants";

export {
  adaptInterpretationPreview,
  adaptPreviewBlock,
  adaptPreviewList,
  adaptPreviewListForCardType,
  adaptPreviewText,
  adaptReportSummaryPreview,
  adaptStrengthPreview,
  resolveSectionCardType,
  truncateText,
} from "./presentationAdapter";
export type {
  InterpretationPreviewModel,
  ReportSummaryPreviewModel,
  StrengthPreviewModel,
} from "./presentationAdapter";

export type {
  LineClampField,
  OverflowStrategy,
  PresentationCardType,
  PresentationTypographyRole,
  PreviewBlock,
  PreviewList,
  PreviewText,
  ResultSectionId,
} from "./types";
