/**
 * Live analyze payload → CanonicalReportInput for Result V2.
 * Pure mapping only. No fabrication of consulting content.
 */

import {
  asNarrativeResult,
  careerFieldText,
  careerSelectionFromNarrative,
  executiveFromNarrative,
  hasUsableNarrativeResult,
  primaryRecommendationFromNarrative,
  type NarrativeRecommendationDto,
  type NarrativeResultDto,
  type NarrativeSectionDto,
} from "../../adapters/narrativeResultAdapter";
import {
  canonicalStrengthLabel,
  formatCanonicalStrengthScore,
  readCanonicalStrengthScore,
} from "../../adapters/canonicalStrength";
import {
  canonicalBalancingNeedLabel,
  canonicalClimateStateLabel,
  canonicalTemperatureEvidence,
  canonicalTemperatureScore,
} from "../../adapters/canonicalTemperature";
import {
  formatFiveElementsCompact,
  canonicalFiveElementCounts,
  fiveElementUnitTotal,
  publishedFiveElementsMethodNote,
} from "../../adapters/canonicalFiveElements";
import type { AnalysisDataDto, BaziDto, CustomerEchoDto, PillarDto } from "../../models";
import type {
  CanonicalReportInput,
  PresentationIdentity,
  PresentationKnowledge,
  PresentationRecommendation,
  PresentationTechnical,
  PresentationWarning,
  ReportPresentationEnvelope,
} from "../result_v2/adapter/reportInput";

export type LiveAnalysisAdapterOptions = {
  readonly analysis_id?: string | null;
};

export type LiveAnalysisMapSuccess = {
  readonly ok: true;
  readonly report: CanonicalReportInput;
};

export type LiveAnalysisMapFailure = {
  readonly ok: false;
  readonly error_code: string;
  readonly error_message: string;
};

export type LiveAnalysisMapResult = LiveAnalysisMapSuccess | LiveAnalysisMapFailure;

const ERROR_MALFORMED_VI =
  "Không thể hiển thị kết quả vì dữ liệu phân tích không hợp lệ.";
const ERROR_INCOMPLETE_VI =
  "Không thể hiển thị kết quả vì thiếu nội dung tư vấn cần thiết.";

function asText(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  return text.length > 0 ? text : null;
}

function mapConsultationStatus(status: string | null | undefined): string {
  switch ((status ?? "").trim().toLowerCase()) {
    case "complete":
      return "ready";
    case "failed":
      return "error";
    case "partial_insufficient":
      return "partial";
    default:
      return "partial";
  }
}

function formatPillar(pillar: PillarDto | undefined): string | null {
  if (!pillar) return null;
  const stem = asText(pillar.stem);
  const branch = asText(pillar.branch);
  if (!stem && !branch) return null;
  return [stem, branch].filter(Boolean).join(" ");
}

/** Labeled four pillars for first-read technical display. */
export function formatLabeledPillars(bazi: BaziDto | undefined): string | null {
  if (!bazi) return null;
  const rows: string[] = [];
  const year = formatPillar(bazi.year_pillar);
  const month = formatPillar(bazi.month_pillar);
  const day = formatPillar(bazi.day_pillar);
  const hour = formatPillar(bazi.hour_pillar);
  if (year) rows.push(`Năm ${year}`);
  if (month) rows.push(`Tháng ${month}`);
  if (day) rows.push(`Ngày ${day}`);
  if (hour) rows.push(`Giờ ${hour}`);
  return rows.length > 0 ? rows.join(" · ") : null;
}

function pickPatternLabel(data: AnalysisDataDto): string | null {
  const pattern = data.pattern;
  if (!pattern || typeof pattern !== "object") return null;
  return (
    asText(pattern.cach_cuc) ??
    asText(pattern.tong_cach) ??
    asText(pattern.pattern)
  );
}

function pickDayMaster(data: AnalysisDataDto): string | null {
  return asText(data.bazi?.day_master);
}

function pickStrengthLabel(data: AnalysisDataDto): string | null {
  const mapped = canonicalStrengthLabel(data);
  if (mapped) return mapped;
  const strength = data.strength;
  if (!strength || typeof strength !== "object") return null;
  return asText(strength.reasoning) ?? asText(strength.strength_level);
}

function pickStrengthScore(data: AnalysisDataDto): string | null {
  const raw = readCanonicalStrengthScore(data);
  if (raw === null) return null;
  return formatCanonicalStrengthScore(raw);
}

function pickScoreGrade(data: AnalysisDataDto): string | null {
  return asText(data.score?.grade);
}

function pickScoreRecommendation(data: AnalysisDataDto): string | null {
  return asText(data.score?.recommendation);
}

