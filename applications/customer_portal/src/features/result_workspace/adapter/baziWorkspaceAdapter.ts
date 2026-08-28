/**
 * BaziWorkspaceAdapter — canonical analysis → workspace view model.
 *
 * May rename, localize, format, and map published arrays.
 * Must not calculate, score, infer, rank, classify, or derive luck / ShenSha.
 *
 * Five-element percents: count / canonical total (unit_total or sum of counts).
 * Isolated presentation math. No analytical reweighting.
 */

import {
  canonicalClimateStateLabel,
} from "../../../adapters/canonicalTemperature";
import {
  canonicalFiveElementCounts,
  FIVE_ELEMENT_ROWS,
  fiveElementUnitTotal,
  publishedFiveElementsDisclaimer,
  publishedFiveElementsMethodNote,
} from "../../../adapters/canonicalFiveElements";
import { shenShaEntriesFromAnalysis } from "../../../adapters/canonicalShenSha";
import {
  canonicalStrengthLabel,
  formatCanonicalStrengthScore,
  readCanonicalStrengthScore,
} from "../../../adapters/canonicalStrength";
import {
  canonicalFavorableDisplay,
  canonicalUnfavorableDisplay,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
} from "../../../adapters/canonicalUsefulGod";
import { UNAVAILABLE_CONCLUSION } from "../../../adapters/contentGuards";
import {
  asNarrativeResult,
  sectionParagraphTexts,
  summaryText,
} from "../../../adapters/narrativeResultAdapter";
import type { AnalysisDataDto, PillarDto } from "../../../models";
import { analyticalTenGods } from "../../../resultState/currentResult";
import { ACTION_CHIPS, SHEN_SHA_NAMES } from "../catalog";
import type { TuTruSlotPillar } from "../types";
import {
  CONCLUSION_SECTION_MAP,
  CONFIDENCE_LABELS,
  INTERPRETATION_SECTION_MAP,
  NAYIN_ELEMENT_ONLY,
  TEN_GOD_ALIASES,
} from "./mapping";
import type {
  BaziWorkspaceViewModel,
  WorkspaceBoneWeightView,
  WorkspaceConclusionView,
  WorkspaceField,
  WorkspaceFiveElementsView,
  WorkspaceInterpretationView,
  WorkspaceLuckCycleView,
  WorkspaceLuckView,
  WorkspaceOverviewView,
  WorkspacePatternView,
  WorkspacePersonView,
  WorkspaceShenShaView,
  WorkspaceTenGodsView,
} from "./types";

export type AdaptWorkspaceOptions = {
  readonly analysisId?: string | null;
  readonly input?: Record<string, unknown> | null;
};

function field<T>(value: T | null | undefined, source: string): WorkspaceField<T> {
  if (value === null || value === undefined) {
    return { value: null, available: false, source };
  }
  if (typeof value === "string" && !value.trim()) {
    return { value: null, available: false, source };
  }
  return { value, available: true, source };
}

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function pad2(value: number): string {
  return String(value).padStart(2, "0");
}

function joinStemBranch(pillar: PillarDto | undefined): string {
  const stem = text(pillar?.stem);
  const branch = text(pillar?.branch);
  if (stem && branch) return `${stem} ${branch}`.replace(/\s+/g, " ").trim();
  return stem || branch;
}

function nayinElementOnly(pillar: PillarDto | undefined): string {
  const raw = asRecord(pillar);
  const candidates = [text(raw.nayin_element), text(raw.nayin)];
  for (const item of candidates) {
    if (NAYIN_ELEMENT_ONLY.has(item)) return item;
  }
  return "";
}

function pillarCungPhi(pillar: PillarDto | undefined): string {
  const raw = asRecord(pillar);
  return text(raw.cung_phi) || text(raw.cung);
}

function bindPillar(
  canChi: string,
  pillar: PillarDto | undefined,
  dayCungPhi: string,
  isDay: boolean,
): TuTruSlotPillar {
  const cung = pillarCungPhi(pillar) || (isDay ? dayCungPhi : "");
  return {
    canChi: canChi || joinStemBranch(pillar),
    napAm: nayinElementOnly(pillar),
    cungPhi: cung,
  };
}

