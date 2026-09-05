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
  readonly cung_phi?: string;
  readonly source_nguyen?: string;
  readonly ganzhi?: string;
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
  readonly shen_sha?: ShenShaPack07Dto;
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
  readonly house_group?: string;
  readonly tam_nguyen?: string;
  readonly cuu_van?: number | string;
  readonly gua_number?: number;
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
  readonly stem_element?: string;
  readonly branch_element?: string;
};

export type LuckActivationItemDto = {
  readonly id?: string;
  readonly title?: string;
  readonly state?: string;
  readonly state_label?: string;
  readonly driver?: string;
  readonly support?: string;
  readonly stress?: string;
  readonly marker?: string;
  readonly bottleneck?: string;
  readonly conditions?: readonly string[];
};

export type LuckActivationDto = {
  readonly title?: string;
  readonly time_window?: string;
  readonly gan_zhi?: string;
  readonly items?: readonly LuckActivationItemDto[];
};

export type LuckInteractionEdgeDto = {
  readonly source?: string;
  readonly target?: string;
  readonly type?: string;
  readonly explanation?: string;
  readonly condition?: string;
};

export type LuckInteractionDto = {
  readonly title?: string;
  readonly situation?: string;
  readonly driver?: string;
  readonly bottleneck?: string;
  readonly opportunity?: string;
  readonly risk?: string;
  readonly edges?: readonly LuckInteractionEdgeDto[];
};

export type LuckAnnualItemDto = {
  readonly id?: string;
  readonly title?: string;
  readonly year?: string;
  readonly natal_state?: string;
  readonly natal_label?: string;
  readonly luck_state?: string;
  readonly luck_label?: string;
  readonly annual_state?: string;
  readonly annual_label?: string;
  readonly driver?: string;
  readonly bottleneck?: string;
  readonly support?: string;
  readonly stress?: string;
  readonly recovery?: string;
  readonly conditions?: readonly string[];
};

export type LuckAnnualDto = {
  readonly title?: string;
  readonly year?: string;
  readonly gan_zhi?: string;
  readonly dominant_activation?: string;
  readonly dominant_suppression?: string;
  readonly stress?: string;
  readonly recovery?: string;
  readonly items?: readonly LuckAnnualItemDto[];
};

export type LuckDto = {
  readonly available?: boolean;
  readonly direction?: string;
  readonly direction_label?: string;
  readonly start_age?: number;
  readonly current_cycle?: LuckCycleDto | null;
  readonly cycles?: readonly LuckCycleDto[];
  readonly evidence?: string;
  readonly method_note?: string;
  readonly precision?: string;
  readonly current_age_for_luck?: number;
  readonly gender_label?: string;
  readonly activation?: LuckActivationDto | null;
  readonly interaction?: LuckInteractionDto | null;
  readonly annual?: LuckAnnualDto | null;
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
  readonly gender_label?: string | null;
  readonly timezone?: string | null;
  readonly customer_id?: string | null;
};

/** Frozen INT-02 IntegratedNarrative block on Analysis Result. */
export type IntegratedNarrativeBlockDto = {
  readonly slot?: string;
  readonly title?: string;
  readonly sentences?: readonly string[];
  readonly available?: boolean;
  readonly insufficient?: boolean;
};

/** Frozen INT-02 IntegratedNarrative unit. Workspace reads this only. */
export type IntegratedNarrativeDto = {
  readonly topic_id?: string;
  readonly status?: string;
  readonly executive_summary?: IntegratedNarrativeBlockDto;
  readonly observation?: IntegratedNarrativeBlockDto;
  readonly reasoning?: IntegratedNarrativeBlockDto;
  readonly impact?: IntegratedNarrativeBlockDto;
  readonly recommendation?: IntegratedNarrativeBlockDto;
  readonly summary?: IntegratedNarrativeBlockDto;
};

/** Pack 07 natal Ten God customer projection. Labels only; no traces. */
export type TenGodDetailedItemDto = {
  readonly name?: string;
  readonly status_label?: string;
  readonly role_label?: string;
  readonly positives?: readonly string[];
  readonly risks?: readonly string[];
  readonly conditions?: readonly string[];
  readonly unresolved?: boolean;
  readonly fallback?: string;
};