/**
 * Hero uses concise chart facts from structured API fields — not long career prose.
 */
function buildIdentity(
  customer: CustomerEchoDto | undefined,
  data: AnalysisDataDto,
  narrative: NarrativeResultDto,
): PresentationIdentity | null {
  const fullName = asText(customer?.full_name);
  if (!fullName) return null;

  const dayMaster = pickDayMaster(data);
  const pattern = pickPatternLabel(data);
  const chartHeadline = [dayMaster, pattern].filter(Boolean).join(" · ");

  const strength = pickStrengthLabel(data);
  const grade = pickScoreGrade(data);
  const scoreLine = pickScoreRecommendation(data);
  const chartOneLine =
    [strength, grade ? `Hạng ${grade}` : null].filter(Boolean).join(" · ") ||
    scoreLine;

  const executive = executiveFromNarrative(narrative);
  const headline =
    asText(chartHeadline) ??
    asText(executive?.central_message) ??
    asText(narrative.summary?.identity);
  const oneLine =
    asText(chartOneLine) ??
    asText(executive?.conclusion) ??
    asText(narrative.summary?.priority_recommendation) ??
    asText(narrative.summary?.next_action);

  if (!headline || !oneLine) return null;

  return {
    full_name: fullName,
    headline,
    one_line_summary: oneLine,
    consultation_status: mapConsultationStatus(narrative.status),
  };
}

/**
 * Summary leads with chart fundamentals, then optional short executive points.
 */
function collectSummaryBullets(
  data: AnalysisDataDto,
  narrative: NarrativeResultDto,
): string[] {
  const bullets: string[] = [];
  const push = (value: unknown): void => {
    const text = asText(value);
    if (!text) return;
    if (bullets.includes(text)) return;
    bullets.push(text);
  };

  const pillars = formatLabeledPillars(data.bazi);
  if (pillars) push(pillars);
  const dayMaster = pickDayMaster(data);
  if (dayMaster) push(`Nhật chủ: ${dayMaster}`);
  const pattern = pickPatternLabel(data);
  if (pattern) push(`Cách cục: ${pattern}`);
  const strength = pickStrengthLabel(data);
  const strengthScore = pickStrengthScore(data);
  if (strength && strengthScore) push(`${strength} (${strengthScore})`);
  else if (strength) push(strength);
  const grade = pickScoreGrade(data);
  const scoreRec = pickScoreRecommendation(data);
  if (grade && scoreRec) push(`Điểm ${grade}: ${scoreRec}`);
  else if (grade) push(`Điểm: ${grade}`);
  else if (scoreRec) push(scoreRec);

  const executive = executiveFromNarrative(narrative);
  for (const point of executive?.supporting_points ?? []) {
    if (bullets.length >= 5) break;
    push(point);
  }

  if (bullets.length === 0) {
    for (const strengthItem of narrative.summary?.strengths ?? []) {
      push(strengthItem);
      if (bullets.length >= 5) break;
    }
  }

  return bullets.slice(0, 5);
}

function mapPriorityNumber(priority: string | null | undefined): number | null {
  switch ((priority ?? "").trim().toLowerCase()) {
    case "critical":
      return 1;
    case "high":
      return 2;
    case "medium":
      return 3;
    case "low":
      return 4;
    default:
      return null;
  }
}

function mapPrimaryCareerRecommendation(
  narrative: NarrativeResultDto,
): PresentationRecommendation | null {
  const primary = primaryRecommendationFromNarrative(narrative);
  if (!primary) return null;
  const title = asText(primary.what);
  const reason = asText(primary.why);
  const action = asText(primary.how);
  const expected = asText(primary.expected_outcome);
  if (!title || !reason || !action || !expected) return null;
  return {
    id: "rec_career_primary",
    domain: "career",
    title,
    reason,
    expected_result: expected,
    action,
    detail: asText(primary.composed_text) ?? asText(primary.when),
    priority: 1,
  };
}

function mapRootRecommendationsWithDomain(
  items: readonly NarrativeRecommendationDto[] | undefined,
): PresentationRecommendation[] {
  if (!items?.length) return [];
  const mapped: PresentationRecommendation[] = [];
  for (const [index, item] of items.entries()) {
    if (item.insufficient_data) continue;
    const record = item as NarrativeRecommendationDto & { domain?: string };
    const domain = asText(record.domain);
    if (
      domain !== "career" &&
      domain !== "wealth" &&
      domain !== "relationship" &&
      domain !== "health" &&
      domain !== "luck"
    ) {
      continue;
    }
    const title = asText(item.action);
    const reason = asText(item.reason);
    const expected = asText(item.benefit);
    const action = asText(item.action);
    if (!title || !reason || !expected || !action) continue;
    mapped.push({
      id: asText(item.id) ?? `rec_${domain}_${index}`,
      domain,
      title,
      reason,
      expected_result: expected,
      action,
      detail: null,
      priority: mapPriorityNumber(item.priority),
    });
  }
  return mapped;
}

