/**
 * Executive Insight presentation ViewModels — WP-0006.
 * Presentation-ready analysis display only. No engine entities.
 */

import type { PresentationStatus, PresentationTone } from "./executive_summary";

export type InsightConfidenceLevel = "low" | "medium" | "high";

export type InsightEvidenceViewModel = {
  id: string;
  label: string;
  detail?: string;
  meta?: string;
};

export type InsightSectionViewModel = {
  id: string;
  title: string;
  summary: string;
  body?: string;
  confidence?: InsightConfidenceLevel;
  priorityLabel?: string;
  tone?: PresentationTone;
  evidence?: InsightEvidenceViewModel[];
};

export type InsightOpportunityViewModel = {
  id: string;
  title: string;
  body: string;
  priorityLabel?: string;
};

export type InsightRiskViewModel = {
  id: string;
  title: string;
  body: string;
  priorityLabel?: string;
};

export type ExecutiveConclusionViewModel = {
  title: string;
  body: string;
  confidence?: InsightConfidenceLevel;
};

export type InsightSummaryViewModel = {
  title?: string;
  paragraphs: string[];
};

export type ExecutiveInsightHeroViewModel = {
  headline?: string;
  subtitle?: string;
};

export type ExecutiveInsightRecommendationViewModel = {
  title: string;
  body: string;
  priorityLabel?: string;
};

export type ExecutiveInsightTransitionViewModel = {
  label: string;
  href?: string;
};

export type ExecutiveInsightReadyViewModel = {
  status: "ready";
  title?: string;
  hero?: ExecutiveInsightHeroViewModel;
  conclusion: ExecutiveConclusionViewModel;
  summary?: InsightSummaryViewModel;
  insights: InsightSectionViewModel[];
  opportunities: InsightOpportunityViewModel[];
  risks: InsightRiskViewModel[];
  recommendation: ExecutiveInsightRecommendationViewModel;
  transition?: ExecutiveInsightTransitionViewModel;
};

export type ExecutiveInsightPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type ExecutiveInsightErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type ExecutiveInsightViewModel =
  | ExecutiveInsightReadyViewModel
  | ExecutiveInsightPendingViewModel
  | ExecutiveInsightErrorViewModel;
