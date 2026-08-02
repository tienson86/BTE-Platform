/**
 * Metrics presentation ViewModels — WP-0007.
 * Presentation-ready metric display only. No calculation.
 */

import type { PresentationStatus, PresentationTone } from "./executive_summary";

export type MetricConfidenceLevel = "low" | "medium" | "high";

export type MetricItemViewModel = {
  id: string;
  label: string;
  value: string;
  hint?: string;
  description?: string;
  tone?: PresentationTone;
  rangeLabel?: string;
};

export type MetricIndicatorViewModel = {
  id: string;
  label: string;
  value: string;
  statusLabel?: string;
  tone?: PresentationTone;
};

export type MetricSectionViewModel = {
  id: string;
  title: string;
  description?: string;
  metrics: MetricItemViewModel[];
};

export type MetricsSummaryViewModel = {
  title?: string;
  lead: string;
  items: MetricItemViewModel[];
};

export type MetricExplanationViewModel = {
  title?: string;
  paragraphs: string[];
};

export type BalancePanelViewModel = {
  title?: string;
  summary: string;
  indicators: MetricIndicatorViewModel[];
};

export type ConfidencePanelViewModel = {
  title?: string;
  level: MetricConfidenceLevel;
  summary?: string;
  items?: MetricIndicatorViewModel[];
};

export type MetricsTransitionViewModel = {
  label: string;
  href?: string;
};

export type MetricsHeroViewModel = {
  headline?: string;
  subtitle?: string;
};

export type MetricsReadyViewModel = {
  status: "ready";
  title?: string;
  hero?: MetricsHeroViewModel;
  summary: MetricsSummaryViewModel;
  explanation?: MetricExplanationViewModel;
  sections: MetricSectionViewModel[];
  balance: BalancePanelViewModel;
  confidence: ConfidencePanelViewModel;
  transition?: MetricsTransitionViewModel;
};

export type MetricsPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type MetricsErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type MetricsViewModel =
  | MetricsReadyViewModel
  | MetricsPendingViewModel
  | MetricsErrorViewModel;
