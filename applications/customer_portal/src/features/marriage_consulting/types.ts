/**
 * Public Marriage API DTO types. Frontend boundary only.
 */

export type GenderValue = "male" | "female";

export type PersonFormValue = {
  full_name: string;
  gender: GenderValue | "";
  birth_date: string;
  birth_time: string;
  birth_place: string;
};

export type MarriageEnvelope<T> = {
  status: string;
  data: T | null;
  warnings: MarriageWarning[];
  errors: MarriagePublicError[];
  version_bundle?: Record<string, string | null>;
};

export type MarriageWarning = {
  code: string;
  description: string | null;
  affected_domain: string | null;
};

export type MarriagePublicError = {
  code: string;
  stage: string;
  message: string;
  retryable: boolean;
  consultation_id: string | null;
  trace_id?: string | null;
};

export type MarriagePersonSummary = {
  display_name: string | null;
  gender: string | null;
  correlation_id?: string | null;
};

export type MarriageConsultationDto = {
  consultation_id: string;
  status: string;
  created_at?: string;
  person_a: MarriagePersonSummary;
  person_b: MarriagePersonSummary;
  overall_state: string | null;
  score: number | null;
  grade: string | null;
  confidence: { level: string; overall: number };
  limitations: string[];
  headline: string | null;
  action_themes?: string[];
  expert?: Record<string, unknown>;
};

export type MarriageReportBlock = {
  block_id: string;
  kind: string;
  title: string | null;
  body: string | null;
  semantic_key: string | null;
  state: string | null;
  domain: string | null;
  visibility?: string;
  source_finding_ids?: string[];
  source_recommendation_ids?: string[];
};

export type MarriageReportSection = {
  section_id: string;
  title: string;
  summary: string | null;
  blocks: MarriageReportBlock[];
};

export type MarriageReportDto = {
  consultation_id: string;
  score: number | null;
  grade: string | null;
  metadata?: Record<string, unknown>;
  sections: MarriageReportSection[];
};

export type DomainCardVm = {
  domain: string;
  title: string;
  stateLabel: string;
  summary: string;
  explanation: string;
  relatedActionKeys: string[];
};

export type ActionCardVm = {
  key: string;
  title: string;
  what: string;
  objective: string;
  priorityLabel: string;
  priority: string;
  when: string;
  outcome: string;
};

export type ComparisonGroupVm = {
  id: string;
  title: string;
  items: string[];
};

export type MarriageViewModel = {
  consultationId: string;
  overallState: string | null;
  score: number | null;
  grade: string | null;
  identityTitle: string;
  personAName: string;
  personBName: string;
  heroEyebrow: string;
  heroHeadline: string;
  heroSummary: string;
  heroStateLabel: string;
  heroStrengths: string[];
  heroRisks: string[];
  confidenceLabel: string;
  executiveSummary: string;
  strengths: string[];
  risks: string[];
  comparisonGroups: ComparisonGroupVm[];
  domains: DomainCardVm[];
  unavailableNote: string | null;
  timingSummary: string | null;
  actions: ActionCardVm[];
  limitations: string[];
  confidenceBody: string;
  conclusion: string;
  appendix: string;
  warnings: MarriageWarning[];
  expertTrace: string | null;
};
