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

/**
 * Copy canonical Pattern labels into the Card view. Does not classify cách.
 */
export function adaptPatternCard(data: AnalysisDataDto | null | undefined): PatternView {
  const row = asRecord(data?.pattern);
  const primary = customerLabel(canonicalPatternLabel(data));
  return {
    title: PATTERN_TITLE,
    available: Boolean(primary),
    primary,
    status: copyStatus(row),
    secondary: copySecondary(row),
    formation: copyFormation(row),
    summary: copySummary(row),
  };
}
