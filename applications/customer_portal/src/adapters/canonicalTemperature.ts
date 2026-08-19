/**
 * Canonical Temperature / Điều hậu V1.0 presentation helpers.
 * Climate state comes from data.temperature. Does not recompute score.
 * Does not read pattern.dieu_hau (that field is month 得令, not Điều hậu).
 */

import type { AnalysisDataDto } from "../models";

const CLIMATE_STATE_LABELS: Record<string, string> = {
  cold: "Hàn",
  cool: "Lương",
  warm: "Ôn",
  hot: "Nhiệt",
};

const BALANCING_NEED_LABELS: Record<string, string> = {
  warming: "Cần ôn ấm",
  cooling: "Cần làm mát",
  balance: "Cần cân Hỏa Thủy",
};

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function text(value: unknown): string {
  return String(value ?? "").trim();
}

export function canonicalClimateState(
  data: Pick<AnalysisDataDto, "temperature"> | null | undefined,
): string {
  const row = asRecord(data?.temperature);
  return text(row.climate_state) || text(row.temperature_level);
}

export function canonicalClimateStateLabel(
  data: Pick<AnalysisDataDto, "temperature"> | null | undefined,
): string {
  const row = asRecord(data?.temperature);
  const labeled = text(row.climate_state_label);
  if (labeled) return labeled;
  const state = canonicalClimateState(data);
  return CLIMATE_STATE_LABELS[state] || state;
}

export function canonicalBalancingNeed(
  data: Pick<AnalysisDataDto, "temperature"> | null | undefined,
): string {
  const row = asRecord(data?.temperature);
  return text(row.balancing_need);
}

export function canonicalBalancingNeedLabel(
  data: Pick<AnalysisDataDto, "temperature"> | null | undefined,
): string {
  const row = asRecord(data?.temperature);
  const labeled = text(row.balancing_need_label);
  if (labeled) return labeled;
  const need = canonicalBalancingNeed(data);
  return BALANCING_NEED_LABELS[need] || need;
}

export function canonicalTemperatureEvidence(
  data: Pick<AnalysisDataDto, "temperature"> | null | undefined,
): string {
  const row = asRecord(data?.temperature);
  return text(row.evidence_compact);
}

export function canonicalTemperatureScore(
  data: Pick<AnalysisDataDto, "temperature"> | null | undefined,
): string {
  const row = asRecord(data?.temperature);
  const raw = row.temperature_score;
  if (typeof raw !== "number" || !Number.isFinite(raw)) return "";
  return raw.toFixed(2);
}
