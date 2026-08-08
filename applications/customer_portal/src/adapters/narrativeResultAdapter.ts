/**
 * Pack 05 NarrativeResult → Result presentation helpers.
 * Official Portal consumer of commercial narrative.
 */

import {
  UNAVAILABLE_CONCLUSION,
  commercialOrUnavailable,
  firstCommercialSnippet,
} from "./contentGuards";

export type NarrativeResultSummaryDto = {
  readonly identity?: string;
  readonly strengths?: readonly string[];
  readonly weaknesses?: readonly string[];
  readonly priority_recommendation?: string;
  readonly next_action?: string;
  readonly overall_confidence?: number;
  readonly insufficient_flags?: readonly string[];
};

export type NarrativeParagraphDto = {
  readonly id?: string;
  readonly role?: string;
  readonly text?: string;
  readonly evidence_refs?: readonly string[];
  readonly interpretation_refs?: readonly string[];
  readonly confidence?: number;
  readonly insufficient_data?: boolean;
};

export type NarrativeRecommendationDto = {
  readonly id?: string;
  readonly priority?: string;
  readonly action?: string;
  readonly reason?: string;
  readonly benefit?: string;
  readonly insufficient_data?: boolean;
};

export type NarrativeSectionDto = {
  readonly id?: string;
  readonly intent?: string;
  readonly title?: string;
  readonly paragraphs?: readonly NarrativeParagraphDto[];
  readonly recommendations?: readonly NarrativeRecommendationDto[];
  readonly insufficient_data?: boolean;
  readonly tone?: string;
};

export type NarrativeResultDto = {
  readonly summary?: NarrativeResultSummaryDto;
  readonly sections?: readonly NarrativeSectionDto[];
  readonly recommendations?: readonly NarrativeRecommendationDto[];
  readonly confidence?: number;
  readonly status?: string;
  readonly run_id?: string;
  readonly contract?: string;
  /** Career Selection Assessment projection (no raw Knowledge Units). */
  readonly career_selection_assessment?: CareerSelectionAssessmentDto | null;
  /** Promotion Readiness Assessment projection (no raw Knowledge Units). */
  readonly promotion_readiness_assessment?: PromotionReadinessAssessmentDto | null;
  readonly commercial_knowledge_bundle?: {
    readonly career_selection_assessment?: CareerSelectionAssessmentDto | null;
    readonly promotion_readiness_assessment?: PromotionReadinessAssessmentDto | null;
    readonly [key: string]: unknown;
  } | null;
};

export type CareerSelectionFieldDto = {
  readonly text?: string;
  readonly knowledge_unit_id?: string;
  readonly evidence_kind?: string;
  readonly version?: string;
  readonly confidence?: number;
};

export type CareerSelectionAssessmentDto = {
  readonly capability_id?: string;
  readonly status?: string;
  readonly career_direction?: CareerSelectionFieldDto | null;
  readonly working_environment?: CareerSelectionFieldDto | null;
  readonly preferred_role?: CareerSelectionFieldDto | null;
  readonly leadership_posture?: CareerSelectionFieldDto | null;
  readonly employment_posture?: CareerSelectionFieldDto | null;
  readonly career_strengths?: CareerSelectionFieldDto | null;
  readonly career_risks?: CareerSelectionFieldDto | null;
  readonly career_mitigation?: CareerSelectionFieldDto | null;
  readonly development_focus?: CareerSelectionFieldDto | null;
  readonly timing_guidance?: CareerSelectionFieldDto | null;
  readonly action_plan_90d?: CareerSelectionFieldDto | null;
  readonly knowledge_unit_ids?: readonly string[];
};

export function asCareerSelectionAssessment(
  value: unknown,
): CareerSelectionAssessmentDto | null {
  if (!value || typeof value !== "object") return null;
  const record = value as Record<string, unknown>;
  if (record.capability_id !== "CAP-D1-CA-SEL" && !record.career_direction) {
    return null;
  }
  return value as CareerSelectionAssessmentDto;
}

export function careerSelectionFromNarrative(
  narrative: NarrativeResultDto | null | undefined,
): CareerSelectionAssessmentDto | null {
  if (!narrative) return null;
  return (
    asCareerSelectionAssessment(narrative.career_selection_assessment) ||
    asCareerSelectionAssessment(
      narrative.commercial_knowledge_bundle?.career_selection_assessment,
    )
  );
}

export function careerFieldText(
  assessment: CareerSelectionAssessmentDto | null | undefined,
  key: keyof CareerSelectionAssessmentDto,
): string {
  if (!assessment) return "";
  const value = assessment[key];
  if (!value || typeof value !== "object") return "";
  const text = (value as CareerSelectionFieldDto).text;
  return text == null ? "" : String(text).trim();
}