export type TenGodsDetailedDto = {
  readonly state?: string;
  readonly items?: readonly TenGodDetailedItemDto[];
};

export type TenGodRelationItemDto = {
  readonly name?: string;
  readonly state_label?: string;
  readonly mechanism?: string;
  readonly condition?: string;
  readonly unresolved?: boolean;
  readonly fallback?: string;
};

export type TenGodsRelationsDto = {
  readonly state?: string;
  readonly items?: readonly TenGodRelationItemDto[];
};

export type TenGodEcosystemRoleDto = {
  readonly label?: string;
  readonly unresolved?: boolean;
};

export type TenGodsEcosystemDto = {
  readonly state?: string;
  readonly unresolved?: boolean;
  readonly fallback?: string;
  readonly driver?: TenGodEcosystemRoleDto;
  readonly support?: TenGodEcosystemRoleDto;
  readonly bottleneck?: TenGodEcosystemRoleDto;
  readonly blocked?: TenGodEcosystemRoleDto;
  readonly suppressed?: TenGodEcosystemRoleDto;
  readonly excessive?: TenGodEcosystemRoleDto;
  readonly deficient?: TenGodEcosystemRoleDto;
  readonly missing?: TenGodEcosystemRoleDto;
  readonly flow?: string;
  readonly flow_quality?: string;
};

/** Pack 07 Shen Sha customer projection. Labels only; no traces. */
export type ShenShaStarItemDto = {
  readonly name?: string;
  readonly category?: string;
  readonly state_label?: string;
  readonly placement?: string;
  readonly explanation?: string;
  readonly unresolved?: boolean;
  readonly warning?: boolean;
};

export type ShenShaIndividualDto = {
  readonly state?: string;
  readonly items?: readonly ShenShaStarItemDto[];
};

export type ShenShaClusterItemDto = {
  readonly name?: string;
  readonly state_label?: string;
  readonly explanation?: string;
  readonly warning?: boolean;
  readonly unresolved?: boolean;
  readonly prominent?: boolean;
};

export type ShenShaEcosystemDto = {
  readonly state?: string;
  readonly dominant?: string;
  readonly dominant_unresolved?: boolean;
  readonly supporting?: string;
  readonly warning?: string;
  readonly unresolved_label?: string;
  readonly clusters?: readonly ShenShaClusterItemDto[];
};

export type ShenShaPack07Dto = {
  readonly individual?: ShenShaIndividualDto;
  readonly ecosystem?: ShenShaEcosystemDto;
};

/** Canonical Cân Xương Đoán Mệnh object published by the engine. */
export type CanXuongDto = {
  readonly total_weight?: number;
  readonly liang?: number;
  readonly chi?: number;
  readonly display_weight?: string;
  readonly classification?: string;
  readonly rating?: string;
  readonly summary?: string;
  readonly interpretation?: string;
  readonly source?: string;
  readonly version?: string;
  readonly weight?: string;
  readonly total?: string;
  readonly poem?: string;
};

/** Narrative V2 Presentation envelope stored beside Pack05. Switch chooses which to render. */
export type NarrativeV2ShadowEnvelopeDto = {
  readonly status?: string;
  readonly portal_connection?: string;
  readonly replaces_pack05?: boolean;
  readonly presentation?: Record<string, unknown> | null;
  readonly error?: string | null;
};

/** Compact Evidence Priority customer summary. Labels only. */
export type EvidencePrioritySummaryDto = {
  readonly title?: string;
  readonly driver?: string;
  readonly bottleneck?: string;
  readonly risk?: string;
  readonly opportunity?: string;
  readonly condition?: string;
};

export type DomainSummaryDto = {
  readonly id?: string;
  readonly title?: string;
  readonly state?: string;
  readonly state_label?: string;
  readonly driver?: string;
  readonly driver_id?: string;
  readonly support?: string;
  readonly bottleneck?: string;
  readonly opportunity?: string;
  readonly caution?: string;
  readonly condition?: string;
  readonly confidence?: string;
  readonly summary?: string;
  readonly dimensions?: readonly { readonly label?: string; readonly value?: string }[];
  readonly unresolved?: boolean;
};

export type DomainInterpretationSummaryDto = {
  readonly title?: string;
  readonly items?: readonly DomainSummaryDto[];
};

