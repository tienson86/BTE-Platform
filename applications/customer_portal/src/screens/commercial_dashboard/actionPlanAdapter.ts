/**
 * Bind Action Plan from published consulting and narrative recommendations.
 * Copy only. Does not infer actions from raw chart facts.
 */

import { isTechnicalRuleText } from "../../adapters/contentGuards";
import type { AnalysisDataDto } from "../../models";
import { ACTION_PLAN_EMPTY, ACTION_PLAN_TITLE, OPTIMIZATION_LABELS } from "./cards";
import type {
  ActionItemView,
  ActionPlanView,
  OptimizationActionView,
  OptimizationConflictView,
  OptimizationDomainView,
  OptimizationElementView,
  OptimizationPlanView,
  OptimizationPriorityView,
} from "./types";

const ACTION_LIMIT = 6;
const RULE_ID = /\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|spe|cmb|root)_[a-z0-9_]+\b/gi;
const TECHNICAL =
  /\{|\}|dayun_runtime|source_unit|rule_id|catalog_id|schema_version|UNKNOWN|matcher|engine_id|chưa đủ căn cứ|đã công bố/i;
const FEAR = /chắc chắn thất bại|chắc chắn ly hôn|tai họa|bệnh nặng|đại hung/;
const GENERIC = /sống tích cực|cố gắng hơn|giữ tinh thần lạc quan|làm việc chăm chỉ/i
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

function list(value: unknown): readonly unknown[] {
  return Array.isArray(value) ? value : [];
}

function recDraft(rec: Record<string, unknown>, source: string): Draft | null {
  if (rec.insufficient_data) return null;
  const line = customerLine(rec.action);
  if (!line) return null;
  const item = splitItem(line, "", source);
  if (!item) return null;
  if (item.detail) return item;
  const reason = customerLine(rec.reason);
  if (!reason || reason === item.title) return item;
  return { ...item, detail: reason.replace(/[.。]+$/, "") };
}

