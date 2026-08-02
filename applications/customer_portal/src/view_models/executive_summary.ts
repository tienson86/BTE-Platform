/**
 * Executive Summary presentation ViewModels — WP-0004.
 * Presentation-ready data only. No engine entities.
 */

export type PresentationStatus =
  | "loading"
  | "ready"
  | "empty"
  | "unavailable"
  | "error";

export type PresentationTone =
  | "neutral"
  | "accent"
  | "success"
  | "warning"
  | "danger"
  | "info";

export type ExecutiveIdentityViewModel = {
  dayMaster: string;
  dayMasterLabel?: string;
  chartTitle?: string;
  subtitle?: string;
};

export type ExecutiveVerdictViewModel = {
  label: string;
  summary?: string;
  tone?: PresentationTone;
};

export type ExecutiveRecommendationViewModel = {
  title: string;
  body: string;
  priorityLabel?: string;
};

export type ExecutiveGlanceItemViewModel = {
  id: string;
  label: string;
  value: string;
  hint?: string;
};

export type ExecutiveHighlightViewModel = {
  id: string;
  label: string;
  value: string;
  tone?: PresentationTone;
};

export type ExecutiveOverviewViewModel = {
  title?: string;
  paragraphs: string[];
};

export type ExecutiveTransitionViewModel = {
  label: string;
  href?: string;
};

export type ExecutiveHeroViewModel = {
  identity: ExecutiveIdentityViewModel;
  verdict: ExecutiveVerdictViewModel;
};

export type ExecutiveSummaryReadyViewModel = {
  status: "ready";
  hero: ExecutiveHeroViewModel;
  recommendation: ExecutiveRecommendationViewModel;
  overview: ExecutiveOverviewViewModel;
  glance: ExecutiveGlanceItemViewModel[];
  highlights: ExecutiveHighlightViewModel[];
  transition?: ExecutiveTransitionViewModel;
};

export type ExecutiveSummaryPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type ExecutiveSummaryErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type ExecutiveSummaryViewModel =
  | ExecutiveSummaryReadyViewModel
  | ExecutiveSummaryPendingViewModel
  | ExecutiveSummaryErrorViewModel;
