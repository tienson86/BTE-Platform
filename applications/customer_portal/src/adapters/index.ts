/**
 * Adapters barrel (TASK_003A).
 */

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
