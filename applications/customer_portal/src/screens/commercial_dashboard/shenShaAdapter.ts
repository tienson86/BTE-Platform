/**
 * Bind ShenSha Card from canonical analysis. Copy published fields only.
 */

import { stripInternalRuleIds } from "../../adapters/customerFacingPresentation";
import type { AnalysisDataDto, ShenShaMatchDto } from "../../models";
import { SHENSHA_SUPPORTING_NOTE, SHENSHA_TITLE } from "./cards";
import type { ShenShaGroupView, ShenShaItemView, ShenShaView } from "./types";

const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;
const PILLAR_LABELS: Record<string, string> = {
  year: "Năm",
  month: "Tháng",
  day: "Ngày",
  hour: "Giờ",
  Năm: "Năm",
  Tháng: "Tháng",
  Ngày: "Ngày",
  Giờ: "Giờ",
};
const CATEGORY_KEYS = ["category", "group", "nhom"] as const;
const MEANING_KEYS = ["meaning", "customer_meaning", "y_nghia"] as const;
const SUMMARY_KEYS = ["summary", "customer_summary", "shensha_summary"] as const;

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
    const label = customerLabel(stripInternalRuleIds(text(row[key])));
    if (label) return label;
  }
  return "";
}

function pillarDisplay(value: string): string {
  const key = text(value);
  if (!key) return "";
  return PILLAR_LABELS[key] || (TECHNICAL_TOKEN.test(key) ? "" : key);
}

function copyPlacement(match: ShenShaMatchDto): string {
  const fromOccurrences = unique(
    (match.occurrences ?? [])
      .map((item) => pillarDisplay(text(item.pillar)))
      .filter(Boolean),
  );
  if (fromOccurrences.length) return fromOccurrences.join(" · ");
  return pillarDisplay(text(match.pillar));
}

function unique(values: readonly string[]): string[] {
  const seen = new Set<string>();
  const next: string[] = [];
  for (const value of values) {
    if (seen.has(value)) continue;
    seen.add(value);
    next.push(value);
  }
  return next;
}

function copyItem(match: ShenShaMatchDto): ShenShaItemView | null {
  const row = match as ShenShaMatchDto & Record<string, unknown>;
  const name = customerLabel(text(match.canonical_name || match.name));
  if (!name) return null;
  return {
    name,
    placement: copyPlacement(match),
    meaning: firstText(row, MEANING_KEYS),
    category: firstText(row, CATEGORY_KEYS),
  };
}

function copyFromNames(names: readonly string[] | undefined): ShenShaItemView[] {
  return (names ?? [])
    .map((name) => customerLabel(text(name)))
    .filter(Boolean)
    .map((name) => ({ name, placement: "", meaning: "", category: "" }));
}

function groupPublished(items: readonly ShenShaItemView[]): ShenShaGroupView[] {
  if (!items.length || items.some((item) => !item.category)) return [];
  const groups: ShenShaGroupView[] = [];
  const index = new Map<string, number>();
  for (const item of items) {
    const existing = index.get(item.category);
    if (existing == null) {
      index.set(item.category, groups.length);
      groups.push({ heading: item.category, items: [item] });
      continue;
    }
    const current = groups[existing];
    groups[existing] = { heading: current.heading, items: [...current.items, item] };
  }
  return groups;
}

function copySummary(data: AnalysisDataDto): string {
  const extra = data as Record<string, unknown>;
  return firstText(asRecord(extra.shensha), SUMMARY_KEYS) || firstText(asRecord(data.bazi), SUMMARY_KEYS);
}

/**
 * Copy canonical ShenSha names and placements. Does not classify or interpret.
 */
export function adaptShenShaCard(data: AnalysisDataDto | null | undefined): ShenShaView {
  const matches = data?.bazi?.shensha_matches ?? [];
  const fromMatches = matches.map(copyItem).filter((item): item is ShenShaItemView => Boolean(item));
  const items = fromMatches.length ? fromMatches : copyFromNames(data?.bazi?.shensha);
  const groups = groupPublished(items);
  return {
    title: SHENSHA_TITLE,
    available: items.length > 0,
    grouped: groups.length > 0,
    groups,
    items,
    summary: copySummary(data ?? {}),
    note: items.length ? SHENSHA_SUPPORTING_NOTE : "",
  };
}
