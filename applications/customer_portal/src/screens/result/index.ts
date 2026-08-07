/**
 * Result screen barrel — Sprint A architecture.
 */

export { ResultPageBody } from "./ResultPageBody";
export { ResultPageProvider, useResultPageViewModel } from "./ResultPageContext";
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
  groupItems,
  priorityFromIndex,
  sortByRecommendationPriority,
  truncatePrimaryList,
} from "./presentation/previewBuilder";
