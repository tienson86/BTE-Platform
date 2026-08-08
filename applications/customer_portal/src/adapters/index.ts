/**
 * Adapters barrel (TASK_003A).
 */

export {
  asNarrativeResult,
  hasUsableNarrativeResult,
} from "./narrativeResultAdapter";
export type {
  NarrativeResultDto,
  NarrativeResultSummaryDto,
  NarrativeSectionDto,
} from "./narrativeResultAdapter";

export {
  adaptAnalysisToBaZiResult,
  createBaZiResultGateViewModel,
} from "./baziResultAdapter";
export type { AdaptBaZiResultOptions, BaZiResultViewModel } from "./baziResultAdapter";

export { adaptDashboardViewModel } from "./dashboardAdapter";
export type { AdaptDashboardOptions, DashboardViewModel } from "./dashboardAdapter";

export {
  adaptAnalysisToCanonicalDesktop,
  createCanonicalDesktopGateViewModel,
  createCanonicalDesktopMockViewModel,
} from "./canonicalDesktopAdapter";
export type {
  AdaptCanonicalDesktopOptions,
  CanonicalDesktopStatus,
  CanonicalDesktopViewModel,
} from "./canonicalDesktopAdapter";

/** PACK_04 — UI Presentation Adapter (preview models + hasMore). */
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
  CARD_HEIGHT_PX,
  CARD_TYPE_BY_SECTION,
  LINE_CLAMP,
  OVERFLOW_BY_CARD_TYPE,
  PREVIEW_CHAR_LIMIT,
  PREVIEW_LIST_LIMIT,
  PRESENTATION_SPACE,
  PRESENTATION_SPACE_SEMANTIC,
  PRESENTATION_TYPE,
  cardHeightForSection,
  cardTypeForSection,
} from "../presentation";
export type {
  InterpretationPreviewModel,
  ReportSummaryPreviewModel,
  StrengthPreviewModel,
  LineClampField,
  OverflowStrategy,
  PresentationCardType,
  PresentationTypographyRole,
  PreviewBlock,
  PreviewList,
  PreviewText,
  ResultSectionId,
} from "../presentation";
