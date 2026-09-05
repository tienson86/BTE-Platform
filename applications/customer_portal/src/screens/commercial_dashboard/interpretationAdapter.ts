/**
 * Bind Interpretation Card from published narrative. Copy only.
 */

import { isTechnicalRuleText } from "../../adapters/contentGuards";
import { asNarrativeResult } from "../../adapters/narrativeResultAdapter";
import type { AnalysisDataDto } from "../../models";
import {
  INTERPRETATION_EMPTY,
  INTERPRETATION_TITLE,
  INTERPRETATION_ZONE_LABELS,
} from "./cards";
import type {
  InterpretationView,
  InterpretationZoneId,
  InterpretationZoneView,
} from "./types";

const RULE_ID = /\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|spe|cmb|root)_[a-z0-9_]+\b/gi;
const RULE_PHRASE = /(?:^|\s|[·|,;])rule\s+[a-z][a-z0-9_]{1,40}/gi;

const DEFAULT_WORD_MAX = 90;
const RECOMMENDATION_DEFAULT_LIMIT = 3;
const TECHNICAL =
  /\{|\}|dayun_runtime|source_unit|rule_id|UNKNOWN|matcher|engine_id|priority token|confidence token|pack05_|schema_version|topic_id|evidence_refs|str_[0-9]|pat_[a-z0-9]|tmp_[0-9]|sea_[0-9]|cli_[0-9]|\+\d+|root đã công bố|chưa đủ căn cứ/i;
const RESTATEMENT = /được đọc là|đã công bố/;
const FEAR = /chắc chắn thất bại|chắc chắn ly hôn|tai họa|bệnh nặng|đại hung/;
const DATA_CHIP = /^(nhật chủ|lệnh tháng|dụng thần|hỷ thần|kỵ thần)(\s+được chọn)?\s*[:：]/i;
const DIAGNOSTIC = /^yếu tố (hỗ trợ|suy giảm|kỵ)/i;

const ZONE_INTENTS: Record<InterpretationZoneId, RegExp> = {
  observation: /observation|quan sát/i,
  reasoning: /reasoning|lý do|lý giải/i,
  impact: /impact|tác động/i,
  recommendation: /recommendation|priority|khuyến/i,
};

const LEAD_INTENT = /overview|executive|tóm tắt điều hành/i;
const CLOSE_INTENT = /closing|conclusion|kết luận/i;

