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
};

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
