/**
 * PortalResultModel — PX-2 `bte.portal.result_ui.v2`.
 * The only shape Result V2 components may consume.
 */

export const RESULT_UI_CONTRACT_ID = "bte.portal.result_ui.v2" as const;
export const RESULT_UI_CONTRACT_VERSION = "2.0.0" as const;

export type PageState =
  | "loading"
  | "ready"
  | "partial_ready"
  | "error"
  | "empty"
  | "offline"
  | "printing"
  | "exporting";

export type HeroStatus = "ready" | "partial" | "in_progress" | "error";

export type DomainKey = "career" | "wealth" | "relationship" | "health" | "luck";

export type WarningSeverity = "attention" | "critical";

export type PageModel = {
  state: PageState;
  partial: boolean;
  error_code: string | null;
  error_message: string | null;
};

export type HeroModel = {
  name: string;
  headline: string;
  one_line_summary: string;
  status: HeroStatus;
  status_label: string;
};

export type SummaryModel = {
  title: string;
  bullets: string[];
};

export type RecommendationModel = {
  id: string;
  domain: DomainKey;
  domain_label: string;
  title: string;
  reason: string;
  expected_result: string;
  action: string;
  detail: string | null;
  expanded: boolean;
  priority: number | null;
};

export type WarningModel = {
  title: string;
  body: string;
  mitigation: string | null;
  severity: WarningSeverity;
  expanded: boolean;
};

export type DomainModel = {
  key: DomainKey;
  title: string;
  available: boolean;
  intro: string | null;
  recommendation_ids: string[];
  analysis_preview: string | null;
  analysis_detail: string | null;
  analysis_expanded: boolean;
};

export type DomainMapModel = Record<DomainKey, DomainModel>;

export type ChartTable = {
  headers: string[];
  rows: string[][];
};

export type ChartModel = {
  title: string;
  caption: string;
  asset_ref: string;
  table: ChartTable | null;
  table_expanded: boolean;
};

export type TechnicalModel = {
  collapsed: boolean;
  calendar: string | null;
  pillars: string | null;
  timezone: string | null;
  schema: string | null;
  ids: string | null;
  metadata: Record<string, string> | null;
  available: boolean;
};

export type KnowledgeModel = {
  title: string;
  teaser: string;
  body: string | null;
  expanded: boolean;
};

export type AppendixModel = {
  scope: string | null;
  reread: string | null;
  limits: string | null;
};

export type CtaModel = {
  primary_label: string;
  primary_enabled: boolean;
  secondary_label: string | null;
  secondary_enabled: boolean;
};

export type NavItemModel = {
  target_ui_id: string;
  label: string;
  visible: boolean;
};

export type NavModel = {
  items: NavItemModel[];
};

export type ChromeModel = {
  skip: string;
  page_loading: string;
  page_offline: string;
  cta_loading: string;
  error_page: string;
  error_retry: string;
  error_retry_section: string;
  error_back_summary: string;
  empty_page: string;
  empty_recommendations: string;
  empty_domain: string;
  section_summary: string;
  section_recommendation: string;
  section_warnings: string;
  section_charts: string;
  section_technical: string;
  section_knowledge: string;
  section_appendix: string;
  field_why: string;
  field_expected_result: string;
  field_action: string;
  expand_more: string;
  expand_less: string;
  expand_analysis: string;
  expand_analysis_less: string;
  expand_table: string;
  expand_table_less: string;
  expand_technical: string;
  expand_technical_less: string;
  expand_knowledge: string;
  expand_knowledge_less: string;
  expand_knowledge_item: string;
  technical_calendar: string;
  technical_pillars: string;
  technical_timezone: string;
  technical_schema: string;
  technical_ids: string;
  technical_metadata: string;
};

export type PortalResultModel = {
  contract_id: typeof RESULT_UI_CONTRACT_ID;
  contract_version: typeof RESULT_UI_CONTRACT_VERSION;
  page: PageModel;
  hero: HeroModel | null;
  summary: SummaryModel | null;
  recommendations: RecommendationModel[];
  warnings: WarningModel[];
  domains: DomainMapModel;
  charts: ChartModel[];
  technical: TechnicalModel;
  knowledge: KnowledgeModel[];
  appendix: AppendixModel | null;
  cta: CtaModel;
  nav: NavModel;
  chrome: ChromeModel;
};

export const DOMAIN_ORDER: readonly DomainKey[] = [
  "career",
  "wealth",
  "relationship",
  "health",
  "luck",
] as const;