function mapCareerWarnings(narrative: NarrativeResultDto): PresentationWarning[] {
  const career = careerSelectionFromNarrative(narrative);
  const risk = careerFieldText(career, "career_risks");
  const mitigation = careerFieldText(career, "career_mitigation");
  if (!risk) return [];
  const title = risk.split(/[.\n]/)[0]?.trim() || risk;
  return [
    {
      title,
      body: risk,
      mitigation: mitigation || null,
      severity: "attention",
    },
  ];
}

function sectionParagraphBody(section: NarrativeSectionDto): string | null {
  const parts: string[] = [];
  for (const paragraph of section.paragraphs ?? []) {
    if (paragraph.insufficient_data) continue;
    const text = asText(paragraph.text);
    if (text) parts.push(text);
  }
  return parts.length > 0 ? parts.join("\n\n") : null;
}

/**
 * Map Pack 05 narrative sections → presentation.knowledge (titled expandable blocks).
 * Preserves source order and section titles; no invented titles.
 */
function mapNarrativeSectionsToKnowledge(
  narrative: NarrativeResultDto,
): PresentationKnowledge[] {
  const items: PresentationKnowledge[] = [];
  for (const section of narrative.sections ?? []) {
    const title = asText(section.title);
    const body = sectionParagraphBody(section);
    if (!title || !body) continue;
    const teaser = asText(section.paragraphs?.[0]?.text) ?? body;
    items.push({
      title,
      teaser,
      body,
    });
  }
  return items;
}

/**
 * Career domain uses Career Selection Assessment fields only.
 * Does not re-mount the seven narrative sections (avoids Portal duplication).
 */
function careerAnalysisFromAssessment(
  narrative: NarrativeResultDto,
): { preview: string | null; detail: string | null } {
  const career = careerSelectionFromNarrative(narrative);
  if (!career) return { preview: null, detail: null };

  // Risks/mitigation already surface in Warnings — omit here.
  const detailKeys = [
    "working_environment",
    "preferred_role",
    "leadership_posture",
    "employment_posture",
    "career_strengths",
    "development_focus",
    "timing_guidance",
    "action_plan_90d",
  ] as const;

  const preview =
    asText(careerFieldText(career, "career_direction")) ??
    asText(careerFieldText(career, "working_environment"));

  const detailParts: string[] = [];
  for (const key of detailKeys) {
    const text = asText(careerFieldText(career, key));
    if (!text) continue;
    if (preview && text === preview) continue;
    detailParts.push(text);
  }

  return {
    preview,
    detail: detailParts.length > 0 ? detailParts.join("\n\n") : null,
  };
}

function buildTechnical(
  data: AnalysisDataDto,
  analysisId: string | null,
  narrative: NarrativeResultDto,
): PresentationTechnical {
  const customer = data.customer;
  const metadata: Record<string, unknown> = {};

  const year = formatPillar(data.bazi?.year_pillar);
  const month = formatPillar(data.bazi?.month_pillar);
  const day = formatPillar(data.bazi?.day_pillar);
  const hour = formatPillar(data.bazi?.hour_pillar);
  if (year) metadata.year_pillar = year;
  if (month) metadata.month_pillar = month;
  if (day) metadata.day_pillar = day;
  if (hour) metadata.hour_pillar = hour;

  const dayMaster = pickDayMaster(data);
  if (dayMaster) metadata.day_master = dayMaster;
  const pattern = pickPatternLabel(data);
  if (pattern) metadata.pattern = pattern;
  const patternEvidence = asText(
    data.pattern && typeof data.pattern === "object"
      ? (data.pattern as { evidence_compact?: unknown }).evidence_compact
      : null,
  );
  if (patternEvidence) metadata.pattern_evidence = patternEvidence;
  const climateState = canonicalClimateStateLabel(data);
  if (climateState) metadata.climate_state = climateState;
  const balancingNeed = canonicalBalancingNeedLabel(data);
  if (balancingNeed) metadata.balancing_need = balancingNeed;
  const climateEvidence = canonicalTemperatureEvidence(data);
  if (climateEvidence) metadata.climate_evidence = climateEvidence;
  const temperatureScore = canonicalTemperatureScore(data);
  if (temperatureScore) metadata.temperature_score = temperatureScore;
  const fiveCounts = canonicalFiveElementCounts(data);
  const distribution = formatFiveElementsCompact(fiveCounts);
  if (distribution) metadata.five_elements_distribution = distribution;
  const unitTotal = fiveElementUnitTotal(fiveCounts);
  if (unitTotal > 0) metadata.five_elements_total = unitTotal;
  const methodNote = publishedFiveElementsMethodNote(data);
  if (fiveCounts) metadata.five_elements_method = methodNote;
  const strength = pickStrengthLabel(data);
  if (strength) metadata.strength = strength;
  const strengthScore = pickStrengthScore(data);
  if (strengthScore) metadata.strength_score = strengthScore;
  const grade = pickScoreGrade(data);
  if (grade) metadata.score_grade = grade;
  const total = data.score?.total_score;
  if (total !== null && total !== undefined && Number.isFinite(Number(total))) {
    metadata.score_total = Number(total);
  }

  if (asText(customer?.birth_place)) metadata.birth_place = customer?.birth_place;
  if (asText(customer?.gender)) metadata.gender = customer?.gender;
  if (asText(data.stage)) metadata.stage = data.stage;
  if (asText(narrative.status)) metadata.narrative_status = narrative.status;
  if (asText(narrative.contract)) metadata.narrative_contract = narrative.contract;
  if (Array.isArray(data.pipeline) && data.pipeline.length > 0) {
    metadata.pipeline = data.pipeline.join(",");
  }

  return {
    calendar: asText(data.calendar?.solar_term?.name) ?? null,
    pillars: formatLabeledPillars(data.bazi),
    timezone: asText(customer?.timezone) ?? null,
    schema: asText(narrative.contract),
    ids: analysisId,
    metadata: Object.keys(metadata).length > 0 ? metadata : null,
  };
}

