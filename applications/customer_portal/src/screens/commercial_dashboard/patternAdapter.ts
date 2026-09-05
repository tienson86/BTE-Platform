/**
 * Bind Pattern Card from canonical analysis. Copy published fields only.
 */

import { canonicalPatternLabel } from "../../adapters/canonicalPattern";
import { stripInternalRuleIds } from "../../adapters/customerFacingPresentation";
import type { AnalysisDataDto } from "../../models";
import { PATTERN_TITLE } from "./cards";
import type { PatternView } from "./types";

const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;
const TRUSTED_STATUS = new Set(["Đắc cách", "Bán cách", "Phá cách", "Thành cách"]);
const STATUS_KEYS = ["status", "pattern_status", "quality", "pattern_quality", "dac_cach"] as const;
const SECONDARY_KEYS = ["secondary_pattern", "phu_cach", "phu_cach_label"] as const;
const SUMMARY_KEYS = ["summary", "customer_summary", "pattern_summary", "tom_tat"] as const;
const FORMATION_ARRAY_KEYS = ["formation", "formation_steps", "evidence"] as const;

function text(value: unknown): string {
  if (value == null) return "";
  return String(value).trim();
}

function customerLabel(value: string): string {
  const next = text(value);
  if (!next || TECHNICAL_TOKEN.test(next)) return "";
  return next;
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function firstText(row: Record<string, unknown>, keys: readonly string[]): string {
  for (const key of keys) {
    const label = customerLabel(text(row[key]));
    if (label) return label;
  }
  return "";
}

function stringList(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => customerLabel(stripInternalRuleIds(text(item)))).filter(Boolean);
}

function trustedStatus(value: string): string {
  const label = customerLabel(value);
  return TRUSTED_STATUS.has(label) ? label : "";
}

function copyStatus(row: Record<string, unknown>): string {
  for (const key of STATUS_KEYS) {
    const status = trustedStatus(text(row[key]));
    if (status) return status;
  }
  return "";
}

function copySecondary(row: Record<string, unknown>): string {
  const named = firstText(row, SECONDARY_KEYS);
  if (named) return named;
  const listed = stringList(row.secondary_patterns);
  return listed[0] || "";
}

function splitCompact(value: string): string[] {
  const cleaned = stripInternalRuleIds(value);
  if (!cleaned) return [];
  return cleaned
    .split(/\s·\s|[.;\n]+/)
    .map((part) => customerLabel(part.replace(/^rule\s+/i, "").trim()))
    .filter(Boolean);
}

function copyFormation(row: Record<string, unknown>): string[] {
  for (const key of FORMATION_ARRAY_KEYS) {
    const steps = stringList(row[key]);
    if (steps.length) return steps;
  }
  return splitCompact(text(row.evidence_compact));
}

function copySummary(row: Record<string, unknown>): string {
  for (const key of SUMMARY_KEYS) {
    const label = customerLabel(stripInternalRuleIds(text(row[key])));
    if (label) return label;
  }
  return "";
}

const PURITY_LABEL: Record<string, string> = {
  very_pure: "Rất thuần",
  pure: "Thuần",
  moderately_pure: "Thuần vừa",
  mixed: "Pha tạp",
  heavily_mixed: "Pha tạp mạnh",
  structurally_impure: "Không thuần cấu trúc",
};

const STRENGTH_LABEL: Record<string, string> = {
  very_strong: "Rất mạnh",
  strong: "Mạnh",
  moderate: "Vừa",
  weak: "Yếu",
  very_weak: "Rất yếu",
};

const INTEGRITY_LABEL: Record<string, string> = {
  complete: "Toàn vẹn",
  substantially_complete: "Gần toàn vẹn",
  conditionally_complete: "Toàn vẹn có điều kiện",
  mixed: "Hỗn hợp",
  damaged_but_rescued: "Tổn thương đã cứu",
  damaged: "Tổn thương",
  failed: "Không giữ được",
};

const GRADE_LABEL = new Set(["SS", "S", "A", "B", "C", "D"]);

function nestedText(row: Record<string, unknown>, keys: readonly string[]): string {
  for (const key of keys) {
    const value = row[key];
    if (value && typeof value === "object" && !Array.isArray(value)) {
      const nested = value as Record<string, unknown>;
      const mapped = nestedText(nested, ["classification", "state", "grade", "label"]);
      if (mapped) return mapped;
    }
    const raw = text(value);
    if (raw) return raw;
  }
  return "";
}

function copyMingJuField(
  mingju: Record<string, unknown>,
  keys: readonly string[],
  labels: Record<string, string> | Set<string>,
): string {
  const raw = nestedText(mingju, keys);
  if (!raw) return "";
  if (labels instanceof Set) return labels.has(raw) ? raw : "";
  return labels[raw] || customerLabel(raw);
}

/**
 * Copy canonical Pattern labels into the Card view. Does not classify cách.
 */
export function adaptPatternCard(data: AnalysisDataDto | null | undefined): PatternView {
  const row = asRecord(data?.pattern);
  const mingju = asRecord(data?.mingju);
  const primary = customerLabel(canonicalPatternLabel(data)) || customerLabel(nestedText(mingju, ["pattern"]));
  const summary =
    copySummary(row) || customerLabel(nestedText(asRecord(mingju.decision), ["summary", "headline"]));
  return {
    title: PATTERN_TITLE,
    available: Boolean(primary),
    primary,
    status: copyStatus(row),
    secondary: copySecondary(row),
    formation: copyFormation(row),
    summary,
    purity: customerLabel(text(row.structural_purity)) || copyMingJuField(mingju, ["purity"], PURITY_LABEL),
    patternStrength:
      customerLabel(text(row.structural_strength)) || copyMingJuField(mingju, ["pattern_strength"], STRENGTH_LABEL),
    integrity:
      customerLabel(text(row.structural_integrity)) || copyMingJuField(mingju, ["integrity"], INTEGRITY_LABEL),
    grade: copyMingJuField({ grade: row.structural_grade }, ["grade"], GRADE_LABEL) || copyMingJuField(mingju, ["grade"], GRADE_LABEL),
  };
}