function narrativeRecs(data: AnalysisDataDto): Draft[] {
  const narrative = asRecord(data.narrative_result);
  const drafts: Draft[] = [];
  for (const row of list(narrative.recommendations)) {
    pushUnique(drafts, recDraft(asRecord(row), "narrative_result.recommendations"));
  }
  for (const row of list(narrative.sections)) {
    const section = asRecord(row);
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    if (!/priority|recommend|khuyến nghị|việc nên/i.test(blob)) continue;
    for (const rec of list(section.recommendations)) {
      pushUnique(drafts, recDraft(asRecord(rec), "narrative_result.section.recommendations"));
    }
    for (const paragraph of list(section.paragraphs)) {
      const item = asRecord(paragraph);
      if (item.insufficient_data) continue;
      const line = customerLine(item.text);
      if (!line) continue;
      pushUnique(drafts, splitItem(line, "", "narrative_result.priority"));
    }
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
  const narrative = asRecord(data.narrative_result);
  const drafts: Draft[] = [];
  for (const row of list(narrative.sections)) {
    const section = asRecord(row);
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    if (!/warning|caution|lưu ý|tránh/i.test(blob)) continue;
    for (const paragraph of list(section.paragraphs)) {
      const item = asRecord(paragraph);
      if (item.insufficient_data) continue;
      const line = customerLine(item.text);
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
    if (!line || line.length < 24) continue;
    pushUnique(drafts, splitItem(line, "", `luck.${key}`));
  }
  const narrative = asRecord(data.narrative_result);
  for (const row of list(narrative.sections)) {
    const section = asRecord(row);
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    if (!WATCH_INTENT.test(blob)) continue;
    for (const paragraph of list(section.paragraphs)) {
      const item = asRecord(paragraph);
      const line = customerLine(item.text);
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

/**
 * Bind Pack 07 Life Optimization compact. Returns null when the engine did not publish.
 */
export function adaptOptimizationPlan(
  data: AnalysisDataDto | null | undefined,
): ActionPlanView | null {
  const raw = asRecord(data?.optimization);
  const topRaw = Array.isArray(raw.top_priorities) ? raw.top_priorities : [];
  const natalRaw = asRecord(raw.natal);
  const temporalRaw = asRecord(raw.temporal);
  if (!topRaw.length && !Array.isArray(natalRaw.items) && !Array.isArray(temporalRaw.items)) {
    return null;
  }
  const groupsRaw = asRecord(raw.groups);
  const topPriorities = topRaw.map((item, index) => toPriority(item, index));
  const groups = {
    develop: toActionList(groupsRaw.develop),
    improve: toActionList(groupsRaw.improve),
    control: toActionList(groupsRaw.control),
    avoid: toActionList(groupsRaw.avoid),
    temporal: toActionList(groupsRaw.temporal),
  };
  const natalItems = toActionList(natalRaw.items);
  const temporalItems = toActionList(temporalRaw.items);
  const usefulRaw = asRecord(raw.useful_god);
  const optimization: OptimizationPlanView = {
    subtitle: text(raw.title) || OPTIMIZATION_LABELS.subtitle,
    topPriorities,
    groups,
    natal: {
      title: text(natalRaw.title) || OPTIMIZATION_LABELS.natal,
      items: natalItems,
    },
    temporal: {
      title: text(temporalRaw.title) || OPTIMIZATION_LABELS.temporal,
      year: text(temporalRaw.year),
      items: temporalItems,
    },
    domains: toDomainList(raw.domains),
    conflicts: toConflictList(raw.conflicts),
    usefulGod: text(usefulRaw.element)
      ? {
          element: text(usefulRaw.element),
          functions: Array.isArray(usefulRaw.functions)
            ? usefulRaw.functions.map((item) => text(item)).filter(Boolean).join(" · ")
            : text(usefulRaw.functions),
          reason: text(usefulRaw.reason),
        }
      : null,
    elements: toElementList(raw.elements),
  };
  const first = topPriorities[0];
  return {
    title: ACTION_PLAN_TITLE,
    available: true,
    emptyMessage: ACTION_PLAN_EMPTY,
    priority: first
      ? { title: first.title, detail: first.reason, domain: first.domain, source: "optimization" }
      : null,
    actions: topPriorities.slice(1).map((item) => ({
      title: item.title,
      detail: item.reason,
      domain: item.domain,
      source: "optimization",
    })),
    extraActions: [],
    warnings: groups.avoid.map((item) => ({
      title: item.title,
      detail: item.caution || item.reason,
      domain: item.domain,
      source: "optimization",
    })),
    watch: temporalItems.map((item) => ({
      title: item.title,
      detail: item.reason,
      domain: item.domain,
      source: "optimization",
    })),
    optimization,
  };
}

function toPriority(value: unknown, index: number): OptimizationPriorityView {
  const item = toOptAction(value);
  const row = asRecord(value);
  return {
    ...item,
    rank: Number(row.rank) || index + 1,
    label: text(row.label) || `Ưu tiên ${index + 1}`,
  };
}

function toActionList(value: unknown): OptimizationActionView[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => toOptAction(item)).filter((item) => item.title);
}

function toOptAction(value: unknown): OptimizationActionView {
  const row = asRecord(value);
  return {
    domain: customerLine(row.domain),
    title: customerLine(row.title),
    reason: customerLine(row.reason),
    action: customerLine(row.action),
    effect: customerLine(row.effect),
    scope: customerLine(row.scope),
    condition: customerLine(row.condition),
    caution: customerLine(row.caution),
  };
}

function toDomainList(value: unknown): OptimizationDomainView[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => {
    const row = asRecord(item);
    return {
      id: text(row.id),
      title: customerLine(row.title),
      target: customerLine(row.target),
      driver: customerLine(row.driver),
      bottleneck: customerLine(row.bottleneck),
      leakage: customerLine(row.leakage),
      why: customerLine(row.why),
      action: customerLine(row.action),
      condition: customerLine(row.condition),
      caution: customerLine(row.caution),
      temporal: customerLine(row.temporal),
    };
  }).filter((item) => item.title);
}

function toConflictList(value: unknown): OptimizationConflictView[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => {
    const row = asRecord(item);
    return {
      title: customerLine(row.title),
      domains: customerLine(row.domains),
      resolution: customerLine(row.resolution),
      condition: customerLine(row.condition),
    };
  }).filter((item) => item.title);
}

function toElementList(value: unknown): OptimizationElementView[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => {
    const row = asRecord(item);
    const domains = Array.isArray(row.domains)
      ? row.domains.map((entry) => customerLine(entry)).filter(Boolean).join(" · ")
      : customerLine(row.domains);
    return {
      element: customerLine(row.element),
      function: customerLine(row.function),
      direction: customerLine(row.direction),
      domains,
      reason: customerLine(row.reason),
    };
  }).filter((item) => item.element);
}
