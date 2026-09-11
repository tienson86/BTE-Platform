export const PURPOSE_CONTEXTS = [
  "generic_number",
  "phone_number",
  "car_plate",
  "motorbike_plate",
  "id_number",
  "bank_account",
  "house_number",
] as const;

export type PurposeContext = (typeof PURPOSE_CONTEXTS)[number];

export type NumberEnergyOccurrence = {
  occurrence_id: string;
  source_span: number[];
  source_digits: string;
  pair_digits: string;
  energy_id: string;
  display_name: string;
  strength_rank: number | null;
  classification: string;
  classification_label?: string;
  state: string;
  via_modifier: number | null;
  notes: string;
};

export type NumberEnergyWarning = {
  code: string;
  reason: string;
  customer_reason?: string;
  source_digits: string;
  source_span: number[];
};

export type NumberEnergyNarrative = {
  language?: string;
  system_name?: string;
  system_short_name?: string;
  summary?: string;
  paragraphs?: string[];
  strengths?: string[];
  watchouts?: string[];
  purpose_focus?: string;
  health_disclaimer?: string | null;
  compatibility_note?: string;
  unknown_notice?: string | null;
};

export type NumberEnergyMetadata = {
  engine?: string;
  engine_version?: string;
  knowledge_version?: string;
  system_name?: string;
  system_short_name?: string;
  purpose_context?: string;
  input_raw?: string;
  raw_digits?: number[];
  sequence_states?: string[];
  summary?: Record<string, unknown>;
  pattern_labels?: string[];
};

export type NumberEnergyData = {
  occurrences: NumberEnergyOccurrence[];
  sequence_state: string;
  patterns: string[];
  narrative: NumberEnergyNarrative;
  warnings: NumberEnergyWarning[];
  metadata: NumberEnergyMetadata;
};

export type NumberEnergyEnvelope = {
  success?: boolean;
  message?: string;
  data?: NumberEnergyData | null;
  request_id?: string | null;
  code?: string;
  details?: unknown;
  detail?: unknown;
};
