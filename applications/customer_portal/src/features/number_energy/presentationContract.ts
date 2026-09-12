/**
 * RB04 NumberEnergyPresentationAdapter contract — types and constants only.
 *
 * Do not import this module into NumberEnergyPage, ResultSection,
 * numberEnergyApp, or leftover analyze helpers.
 * Do not add adapter runtime functions in this file.
 * Freeze: NUMBER_ENERGY_STATIC_UI_V1
 */

export const NUMBER_ENERGY_ADAPTER_NAME = "NumberEnergyPresentationAdapter" as const;

export const NUMBER_ENERGY_VIEW_NAME = "NumberEnergyPresentationView" as const;

export const NUMBER_ENERGY_CONTRACT_FREEZE = "NUMBER_ENERGY_STATIC_UI_V1" as const;

export const FIELD_STATUS = {
  PRESENT_FROM_CURRENT_PAYLOAD: "PRESENT_FROM_CURRENT_PAYLOAD",
  ADAPTER_DERIVED_SAFE: "ADAPTER_DERIVED_SAFE",
  REQUIRES_ENGINE: "REQUIRES_ENGINE",
  REQUIRES_API: "REQUIRES_API",
  DO_NOT_BIND: "DO_NOT_BIND",
} as const;

export type FieldStatus = (typeof FIELD_STATUS)[keyof typeof FIELD_STATUS];

export const PRESENTATION_SLOT_IDS = [
  "P-S00",
  "P-S01",
  "P-S02",
  "P-S03",
  "P-S04",
  "P-S05",
  "P-S06",
  "P-S07",
  "P-S08",
  "P-S09",
  "P-S10",
  "P-S11",
] as const;

export type PresentationSlotId = (typeof PRESENTATION_SLOT_IDS)[number];

export type SlotRenderSource = "GOLDEN_FIXTURE" | "RUNTIME";

export type CustomerMode = "customer";

export type AdapterLocale = "vi";

export const PURPOSE_CONTEXT_VALUES = [
  "phone_number",
  "car_plate",
  "motorcycle_plate",
  "motorbike_plate",
  "id_number",
] as const;

export type PurposeContextValue = (typeof PURPOSE_CONTEXT_VALUES)[number];

/** G21: API motorbike_plate aliases Presentation motorcycle_plate. */
export const PURPOSE_CONTEXT_ALIASES = {
  motorbike_plate: "motorcycle_plate",
  motorcycle_plate: "motorcycle_plate",
  phone_number: "phone_number",
  car_plate: "car_plate",
  id_number: "id_number",
} as const;

export const PURPOSE_CONTEXT_CUSTOMER_LABEL = {
  phone_number: "Số điện thoại",
  car_plate: "Biển số Ô tô/Xe máy",
  motorcycle_plate: "Biển số Ô tô/Xe máy",
  motorbike_plate: "Biển số Ô tô/Xe máy",
  id_number: "Số CCCD/Hộ chiếu",
} as const;

export const GOLDEN_PHONE_DISPLAY_EXAMPLE = {
  originalInput: "0328278786",
  groupedDisplay: "0328 278 786",
} as const;

export type CustomerCategoryLabel = "Cát" | "Hung";

export type CustomerStrengthLabel = "Nhẹ" | "Mạnh";

/**
 * Approved kind → category map. Prefer canonical PairOccurrence.category
 * once RB05-A emits it. Never render English kind in Customer Mode.
 */
export const KIND_TO_CATEGORY = {
  supportive: "Cát",
  challenging: "Hung",
} as const;

export const EIGHT_ENERGY_IDS = [
  "SINH_KHI",
  "THIEN_Y",
  "DIEN_NIEN",
  "PHUC_VI",
  "HOA_HAI",
  "NGU_QUY",
  "LUC_SAT",
  "TUYET_MENH",
] as const;

export type EightEnergyId = (typeof EIGHT_ENERGY_IDS)[number];

export type TripleInterpretationStatus = "DEFINED" | "UNDEFINED";