function formatLunar(calendar: AnalysisDataDto["calendar"]): string {
  if (!calendar) return "";
  const published = text(calendar.lunar_date);
  if (published) return published;
  const lunar = calendar.lunar;
  const day = lunar?.day ?? calendar.lunar_day;
  const month = lunar?.month ?? calendar.lunar_month;
  const year = lunar?.year ?? calendar.lunar_year;
  if (day == null || month == null || year == null) return "";
  const leap = Boolean(
    lunar?.is_leap_month ?? lunar?.leap ?? calendar.is_leap_month ?? calendar.leap_month,
  );
  const date = `${pad2(Number(day))}/${pad2(Number(month))}/${Number(year)}`;
  return leap ? `${date} nhuận` : date;
}

function formatBirthTime(
  data: AnalysisDataDto,
  input: Record<string, unknown>,
): string {
  const cal = asRecord(data.calendar);
  const hourRaw = cal.solar_hour ?? input.hour;
  const minuteRaw = cal.solar_minute ?? input.minute;
  const hour = Number(hourRaw);
  const minute = Number(minuteRaw);
  if (!Number.isFinite(hour) || !Number.isFinite(minute)) return "";
  return `${pad2(hour)}:${pad2(minute)}`;
}

function pickPattern(data: AnalysisDataDto): Record<string, unknown> {
  return asRecord(data.pattern);
}

function usefulToken(data: AnalysisDataDto): string {
  const useful = canonicalUsefulGodPayload(data);
  return (
    canonicalUsefulDisplay(useful) ||
    text(useful.useful_god) ||
    text(useful.useful_ten_god) ||
    text(useful.useful_stem)
  );
}

function favorableToken(data: AnalysisDataDto): string {
  const useful = canonicalUsefulGodPayload(data);
  const display = canonicalFavorableDisplay(useful);
  if (display) return display;
  if (Array.isArray(useful.favorable_gods)) {
    return useful.favorable_gods.map((item) => text(item)).filter(Boolean).join(", ");
  }
  return "";
}

function localizeConfidence(raw: unknown): string {
  if (typeof raw === "number" && Number.isFinite(raw)) {
    return String(raw);
  }
  const token = text(raw).toLowerCase();
  return CONFIDENCE_LABELS[token] || text(raw);
}

function bindPerson(
  data: AnalysisDataDto,
  options: AdaptWorkspaceOptions,
): WorkspacePersonView {
  const input = options.input ?? {};
  const calendar = data.calendar;
  const customer = data.customer;
  const name =
    text(customer?.full_name) || text(input.full_name) || text(asRecord(data).customer_name);
  const analysisId =
    text(options.analysisId) ||
    text(data.analysis_id) ||
    text(data.request_id);
  const timezone =
    text(customer?.timezone) || text(input.timezone) || text(calendar?.timezone);
  const location = text(customer?.birth_place) || text(input.birth_place);
  const locationLine = [location, timezone].filter(Boolean).join(" · ");
  return {
    name: field(name, "customer.full_name | input.full_name"),
    solarDate: field(text(calendar?.solar_date), "calendar.solar_date"),
    lunarDate: field(formatLunar(calendar), "calendar.lunar_date"),
    birthTime: field(formatBirthTime(data, input), "calendar.solar_hour/minute | input"),
    location: field(locationLine, "customer.birth_place + timezone"),
    timezone: field(timezone, "customer.timezone | input.timezone"),
    analysisId: field(analysisId, "analysis_id | request_id"),
  };
}

function bindOverview(data: AnalysisDataDto): WorkspaceOverviewView {
  const strengthScore = readCanonicalStrengthScore(data);
  const total = data.score?.total_score;
  const overall =
    typeof total === "number" && Number.isFinite(total) ? total : null;
  const confidence =
    localizeConfidence(data.score?.confidence) ||
    localizeConfidence(data.strength?.confidence);
  return {
    strength: field(canonicalStrengthLabel(data), "strength.strength_level"),
    strengthScore: field(
      strengthScore == null ? "" : formatCanonicalStrengthScore(strengthScore),
      "strength.strength_score",
    ),
    usefulGod: field(usefulToken(data), "useful_god"),
    favorableGod: field(favorableToken(data), "useful_god.favorable_*"),
    avoidGod: field(
      canonicalUnfavorableDisplay(canonicalUsefulGodPayload(data)),
      "useful_god.unfavorable_*",
    ),
    overallScore: field(overall, "score.total_score"),
    overallScoreMax: 100,
    confidence: field(confidence, "score.confidence | strength.confidence"),
  };
}