type SlotCopy = {
  readonly sentences: readonly string[];
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

function wordCount(value: string): number {
  return value.split(/\s+/).filter(Boolean).length;
}

function customerSentence(value: unknown): string {
  let raw = text(value);
  if (!raw) return "";
  raw = raw.replace(RULE_PHRASE, " ").replace(RULE_ID, " ").replace(/\s{2,}/g, " ").trim();
  if (!raw || isTechnicalRuleText(raw)) return "";
  if (TECHNICAL.test(raw) || RESTATEMENT.test(raw) || FEAR.test(raw) || DATA_CHIP.test(raw) || DIAGNOSTIC.test(raw)) {
    return "";
  }
  if (!raw.replace(/[.,·\s]/g, "")) return "";
  return raw;
}

function sanitizeSentences(values: readonly unknown[]): string[] {
  const next: string[] = [];
  const seen = new Set<string>();
  for (const value of values) {
    const line = customerSentence(value);
    if (!line || seen.has(line)) continue;
    seen.add(line);
    next.push(line);
  }
  return next;
}

function blockSentences(block: unknown): string[] {
  const rec = asRecord(block);
  if (rec.available === false) return [];
  const sentences = Array.isArray(rec.sentences) ? rec.sentences : [];
  return sanitizeSentences(sentences);
}

function pack05Sentences(data: AnalysisDataDto, intent: RegExp): string[] {
  const narrative = asNarrativeResult(data.narrative_result);
  if (!narrative) return [];
  const lines: unknown[] = [];
  for (const section of narrative.sections ?? []) {
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    if (!intent.test(blob)) continue;
    for (const paragraph of section.paragraphs ?? []) {
      if (paragraph.insufficient_data) continue;
      lines.push(paragraph.text);
    }
  }
  return sanitizeSentences(lines);
}

function copySlot(data: AnalysisDataDto, id: InterpretationZoneId, integrated: unknown): SlotCopy {
  const fromPack = pack05Sentences(data, ZONE_INTENTS[id]);
  if (fromPack.length) {
    return { sentences: fromPack, source: `narrative_result.${id}` };
  }
  const fromIntegrated = blockSentences(integrated);
  if (fromIntegrated.length) {
    return { sentences: fromIntegrated, source: `integrated_narrative.${id}` };
  }
  return { sentences: [], source: "" };
}

function splitDefault(
  sentences: readonly string[],
  maxWords: number,
  maxItems?: number,
): { readonly body: string; readonly extra: string } {
  const capped = maxItems != null ? sentences.slice(0, maxItems) : [...sentences];
  const hidden: string[] = maxItems != null ? [...sentences.slice(maxItems)] : [];
  const shown: string[] = [];
  let words = 0;
  let overflow = false;
  for (const line of capped) {
    const next = wordCount(line);
    if (overflow || (shown.length > 0 && words + next > maxWords)) {
      overflow = true;
      hidden.push(line);
      continue;
    }
    shown.push(line);
    words += next;
  }
  return { body: shown.join(" "), extra: hidden.join(" ") };
}

function copyLead(data: AnalysisDataDto): { readonly body: string; readonly extra: string; readonly source: string } {
  const fromPack = pack05Sentences(data, LEAD_INTENT);
  if (fromPack.length) {
    const split = splitDefault(fromPack, DEFAULT_WORD_MAX);
    return { ...split, source: "narrative_result.overview" };
  }
  const integrated = asRecord(data.integrated_narrative);
  const fromIntegrated = blockSentences(integrated.executive_summary);
  if (fromIntegrated.length) {
    const split = splitDefault(fromIntegrated, DEFAULT_WORD_MAX);
    return { ...split, source: "integrated_narrative.executive_summary" };
  }
  return { body: "", extra: "", source: "" };
}

function copyClosing(data: AnalysisDataDto): { readonly body: string; readonly source: string } {
  const fromPack = pack05Sentences(data, CLOSE_INTENT);
  if (fromPack.length) {
    return { body: fromPack.join(" "), source: "narrative_result.closing" };
  }
  const integrated = asRecord(data.integrated_narrative);
  const fromIntegrated = blockSentences(integrated.summary);
  if (fromIntegrated.length) {
    return { body: fromIntegrated.join(" "), source: "integrated_narrative.summary" };
  }
  return { body: "", source: "" };
}

function copyZone(data: AnalysisDataDto, id: InterpretationZoneId): InterpretationZoneView {
  const integrated = asRecord(data.integrated_narrative);
  const copied = copySlot(data, id, integrated[id]);
  const limit = id === "recommendation" ? RECOMMENDATION_DEFAULT_LIMIT : undefined;
  const split = splitDefault(copied.sentences, DEFAULT_WORD_MAX, limit);
  return {
    id,
    label: INTERPRETATION_ZONE_LABELS[id],
    body: split.body,
    extra: split.extra,
    source: copied.source,
  };
}

/**
 * Join published Integrated Narrative + Pack 05 commercial sections.
 * Does not compose astrology prose.
 */
export function adaptInterpretationCard(data: AnalysisDataDto | null | undefined): InterpretationView {
  const payload = data ?? {};
  const lead = copyLead(payload);
  const zones = (
    ["observation", "reasoning", "impact", "recommendation"] as const
  ).map((id) => copyZone(payload, id));
  const closing = copyClosing(payload);
  const available = Boolean(lead.body || closing.body || zones.some((zone) => zone.body));
  return {
    title: INTERPRETATION_TITLE,
    available,
    lead: lead.body,
    leadExtra: lead.extra,
    leadSource: lead.source,
    zones,
    closing: closing.body,
    closingSource: closing.source,
    emptyMessage: INTERPRETATION_EMPTY,
    domainTitle: "",
    domains: [],
  };
}