function buildPresentation(
  data: AnalysisDataDto,
  narrative: NarrativeResultDto,
  analysisId: string | null,
): ReportPresentationEnvelope | null {
  const identity = buildIdentity(data.customer, data, narrative);
  if (!identity) return null;

  const bullets = collectSummaryBullets(data, narrative);
  if (bullets.length === 0) return null;

  const primary = mapPrimaryCareerRecommendation(narrative);
  const recommendations = [
    ...(primary ? [primary] : []),
    ...mapRootRecommendationsWithDomain(narrative.recommendations),
  ];

  const careerText = careerAnalysisFromAssessment(narrative);
  // Keep primary recommendation only in the Recommendation zone (no duplicate card).
  const domains =
    primary != null || careerText.preview || careerText.detail
      ? {
          career: {
            available: true,
            recommendation_ids: [] as string[],
            intro: null,
            analysis_preview: careerText.preview,
            analysis_detail: careerText.detail,
          },
        }
      : undefined;

  return {
    identity,
    summary: { bullets },
    recommendations,
    warnings: mapCareerWarnings(narrative),
    domains,
    charts: [],
    technical: buildTechnical(data, analysisId, narrative),
    knowledge: mapNarrativeSectionsToKnowledge(narrative),
    appendix: null,
    cta: {
      primary: { enabled: true },
      secondary: { enabled: false },
    },
  };
}

/**
 * Convert live POST /api/v1/analyze `data` into CanonicalReportInput.
 */
export function adaptLiveAnalysisResult(
  analysisResult: AnalysisDataDto | null | undefined,
  options: LiveAnalysisAdapterOptions = {},
): LiveAnalysisMapResult {
  if (analysisResult == null || typeof analysisResult !== "object") {
    return {
      ok: false,
      error_code: "live_analysis_malformed",
      error_message: ERROR_MALFORMED_VI,
    };
  }

  const narrative = asNarrativeResult(analysisResult.narrative_result);
  if (!hasUsableNarrativeResult(narrative) || !narrative) {
    return {
      ok: false,
      error_code: "live_analysis_incomplete",
      error_message: ERROR_INCOMPLETE_VI,
    };
  }

  const analysisId = asText(options.analysis_id);
  const presentation = buildPresentation(analysisResult, narrative, analysisId);
  if (!presentation) {
    return {
      ok: false,
      error_code: "live_analysis_incomplete",
      error_message: ERROR_INCOMPLETE_VI,
    };
  }

  return {
    ok: true,
    report: {
      success: true,
      report_pipeline_version: asText(narrative.contract) ?? "pack05_narrative_result_v1",
      errors: [],
      presentation,
      canonical_report_artifact: analysisId
        ? {
            success: true,
            artifact_id: analysisId,
            mime_type: "application/json",
            render_version: asText(narrative.contract),
            metadata: {
              analysis_id: analysisId,
              narrative_status: asText(narrative.status),
            },
            content: null,
          }
        : null,
    },
  };
}
