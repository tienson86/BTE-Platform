/**
 * Canonical Pattern V1.0 presentation helpers.
 * Primary identification = data.pattern.cach_cuc. Does not recompute cách.
 */

import type { AnalysisDataDto } from "../models";

export function canonicalPatternLabel(
  data: Pick<AnalysisDataDto, "pattern"> | null | undefined,
): string {
  const pattern = data?.pattern;
  if (!pattern || typeof pattern !== "object") return "";
  const row = pattern as Record<string, unknown>;
  return String(row.cach_cuc || "").trim() || String(row.pattern || "").trim();
}

export function canonicalPatternEvidence(
  data: Pick<AnalysisDataDto, "pattern"> | null | undefined,
): string {
  const pattern = data?.pattern;
  if (!pattern || typeof pattern !== "object") return "";
  const row = pattern as Record<string, unknown>;
  return String(row.evidence_compact || "").trim();
}