function bindFiveElements(data: AnalysisDataDto): WorkspaceFiveElementsView {
  const counts = canonicalFiveElementCounts(data);
  const publishedTotal = Number(data.five_elements?.unit_total);
  const total =
    Number.isFinite(publishedTotal) && publishedTotal > 0
      ? publishedTotal
      : fiveElementUnitTotal(counts);
  const observation =
    publishedFiveElementsMethodNote(data) || publishedFiveElementsDisclaimer(data);
  return {
    unitTotal: field(counts ? total : null, "five_elements.unit_total | sum(counts)"),
    observation: field(counts ? observation : "", "five_elements.method_note | disclaimer"),
    rows: FIVE_ELEMENT_ROWS.map((row) => {
      const count = counts ? counts[row.name] : null;
      const percent =
        counts && total > 0 && count != null
          ? Math.round((count / total) * 100)
          : null;
      return {
        id: row.element,
        name: row.name,
        count: field(count, "five_elements.counts"),
        percent: field(percent, "presentation: count / canonical total"),
      };
    }),
  };
}

function bindTenGods(data: AnalysisDataDto): WorkspaceTenGodsView {
  const payload = data.ten_gods ?? data.ten_gods_result;
  const labels = analyticalTenGods(data);
  const available = Boolean(payload || (data.bazi?.ten_gods && data.bazi.ten_gods.length));
  return {
    available,
    rows: TEN_GOD_ALIASES.map((row) => {
      if (!available) {
        return { name: row.name, count: field<number>(null, "ten_gods") };
      }
      const count = labels.filter((label) => row.aliases.includes(label)).length;
      return { name: row.name, count: field(count, "ten_gods visible labels") };
    }),
  };
}

function bindPattern(data: AnalysisDataDto): WorkspacePatternView {
  const pattern = pickPattern(data);
  const name = text(pattern.cach_cuc) || text(pattern.pattern_label);
  const klass = text(pattern.tong_cach) || text(pattern.pattern);
  const quality = text(pattern.quality) || text(pattern.status);
  const summary = text(pattern.summary) || text(pattern.customer_summary);
  return {
    pattern: field(name, "pattern.cach_cuc"),
    patternClass: field(klass, "pattern.tong_cach | pattern.pattern"),
    climate: field(canonicalClimateStateLabel(data), "temperature.climate_state"),
    quality: field(quality, "pattern.quality | pattern.status"),
    summary: field(summary, "pattern.summary"),
  };
}

function bindShenSha(data: AnalysisDataDto): WorkspaceShenShaView {
  const entries = shenShaEntriesFromAnalysis(data);
  const byName = new Map(entries.map((item) => [item.name, item]));
  const catalogRows = SHEN_SHA_NAMES.map((name) => {
    const hit = byName.get(name);
    return {
      name,
      catalog: true,
      presence: field(hit ? hit.presence || "Có" : "", "bazi.shensha_matches"),
    };
  });
  const extras = entries
    .filter((item) => !(SHEN_SHA_NAMES as readonly string[]).includes(item.name))
    .map((item) => ({
      name: item.name,
      catalog: false,
      presence: field(item.presence || "Có", "bazi.shensha_matches"),
    }));
  return { rows: [...catalogRows, ...extras] };
}

function bindBoneWeight(data: AnalysisDataDto): WorkspaceBoneWeightView {
  const raw = asRecord(data.bone_weight) ;
  const alt = asRecord(data.can_xuong);
  const src = Object.keys(raw).length ? raw : alt;
  const source = Object.keys(raw).length ? "bone_weight" : "can_xuong";
  const amount =
    text(src.amount) ||
    text(src.total) ||
    text(src.tong_can_luong) ||
    [text(src.luong) && `${src.luong} lượng`, text(src.chi) && `${src.chi} chỉ`]
      .filter(Boolean)
      .join(" ");
  return {
    amount: field(amount, source),
    classification: field(
      text(src.classification) || text(src.grade) || text(src.phan_loai),
      source,
    ),
    interpretation: field(
      text(src.interpretation) || text(src.text) || text(src.preview),
      source,
    ),
  };
}

function cycleGanZhi(cycle: Record<string, unknown>): string {
  const published = text(cycle.gan_zhi);
  if (published) return published;
  const stem = text(cycle.stem);
  const branch = text(cycle.branch);
  if (stem && branch) return `${stem} ${branch}`.trim();
  return stem || branch;
}

