/**
 * Bind ShenSha Card from canonical matches + approved ShenSha knowledge.
 * Does not classify categories or invent interpretation.
 */

import { approvedShenShaMeaning } from "../../adapters/shenShaApprovedKnowledge";
import { stripInternalRuleIds } from "../../adapters/customerFacingPresentation";
import type {
  AnalysisDataDto,
  ShenShaEcosystemDto,
  ShenShaMatchDto,
  ShenShaStarItemDto,
} from "../../models";
import { SHENSHA_SUPPORTING_NOTE, SHENSHA_TITLE } from "./cards";
import type {
  ShenShaClusterView,
  ShenShaEcosystemView,
  ShenShaGroupView,
  ShenShaItemView,
  ShenShaView,
} from "./types";

const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;
const TECHNICAL_EVIDENCE = /→|TIAN_|YUE_|HONG_|HUA_|WEN_|rule_|append|detector|source_value|target_value/i;
const TECHNICAL_MEANING = /TIAN_|YUE_|HONG_|append|detector|engine|\{/;
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
const MEANING_KEYS = ["customer_meaning", "y_nghia"] as const;
const SUMMARY_KEYS = ["summary", "customer_summary", "shensha_summary"] as const;

function text(value: unknown): string {
  if (typeof value === "string") return value.trim();
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  return "";
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
    if (label && !TECHNICAL_MEANING.test(label)) return label;
  }
  return "";
}

function pillarDisplay(value: string): string {
  const key = text(value);
  if (!key) return "";
  return PILLAR_LABELS[key] || (TECHNICAL_TOKEN.test(key) ? "" : key);
}

function copyPillars(match: ShenShaMatchDto): string[] {
  const fromOccurrences = unique(
    (match.occurrences ?? [])
      .map((item) => pillarDisplay(text(item.pillar)))
      .filter(Boolean),
  );
  if (fromOccurrences.length) return fromOccurrences;
  const single = pillarDisplay(text(match.pillar));
  return single ? [single] : [];
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

function emptyItem(name: string): ShenShaItemView {
  return {
    name,
    placement: "",
    meaning: "",
    chartRelevance: "",
    evidence: "",
    category: "",
    stateLabel: "",
    explanation: "",
  };
}

function copyEvidence(match: ShenShaMatchDto): string {
  const raw = customerLabel(stripInternalRuleIds(text(match.evidence_text)));
  if (!raw || TECHNICAL_EVIDENCE.test(raw)) return "";
  return raw;
}

function copyItem(match: ShenShaMatchDto): ShenShaItemView | null {
  const row = match as ShenShaMatchDto & Record<string, unknown>;
  const name = customerLabel(text(match.canonical_name || match.name));
  if (!name) return null;
  const pillars = copyPillars(match);
  const placement = pillars.map((pillar) => `Trụ ${pillar}`).join(" · ");
  const payloadMeaning = firstText(row, MEANING_KEYS);
  return {
    name,
    placement,
    meaning: approvedShenShaMeaning(name) || payloadMeaning,
    chartRelevance: pillars.length ? `Xuất hiện tại trụ ${pillars.join(" · ")}.` : "",
    evidence: copyEvidence(match),
    category: firstText(row, CATEGORY_KEYS),
    stateLabel: "",
    explanation: "",
  };
}

function copyFromNames(names: readonly string[] | undefined): ShenShaItemView[] {
  return (names ?? [])
    .map((name) => customerLabel(text(name)))
    .filter(Boolean)
    .map((name) => ({
      ...emptyItem(name),
      meaning: approvedShenShaMeaning(name),
    }));
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
 * Join canonical ShenSha matches with approved knowledge. Does not calculate stars.
 * Pack 07 overlay replaces dictionary prose when structured interpretation is present.
 */
export function adaptShenShaCard(data: AnalysisDataDto | null | undefined): ShenShaView {
  const matches = data?.bazi?.shensha_matches ?? [];
  const fromMatches = matches.map(copyItem).filter((item): item is ShenShaItemView => Boolean(item));
  const items = fromMatches.length ? fromMatches : copyFromNames(data?.bazi?.shensha);
  const pack07 = overlayPack07(items, data);
  const groups = pack07.usePack07 ? [] : groupPublished(pack07.items);
  return {
    title: SHENSHA_TITLE,
    available: pack07.items.length > 0,
    grouped: groups.length > 0,
    groups,
    items: pack07.items,
    summary: pack07.usePack07 ? "" : copySummary(data ?? {}),
    note: pack07.items.length ? `Lưu ý: ${SHENSHA_SUPPORTING_NOTE}` : "",
    usePack07: pack07.usePack07,
    ecosystem: pack07.ecosystem,
  };
}

function overlayPack07(
  items: readonly ShenShaItemView[],
  data: AnalysisDataDto | null | undefined,
): { items: ShenShaItemView[]; usePack07: boolean; ecosystem: ShenShaEcosystemView | null } {
  const block = data?.bazi?.shen_sha;
  const detailed = block?.individual?.items ?? [];
  if (!detailed.length) {
    return { items: [...items], usePack07: false, ecosystem: null };
  }
  const byName = new Map<string, ShenShaStarItemDto>();
  for (const row of detailed) {
    const name = customerLabel(text(row.name));
    if (name) byName.set(name, row);
  }
  const merged = items.map((item) => {
    const row = byName.get(item.name);
    if (!row) {
      return {
        ...item,
        meaning: "",
        explanation: "Tín hiệu phụ; chưa gắn kết luận cấu trúc.",
        stateLabel: "Chưa đủ dữ liệu",
      };
    }
    const explanation = customerLabel(text(row.explanation));
    return {
      ...item,
      meaning: "",
      category: customerLabel(text(row.category)) || item.category,
      placement: customerLabel(text(row.placement)) || item.placement,
      stateLabel: customerLabel(text(row.state_label)) || "Chưa đủ dữ liệu",
      explanation,
    };
  });
  const known = new Set(merged.map((item) => item.name));
  for (const row of detailed) {
    const name = customerLabel(text(row.name));
    if (!name || known.has(name)) continue;
    merged.push({
      ...emptyItem(name),
      category: customerLabel(text(row.category)),
      placement: customerLabel(text(row.placement)),
      stateLabel: customerLabel(text(row.state_label)) || "Chưa đủ dữ liệu",
      explanation: customerLabel(text(row.explanation)),
    });
  }
  return { items: merged, usePack07: true, ecosystem: copyEcosystem(block?.ecosystem) };
}

function copyEcosystem(raw: ShenShaEcosystemDto | undefined): ShenShaEcosystemView | null {
  if (!raw) return null;
  const clusters: ShenShaClusterView[] = (raw.clusters ?? [])
    .filter((item) => item.prominent !== false)
    .map((item) => ({
      name: customerLabel(text(item.name)),
      stateLabel: customerLabel(text(item.state_label)),
      explanation: customerLabel(text(item.explanation)),
      warning: Boolean(item.warning),
      unresolved: Boolean(item.unresolved),
    }))
    .filter((item) => item.name);
  return {
    dominant: customerLabel(text(raw.dominant)),
    dominantUnresolved: Boolean(raw.dominant_unresolved),
    supporting: customerLabel(text(raw.supporting)),
    warning: customerLabel(text(raw.warning)),
    unresolvedLabel: customerLabel(text(raw.unresolved_label)),
    clusters,
  };
}
