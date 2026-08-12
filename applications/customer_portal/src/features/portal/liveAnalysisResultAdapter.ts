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
} from "../../adapters/narrativeResultAdapter";
import type { AnalysisDataDto, BaziDto, CustomerEchoDto } from "../../models";
import type {
  CanonicalReportInput,
  PresentationIdentity,
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

function pillarLine(bazi: BaziDto | undefined): string | null {
  if (!bazi) return null;
  const parts = [
    bazi.year_pillar,
    bazi.month_pillar,
    bazi.day_pillar,
    bazi.hour_pillar,
  ]
    .map((pillar) => {
      if (!pillar) return null;
      const stem = asText(pillar.stem);
      const branch = asText(pillar.branch);
      if (!stem && !branch) return null;
      return [stem, branch].filter(Boolean).join(" ");
    })
    .filter((item): item is string => Boolean(item));
  return parts.length > 0 ? parts.join(" · ") : null;
}

function collectSummaryBullets(narrative: NarrativeResultDto): string[] {
  const bullets: string[] = [];
  const push = (value: unknown): void => {
    const text = asText(value);
    if (!text) return;
    if (bullets.includes(text)) return;
    bullets.push(text);
  };

  const executive = executiveFromNarrative(narrative);
  for (const point of executive?.supporting_points ?? []) {
    push(point);
  }
  for (const strength of narrative.summary?.strengths ?? []) {
    push(strength);
  }
  for (const weakness of narrative.summary?.weaknesses ?? []) {
    push(weakness);
  }
  push(narrative.summary?.priority_recommendation);
  push(narrative.summary?.next_action);

  if (bullets.length === 0) {
    for (const section of narrative.sections ?? []) {
      for (const paragraph of section.paragraphs ?? []) {
        if (paragraph.insufficient_data) continue;
        push(paragraph.text);
        if (bullets.length >= 5) break;
      }
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

/**
 * Map Pack 05 primary commercial recommendation only when all Result V2 fields exist.
 * Domain is career because this structured object is the career commercial enrichment.
 */
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

/**
 * Root narrative recommendations lack a domain field — omit rather than invent domain.
 * Only include items that somehow carry an explicit domain (none today) → empty list.
 * Kept for forward-compatibility if runtime adds domain later.
 */
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

function buildIdentity(
  customer: CustomerEchoDto | undefined,
  narrative: NarrativeResultDto,
): PresentationIdentity | null {
  const fullName = asText(customer?.full_name);
  if (!fullName) return null;

  const executive = executiveFromNarrative(narrative);
  const headline =
    asText(executive?.central_message) ??
    asText(executive?.composed_text) ??
    asText(narrative.summary?.identity);
  const oneLine =
    asText(executive?.conclusion) ??
    asText(narrative.summary?.priority_recommendation) ??
    asText(narrative.summary?.next_action) ??
    asText(narrative.summary?.identity);

  if (!headline || !oneLine) return null;

  return {
    full_name: fullName,
    headline,
    one_line_summary: oneLine,
    consultation_status: mapConsultationStatus(narrative.status),
  };
}

function buildTechnical(
  data: AnalysisDataDto,
  analysisId: string | null,
  narrative: NarrativeResultDto,
): PresentationTechnical {
  const customer = data.customer;
  const metadata: Record<string, unknown> = {};
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
    pillars: pillarLine(data.bazi),
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
  const identity = buildIdentity(data.customer, narrative);
  if (!identity) return null;

  const bullets = collectSummaryBullets(narrative);
  if (bullets.length === 0) return null;

  const primary = mapPrimaryCareerRecommendation(narrative);
  const recommendations = [
    ...(primary ? [primary] : []),
    ...mapRootRecommendationsWithDomain(narrative.recommendations),
  ];

  const domains =
    primary != null
      ? {
          career: {
            available: true,
            recommendation_ids: [primary.id ?? "rec_career_primary"],
            intro: null,
            analysis_preview: null,
            analysis_detail: null,
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
    knowledge: [],
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