function bindLuck(data: AnalysisDataDto): WorkspaceLuckView {
  const luck = data.luck;
  const current = luck?.current_cycle;
  const currentRecord = asRecord(current);
  const ganZhi = cycleGanZhi(currentRecord);
  const ageStart = current?.age_start ?? null;
  const ageEnd = current?.age_end ?? null;
  const ageRange =
    ageStart != null && ageEnd != null ? `${ageStart}–${ageEnd}` : "";
  const years =
    current?.year_start != null && current?.year_end != null
      ? `${current.year_start}–${current.year_end}`
      : "";
  const cycles: WorkspaceLuckCycleView[] = (luck?.cycles ?? []).map((cycle) => {
    const row = asRecord(cycle);
    const gan = cycleGanZhi(row);
    return {
      ganZhi: gan,
      ageStart: cycle.age_start ?? null,
      ageEnd: cycle.age_end ?? null,
      yearStart: cycle.year_start ?? null,
      yearEnd: cycle.year_end ?? null,
      current: Boolean(ganZhi && gan === ganZhi && cycle.age_start === ageStart),
    };
  });
  return {
    current: field(ganZhi || years, "luck.current_cycle"),
    ageRange: field(ageRange, "luck.current_cycle.age_start/end"),
    ganZhi: field(ganZhi, "luck.current_cycle.gan_zhi"),
    currentYear: field("", "luck has no canonical current calendar year"),
    observation: field(text(luck?.evidence) || text(luck?.method_note), "luck.evidence | method_note"),
    cycles,
  };
}

function firstSectionText(
  narrative: ReturnType<typeof asNarrativeResult>,
  matcher: RegExp,
): string {
  if (!narrative) return "";
  const texts = sectionParagraphTexts(narrative, matcher);
  return texts[0] || "";
}

function bindInterpretation(data: AnalysisDataDto): WorkspaceInterpretationView {
  const narrative = asNarrativeResult(data.narrative_result);
  return {
    observe: field(
      firstSectionText(narrative, INTERPRETATION_SECTION_MAP.observe),
      "narrative_result Quan sát",
    ),
    reason: field(
      firstSectionText(narrative, INTERPRETATION_SECTION_MAP.reason),
      "narrative_result Lý giải",
    ),
    impact: field(
      firstSectionText(narrative, INTERPRETATION_SECTION_MAP.impact),
      "narrative_result Tác động",
    ),
    advice: field(
      firstSectionText(narrative, INTERPRETATION_SECTION_MAP.advice),
      "narrative_result Khuyến nghị",
    ),
  };
}

function bindConclusion(data: AnalysisDataDto): WorkspaceConclusionView {
  const narrative = asNarrativeResult(data.narrative_result);
  const closing =
    firstSectionText(narrative, CONCLUSION_SECTION_MAP) ||
    (narrative ? summaryText(narrative.summary, "identity") : "");
  return {
    overall: field(
      closing && closing !== UNAVAILABLE_CONCLUSION ? closing : "",
      "narrative_result kết luận",
    ),
    actions: ACTION_CHIPS.map((chip) => ({
      id: chip.id,
      label: chip.label,
      available: false,
    })),
  };
}

/**
 * Map a stored canonical analysis payload into the frozen workspace panels.
 */
export function adaptBaziWorkspace(
  data: AnalysisDataDto | null | undefined,
  options: AdaptWorkspaceOptions = {},
): BaziWorkspaceViewModel | null {
  if (!data) return null;
  const calendar = data.calendar;
  const dayCung = text(calendar?.cung_phi);
  const person = bindPerson(data, options);
  return {
    analysisId: person.analysisId.value || "",
    person,
    fourPillars: {
      year: bindPillar(text(calendar?.year_can_chi), data.bazi?.year_pillar, dayCung, false),
      month: bindPillar(text(calendar?.month_can_chi), data.bazi?.month_pillar, dayCung, false),
      day: bindPillar(text(calendar?.day_can_chi), data.bazi?.day_pillar, dayCung, true),
      hour: bindPillar(text(calendar?.hour_can_chi), data.bazi?.hour_pillar, dayCung, false),
    },
    overview: bindOverview(data),
    fiveElements: bindFiveElements(data),
    tenGods: bindTenGods(data),
    pattern: bindPattern(data),
    shenSha: bindShenSha(data),
    boneWeight: bindBoneWeight(data),
    luck: bindLuck(data),
    interpretation: bindInterpretation(data),
    conclusion: bindConclusion(data),
  };
}
