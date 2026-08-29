/**
 * Bind Action Plan from published consulting and narrative recommendations.
 * Copy only. Does not infer actions from raw chart facts.
 */

import { isTechnicalRuleText } from "../../adapters/contentGuards";
import { asNarrativeResult } from "../../adapters/narrativeResultAdapter";
import type { AnalysisDataDto } from "../../models";
import { ACTION_PLAN_EMPTY, ACTION_PLAN_TITLE } from "./cards";
import type { ActionItemView, ActionPlanView } from "./types";

const ACTION_LIMIT = 6;
const RULE_ID = /\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|spe|cmb|root)_[a-z0-9_]+\b/gi;
const TECHNICAL =
  /\{|\}|dayun_runtime|source_unit|rule_id|catalog_id|schema_version|UNKNOWN|matcher|engine_id|chưa đủ căn cứ|đã công bố/i;
const FEAR = /chắc chắn thất bại|chắc chắn ly hôn|tai họa|bệnh nặng|đại hung/;
const GENERIC = /sống tích cực|cố gắng hơn|giữ tinh thần lạc quan|làm việc chăm chỉ/;
const RAW_LABEL = /^(bổ hỏa|giảm kim|dùng dụng thần|tránh kỵ thần)$/i;
const PREFIX = /^(?:\d+\.\s*)?(?:xây|làm|củng cố|tránh|hạn chế)\s*:\s*/i;
const WATCH_INTENT = /current|watch|giai đoạn hiện tại|current.period|luck.advice/i;
const WATCH_DOMAIN = /luck|vận|giai đoạn/i;

type Draft = {
  readonly title: string;
  readonly detail: string;
  readonly domain: string;
  readonly source: string;
};

