/**
 * Result screen barrel — Sprint A architecture (frozen) + Sprint C quality.
 */

export { ResultPageBody } from "./ResultPageBody";
export { ResultExportBar } from "./ResultExportBar";
export { ResultPageProvider, useResultPageViewModel } from "./ResultPageContext";
export { ResultPageStatusGate } from "./ResultPageStatusGate";
export type { ResultPageStatusGateProps } from "./ResultPageStatusGate";
export { adaptResultPageViewModel } from "./adapters/resultPresentationAdapter";
export type { ResultPageViewModel } from "./viewModels";
export * from "./zones";
export * from "./layout";
export * from "./cards";
export {
  MAX_PRIMARY_RECOMMENDATIONS,
  RECOMMENDATION_PRIORITY_LABEL,
  RECOMMENDATION_PRIORITY_ORDER,
  bindPlaceholder,
  formatPreviewField,
  priorityFromIndex,
  sortByRecommendationPriority,
  truncatePrimaryList,
} from "./presentation/previewBuilder";
