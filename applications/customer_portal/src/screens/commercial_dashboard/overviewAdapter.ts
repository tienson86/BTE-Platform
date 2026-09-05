/**
 * Bind Overview Card from canonical analysis. Copy published labels only.
 */

import { canonicalPatternLabel } from "../../adapters/canonicalPattern";
import { canonicalStrengthLabel } from "../../adapters/canonicalStrength";
import { canonicalBalancingNeedLabel } from "../../adapters/canonicalTemperature";
import {
  OVERALL_INCOMPLETE_MESSAGE,
  canonicalFavorableDisplay,
  canonicalUnfavorableDisplay,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
} from "../../adapters/canonicalUsefulGod";
import type { AnalysisDataDto } from "../../models";
import { OVERVIEW_SUBTITLE, OVERVIEW_TITLE } from "./cards";
import type { OverviewEvidenceView, OverviewFocusView, OverviewView } from "./types";

const INSIGHT_MAX = 220;
const CONCLUSION_MAX = 220;
const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;

function text(value: unknown): string {
  if (value == null) return "";
  return String(value).trim();
}

function customerLabel(value: string): string {
  const next = text(value);
  if (!next || TECHNICAL_TOKEN.test(next)) return "";
  return next;
}

function clampCopy(value: string, maxChars: number): string {
  const clean = value.replace(/\s+/g, " ").trim();
  if (clean.length <= maxChars) return clean;
  return `${clean.slice(0, maxChars).replace(/\s+\S*$/, "")}…`;
}

function dayMasterDisplay(data: AnalysisDataDto): string {
  const stem = text(data.bazi?.day_master);
  const element = customerLabel(text(data.bazi?.day_master_element));
  return [stem, element].filter(Boolean).join(" ");
}

function strengthDisplay(data: AnalysisDataDto): string {
  const mapped = canonicalStrengthLabel(data);
  if (mapped) return mapped;
  const raw = text(data.strength?.strength_level);
  return /thân/i.test(raw) ? raw : "";
}

function usefulDisplay(data: AnalysisDataDto): string {
  const payload = canonicalUsefulGodPayload(data);
  const display = canonicalUsefulDisplay(payload);
  return publishedChipValue(display);
}

function favorableDisplay(data: AnalysisDataDto): string {
  const payload = canonicalUsefulGodPayload(data);
  return publishedChipValue(compactCanonicalList(canonicalFavorableDisplay(payload)));
}

function compactCanonicalList(value: string): string {
  return value.replace(/\s*,\s*/g, " · ").replace(/\s{2,}/g, " ").trim();
}

function avoidDisplay(data: AnalysisDataDto): string {
  const payload = canonicalUsefulGodPayload(data);
  return publishedChipValue(compactCanonicalList(canonicalUnfavorableDisplay(payload)));
}

function publishedChipValue(value: string): string {
  const next = customerLabel(value);
  if (!next || next === OVERALL_INCOMPLETE_MESSAGE || /chưa đủ căn cứ/i.test(next)) return "";
  return next;
}

/**
 * Copy published executive facts only. Omits empty or incomplete fields.
 */
export function adaptOverviewExecutiveFacts(data: AnalysisDataDto | null | undefined): {
  readonly identity: readonly OverviewEvidenceView[];
  readonly balance: readonly OverviewEvidenceView[];
} {
  const payload = data ?? {};
  const identity = [
    evidence("day-master", "Nhật Chủ", dayMasterDisplay(payload)),
    evidence("strength", "Thân", strengthDisplay(payload)),
    evidence("pattern", "Mệnh Cục", customerLabel(canonicalPatternLabel(payload))),
  ].filter((item): item is OverviewEvidenceView => item != null);
  const balance = [
    evidence("useful-god", "Dụng Thần", usefulDisplay(payload)),
    evidence("favorable-god", "Hỷ Thần", favorableDisplay(payload)),
    evidence("avoid-god", "Kỵ Thần", avoidDisplay(payload)),
  ].filter((item): item is OverviewEvidenceView => item != null);
  return { identity, balance };
}

function evidence(
  key: OverviewEvidenceView["key"],
  label: string,
  value: string,
): OverviewEvidenceView | null {
  const next = customerLabel(value);
  if (!next) return null;
  return { key, label, value: next };
}

