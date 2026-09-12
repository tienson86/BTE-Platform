/**
 * RB06 NumberEnergyPresentationAdapter.
 *
 * Maps a live RB05 analyze `data` object to NumberEnergyPresentationView.
 * Do not import this module into NumberEnergyPage, ResultSection,
 * numberEnergyApp, or leftover analyze helpers.
 * Freeze: NUMBER_ENERGY_STATIC_UI_V1
 */

import {
  GOLDEN_ASSESSMENT_FLOW,
  GOLDEN_ASSESSMENT_STORY,
  GOLDEN_ASSESSMENT_TITLE,
  GOLDEN_RECOMMENDATION_STATE,
  GOLDEN_RECOMMENDATION_SUPPORTING,
  GOLDEN_RECOMMENDATION_TITLE,
} from "./goldenAssessment";
import {
  GOLDEN_BASIS_EVIDENCE,
  GOLDEN_BASIS_HELPER,
  GOLDEN_BASIS_HIGHLIGHTS,
  GOLDEN_BASIS_PRINCIPLES,
  GOLDEN_BASIS_TITLE,
} from "./goldenBasis";
import { GOLDEN_DOMAIN_INSIGHTS } from "./goldenDomains";
import { GOLDEN_ENERGY_DISTRIBUTION } from "./goldenDistribution";
import { GOLDEN_PHONE_HERO } from "./goldenHero";
import { GOLDEN_PHONE_PAIRS } from "./goldenPairs";
import { GOLDEN_QUICK_STRUCTURE } from "./goldenQuickStructure";
import {
  GOLDEN_SCORE_BREAKDOWN,
  GOLDEN_SCORE_GRADE,
  GOLDEN_SCORE_NOTE,
  GOLDEN_SCORE_REASONS,
  GOLDEN_SCORE_TOTAL,
} from "./goldenScore";
import { GOLDEN_CAUTIONS, GOLDEN_STRENGTHS } from "./goldenStrengths";
import { GOLDEN_PHONE_TRIPLES } from "./goldenTriples";
import {
  GOLDEN_WEALTH_STAGES,
  GOLDEN_WEALTH_STORY,
  GOLDEN_WEALTH_SYNTHESIS,
} from "./goldenWealthFlow";
import {
  KIND_TO_CATEGORY,
  NUMBER_ENERGY_CONTRACT_FREEZE,
  PURPOSE_CONTEXT_ALIASES,
  PURPOSE_CONTEXT_CUSTOMER_LABEL,
  RUNTIME_GAP_STATUS,
  type CustomerCategoryLabel,
  type CustomerStrengthLabel,
  type NumberEnergyAdapterResult,
  type NumberEnergyAdapterSource,
  type NumberEnergyPresentationAdapter,
  type PresentationAssessment,
  type PresentationBasis,
  type PresentationDistributionRow,
  type PresentationDomainCard,
  type PresentationExpertSeam,
  type PresentationFindingCard,
  type PresentationFindings,
  type PresentationHero,
  type PresentationPairCard,
  type PresentationQuickStructure,
  type PresentationScore,
  type PresentationSlotId,
  type PresentationTripleCard,
  type PresentationWealthFlow,
  type PresentationWealthStage,
  type RuntimeGap,
  type RuntimeGapId,
  type SlotRenderSource,
} from "./presentationContract";

const HERO_EYEBROW = "Kết quả tư vấn năng lượng số";
const HERO_PRIMARY_LABEL = "Trường chủ đạo";
const HERO_TERMINAL_LABEL = "Năng lượng kết";
const QUICK_FAVORABLE_LABEL = "Cát tinh";
const QUICK_CHALLENGING_LABEL = "Hung tinh";
const QUICK_PRIMARY_LABEL = "Chủ đạo";
const QUICK_TERMINAL_LABEL = "Năng lượng kết";
const PAIR_UNIT = "cặp";
const METHOD_PRINCIPLES = GOLDEN_BASIS_PRINCIPLES.slice(0, 4);
const WEALTH_STAGE_IDS = ["WF-01", "WF-02", "WF-03", "WF-04"] as const;
const HIDDEN_EXPERT: PresentationExpertSeam = {
  visible: false,
  hidden: true,
  ariaHidden: true,
};

/** Catalog chrome for Hero keyword hints. Lookup only — not new copy. */
const HERO_ENERGY_KEYWORDS: Record<string, string> = {
  "Diên Niên": "Công việc · năng lực · trách nhiệm",
  "Thiên Y": "Tài vận · tài nguyên · thành quả",
  "Sinh Khí": "Quý nhân · Cơ hội",
  "Họa Hại": "Giao tiếp · Khẩu tài",
};