/** `data` payload from POST /analyze. */
export type AnalysisDataDto = {
  readonly pipeline?: readonly string[];
  readonly stage?: string;
  readonly calendar?: CalendarDto;
  readonly bazi?: BaziDto;
  readonly pattern?: Record<string, unknown>;
  readonly mingju?: Record<string, unknown>;
  readonly strength?: StrengthDto;
  readonly temperature?: Record<string, unknown>;
  readonly useful_god?: Record<string, unknown>;
  readonly useful_god_source?: Record<string, unknown>;
  readonly result_meta?: Record<string, unknown>;
  readonly analysis_id?: string | null;
  readonly request_id?: string | null;
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
    readonly detailed?: TenGodsDetailedDto;
    readonly relations?: TenGodsRelationsDto;
    readonly ecosystem?: TenGodsEcosystemDto;
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
  /** Narrative V2 Presentation envelope. Independent of Pack05. */
  readonly narrative_v2_shadow?: NarrativeV2ShadowEnvelopeDto | null;
  /** Frozen INT-02 IntegratedNarrative. Workspace Panel 9/10 consume this only. */
  readonly integrated_narrative?: IntegratedNarrativeDto;
  readonly customer?: CustomerEchoDto;
  /** Canonical Identity Layer (BZ-ID). Presentation reads this for identity fields. */
  readonly identity?: CanonicalIdentityDto;
  /** Canonical Cân Xương Đoán Mệnh (G1-11). Header and S10 copy this object. */
  readonly can_xuong?: CanXuongDto;
  /** Pre-composed CK-01 commercial consulting. Presentation copies only. */
  readonly commercial_consulting?: CommercialConsultingDto;
  readonly evidence_priority?: EvidencePrioritySummaryDto;
  readonly domains?: DomainInterpretationSummaryDto;
  readonly optimization?: Record<string, unknown>;
  /** Pack 07 Narrative Composer customer compact. Does not replace payload.narrative. */
  readonly detailed_narrative?: Record<string, unknown>;
  readonly [key: string]: unknown;
};

export type CommercialConsultingSectionDto = {
  readonly domain?: string;
  readonly title?: string;
  readonly summary?: string;
  readonly meaning?: readonly string[];
  readonly recommendations?: readonly string[];
  readonly references?: readonly string[];
  readonly source_unit_ids?: readonly string[];
};

export type CommercialConsultingDto = {
  readonly status?: string;
  readonly catalog_id?: string;
  readonly schema_version?: string;
  readonly sections?: readonly CommercialConsultingSectionDto[];
};

export type IdentityPillarDto = {
  readonly stem?: string;
  readonly branch?: string;
  readonly can_chi?: string;
  readonly nayin_element?: string;
  readonly cung_phi?: string;
  readonly pillar_type?: string;
};

export type CanonicalIdentityDto = {
  readonly person?: {
    readonly full_name?: string;
    readonly gender?: string;
    readonly solar_birth?: string;
    readonly lunar_birth?: string;
    readonly birth_time?: string;
    readonly birth_place?: string;
    readonly timezone?: string;
  };
  readonly calendar?: Record<string, unknown>;
  readonly four_pillars?: {
    readonly year?: IdentityPillarDto;
    readonly month?: IdentityPillarDto;
    readonly day?: IdentityPillarDto;
    readonly hour?: IdentityPillarDto;
  };
  readonly bone_weight?: {
    readonly weight?: string;
    readonly classification?: string;
    readonly rating?: string;
    readonly summary?: string;
  };
  readonly luck?: {
    readonly current_cycle?: string;
    readonly current_cycle_age?: string;
    readonly current_cycle_ganzhi?: string;
    readonly cycle_index?: string;
    readonly reference_year?: string;
    readonly current_year?: string;
    readonly current_liunian_ganzhi?: string;
    readonly current_liunian_year?: string;
  };
  readonly interpretation?: {
    readonly observation_id?: string;
    readonly reasoning_id?: string;
    readonly recommendation_id?: string;
    readonly conclusion_id?: string;
    readonly conclusion?: string;
    readonly action?: Record<string, unknown>;
    readonly section_keys?: readonly string[];
  };
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
