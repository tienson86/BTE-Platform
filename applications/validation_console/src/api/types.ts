export type DatasetStatus =
  | "draft"
  | "review"
  | "approved"
  | "released"
  | "rejected";

export type CaseResultStatus = "pass" | "fail" | "skip" | "error";
export type WorkflowAction = "submit" | "approve" | "reject" | "release";

export interface ApiEnvelope<T> {
  success: boolean;
  message: string;
  data: T;
  request_id?: string | null;
}

export interface GoldenCase {
  case_id: string;
  description: string;
  input_fixture: Record<string, unknown>;
  expected_output: Record<string, unknown>;
  actual_output: Record<string, unknown> | null;
  tags: string[];
  coverage_goal: string;
  tolerance_policy: string;
  metadata: Record<string, unknown>;
}

export interface DiffItem {
  field: string;
  expected: unknown;
  actual: unknown;
}

export interface CaseCompareResult {
  case_id: string;
  status: CaseResultStatus;
  differences: DiffItem[];
  message: string;
}

export interface RegressionReport {
  report_id: string;
  dataset_id: string;
  ran_at: string;
  actor: string;
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  errors: number;
  case_results: CaseCompareResult[];
}

export interface HistoryEntry {
  event_id: string;
  action: string;
  actor: string;
  at: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface GoldenDataset {
  dataset_id: string;
  name: string;
  description: string;
  version: string;
  status: DatasetStatus;
  module: string;
  cases: GoldenCase[];
  reports: RegressionReport[];
  history: HistoryEntry[];
  created_at: string;
  updated_at: string;
  created_by: string;
  updated_by: string;
  metadata: Record<string, unknown>;
  case_count: number;
}

export interface CompareResponse {
  dataset_id: string;
  results: CaseCompareResult[];
  summary: {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    errors: number;
  };
}

export interface Statistics {
  dataset_id: string;
  case_count: number;
  with_actual: number;
  without_actual: number;
  unique_tags: string[];
  tag_count: number;
  report_count: number;
  latest_regression: {
    report_id: string;
    ran_at: string;
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    errors: number;
    pass_rate: number;
  } | null;
  status: DatasetStatus;
  version: string;
}

export interface CoverageReport {
  dataset_id: string;
  case_count: number;
  tag_coverage: Array<{ tag: string; count: number }>;
  goal_coverage: Array<{ goal: string; count: number }>;
  required_goals: string[];
  covered_goals: string[];
  missing_goals: string[];
  coverage_ratio: number;
  complete: boolean;
}
