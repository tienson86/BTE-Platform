/**
 * Shared request / response DTOs aligned with FastAPI schemas (TASK_003A).
 */

/** POST /analyze (and related engine) birth payload. */
export type CreateChartRequest = {
  readonly year: number;
  readonly month: number;
  readonly day: number;
  readonly hour?: number;
  readonly minute?: number;
  readonly gender?: string | null;
  readonly timezone?: string;
  readonly full_name?: string | null;
  readonly birth_place?: string | null;
  readonly customer_id?: string | null;
  readonly metadata?: Readonly<Record<string, unknown>> | null;
};

/** Alias — analyze uses the same birth contract. */
export type AnalyzeChartRequest = CreateChartRequest;

/** Report generation uses the same birth contract today. */
export type GenerateReportRequest = CreateChartRequest;

export type ApiErrorResponse = {
  readonly success: false;
  readonly message: string;
  readonly code?: string;
  readonly details?: unknown;
  readonly errors?: readonly unknown[];
  readonly request_id?: string | null;
};

export type PillarDto = {
  readonly stem?: string;
  readonly branch?: string;
  readonly hidden_stems?: readonly string[];
  readonly ten_god?: string;
  readonly nap_am?: string;
  readonly truong_sinh?: string;
};

export type BaziDto = {
  readonly year_pillar?: PillarDto;
  readonly month_pillar?: PillarDto;
  readonly day_pillar?: PillarDto;
  readonly hour_pillar?: PillarDto;
  readonly day_master?: string;
  readonly day_master_element?: string;
  readonly day_master_yin_yang?: string;
  readonly gender?: string | null;
  readonly hidden_stems?: readonly string[];
  readonly ten_gods?: readonly string[];
  readonly shensha?: readonly string[];
};

export type CalendarDto = {
  readonly year_can_chi?: string;
  readonly month_can_chi?: string;
  readonly day_can_chi?: string;
  readonly hour_can_chi?: string;
  readonly solar_term?: { readonly name?: string } | null;
  readonly cung_phi?: string;
  readonly menh_quai?: string;
  readonly [key: string]: unknown;
};

export type SeriesItemDto = {
  readonly label?: string;
  readonly name?: string;
  readonly element?: string;
  readonly value?: number;
  readonly count?: number;
  readonly score?: number;
};

export type ScoreDto = {
  readonly success?: boolean;
  readonly total_score?: number;
  readonly strength_score?: number;
  readonly pattern_score?: number;
  readonly ten_god_score?: number;
  readonly wuxing_score?: number;
  readonly grade?: string;
  readonly confidence?: string;
  readonly recommendation?: string;
  readonly wuxing_series?: readonly SeriesItemDto[];
  readonly ten_god_series?: readonly SeriesItemDto[];
  readonly [key: string]: unknown;
};

export type StrengthDto = {
  readonly strength_level?: string;
  readonly strength_score?: number;
  readonly reasoning?: string;
  readonly confidence?: number;
  readonly [key: string]: unknown;
};

export type CustomerEchoDto = {
  readonly full_name?: string | null;
  readonly birth_place?: string | null;
  readonly gender?: string | null;
  readonly timezone?: string | null;
  readonly customer_id?: string | null;
};

/** `data` payload from POST /analyze. */
export type AnalysisDataDto = {
  readonly pipeline?: readonly string[];
  readonly stage?: string;
  readonly calendar?: CalendarDto;
  readonly bazi?: BaziDto;
  readonly pattern?: Record<string, unknown>;
  readonly strength?: StrengthDto;
  readonly temperature?: Record<string, unknown>;
  readonly useful_god?: Record<string, unknown>;
  readonly score?: ScoreDto;
  readonly interpretation?: Record<string, unknown>;
  readonly report?: Record<string, unknown>;
  readonly narrative?: Record<string, unknown>;
  readonly customer?: CustomerEchoDto;
  readonly [key: string]: unknown;
};

export type AnalysisResponse = {
  readonly success: boolean;
  readonly message: string;
  readonly data: AnalysisDataDto;
  readonly request_id?: string | null;
};

/** Chart-focused alias (bazi slice). */
export type ChartResponse = AnalysisResponse;

export type InterpretationResponse = AnalysisResponse;
export type ReportResponse = AnalysisResponse;

export type HealthResponse = {
  readonly status: string;
  readonly service?: string;
  readonly version?: string;
};

export type CaseDto = {
  readonly case_id: string;
  readonly customer_id: string;
  readonly created_at: string;
  readonly engine_version?: string;
  readonly input_snapshot?: Readonly<Record<string, unknown>>;
  readonly report_result?: Readonly<Record<string, unknown>>;
  readonly [key: string]: unknown;
};

export type CasesListData = {
  readonly cases: readonly CaseDto[];
  readonly count: number;
};

export type CustomersListData = {
  readonly customers: readonly Record<string, unknown>[];
  readonly count: number;
};
