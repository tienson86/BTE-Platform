/**
 * Canonical Report input shape for the Portal adapter.
 * Structural fields only — no engine module types.
 */

import type { DomainKey, HeroStatus, WarningSeverity } from "./PortalResultModel";

export type PresentationIdentity = {
  full_name?: string | null;
  headline?: string | null;
  one_line_summary?: string | null;
  consultation_status?: HeroStatus | string | null;
};

export type PresentationRecommendation = {
  id?: string | null;
  domain?: DomainKey | string | null;
  title?: string | null;
  reason?: string | null;
  expected_result?: string | null;
  action?: string | null;
  detail?: string | null;
  priority?: number | null;
};

export type PresentationWarning = {
  title?: string | null;
  body?: string | null;
  mitigation?: string | null;
  severity?: WarningSeverity | string | null;
};

export type PresentationDomain = {
  available?: boolean | null;
  intro?: string | null;
  recommendation_ids?: string[] | null;
  analysis_preview?: string | null;
  analysis_detail?: string | null;
};

export type PresentationChart = {
  title?: string | null;
  caption?: string | null;
  asset_ref?: string | null;
  table?: { headers?: string[]; rows?: string[][] } | null;
};

export type PresentationTechnical = {
  calendar?: string | null;
  pillars?: string | null;
  timezone?: string | null;
  schema?: string | null;
  ids?: string | null;
  metadata?: Record<string, unknown> | null;
};

export type PresentationKnowledge = {
  title?: string | null;
  teaser?: string | null;
  body?: string | null;
};

export type PresentationAppendix = {
  scope?: string | null;
  reread?: string | null;
  limits?: string | null;
};

export type ReportPresentationEnvelope = {
  identity?: PresentationIdentity | null;
  summary?: { bullets?: string[] | null } | null;
  recommendations?: PresentationRecommendation[] | null;
  warnings?: PresentationWarning[] | null;
  domains?: Partial<Record<DomainKey, PresentationDomain | null>> | null;
  charts?: PresentationChart[] | null;
  technical?: PresentationTechnical | null;
  knowledge?: PresentationKnowledge[] | null;
  appendix?: PresentationAppendix | null;
  cta?: {
    primary?: { enabled?: boolean | null } | null;
    secondary?: { enabled?: boolean | null } | null;
  } | null;
};

export type LayoutSectionInput = {
  module_id?: string | null;
  status?: string | null;
};

export type LayoutBlockInput = {
  block_type?: string | null;
  status?: string | null;
};

export type CanonicalReportInput = {
  success?: boolean | null;
  errors?: string[] | null;
  report_pipeline_version?: string | null;
  presentation?: ReportPresentationEnvelope | null;
  layout_result?: {
    success?: boolean | null;
    sections?: LayoutSectionInput[] | null;
    blocks?: LayoutBlockInput[] | null;
  } | null;
  canonical_report_artifact?: {
    success?: boolean | null;
    artifact_id?: string | null;
    mime_type?: string | null;
    render_version?: string | null;
    metadata?: Record<string, unknown> | null;
    content?: unknown;
  } | null;
};

export type AdapterOptions = {
  loading?: boolean;
  offline?: boolean;
  printing?: boolean;
  exporting?: boolean;
};
