/**
 * Canonical Strength V1.0 binding helpers.
 * Điểm thân = data.strength.strength_score only. Never score.strength_score.
 */

import type { AnalysisDataDto } from "../models";

export const STRENGTH_LEVEL_LABELS: Record<string, string> = {
  weak: "Thân nhược",
  balanced: "Thân cân bằng",
  strong: "Thân vượng",
};

/**
 * Read the canonical Strength score (0–1). Ignores Score Engine.
 */
export function readCanonicalStrengthScore(
  data: Pick<AnalysisDataDto, "strength"> | null | undefined,
): number | null {
  const raw = data?.strength?.strength_score;
  if (raw === null || raw === undefined) return null;
  const n = Number(raw);
  if (!Number.isFinite(n)) return null;
  return n;
}

/**
 * Format canonical Strength for display. Keep 0.87 as "0.87".
 */
export function formatCanonicalStrengthScore(score: number): string {
  if (score >= 0 && score <= 1) {
    return (Math.round(score * 100) / 100).toFixed(2);
  }
  return String(score);
}

/**
 * Meter width only. 0.87 → 87. Does not write back into analysis.
 */
export function canonicalStrengthMeterPercent(score: number): number {
  if (score >= 0 && score <= 1) {
    return Math.round(score * 100);
  }
  return Math.min(100, Math.max(0, Math.round(score)));
}

/**
 * V1.0 class label from strength.strength_level. Does not use Pattern.than.
 */
export function canonicalStrengthLabel(
  data: Pick<AnalysisDataDto, "strength"> | null | undefined,
): string {
  const level = String(data?.strength?.strength_level || "")
    .trim()
    .toLowerCase();
  return STRENGTH_LEVEL_LABELS[level] || "";
}

/**
 * Compact evidence already published by StrengthView.
 */
export function canonicalStrengthEvidence(
  data: Pick<AnalysisDataDto, "strength"> | null | undefined,
): string {
  const extra = data?.strength as { evidence_compact?: unknown } | undefined;
  const text = String(extra?.evidence_compact || "").trim();
  if (text) return text;
  return String(data?.strength?.reasoning || "").trim();
}