export type RuntimeGapId =
  | "G01"
  | "G02"
  | "G03"
  | "G04"
  | "G05"
  | "G06"
  | "G07"
  | "G08"
  | "G09"
  | "G10"
  | "G11"
  | "G12"
  | "G13"
  | "G14"
  | "G15"
  | "G16"
  | "G17"
  | "G18"
  | "G19"
  | "G20"
  | "G21";

export const RUNTIME_GAP_STATUS = "RUNTIME_GAP" as const;

export type RuntimeGapStatus = typeof RUNTIME_GAP_STATUS | FieldStatus;

export type RuntimeGap = {
  id: RuntimeGapId;
  slot: PresentationSlotId;
  status: RuntimeGapStatus;
  message: string;
};

export const CUSTOMER_DO_NOT_BIND_FIELDS = [
  "occurrence_id",
  "source_span",
  "energy_id",
  "strength_rank",
  "classification",
  "classification_label",
  "state",
  "sequence_state",
  "via_modifier",
  "analyzed_input",
  "analysis_body",
  "force_level",
  "kind",
  "request_id",
  "cccd_note",
  "knowledge_version",
  "engine_version",
  "raw_digits",
  "fixture_id",
  "verified_by_runtime",
  "narrative.paragraphs",
] as const;

export type AdapterIdentityInput = {
  original_input: string;
  display_value?: string | null;
  analysis_body?: string | null;
};

export type CanonicalPairOccurrence = {
  occurrence_id?: string;
  digits: string;
  energy_label: string;
  category?: CustomerCategoryLabel | null;
  strength_label?: CustomerStrengthLabel | null;
  strength_level?: number | null;
  position_zone?: string | null;
  distance_to_tail?: number | null;
};

export type PairSummary = {
  pair_count: number;
  favorable_count: number;
  challenging_count: number;
};

export type EnergyDistributionInput = {
  counts: Record<EightEnergyId, number>;
};

export type CanonicalTripleOccurrence = {
  digits: string;
  source_label?: string | null;
  target_label?: string | null;
  canonical_meaning_key?: string | null;
  customer_summary_key?: string | null;
  interpretation_status?: TripleInterpretationStatus | null;
  domains?: readonly string[] | null;
  priority?: "featured" | "standard" | "compact" | null;
};

export type CanonicalChain = {
  primary_energy_label: string;
  secondary_energy_labels?: readonly string[] | null;
  terminal_energy_label: string;
  terminal_pair_digits?: string | null;
  terminal_state?: string | null;
};

export type CanonicalWealthStage = {
  id: "WF-01" | "WF-02" | "WF-03" | "WF-04";
  label_key: string;
  headline_key: string;
  evidence: string;
  interaction_key?: string | null;
  narrative_key: string;
};

export type CanonicalWealthFlow = {
  stages: readonly CanonicalWealthStage[];
  story_keys: readonly string[];
  synthesis_key: string;
  later_outcome_key?: string | null;
};

export type CanonicalFinding = {
  finding_id: string;
  domain: string;
  semantic_key: string;
  evidence_refs: readonly string[];
  narrative_keys?: readonly string[] | null;
};

export type CanonicalScore = {
  final_score: number;
  grade: string;
  energy_structure_score: { earned: number; max: number };
  wealth_flow_score: { earned: number; max: number };
  career_support_score: { earned: number; max: number };
  stability_risk_score: { earned: number; max: number };
  tail_score: { earned: number; max: number };
  score_reasons: readonly { reason_key: string }[];
  verified_by_runtime: boolean;
};

export type CanonicalRecommendation = {
  state: string;
  copy_key: string;
  supporting_key?: string | null;
};

export type CanonicalEvidence = {
  groups: readonly { group_key: string; item_keys: readonly string[] }[];
};

/**
 * Interim live-payload slice. Only listed fields may be read.
 * Do not pass narrative.paragraphs, metadata.summary, or occurrences technical fields.
 */
export type LegacySafeAnalyzeSlice = {
  input_raw?: string | null;
  purpose_context?: string | null;
  display_number?: string | null;
  pairs?: readonly {
    pair_digits: string;
    display_name: string;
    kind?: keyof typeof KIND_TO_CATEGORY | string | null;
  }[] | null;
  triplets?: readonly {
    digits: string;
    left_name?: string | null;
    right_name?: string | null;
  }[] | null;
};

