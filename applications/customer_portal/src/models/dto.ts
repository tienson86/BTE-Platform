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
  readonly element?: string;
  readonly nap_am?: string;
  readonly truong_sinh?: string;
};

export type ShenShaOccurrenceDto = {
  readonly pillar?: string;
  readonly location?: string;
  readonly target_value?: string;
};

export type ShenShaMatchDto = {
  readonly id?: string;
  readonly canonical_name?: string;
  readonly name?: string;
  readonly aliases?: readonly string[];
  readonly source_type?: string;
  readonly source_value?: string;
  readonly target_type?: string;
  readonly target_value?: string;
  readonly pillar?: string;
  readonly location?: string;
  readonly rule_source?: string;
  readonly presence_label?: string;
  readonly evidence_text?: string;
  readonly occurrences?: readonly ShenShaOccurrenceDto[];
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
  readonly shensha_matches?: readonly ShenShaMatchDto[];
};

export type CalendarDto = {
  readonly year_can_chi?: string;
  readonly month_can_chi?: string;
  readonly day_can_chi?: string;
  readonly hour_can_chi?: string;
  readonly solar_date?: string;
  readonly lunar_date?: string;
  readonly lunar_year?: number;
  readonly lunar_month?: number;
  readonly lunar_day?: number;
  readonly leap_month?: boolean;
  readonly is_leap_month?: boolean;
  readonly lunar?: {
    readonly year?: number;
    readonly month?: number;
    readonly day?: number;
    readonly leap?: boolean;
    readonly is_leap_month?: boolean;
    readonly year_can_chi?: string;
  };
  readonly lunar_can_chi?: {
    readonly year?: string;
    readonly day?: string;
  };
  readonly solar_term?: { readonly name?: string } | null;
  readonly cung_phi?: string;
  readonly menh_quai?: string;
  readonly nhom_trach?: string;
  readonly [key: string]: unknown;
};

export type FiveElementsDto = {
  readonly wood?: { readonly count?: number; readonly status?: string } | number;
  readonly fire?: { readonly count?: number; readonly status?: string } | number;
  readonly earth?: { readonly count?: number; readonly status?: string } | number;
  readonly metal?: { readonly count?: number; readonly status?: string } | number;
  readonly water?: { readonly count?: number; readonly status?: string } | number;
  readonly counts?: Readonly<Record<string, number | null | undefined>>;
  readonly status?: string;
  readonly dominant?: string;
  readonly missing?: readonly string[];
  readonly method_note?: string;
  readonly unit_total?: number;
  readonly count_model?: string;
};

export type LuckCycleDto = {
  readonly index?: number;
  readonly age_start?: number;
  readonly age_end?: number;
  readonly year_start?: number;
  readonly year_end?: number;
  readonly gan_zhi?: string;
  readonly stem?: string;
  readonly branch?: string;
};

export type LuckDto = {
  readonly available?: boolean;
  readonly direction?: string;
  readonly start_age?: number;
  readonly current_cycle?: LuckCycleDto | null;
  readonly cycles?: readonly LuckCycleDto[];
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
  readonly evidence_compact?: string;
  readonly confidence?: number;
  readonly matched_rules?: readonly string[];
  readonly raw_total?: number;
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
  readonly five_elements?: FiveElementsDto;
  readonly ten_gods?: {
    readonly visible?: readonly unknown[];
    readonly hidden?: readonly unknown[];
    readonly visible_labels?: readonly string[];
    readonly hidden_labels?: readonly string[];
    readonly visible_summary?: string;
    readonly hidden_summary?: string;
    readonly summary?: string;
    readonly note?: string;
  };
  readonly ten_gods_result?: {
    readonly visible?: readonly unknown[];
    readonly hidden?: readonly unknown[];
    readonly visible_labels?: readonly string[];
    readonly hidden_labels?: readonly string[];
    readonly visible_summary?: string;
    readonly hidden_summary?: string;
    readonly note?: string;
  };
  readonly luck?: LuckDto;
  readonly interpretation?: Record<string, unknown>;
  readonly report?: Record<string, unknown>;
  /** ReportEngine delivery markdown/html (legacy delivery alias). */
  readonly narrative?: Record<string, unknown>;
  /** Pack 05 official commercial NarrativeResult. */
  readonly narrative_result?: Record<string, unknown>;
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
