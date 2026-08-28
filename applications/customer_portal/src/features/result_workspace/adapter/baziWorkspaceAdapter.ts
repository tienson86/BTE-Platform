/**
 * BaziWorkspaceAdapter — canonical analysis → workspace view model.
 *
 * View model: Identity + Analysis + Integrated Narrative only.
 * Panel 9/10 copy published IntegratedNarrative. No topic merge.
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
import type { AnalysisDataDto, CanonicalIdentityDto } from "../../../models";
import { analyticalTenGods } from "../../../resultState/currentResult";
import { ACTION_CHIPS, SHEN_SHA_NAMES } from "../catalog";
import { EMPTY_TU_TRU_PILLAR } from "../layout";
import type { TuTruSlotPillar } from "../types";
import { CONFIDENCE_LABELS, TEN_GOD_ALIASES } from "./mapping";
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

function identityOf(data: AnalysisDataDto): CanonicalIdentityDto {
  return asRecord(data.identity) as CanonicalIdentityDto;
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
  const person = asRecord(identityOf(data).person);
  const analysisId =
    text(options.analysisId) ||
    text(data.analysis_id) ||
    text(data.request_id);
  return {
    name: field(text(person.full_name), "identity.person.full_name"),
    gender: field(text(person.gender), "identity.person.gender"),
    solarDate: field(text(person.solar_birth), "identity.person.solar_birth"),
    lunarDate: field(text(person.lunar_birth), "identity.person.lunar_birth"),
    birthTime: field(text(person.birth_time), "identity.person.birth_time"),
    location: field(text(person.birth_place), "identity.person.birth_place"),
    timezone: field(text(person.timezone), "identity.person.timezone"),
    analysisId: field(analysisId, "analysis_id | request_id"),
  };
}

function bindIdentityPillar(raw: unknown): TuTruSlotPillar {
  const cell = asRecord(raw);
  if (!Object.keys(cell).length) return EMPTY_TU_TRU_PILLAR;
  return {
    stem: text(cell.stem),
    branch: text(cell.branch),
    canChi: text(cell.can_chi),
    napAm: text(cell.nayin_element),
    cungPhi: text(cell.cung_phi),
  };
}

function bindFourPillars(data: AnalysisDataDto): BaziWorkspaceViewModel["fourPillars"] {
  /** Owner: identity.four_pillars — no calendar/bazi reconstruction. */
  const four = asRecord(identityOf(data).four_pillars);
  return {
    year: bindIdentityPillar(four.year),
    month: bindIdentityPillar(four.month),
    day: bindIdentityPillar(four.day),
    hour: bindIdentityPillar(four.hour),
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
  const src = asRecord(identityOf(data).bone_weight);
  return {
    amount: field(text(src.weight), "identity.bone_weight.weight"),
    classification: field(text(src.classification), "identity.bone_weight.classification"),
    interpretation: field(text(src.summary), "identity.bone_weight.summary"),
  };
}

function bindLuck(data: AnalysisDataDto): WorkspaceLuckView {
  const published = asRecord(identityOf(data).luck);
  const luck = data.luck;
  const ganZhi = text(published.current_cycle_ganzhi) || text(published.current_cycle);
  const current = text(published.current_cycle) || ganZhi;
  const cycles: WorkspaceLuckCycleView[] = (luck?.cycles ?? []).map((cycle) => {
    const row = asRecord(cycle);
    const gan = text(row.gan_zhi);
    return {
      ganZhi: gan,
      ageStart: cycle.age_start ?? null,
      ageEnd: cycle.age_end ?? null,
      yearStart: cycle.year_start ?? null,
      yearEnd: cycle.year_end ?? null,
      current: Boolean(ganZhi && gan === ganZhi),
    };
  });
  return {
    current: field(current, "identity.luck.current_cycle"),
    ageRange: field(text(published.current_cycle_age), "identity.luck.current_cycle_age"),
    ganZhi: field(ganZhi, "identity.luck.current_cycle_ganzhi"),
    currentYear: field(text(published.current_year), "identity.luck.current_year"),
    currentLiunian: field(
      text(published.current_liunian_ganzhi),
      "identity.luck.current_liunian_ganzhi",
    ),
    observation: field(text(luck?.evidence) || text(luck?.method_note), "luck.evidence | method_note"),
    cycles,
  };
}

function integratedBlockText(raw: unknown): string {
  const rec = asRecord(raw);
  if (!Array.isArray(rec.sentences)) return "";
  return rec.sentences.map((item) => text(item)).filter(Boolean).join(" ");
}

function bindIntegratedBlock(raw: unknown, source: string): WorkspaceField<string> {
  return field(integratedBlockText(raw), source);
}

function bindInterpretation(data: AnalysisDataDto): WorkspaceInterpretationView {
  const published = asRecord(identityOf(data).interpretation);
  const integrated = asRecord(data.integrated_narrative);
  const observationId = text(published.observation_id);
  const reasoningId = text(published.reasoning_id);
  const recommendationId = text(published.recommendation_id);
  const conclusionId = text(published.conclusion_id);
  const sectionKeys = Array.isArray(published.section_keys)
    ? published.section_keys.map((item) => text(item)).filter(Boolean)
    : [];
  return {
    executive: bindIntegratedBlock(
      integrated.executive_summary,
      "integrated_narrative.executive_summary",
    ),
    observe: bindIntegratedBlock(integrated.observation, "integrated_narrative.observation"),
    reason: bindIntegratedBlock(integrated.reasoning, "integrated_narrative.reasoning"),
    impact: bindIntegratedBlock(integrated.impact, "integrated_narrative.impact"),
    advice: bindIntegratedBlock(
      integrated.recommendation,
      "integrated_narrative.recommendation",
    ),
    summary: bindIntegratedBlock(integrated.summary, "integrated_narrative.summary"),
    observationId: field(observationId, "identity.interpretation.observation_id"),
    reasoningId: field(reasoningId, "identity.interpretation.reasoning_id"),
    recommendationId: field(recommendationId, "identity.interpretation.recommendation_id"),
    conclusionId: field(conclusionId, "identity.interpretation.conclusion_id"),
    sectionKeys,
  };
}

function bindConclusion(data: AnalysisDataDto): WorkspaceConclusionView {
  const published = asRecord(identityOf(data).interpretation);
  const action = asRecord(published.action);
  const integrated = asRecord(data.integrated_narrative);
  return {
    summary: bindIntegratedBlock(integrated.summary, "integrated_narrative.summary"),
    overall: field(text(published.conclusion), "identity.interpretation.conclusion"),
    action: field(
      text(action.next_action) || text(action.priority_recommendation),
      "identity.interpretation.action",
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
  const person = bindPerson(data, options);
  return {
    analysisId: person.analysisId.value || "",
    person,
    fourPillars: bindFourPillars(data),
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
