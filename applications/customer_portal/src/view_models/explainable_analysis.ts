/**
 * Explainable Analysis presentation ViewModels — WP-0008.
 * Presentation-ready explanations only. No engine/rule evaluation.
 */

import type { PresentationStatus } from "./executive_summary";
import type { ConfidencePanelViewModel } from "./metrics";

export type AnalysisEvidenceItemViewModel = {
  id: string;
  label: string;
  detail?: string;
  meta?: string;
};

export type AnalysisRuleReferenceViewModel = {
  id: string;
  label: string;
  citation?: string;
  source?: string;
};

export type AnalysisKnowledgeReferenceViewModel = {
  id: string;
  citation: string;
  source?: string;
};

export type AnalysisConclusionViewModel = {
  title: string;
  body: string;
};

export type AnalysisExplanationViewModel = {
  title?: string;
  paragraphs: string[];
};

export type AnalysisRecommendationViewModel = {
  title: string;
  body: string;
  priorityLabel?: string;
};

export type AnalysisSummaryViewModel = {
  title?: string;
  paragraphs: string[];
};

export type AnalysisBlockViewModel = {
  id: string;
  title: string;
  conclusion: AnalysisConclusionViewModel;
  explanation: AnalysisExplanationViewModel;
  evidence: AnalysisEvidenceItemViewModel[];
  rules: AnalysisRuleReferenceViewModel[];
  confidence: ConfidencePanelViewModel;
  knowledge: AnalysisKnowledgeReferenceViewModel[];
  recommendation?: AnalysisRecommendationViewModel;
};

export type ExplainableAnalysisTransitionViewModel = {
  label: string;
  href?: string;
};

export type ExplainableAnalysisReadyViewModel = {
  status: "ready";
  title?: string;
  subtitle?: string;
  summary?: AnalysisSummaryViewModel;
  blocks: AnalysisBlockViewModel[];
  transition?: ExplainableAnalysisTransitionViewModel;
};

export type ExplainableAnalysisPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type ExplainableAnalysisErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type ExplainableAnalysisViewModel =
  | ExplainableAnalysisReadyViewModel
  | ExplainableAnalysisPendingViewModel
  | ExplainableAnalysisErrorViewModel;
