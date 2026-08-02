/**
 * Appendix presentation ViewModels — WP-0010.
 * Presentation-ready reference material only. No knowledge lookup.
 */

import type { PresentationStatus } from "./executive_summary";

export type AppendixGlossaryEntryViewModel = {
  id: string;
  term: string;
  definition: string;
};

export type AppendixTerminologyItemViewModel = {
  id: string;
  term: string;
  definition: string;
  abbreviation?: string;
};

export type AppendixReferenceItemViewModel = {
  id: string;
  citation: string;
  source?: string;
};

export type AppendixVersionViewModel = {
  title?: string;
  items: Array<{ id: string; label: string; value: string }>;
};

export type AppendixCreditsViewModel = {
  title?: string;
  paragraphs: string[];
  items?: Array<{ id: string; label: string; value: string }>;
};

export type AppendixSummaryViewModel = {
  title?: string;
  paragraphs: string[];
};

export type AppendixHeaderViewModel = {
  title?: string;
  subtitle?: string;
};

export type AppendixTransitionViewModel = {
  label: string;
  href?: string;
};

export type AppendixReadyViewModel = {
  status: "ready";
  header?: AppendixHeaderViewModel;
  summary?: AppendixSummaryViewModel;
  glossary: AppendixGlossaryEntryViewModel[];
  terminology: AppendixTerminologyItemViewModel[];
  knowledgeReferences: AppendixReferenceItemViewModel[];
  ruleReferences: AppendixReferenceItemViewModel[];
  citations: AppendixReferenceItemViewModel[];
  credits: AppendixCreditsViewModel;
  version: AppendixVersionViewModel;
  transition?: AppendixTransitionViewModel;
};

export type AppendixPendingViewModel = {
  status: Exclude<PresentationStatus, "ready" | "error">;
};

export type AppendixErrorViewModel = {
  status: "error";
  errorMessage?: string;
};

export type AppendixViewModel =
  | AppendixReadyViewModel
  | AppendixPendingViewModel
  | AppendixErrorViewModel;