export type NumberEnergyAdapterInput = {
  locale: AdapterLocale;
  mode: CustomerMode;
  purpose_context: PurposeContextValue;
  identity: AdapterIdentityInput;
  pair_occurrences?: readonly CanonicalPairOccurrence[] | null;
  pair_summary?: PairSummary | null;
  energy_distribution?: EnergyDistributionInput | null;
  triple_occurrences?: readonly CanonicalTripleOccurrence[] | null;
  chain?: CanonicalChain | null;
  wealth_flow?: CanonicalWealthFlow | null;
  findings?: readonly CanonicalFinding[] | null;
  score?: CanonicalScore | null;
  recommendation?: CanonicalRecommendation | null;
  evidence?: CanonicalEvidence | null;
  expert_trace?: unknown;
  legacy?: LegacySafeAnalyzeSlice | null;
};

/**
 * Live analyze `data` object from RB05-A/B/C/D/F/E.
 * Adapter may also receive `{ data: payload }` envelopes.
 */
export type NumberEnergyRuntimePayload = {
  locale?: AdapterLocale;
  mode?: CustomerMode;
  purpose_context?: string | null;
  identity?: AdapterIdentityInput | null;
  metadata?: {
    input_raw?: string | null;
    purpose_context?: string | null;
  } | null;
  input_raw?: string | null;
  reading?: { display_number?: string | null } | null;
  pair_occurrences?: readonly unknown[] | null;
  pair_summary?: unknown;
  energy_distribution?: unknown;
  triple_occurrences?: readonly unknown[] | null;
  chain?: unknown;
  wealth_flow?: unknown;
  wealth_story?: unknown;
  later_outcome?: unknown;
  domain_insights?: readonly unknown[] | null;
  strengths?: readonly unknown[] | null;
  cautions?: readonly unknown[] | null;
  evidence?: unknown;
  assessment?: unknown;
  recommendation?: unknown;
  score?: unknown;
  grade?: string | null;
  verified_by_runtime?: boolean | null;
  data?: NumberEnergyRuntimePayload | null;
};

export type NumberEnergyAdapterSource =
  | NumberEnergyAdapterInput
  | NumberEnergyRuntimePayload;

export type PresentationHero = {
  eyebrow: string;
  analysisTypeLabel: string;
  displayValue: string;
  scoreDisplay: string;
  grade: string;
  primaryLabel: string;
  primaryEnergy: string;
  primaryKeywords: string;
  terminalLabel: string;
  terminalEnergy: string;
  terminalKeywords: string;
  summary: string;
};

export type PresentationPairCard = {
  digits: string;
  energyLabel: string;
  categoryLabel: CustomerCategoryLabel;
  strengthLabel: CustomerStrengthLabel;
  strengthDots: readonly [boolean, boolean, boolean, boolean];
  keywords: string;
};

export type PresentationQuickStructure = {
  favorableLabel: string;
  favorableValue: string;
  challengingLabel: string;
  challengingValue: string;
  primaryLabel: string;
  primaryValue: string;
  terminalLabel: string;
  terminalValue: string;
  summary: string;
};

export type PresentationWealthStage = {
  id: "WF-01" | "WF-02" | "WF-03" | "WF-04";
  label: string;
  headline: string;
  evidence: string;
  interaction: string;
  narrative: string;
};

export type PresentationWealthFlow = {
  stages: readonly PresentationWealthStage[];
  story: readonly string[];
  synthesis: string;
};

export type PresentationTripleCard = {
  digits: string;
  sourceLabel: string;
  targetLabel: string;
  title: string;
  narrative: string;
  domains: string;
  priority: "featured" | "standard" | "compact";
};

export type PresentationDistributionRow = {
  label: string;
  count: number;
  role: "primary" | "secondary" | "none";
};

export type PresentationDomainCard = {
  title: string;
  conclusion: string;
  narrative: string;
  caution: string;
};

export type PresentationFindingCard = {
  title: string;
  copy: string;
};