type SourceRecord = Record<string, unknown>;

type SlotOutcome<T> = {
  value: T;
  source: SlotRenderSource;
  gaps: RuntimeGap[];
};

type ChainView = {
  primary: string;
  secondaries: readonly string[];
  terminal: string;
  terminalPair: string | null;
  flowSummary: string;
};

type ScoreView = {
  display: string;
  grade: string;
  breakdown: PresentationScore["breakdown"];
  reasons: PresentationScore["reasons"];
};

/**
 * Map runtime analyze data to the frozen Customer presentation view.
 * Missing required fields keep that slot on the Static Golden Fixture.
 */
export const adaptNumberEnergyPresentation: NumberEnergyPresentationAdapter = (
  input: NumberEnergyAdapterSource,
): NumberEnergyAdapterResult => {
  const data = unwrapSource(input);
  const hero = mapHero(data);
  const pairs = mapPairs(data);
  const quick = mapQuickStructure(data);
  const wealth = mapWealthFlow(data);
  const triples = mapTriples(data);
  const distribution = mapDistribution(data);
  const domains = mapDomains(data);
  const findings = mapFindings(data);
  const score = mapScore(data);
  const assessment = mapAssessment(data);
  const basis = mapBasis(data);
  const slotSource: Record<PresentationSlotId, SlotRenderSource> = {
    "P-S00": hero.source,
    "P-S01": pairs.source,
    "P-S02": quick.source,
    "P-S03": wealth.source,
    "P-S04": triples.source,
    "P-S05": distribution.source,
    "P-S06": domains.source,
    "P-S07": findings.source,
    "P-S08": score.source,
    "P-S09": assessment.source,
    "P-S10": basis.source,
    "P-S11": "GOLDEN_FIXTURE",
  };
  return {
    freezeLabel: NUMBER_ENERGY_CONTRACT_FREEZE,
    view: {
      hero: hero.value,
      pairs: pairs.value,
      quick_structure: quick.value,
      wealth_flow: wealth.value,
      triples: triples.value,
      distribution: distribution.value,
      domains: domains.value,
      findings: findings.value,
      score: score.value,
      assessment: assessment.value,
      basis: basis.value,
      expert_seam: HIDDEN_EXPERT,
    },
    slotSource,
    gaps: [
      ...hero.gaps,
      ...pairs.gaps,
      ...quick.gaps,
      ...wealth.gaps,
      ...triples.gaps,
      ...distribution.gaps,
      ...domains.gaps,
      ...findings.gaps,
      ...score.gaps,
      ...assessment.gaps,
      ...basis.gaps,
    ],
  };
};

function unwrapSource(input: NumberEnergyAdapterSource): SourceRecord {
  if (!isRecord(input)) {
    return {};
  }
  const nested = "data" in input ? input.data : undefined;
  const hasLiveKeys =
    "pair_occurrences" in input ||
    "identity" in input ||
    "chain" in input ||
    "score" in input ||
    "pair_summary" in input;
  if (!hasLiveKeys && isRecord(nested)) {
    return nested;
  }
  return input;
}

