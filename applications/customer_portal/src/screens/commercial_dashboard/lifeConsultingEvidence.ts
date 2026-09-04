/**
 * Copy published tokens used by Life Consulting lookup.
 * Does not calculate astrology or invent missing fields.
 */

import { canonicalPatternLabel } from "../../adapters/canonicalPattern";
import { canonicalStrengthLabel } from "../../adapters/canonicalStrength";
import {
  canonicalClimateStateLabel,
  canonicalBalancingNeedLabel,
} from "../../adapters/canonicalTemperature";
import {
  OVERALL_INCOMPLETE_MESSAGE,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
} from "../../adapters/canonicalUsefulGod";
import {
  asTenGodsPayload,
  hiddenLabels,
  tenGodLabel,
  visibleLabels,
} from "../../adapters/tenGodsDisplay";
import type { AnalysisDataDto, BaziDto, PillarDto } from "../../models";

export type LifeConsultingGender = "male" | "female" | "";

export type LifeConsultingEvidence = {
  readonly gender: LifeConsultingGender;
  readonly visible: readonly string[];
  readonly hidden: readonly string[];
  readonly pattern: string;
  readonly strength: string;
  readonly usefulDisplay: string;
  readonly shensha: readonly string[];
  readonly climate: string;
  readonly climateNeed: string;
  readonly fiveElementsStatus: string;
  readonly hasCurrentLuck: boolean;
};

const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;
const DAY_MASTER_LABEL = "Nhật Chủ";
const PILLAR_KEYS = ["year", "month", "day", "hour"] as const;
const TRUSTED_BALANCE = new Set(["CÂN BẰNG", "MẤT CÂN BẰNG NHẸ", "LỆCH RÕ"]);

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

function unique(values: readonly string[]): string[] {
  const seen = new Set<string>();
  const next: string[] = [];
  for (const value of values) {
    if (!value || seen.has(value)) continue;
    seen.add(value);
    next.push(value);
  }
  return next;
}

function pillarOf(bazi: BaziDto | undefined, key: (typeof PILLAR_KEYS)[number]): PillarDto | undefined {
  if (!bazi) return undefined;
  if (key === "year") return bazi.year_pillar;
  if (key === "month") return bazi.month_pillar;
  if (key === "day") return bazi.day_pillar;
  return bazi.hour_pillar;
}

function normalizeGender(value: string): LifeConsultingGender {
  const next = text(value).toLowerCase();
  if (next === "male" || next === "nam" || next === "m") return "male";
  if (next === "female" || next === "nữ" || next === "nu" || next === "f") return "female";
  return "";
}

export type LifeConsultingEvidenceOptions = {
  readonly genderHint?: string | null;
};

function publishedGender(data: AnalysisDataDto, genderHint?: string | null): LifeConsultingGender {
  return (
    normalizeGender(text(data.identity?.person?.gender)) ||
    normalizeGender(text(data.bazi?.gender)) ||
    normalizeGender(text(data.customer?.gender)) ||
    normalizeGender(text(genderHint))
  );
}

function publishedGods(data: AnalysisDataDto): {
  readonly visible: readonly string[];
  readonly hidden: readonly string[];
} {
  const payload = asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  const fromPayload = visibleLabels(payload)
    .map(customerLabel)
    .filter((name) => name && name !== DAY_MASTER_LABEL);
  const fromPillars = PILLAR_KEYS.map((key) => customerLabel(text(pillarOf(data.bazi, key)?.ten_god)))
    .filter((name) => name && name !== DAY_MASTER_LABEL);
  const hidden = hiddenLabels(payload)
    .map(customerLabel)
    .filter((name) => name && name !== DAY_MASTER_LABEL);
  const extraHidden = (payload?.hidden ?? [])
    .map(tenGodLabel)
    .map(customerLabel)
    .filter((name) => name && name !== DAY_MASTER_LABEL);
  return {
    visible: unique([...fromPayload, ...fromPillars]),
    hidden: unique([...hidden, ...extraHidden]),
  };
}

function publishedUseful(data: AnalysisDataDto): string {
  const display = customerLabel(canonicalUsefulDisplay(canonicalUsefulGodPayload(data)));
  if (!display || display === OVERALL_INCOMPLETE_MESSAGE || /chưa đủ căn cứ/i.test(display)) {
    return "";
  }
  return display;
}

function pushName(names: string[], value: unknown): void {
  const label = customerLabel(text(value));
  if (label) names.push(label);
}

function publishedShensha(data: AnalysisDataDto): readonly string[] {
  const names: string[] = [];
  for (const item of data.bazi?.shensha ?? []) pushName(names, item);
  for (const match of data.bazi?.shensha_matches ?? []) {
    pushName(names, match.canonical_name || match.name);
  }
  const extra = data as Record<string, unknown>;
  const block = extra.shensha;
  if (Array.isArray(block)) {
    for (const item of block) {
      if (typeof item === "string") pushName(names, item);
      else pushName(names, asRecord(item).canonical_name || asRecord(item).name);
    }
  } else {
    const row = asRecord(block);
    const lists = [row.items, row.matches, row.names];
    for (const list of lists) {
      if (!Array.isArray(list)) continue;
      for (const item of list) {
        if (typeof item === "string") pushName(names, item);
        else pushName(names, asRecord(item).canonical_name || asRecord(item).name);
      }
    }
  }
  return unique(names);
}

function publishedFiveElementsStatus(data: AnalysisDataDto): string {
  const facts = asRecord(data.five_elements);
  const status = text(facts.status);
  return TRUSTED_BALANCE.has(status) ? status : "";
}

function publishedCurrentLuck(data: AnalysisDataDto): boolean {
  const cycle = data.luck?.current_cycle;
  if (cycle && customerLabel(text(cycle.gan_zhi))) return true;
  const identityLuck = data.identity?.luck;
  return Boolean(
    identityLuck &&
      (customerLabel(text(identityLuck.current_cycle_ganzhi)) ||
        customerLabel(text(identityLuck.current_cycle))),
  );
}

/**
 * Snapshot of published tokens. Empty fields stay empty; nothing is inferred.
 */
export function collectLifeConsultingEvidence(
  data: AnalysisDataDto | null | undefined,
  options?: LifeConsultingEvidenceOptions,
): LifeConsultingEvidence {
  const payload = data ?? {};
  const gods = publishedGods(payload);
  return {
    gender: publishedGender(payload, options?.genderHint),
    visible: gods.visible,
    hidden: gods.hidden,
    pattern: customerLabel(canonicalPatternLabel(payload)),
    strength: canonicalStrengthLabel(payload) || (/thân/i.test(text(payload.strength?.strength_level))
      ? customerLabel(text(payload.strength?.strength_level))
      : ""),
    usefulDisplay: publishedUseful(payload),
    shensha: publishedShensha(payload),
    climate: customerLabel(canonicalClimateStateLabel(payload)),
    climateNeed: customerLabel(canonicalBalancingNeedLabel(payload)),
    fiveElementsStatus: publishedFiveElementsStatus(payload),
    hasCurrentLuck: publishedCurrentLuck(payload),
  };
}