export type PresentationFindings = {
  strengths: readonly PresentationFindingCard[];
  cautions: readonly PresentationFindingCard[];
};

export type PresentationScoreDimension = {
  label: string;
  earned: number;
  max: number;
};

export type PresentationScoreReason = {
  title: string;
  copy: string;
};

export type PresentationScore = {
  totalDisplay: string;
  grade: string;
  note: string;
  breakdown: readonly PresentationScoreDimension[];
  reasons: readonly PresentationScoreReason[];
};

export type PresentationAssessment = {
  title: string;
  story: readonly string[];
  flow: readonly string[];
  recommendationTitle: string;
  recommendationState: string;
  recommendationSupporting: string;
};

export type PresentationBasis = {
  title: string;
  helper: string;
  principles: readonly string[];
  highlights: readonly { label: string; value: string }[];
  evidence: readonly { group: string; items: readonly string[] }[];
};

export type PresentationExpertSeam = {
  visible: false;
  hidden: true;
  ariaHidden: true;
};

export type NumberEnergyPresentationView = {
  hero: PresentationHero;
  pairs: readonly PresentationPairCard[];
  quick_structure: PresentationQuickStructure;
  wealth_flow: PresentationWealthFlow;
  triples: readonly PresentationTripleCard[];
  distribution: readonly PresentationDistributionRow[];
  domains: readonly PresentationDomainCard[];
  findings: PresentationFindings;
  score: PresentationScore;
  assessment: PresentationAssessment;
  basis: PresentationBasis;
  expert_seam: PresentationExpertSeam;
};

export type NumberEnergyAdapterResult = {
  freezeLabel: typeof NUMBER_ENERGY_CONTRACT_FREEZE;
  view: NumberEnergyPresentationView;
  slotSource: Record<PresentationSlotId, SlotRenderSource>;
  gaps: readonly RuntimeGap[];
};

/** Maps runtime/API payload to the frozen Customer view. Implemented in RB06. */
export type NumberEnergyPresentationAdapter = (
  input: NumberEnergyAdapterSource,
) => NumberEnergyAdapterResult;

export const SLOT_ENGINE_REQUIREMENT: Record<PresentationSlotId, FieldStatus> = {
  "P-S00": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S01": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S02": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S03": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S04": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S05": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S06": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S07": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S08": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S09": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S10": FIELD_STATUS.REQUIRES_ENGINE,
  "P-S11": FIELD_STATUS.DO_NOT_BIND,
};

export const CURRENT_PAYLOAD_SAFE_FIELDS: Record<string, FieldStatus> = {
  "identity.original_input": FIELD_STATUS.PRESENT_FROM_CURRENT_PAYLOAD,
  "identity.display_value": FIELD_STATUS.ADAPTER_DERIVED_SAFE,
  "purpose_context": FIELD_STATUS.ADAPTER_DERIVED_SAFE,
  "legacy.pairs.pair_digits": FIELD_STATUS.PRESENT_FROM_CURRENT_PAYLOAD,
  "legacy.pairs.display_name": FIELD_STATUS.PRESENT_FROM_CURRENT_PAYLOAD,
  "legacy.triplets.digits": FIELD_STATUS.PRESENT_FROM_CURRENT_PAYLOAD,
  "pair_summary": FIELD_STATUS.REQUIRES_ENGINE,
  "energy_distribution": FIELD_STATUS.REQUIRES_ENGINE,
  "chain": FIELD_STATUS.REQUIRES_ENGINE,
  "wealth_flow": FIELD_STATUS.REQUIRES_ENGINE,
  "findings": FIELD_STATUS.REQUIRES_ENGINE,
  "score": FIELD_STATUS.REQUIRES_ENGINE,
  "recommendation": FIELD_STATUS.REQUIRES_ENGINE,
  "evidence": FIELD_STATUS.REQUIRES_ENGINE,
  "expert_trace": FIELD_STATUS.DO_NOT_BIND,
};

export const FALLBACK_POLICY = {
  missingSlotUsesGoldenFixture: true,
  reportRuntimeGap: true,
  doNotEditGoldenFixture: true,
  freezeUnchanged: true,
  expertSeamHiddenByDefault: true,
} as const;