function mapHero(data: SourceRecord): SlotOutcome<PresentationHero> {
  const gaps: RuntimeGap[] = [];
  const original = readOriginalInput(data);
  const purposeLabel = readPurposeLabel(data);
  const chain = readChain(data);
  const score = readVerifiedScore(data);
  if (!original) {
    gaps.push(gap("G16", "P-S00", "Thiếu dãy số gốc để nhóm hiển thị."));
  }
  if (!purposeLabel) {
    gaps.push(gap("G21", "P-S00", "Thiếu ngữ cảnh sử dụng hợp lệ."));
  }
  if (!chain) {
    gaps.push(gap("G07", "P-S00", "Thiếu chuỗi năng lượng chủ đạo / kết."));
  }
  collectScoreGaps(data, "P-S00", gaps, score);
  if (!original || !purposeLabel || !chain || !score) {
    return { value: { ...GOLDEN_PHONE_HERO }, source: "GOLDEN_FIXTURE", gaps };
  }
  return {
    value: {
      eyebrow: HERO_EYEBROW,
      analysisTypeLabel: purposeLabel,
      displayValue: groupDisplayValue(original, purposeLabel),
      scoreDisplay: score.display,
      grade: score.grade,
      primaryLabel: HERO_PRIMARY_LABEL,
      primaryEnergy: chain.primary,
      primaryKeywords: HERO_ENERGY_KEYWORDS[chain.primary] ?? "",
      terminalLabel: HERO_TERMINAL_LABEL,
      terminalEnergy: chain.terminal,
      terminalKeywords: HERO_ENERGY_KEYWORDS[chain.terminal] ?? "",
      summary: chain.flowSummary,
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapPairs(data: SourceRecord): SlotOutcome<readonly PresentationPairCard[]> {
  const rows = asArray(data.pair_occurrences);
  const mapped = rows ? rows.map(mapPairRow) : null;
  if (!mapped || mapped.some((item) => item === null)) {
    return {
      value: clonePairs(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G19", "P-S01", "Thiếu cặp năng lượng hợp lệ từ runtime.")],
    };
  }
  return { value: mapped as PresentationPairCard[], source: "RUNTIME", gaps: [] };
}

function mapPairRow(value: unknown): PresentationPairCard | null {
  if (!isRecord(value)) {
    return null;
  }
  const digits = asString(value.pair_digits) ?? asString(value.digits);
  const energyLabel = asString(value.display_name) ?? asString(value.energy_label);
  const categoryLabel = readCategory(value);
  const strengthLabel = readStrength(value);
  const strengthDots = readDots(value, strengthLabel);
  if (!digits || !energyLabel || !categoryLabel || !strengthLabel || !strengthDots) {
    return null;
  }
  return {
    digits,
    energyLabel,
    categoryLabel,
    strengthLabel,
    strengthDots,
    keywords: "",
  };
}

function mapQuickStructure(data: SourceRecord): SlotOutcome<PresentationQuickStructure> {
  const summary = readPairSummary(data);
  const chain = readChain(data);
  const gaps: RuntimeGap[] = [];
  if (!summary) {
    gaps.push(gap("G17", "P-S02", "Thiếu tóm tắt số cặp Cát / Hung."));
  }
  if (!chain) {
    gaps.push(gap("G07", "P-S02", "Thiếu chuỗi năng lượng cho cấu trúc nhanh."));
  }
  if (!summary || !chain) {
    return { value: { ...GOLDEN_QUICK_STRUCTURE }, source: "GOLDEN_FIXTURE", gaps };
  }
  return {
    value: {
      favorableLabel: QUICK_FAVORABLE_LABEL,
      favorableValue: `${summary.supportive} ${PAIR_UNIT}`,
      challengingLabel: QUICK_CHALLENGING_LABEL,
      challengingValue: `${summary.challenging} ${PAIR_UNIT}`,
      primaryLabel: QUICK_PRIMARY_LABEL,
      primaryValue: chain.primary,
      terminalLabel: QUICK_TERMINAL_LABEL,
      terminalValue: chain.terminal,
      summary: chain.flowSummary,
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapWealthFlow(data: SourceRecord): SlotOutcome<PresentationWealthFlow> {
  const flow = isRecord(data.wealth_flow) ? data.wealth_flow : null;
  const rows = flow ? asArray(flow.stages) : null;
  const stages = rows ? rows.map(mapWealthStage) : null;
  if (!stages || stages.length !== 4 || stages.some((item) => item === null)) {
    return {
      value: cloneWealth(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G05", "P-S03", "Thiếu bốn tầng dòng tài vận từ runtime.")],
    };
  }
  const story = readWealthStory(data);
  return {
    value: {
      stages: stages as PresentationWealthStage[],
      story: story.nodes,
      synthesis: story.synthesis,
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapWealthStage(value: unknown): PresentationWealthStage | null {
  if (!isRecord(value)) {
    return null;
  }
  const id = asString(value.id);
  const headline = asString(value.headline) ?? asString(value.headline_key);
  const narrative = asString(value.narrative) ?? asString(value.narrative_key);
  if (!id || !isWealthStageId(id)) {
    return null;
  }
  return {
    id,
    label: asString(value.label) ?? asString(value.label_key) ?? "",
    headline: headline ?? "",
    evidence: asString(value.evidence) ?? "",
    interaction: asString(value.interaction) ?? asString(value.interaction_key) ?? "",
    narrative: narrative ?? "",
  };
}

function mapTriples(data: SourceRecord): SlotOutcome<readonly PresentationTripleCard[]> {
  const rows = asArray(data.triple_occurrences);
  if (!rows) {
    return {
      value: cloneTriples(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G08", "P-S04", "Thiếu bộ ba năng lượng từ runtime.")],
    };
  }
  const mapped = rows.map(mapTripleRow);
  if (mapped.some((item) => item === null)) {
    return {
      value: cloneTriples(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G09", "P-S04", "Bộ ba runtime thiếu diễn giải khách hàng.")],
    };
  }
  return { value: mapped as PresentationTripleCard[], source: "RUNTIME", gaps: [] };
}

function mapTripleRow(value: unknown): PresentationTripleCard | null {
  if (!isRecord(value)) {
    return null;
  }
  const digits = asString(value.digits);
  const sourceLabel = asString(value.left_energy_label) ?? asString(value.source_label);
  const targetLabel = asString(value.right_energy_label) ?? asString(value.target_label);
  if (!digits || !sourceLabel || !targetLabel) {
    return null;
  }
  const undefinedStatus = asString(value.interpretation_status) === "UNDEFINED";
  const title = undefinedStatus ? "" : asString(value.customer_title) ?? "";
  const narrative = undefinedStatus ? "" : asString(value.customer_summary) ?? "";
  if (!undefinedStatus && (!title || !narrative)) {
    return null;
  }
  return {
    digits,
    sourceLabel,
    targetLabel,
    title,
    narrative,
    domains: formatDomains(value.domains),
    priority: readTriplePriority(value.priority),
  };
}

function mapDistribution(data: SourceRecord): SlotOutcome<readonly PresentationDistributionRow[]> {
  const rows = readDistributionRows(data);
  const chain = readChain(data);
  const gaps: RuntimeGap[] = [];
  if (!rows || rows.length !== 8) {
    gaps.push(gap("G18", "P-S05", "Thiếu đủ tám trường phân bố từ runtime."));
  }
  if (!chain) {
    gaps.push(gap("G07", "P-S05", "Thiếu chuỗi năng lượng để gán vai trò phân bố."));
  }
  if (!rows || rows.length !== 8 || !chain) {
    return { value: cloneDistribution(), source: "GOLDEN_FIXTURE", gaps };
  }
  return {
    value: rows.map((row) => ({
      label: row.label,
      count: row.count,
      role:
        row.label === chain.primary
          ? "primary"
          : chain.secondaries.includes(row.label)
            ? "secondary"
            : "none",
    })),
    source: "RUNTIME",
    gaps: [],
  };
}

function mapDomains(data: SourceRecord): SlotOutcome<readonly PresentationDomainCard[]> {
  const rows = asArray(data.domain_insights);
  const mapped = rows ? rows.map(mapDomainRow) : null;
  if (!mapped || mapped.length !== 5 || mapped.some((item) => item === null)) {
    return {
      value: cloneDomains(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G10", "P-S06", "Thiếu năm miền luận giải từ runtime.")],
    };
  }
  return { value: mapped as PresentationDomainCard[], source: "RUNTIME", gaps: [] };
}

function mapDomainRow(value: unknown): PresentationDomainCard | null {
  if (!isRecord(value)) {
    return null;
  }
  const title = asString(value.domain) ?? asString(value.title);
  const conclusion = asString(value.conclusion);
  const narrative = asString(value.narrative);
  if (!title || !conclusion || narrative === null) {
    return null;
  }
  return {
    title,
    conclusion,
    narrative,
    caution: asString(value.caution) ?? "",
  };
}

function mapFindings(data: SourceRecord): SlotOutcome<PresentationFindings> {
  const strengths = asArray(data.strengths);
  const cautions = asArray(data.cautions);
  const mappedStrengths = strengths ? strengths.map(mapFindingRow) : null;
  const mappedCautions = cautions ? cautions.map(mapFindingRow) : null;
  if (
    !mappedStrengths ||
    !mappedCautions ||
    mappedStrengths.some((item) => item === null) ||
    mappedCautions.some((item) => item === null)
  ) {
    return {
      value: cloneFindings(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G12", "P-S07", "Thiếu điểm mạnh / lưu ý từ runtime.")],
    };
  }
  return {
    value: {
      strengths: mappedStrengths as PresentationFindingCard[],
      cautions: mappedCautions as PresentationFindingCard[],
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapFindingRow(value: unknown): PresentationFindingCard | null {
  if (!isRecord(value)) {
    return null;
  }
  const title = asString(value.title);
  const copy = asString(value.summary) ?? asString(value.copy);
  if (!title || copy === null) {
    return null;
  }
  return { title, copy };
}

function mapScore(data: SourceRecord): SlotOutcome<PresentationScore> {
  const score = readVerifiedScore(data);
  const gaps: RuntimeGap[] = [];
  collectScoreGaps(data, "P-S08", gaps, score);
  if (!score) {
    return { value: cloneScore(), source: "GOLDEN_FIXTURE", gaps };
  }
  return {
    value: {
      totalDisplay: score.display,
      grade: score.grade,
      note: "",
      breakdown: score.breakdown,
      reasons: score.reasons,
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapAssessment(data: SourceRecord): SlotOutcome<PresentationAssessment> {
  const assessment = isRecord(data.assessment) ? data.assessment : null;
  const recommendation = isRecord(data.recommendation) ? data.recommendation : null;
  const gaps: RuntimeGap[] = [];
  if (!assessment) {
    gaps.push(gap("G13", "P-S09", "Thiếu đánh giá tổng thể từ runtime."));
  }
  if (!recommendation) {
    gaps.push(gap("G14", "P-S09", "Thiếu khuyến nghị từ runtime."));
  }
  const title = assessment ? asString(assessment.title) : null;
  const summary = assessment ? asString(assessment.summary) : null;
  const state =
    (recommendation ? asString(recommendation.label) : null) ??
    (recommendation ? asString(recommendation.state) : null);
  const supporting = recommendation ? asString(recommendation.summary) : null;
  if (!assessment || !recommendation || !title || !summary || supporting === null) {
    return { value: cloneAssessment(), source: "GOLDEN_FIXTURE", gaps };
  }
  return {
    value: {
      title,
      story: splitStory(summary),
      flow: readAssessmentFlow(assessment),
      recommendationTitle: GOLDEN_RECOMMENDATION_TITLE,
      recommendationState: state ?? "CẦN CÂN BẰNG THÊM",
      recommendationSupporting: supporting,
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapBasis(data: SourceRecord): SlotOutcome<PresentationBasis> {
  const groups = asArray(data.evidence);
  const chain = readChain(data);
  const summary = readPairSummary(data);
  if (!groups || groups.length === 0) {
    return {
      value: cloneBasis(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G15", "P-S10", "Thiếu nhóm bằng chứng từ runtime.")],
    };
  }
  const evidence = groups.map(mapEvidenceGroup).filter((item): item is NonNullable<typeof item> => item !== null);
  if (evidence.length === 0) {
    return {
      value: cloneBasis(),
      source: "GOLDEN_FIXTURE",
      gaps: [gap("G15", "P-S10", "Thiếu nhóm bằng chứng từ runtime.")],
    };
  }
  return {
    value: {
      title: GOLDEN_BASIS_TITLE,
      helper: GOLDEN_BASIS_HELPER,
      principles: METHOD_PRINCIPLES,
      highlights: buildHighlights(chain, summary),
      evidence,
    },
    source: "RUNTIME",
    gaps: [],
  };
}

function mapEvidenceGroup(
  value: unknown,
): { group: string; items: readonly string[] } | null {
  if (!isRecord(value)) {
    return null;
  }
  const group = asString(value.title) ?? asString(value.group);
  const items = asArray(value.items);
  if (!group || !items) {
    return null;
  }
  const mapped = items
    .map(formatEvidenceItem)
    .filter((item): item is string => Boolean(item));
  if (mapped.length === 0) {
    return null;
  }
  return { group, items: mapped };
}

function formatEvidenceItem(value: unknown): string | null {
  if (typeof value === "string" && value.trim()) {
    return value.trim();
  }
  if (!isRecord(value)) {
    return null;
  }
  const label = asString(value.label);
  const ref = asString(value.ref);
  if (label && ref && isCustomerRef(ref)) {
    return `${ref} · ${label}`;
  }
  if (label) {
    return label;
  }
  if (ref && isCustomerRef(ref)) {
    return ref;
  }
  return null;
}

function buildHighlights(
  chain: ChainView | null,
  summary: { pairCount: number; supportive: number; challenging: number } | null,
): readonly { label: string; value: string }[] {
  const highlights: { label: string; value: string }[] = [];
  if (chain) {
    const labels = [chain.primary];
    if (!labels.includes(chain.terminal)) {
      labels.push(chain.terminal);
    }
    for (const item of chain.secondaries) {
      if (!labels.includes(item)) {
        labels.push(item);
      }
    }
    highlights.push({ label: "Trường nổi bật", value: labels.join(" · ") });
    const terminalValue = chain.terminalPair
      ? `${chain.terminalPair} · ${chain.terminal}`
      : chain.terminal;
    highlights.push({ label: "Năng lượng kết", value: terminalValue });
  }
  if (summary) {
    highlights.push({
      label: "Tổng cặp",
      value: `${summary.pairCount} cặp · ${summary.supportive} Cát · ${summary.challenging} Hung`,
    });
  }
  return highlights;
}

function readOriginalInput(data: SourceRecord): string | null {
  const identity = isRecord(data.identity) ? data.identity : null;
  return (
    (identity ? asString(identity.original_input) : null) ??
    asString(data.input_raw) ??
    (isRecord(data.metadata) ? asString(data.metadata.input_raw) : null) ??
    (isRecord(data.reading) ? asString(data.reading.display_number) : null)
  );
}

function readPurposeLabel(data: SourceRecord): string | null {
  const raw =
    asString(data.purpose_context) ??
    (isRecord(data.metadata) ? asString(data.metadata.purpose_context) : null);
  if (!raw) {
    return null;
  }
  const aliased =
    PURPOSE_CONTEXT_ALIASES[raw as keyof typeof PURPOSE_CONTEXT_ALIASES] ?? raw;
  return PURPOSE_CONTEXT_CUSTOMER_LABEL[aliased as keyof typeof PURPOSE_CONTEXT_CUSTOMER_LABEL] ?? null;
}

function readChain(data: SourceRecord): ChainView | null {
  if (!isRecord(data.chain)) {
    return null;
  }
  const primary = asString(data.chain.primary_energy_label);
  const terminal = asString(data.chain.terminal_energy_label);
  if (!primary || !terminal) {
    return null;
  }
  const secondaries = asArray(data.chain.secondary_energy_labels)
    ?.map((item) => asString(item))
    .filter((item): item is string => Boolean(item)) ?? [];
  return {
    primary,
    secondaries,
    terminal,
    terminalPair: asString(data.chain.terminal_pair_digits),
    flowSummary: asString(data.chain.dominant_flow_summary) ?? "",
  };
}

function readPairSummary(
  data: SourceRecord,
): { pairCount: number; supportive: number; challenging: number } | null {
  if (!isRecord(data.pair_summary)) {
    return null;
  }
  const pairCount = asNumber(data.pair_summary.pair_count);
  const supportive =
    asNumber(data.pair_summary.supportive_pair_count) ??
    asNumber(data.pair_summary.favorable_count);
  const challenging =
    asNumber(data.pair_summary.challenging_pair_count) ??
    asNumber(data.pair_summary.challenging_count);
  if (pairCount === null || supportive === null || challenging === null) {
    return null;
  }
  return { pairCount, supportive, challenging };
}

function readVerifiedScore(data: SourceRecord): ScoreView | null {
  const score = isRecord(data.score) ? data.score : null;
  if (!score) {
    return null;
  }
  const verified =
    data.verified_by_runtime === true || score.verified_by_runtime === true;
  if (!verified) {
    return null;
  }
  const display =
    asString(score.display) ??
    (asNumber(score.total) !== null && asNumber(score.max) !== null
      ? `${asNumber(score.total)} / ${asNumber(score.max)}`
      : asNumber(score.final_score) !== null
        ? `${asNumber(score.final_score)} / 100`
        : null);
  const grade = asString(score.grade) ?? asString(data.grade);
  const breakdown = readScoreBreakdown(score);
  const reasons = readScoreReasons(score);
  if (!display || !grade || !breakdown) {
    return null;
  }
  return { display, grade, breakdown, reasons: reasons ?? [] };
}

function readScoreBreakdown(score: SourceRecord): PresentationScore["breakdown"] | null {
  const rows = asArray(score.breakdown);
  if (!rows || rows.length !== 5) {
    return null;
  }
  const mapped = rows.map((item) => {
    if (!isRecord(item)) {
      return null;
    }
    const label = asString(item.label);
    const earned = asNumber(item.earned);
    const max = asNumber(item.max);
    if (!label || earned === null || max === null) {
      return null;
    }
    return { label, earned, max };
  });
  if (mapped.some((item) => item === null)) {
    return null;
  }
  return mapped as PresentationScore["breakdown"];
}

function readScoreReasons(score: SourceRecord): PresentationScore["reasons"] | null {
  const rows = asArray(score.reasons) ?? asArray(score.score_reasons);
  if (!rows || rows.length === 0) {
    return null;
  }
  const mapped = rows.map((item) => {
    if (!isRecord(item)) {
      return null;
    }
    const title = asString(item.title);
    const copy = asString(item.summary) ?? asString(item.copy);
    if (!title || copy === null) {
      return null;
    }
    return { title, copy };
  });
  if (mapped.some((item) => item === null)) {
    return null;
  }
  return mapped as PresentationScore["reasons"];
}

function collectScoreGaps(
  data: SourceRecord,
  slot: PresentationSlotId,
  gaps: RuntimeGap[],
  score: ScoreView | null,
): void {
  if (score) {
    return;
  }
  const raw = isRecord(data.score) ? data.score : null;
  if (!raw) {
    gaps.push(gap("G01", slot, "Thiếu điểm đánh giá từ runtime."));
    gaps.push(gap("G02", slot, "Thiếu xếp loại từ runtime."));
    gaps.push(gap("G20", slot, "Điểm chưa được runtime xác nhận."));
    return;
  }
  if (data.verified_by_runtime !== true && raw.verified_by_runtime !== true) {
    gaps.push(gap("G20", slot, "Điểm chưa được runtime xác nhận."));
  }
  if (!asString(raw.display) && asNumber(raw.total) === null && asNumber(raw.final_score) === null) {
    gaps.push(gap("G01", slot, "Thiếu điểm đánh giá từ runtime."));
  }
  if (!asString(raw.grade) && !asString(data.grade)) {
    gaps.push(gap("G02", slot, "Thiếu xếp loại từ runtime."));
  }
}

function readDistributionRows(
  data: SourceRecord,
): { label: string; count: number }[] | null {
  const rows = asArray(data.energy_distribution);
  if (!rows) {
    return null;
  }
  const mapped = rows.map((item) => {
    if (!isRecord(item)) {
      return null;
    }
    const label = asString(item.energy_label) ?? asString(item.label);
    const count = asNumber(item.count);
    if (!label || count === null) {
      return null;
    }
    return { label, count };
  });
  if (mapped.some((item) => item === null)) {
    return null;
  }
  return mapped as { label: string; count: number }[];
}

function readWealthStory(data: SourceRecord): { nodes: readonly string[]; synthesis: string } {
  if (!isRecord(data.wealth_story)) {
    return { nodes: [], synthesis: "" };
  }
  const nodes = asArray(data.wealth_story.nodes)
    ?.map((item) => asString(item))
    .filter((item): item is string => Boolean(item));
  if (nodes && nodes.length > 0) {
    return {
      nodes,
      synthesis: asString(data.wealth_story.synthesis) ?? "",
    };
  }
  const display = asString(data.wealth_story.display);
  return {
    nodes: display ? display.split(" → ").map((item) => item.trim()).filter(Boolean) : [],
    synthesis: asString(data.wealth_story.synthesis) ?? "",
  };
}

function readAssessmentFlow(assessment: SourceRecord): readonly string[] {
  const nodes = asArray(assessment.story_nodes)
    ?.map((item) => asString(item))
    .filter((item): item is string => Boolean(item));
  if (nodes && nodes.length > 0) {
    return nodes;
  }
  const line = asString(assessment.story_line);
  return line ? line.split(" → ").map((item) => item.trim()).filter(Boolean) : [];
}

function readCategory(row: SourceRecord): CustomerCategoryLabel | null {
  const label = asString(row.category_label);
  if (label === "Cát" || label === "Hung") {
    return label;
  }
  const category = asString(row.category);
  if (category === "Cát" || category === "Hung") {
    return category;
  }
  if (category === "CAT") {
    return "Cát";
  }
  if (category === "HUNG") {
    return "Hung";
  }
  const kind = asString(row.kind);
  if (kind === "supportive" || kind === "challenging") {
    return KIND_TO_CATEGORY[kind];
  }
  return null;
}

function readStrength(row: SourceRecord): CustomerStrengthLabel | null {
  const label = asString(row.strength_label);
  if (label === "Nhẹ" || label === "Mạnh") {
    return label;
  }
  return null;
}

function readDots(
  row: SourceRecord,
  label: CustomerStrengthLabel | null,
): [boolean, boolean, boolean, boolean] | null {
  const visual = row.strength_visual;
  if (Array.isArray(visual) && visual.length === 4 && visual.every((item) => typeof item === "boolean")) {
    return [visual[0], visual[1], visual[2], visual[3]];
  }
  if (label === "Nhẹ") {
    return [true, false, false, false];
  }
  if (label === "Mạnh") {
    return [true, true, true, false];
  }
  return null;
}

function readTriplePriority(value: unknown): PresentationTripleCard["priority"] {
  const raw = asString(value)?.toLowerCase();
  if (raw === "featured" || raw === "compact" || raw === "standard") {
    return raw;
  }
  return "standard";
}

function formatDomains(value: unknown): string {
  if (typeof value === "string") {
    return value;
  }
  const rows = asArray(value)
    ?.map((item) => asString(item))
    .filter((item): item is string => Boolean(item));
  return rows ? rows.join(" · ") : "";
}

function groupDisplayValue(original: string, purposeLabel: string): string {
  if (purposeLabel !== PURPOSE_CONTEXT_CUSTOMER_LABEL.phone_number) {
    return original;
  }
  const digits = original.replace(/\D/g, "");
  if (digits.length === 10) {
    return `${digits.slice(0, 4)} ${digits.slice(4, 7)} ${digits.slice(7)}`;
  }
  return digits || original;
}

function splitStory(summary: string): readonly string[] {
  const parts = summary.split(/(?<=\.)\s+/).map((item) => item.trim()).filter(Boolean);
  return parts.length > 0 ? parts : [summary];
}

function isCustomerRef(ref: string): boolean {
  if (ref.startsWith("WF-") || ref.includes("_")) {
    return false;
  }
  return /[0-9]/.test(ref) || /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/.test(ref);
}

function isWealthStageId(value: string): value is PresentationWealthStage["id"] {
  return (WEALTH_STAGE_IDS as readonly string[]).includes(value);
}

function clonePairs(): PresentationPairCard[] {
  return GOLDEN_PHONE_PAIRS.map((pair) => ({
    ...pair,
    strengthDots: cloneDots(pair.strengthDots),
  }));
}

function cloneWealth(): PresentationWealthFlow {
  return {
    stages: GOLDEN_WEALTH_STAGES.map((stage) => ({ ...stage })),
    story: [...GOLDEN_WEALTH_STORY],
    synthesis: GOLDEN_WEALTH_SYNTHESIS,
  };
}

function cloneTriples(): PresentationTripleCard[] {
  return GOLDEN_PHONE_TRIPLES.map((item) => ({ ...item }));
}

function cloneDistribution(): PresentationDistributionRow[] {
  return GOLDEN_ENERGY_DISTRIBUTION.map((item) => ({
    label: item.label,
    count: item.count,
    role: item.role,
  }));
}

function cloneDomains(): PresentationDomainCard[] {
  return GOLDEN_DOMAIN_INSIGHTS.map((item) => ({ ...item }));
}

function cloneFindings(): PresentationFindings {
  return {
    strengths: GOLDEN_STRENGTHS.map((item) => ({ ...item })),
    cautions: GOLDEN_CAUTIONS.map((item) => ({ ...item })),
  };
}

function cloneScore(): PresentationScore {
  return {
    totalDisplay: GOLDEN_SCORE_TOTAL,
    grade: GOLDEN_SCORE_GRADE,
    note: GOLDEN_SCORE_NOTE,
    breakdown: GOLDEN_SCORE_BREAKDOWN.map((item) => ({ ...item })),
    reasons: GOLDEN_SCORE_REASONS.map((item) => ({ ...item })),
  };
}

function cloneAssessment(): PresentationAssessment {
  return {
    title: GOLDEN_ASSESSMENT_TITLE,
    story: [...GOLDEN_ASSESSMENT_STORY],
    flow: [...GOLDEN_ASSESSMENT_FLOW],
    recommendationTitle: GOLDEN_RECOMMENDATION_TITLE,
    recommendationState: GOLDEN_RECOMMENDATION_STATE,
    recommendationSupporting: GOLDEN_RECOMMENDATION_SUPPORTING,
  };
}

function cloneBasis(): PresentationBasis {
  return {
    title: GOLDEN_BASIS_TITLE,
    helper: GOLDEN_BASIS_HELPER,
    principles: [...GOLDEN_BASIS_PRINCIPLES],
    highlights: GOLDEN_BASIS_HIGHLIGHTS.map((item) => ({ ...item })),
    evidence: GOLDEN_BASIS_EVIDENCE.map((item) => ({
      group: item.group,
      items: [...item.items],
    })),
  };
}

function cloneDots(
  dots: readonly [boolean, boolean, boolean, boolean],
): [boolean, boolean, boolean, boolean] {
  return [dots[0], dots[1], dots[2], dots[3]];
}

function gap(id: RuntimeGapId, slot: PresentationSlotId, message: string): RuntimeGap {
  return { id, slot, status: RUNTIME_GAP_STATUS, message };
}

function isRecord(value: unknown): value is SourceRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function asArray(value: unknown): unknown[] | null {
  return Array.isArray(value) ? value : null;
}

function asString(value: unknown): string | null {
  return typeof value === "string" && value.trim() ? value.trim() : null;
}

function asNumber(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}