function text(value: unknown): string {
  if (typeof value !== "string") return "";
  return value.trim();
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function customerLine(value: unknown): string {
  let raw = text(value).replace(RULE_ID, " ").replace(/\s{2,}/g, " ").trim();
  if (!raw || isTechnicalRuleText(raw)) return "";
  if (TECHNICAL.test(raw) || FEAR.test(raw) || GENERIC.test(raw)) return "";
  return raw;
}

function splitItem(raw: string, domain: string, source: string): Draft | null {
  const cleaned = raw.replace(/^\d+\.\s*/, "").replace(PREFIX, "").trim();
  if (!cleaned || RAW_LABEL.test(cleaned) || !cleaned.replace(/[.,·\s]/g, "")) return null;
  const match = cleaned.match(/^(.+?[.。])(?:\s+|$)([\s\S]*)$/);
  const title = (match ? match[1] : cleaned).replace(/[.。]+$/, "").trim();
  const detail = match ? match[2].trim().replace(/[.。]+$/, "") : "";
  if (!title) return null;
  return { title, detail, domain, source };
}

function keyOf(item: Draft): string {
  return `${item.title} ${item.detail}`.toLowerCase().replace(/\s+/g, " ").trim();
}

function isDuplicate(item: Draft, seen: readonly Draft[]): boolean {
  const key = keyOf(item);
  return seen.some((other) => {
    const prior = keyOf(other);
    return key === prior || key.includes(prior) || prior.includes(key);
  });
}

function pushUnique(target: Draft[], item: Draft | null): void {
  if (!item || isDuplicate(item, target)) return;
  target.push(item);
}

function consultingDrafts(data: AnalysisDataDto): Draft[] {
  const consulting = asRecord(data.commercial_consulting);
  if (text(consulting.status) && text(consulting.status) !== "complete") return [];
  const sections = Array.isArray(consulting.sections) ? consulting.sections : [];
  const drafts: Draft[] = [];
  for (const row of sections) {
    const section = asRecord(row);
    const domain = customerLine(section.title);
    for (const rec of Array.isArray(section.recommendations) ? section.recommendations : []) {
      const line = customerLine(rec);
      if (!line) continue;
      pushUnique(drafts, splitItem(line, domain, "commercial_consulting.recommendations"));
    }
  }
  return drafts;
}

function narrativeRecs(data: AnalysisDataDto): Draft[] {
  const narrative = asNarrativeResult(data.narrative_result);
  if (!narrative) return [];
  const drafts: Draft[] = [];
  for (const rec of narrative.recommendations ?? []) {
    const line = customerLine(rec.action);
    if (!line) continue;
    pushUnique(drafts, splitItem(line, "", "narrative_result.recommendations"));
  }
  if (drafts.length) return drafts;
  const summary = asRecord(narrative.summary);
  for (const key of ["priority_recommendation", "next_action"] as const) {
    const line = customerLine(summary[key]);
    if (!line) continue;
    pushUnique(drafts, splitItem(line, "", `narrative_result.summary.${key}`));
  }
  return drafts;
}

function warningDrafts(data: AnalysisDataDto): Draft[] {
  const narrative = asNarrativeResult(data.narrative_result);
  if (!narrative) return [];
  const drafts: Draft[] = [];
  for (const section of narrative.sections ?? []) {
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    if (!/warning|caution|lưu ý|tránh/i.test(blob)) continue;
    for (const paragraph of section.paragraphs ?? []) {
      if (paragraph.insufficient_data) continue;
      const line = customerLine(paragraph.text);
      if (!line) continue;
      pushUnique(drafts, splitItem(line, "", "narrative_result.warning"));
    }
  }
  return drafts;
}

function watchDrafts(data: AnalysisDataDto): Draft[] {
  const drafts: Draft[] = [];
  const luck = asRecord(data.luck);
  for (const key of ["customer_summary", "trend"] as const) {
    const line = customerLine(luck[key]);
    if (!line) continue;
    pushUnique(drafts, splitItem(line, "", `luck.${key}`));
  }
  const narrative = asNarrativeResult(data.narrative_result);
  for (const section of narrative?.sections ?? []) {
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    if (!WATCH_INTENT.test(blob)) continue;
    for (const paragraph of section.paragraphs ?? []) {
      const line = customerLine(paragraph.text);
      if (!line) continue;
      pushUnique(drafts, splitItem(line, "", "narrative_result.watch"));
    }
  }
  const consulting = asRecord(data.commercial_consulting);
  const sections = Array.isArray(consulting.sections) ? consulting.sections : [];
  for (const row of sections) {
    const section = asRecord(row);
    const domain = customerLine(section.title);
    if (!WATCH_DOMAIN.test(`${section.domain ?? ""} ${domain}`)) continue;
    for (const rec of Array.isArray(section.recommendations) ? section.recommendations : []) {
      const line = customerLine(rec);
      if (!line) continue;
      pushUnique(drafts, splitItem(line, domain, "commercial_consulting.watch"));
    }
  }
  return drafts.slice(0, 2);
}

function toView(item: Draft): ActionItemView {
  return {
    title: item.title,
    detail: item.detail,
    domain: item.domain,
    source: item.source,
  };
}

/**
 * Join approved consulting + narrative actions. Does not generate advice.
 */
export function adaptActionPlanCard(data: AnalysisDataDto | null | undefined): ActionPlanView {
  const payload = data ?? {};
  const consulting = consultingDrafts(payload);
  const narrative = narrativeRecs(payload);
  const merged: Draft[] = [];
  for (const item of [...consulting, ...narrative]) pushUnique(merged, item);
  const priority = merged[0] ?? null;
  const rest = priority ? merged.slice(1) : [];
  const visible = rest.slice(0, ACTION_LIMIT);
  const extra = rest.slice(ACTION_LIMIT);
  const warnings = warningDrafts(payload).filter((item) => !isDuplicate(item, merged));
  const watch = watchDrafts(payload).filter((item) => !isDuplicate(item, [...merged, ...warnings]));
  const available = Boolean(priority || visible.length || warnings.length || watch.length);
  return {
    title: ACTION_PLAN_TITLE,
    available,
    emptyMessage: ACTION_PLAN_EMPTY,
    priority: priority ? toView(priority) : null,
    actions: visible.map(toView),
    extraActions: extra.map(toView),
    warnings: warnings.map(toView),
    watch: watch.map(toView),
  };
}
