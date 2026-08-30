/**
 * Bind Overview Card from canonical analysis. Copy published labels only.
 */

import { canonicalStrengthLabel } from "../../adapters/canonicalStrength";
import { canonicalBalancingNeedLabel } from "../../adapters/canonicalTemperature";
import {
  OVERALL_INCOMPLETE_MESSAGE,
  canonicalUnfavorableDisplay,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
} from "../../adapters/canonicalUsefulGod";
import type { AnalysisDataDto } from "../../models";
import { OVERVIEW_SUBTITLE, OVERVIEW_TITLE } from "./cards";
import type { OverviewEvidenceView, OverviewView } from "./types";

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
  if (!display || display === OVERALL_INCOMPLETE_MESSAGE) return "";
  return customerLabel(display);
}

function compactCanonicalList(value: string): string {
  return value.replace(/\s*,\s*/g, " · ").replace(/\s{2,}/g, " ").trim();
}

function avoidDisplay(data: AnalysisDataDto): string {
  const payload = canonicalUsefulGodPayload(data);
  const display = compactCanonicalList(canonicalUnfavorableDisplay(payload));
  if (!display || display === OVERALL_INCOMPLETE_MESSAGE) return "";
  return customerLabel(display);
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
  const identity = [
    evidence("day-master", "Nhật Chủ", dayMaster),
    evidence("strength", "Thân", strength),
    evidence("avoid-god", "Kỵ Thần", avoidGod),
  ].filter((item): item is OverviewEvidenceView => item != null);
  const balance = [
    evidence("useful-god", "Dụng Thần", usefulGod),
    evidence("temperature", "Điều Hậu", climate),
  ].filter((item): item is OverviewEvidenceView => item != null);
  return {
    title: OVERVIEW_TITLE,
    subtitle: OVERVIEW_SUBTITLE,
    insight: composeOverviewInsight({ strength, dayMaster }),
    insightSource:
      "canonical labels: strength.strength_level + bazi.day_master + useful_god.unfavorable_display",
    conclusion: conclusion.text,
    conclusionSource: conclusion.source,
    identity,
    balance,
  };
}