export type PromotionReadinessAssessmentDto = {
  readonly capability_id?: string;
  readonly status?: string;
  readonly promotion_readiness?: CareerSelectionFieldDto | null;
  readonly management_role_posture?: CareerSelectionFieldDto | null;
  readonly competency_gaps?: CareerSelectionFieldDto | null;
  readonly promotion_strengths?: CareerSelectionFieldDto | null;
  readonly advancement_posture?: CareerSelectionFieldDto | null;
  readonly timing_guidance?: CareerSelectionFieldDto | null;
  readonly advancement_window?: CareerSelectionFieldDto | null;
  readonly promotion_risks?: CareerSelectionFieldDto | null;
  readonly promotion_mitigation?: CareerSelectionFieldDto | null;
  readonly action_plan_90d?: CareerSelectionFieldDto | null;
  readonly knowledge_unit_ids?: readonly string[];
};

export function asPromotionReadinessAssessment(
  value: unknown,
): PromotionReadinessAssessmentDto | null {
  if (!value || typeof value !== "object") return null;
  const record = value as Record<string, unknown>;
  if (
    record.capability_id !== "CAP-D1-CA-PRO" &&
    !record.promotion_readiness
  ) {
    return null;
  }
  return value as PromotionReadinessAssessmentDto;
}

export function promotionReadinessFromNarrative(
  narrative: NarrativeResultDto | null | undefined,
): PromotionReadinessAssessmentDto | null {
  if (!narrative) return null;
  return (
    asPromotionReadinessAssessment(narrative.promotion_readiness_assessment) ||
    asPromotionReadinessAssessment(
      narrative.commercial_knowledge_bundle?.promotion_readiness_assessment,
    )
  );
}

export function promotionFieldText(
  assessment: PromotionReadinessAssessmentDto | null | undefined,
  key: keyof PromotionReadinessAssessmentDto,
): string {
  if (!assessment) return "";
  const value = assessment[key];
  if (!value || typeof value !== "object") return "";
  const text = (value as CareerSelectionFieldDto).text;
  return text == null ? "" : String(text).trim();
}

export function asNarrativeResult(
  value: unknown,
): NarrativeResultDto | null {
  if (!value || typeof value !== "object") return null;
  const record = value as Record<string, unknown>;
  if (!record.summary && !Array.isArray(record.sections)) return null;
  return value as NarrativeResultDto;
}

export function hasUsableNarrativeResult(
  value: NarrativeResultDto | null | undefined,
): boolean {
  if (!value) return false;
  if (value.contract === "pack05_narrative_result_v1") return true;
  return Boolean(value.summary) || (Array.isArray(value.sections) && value.sections.length > 0);
}

export function summaryText(
  summary: NarrativeResultSummaryDto | undefined,
  key: keyof NarrativeResultSummaryDto,
): string {
  if (!summary) return UNAVAILABLE_CONCLUSION;
  const raw = summary[key];
  if (Array.isArray(raw)) {
    const joined = raw.map(String).filter(Boolean).join("; ");
    return commercialOrUnavailable(joined);
  }
  return commercialOrUnavailable(raw == null ? "" : String(raw));
}

export function sectionParagraphTexts(
  narrative: NarrativeResultDto,
  intentOrId: RegExp,
): string[] {
  const sections = narrative.sections ?? [];
  const matched = sections.filter((section) => {
    const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
    return intentOrId.test(blob);
  });
  const texts: string[] = [];
  for (const section of matched) {
    for (const paragraph of section.paragraphs ?? []) {
      if (paragraph.insufficient_data) continue;
      const snippet = firstCommercialSnippet(paragraph.text);
      if (snippet !== UNAVAILABLE_CONCLUSION) texts.push(snippet);
    }
  }
  return texts;
}

export function recommendationActions(
  narrative: NarrativeResultDto,
): string[] {
  const fromRoot = narrative.recommendations ?? [];
  const fromSections = (narrative.sections ?? []).flatMap(
    (section) => section.recommendations ?? [],
  );
  const items = [...fromRoot, ...fromSections];
  const actions: string[] = [];
  for (const item of items) {
    if (item.insufficient_data) continue;
    const text = firstCommercialSnippet(item.action);
    if (text !== UNAVAILABLE_CONCLUSION) actions.push(text);
  }
  return actions;
}

export function paragraphByRole(
  narrative: NarrativeResultDto,
  role: string,
): string {
  for (const section of narrative.sections ?? []) {
    for (const paragraph of section.paragraphs ?? []) {
      if ((paragraph.role ?? "").toLowerCase() !== role.toLowerCase()) continue;
      if (paragraph.insufficient_data) continue;
      return commercialOrUnavailable(paragraph.text);
    }
  }
  return UNAVAILABLE_CONCLUSION;
}