/**
 * Insight from canonical labels only. No dedicated Overview insight field exists.
 */
export function composeOverviewInsight(input: {
  readonly strength: string;
  readonly dayMaster: string;
  readonly pattern?: string;
}): string {
  const sentences: string[] = [];
  if (input.strength) sentences.push(`Bạn thuộc nhóm ${input.strength}.`);
  if (input.dayMaster) sentences.push(`Nhật chủ ${input.dayMaster}.`);
  return clampCopy(sentences.join(" "), INSIGHT_MAX);
}

/**
 * Quick conclusion from canonical labels only. No dedicated Overview close field exists.
 */
export function composeOverviewConclusion(input: {
  readonly strength: string;
  readonly usefulGod: string;
  readonly climate: string;
  readonly avoidGod?: string;
}): { readonly text: string; readonly source: string } {
  const sentences: string[] = [];
  if (input.strength) sentences.push(`Đây là lá số ${input.strength}.`);
  if (input.usefulGod && input.usefulGod !== OVERALL_INCOMPLETE_MESSAGE) {
    sentences.push(`Dụng thần ${input.usefulGod}.`);
  }
  if (input.avoidGod && input.avoidGod !== OVERALL_INCOMPLETE_MESSAGE) {
    sentences.push(`Kỵ thần ${input.avoidGod}.`);
  }
  if (input.climate) {
    sentences.push(input.climate.endsWith(".") ? input.climate : `${input.climate}.`);
  }
  return {
    text: clampCopy(sentences.join(" "), CONCLUSION_MAX),
    source: "canonical labels: strength + useful_display + unfavorable_display + temperature.balancing_need",
  };
}

/**
 * Map published analysis fields onto the Overview Card view.
 */
export function adaptOverviewCard(data: AnalysisDataDto | null | undefined): OverviewView {
  const payload = data ?? {};
  const dayMaster = dayMasterDisplay(payload);
  const strength = strengthDisplay(payload);
  const avoidGod = avoidDisplay(payload);
  const usefulGod = usefulDisplay(payload);
  const climate = customerLabel(canonicalBalancingNeedLabel(payload));
  const conclusion = composeOverviewConclusion({
    strength,
    usefulGod,
    avoidGod,
    climate,
  });
  const facts = adaptOverviewExecutiveFacts(payload);
  const focus = adaptOverviewFocus(payload);
  return {
    title: OVERVIEW_TITLE,
    subtitle: OVERVIEW_SUBTITLE,
    insight: composeOverviewInsight({ strength, dayMaster }),
    insightSource: "canonical labels: strength.strength_level + bazi.day_master",
    summary: "",
    summarySource: "",
    conclusion: conclusion.text,
    conclusionSource: conclusion.source,
    identity: facts.identity,
    balance: facts.balance,
    focusTitle: focus.title,
    focus: focus.items,
  };
}

const FOCUS_ROWS: readonly { key: OverviewFocusView["key"]; label: string; field: string }[] = [
  { key: "driver", label: "Động lực chính", field: "driver" },
  { key: "bottleneck", label: "Điểm nghẽn", field: "bottleneck" },
  { key: "risk", label: "Rủi ro chính", field: "risk" },
  { key: "opportunity", label: "Cơ hội chính", field: "opportunity" },
  { key: "condition", label: "Điều kiện phát huy", field: "condition" },
];

/**
 * Copy published Evidence Priority labels only. No IDs or traces.
 */
export function adaptOverviewFocus(data: AnalysisDataDto | null | undefined): {
  readonly title: string;
  readonly items: readonly OverviewFocusView[];
} {
  const block = data?.evidence_priority;
  if (!block || typeof block !== "object") {
    return { title: "", items: [] };
  }
  const record = block as Record<string, unknown>;
  const items = FOCUS_ROWS.map((row) => {
    const value = customerLabel(text(record[row.field]));
    if (!value) return null;
    return { key: row.key, label: row.label, value };
  }).filter((item): item is OverviewFocusView => item != null);
  if (!items.length) return { title: "", items: [] };
  const title = customerLabel(text(record.title)) || "Trọng tâm lá số";
  return { title, items };
}
