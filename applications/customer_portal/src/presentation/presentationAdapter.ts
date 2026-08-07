/**
 * PACK_04 — UI Presentation Adapter.
 * Converts raw engine / ViewModel content into UI-friendly preview models.
 * No BaZi business logic — truncation and preview shaping only.
 */

import {
  CARD_TYPE_BY_SECTION,
  LINE_CLAMP,
  PREVIEW_CHAR_LIMIT,
  PREVIEW_LIST_LIMIT,
} from "./constants";
import type {
  LineClampField,
  PresentationCardType,
  PreviewBlock,
  PreviewList,
  PreviewText,
  ResultSectionId,
} from "./types";

function normalizeText(value: string | null | undefined): string {
  if (value === null || value === undefined) {
    return "";
  }
  return String(value).replace(/\s+/g, " ").trim();
}

/**
 * Truncate a string to a character budget without splitting mid-word when possible.
 */
export function truncateText(raw: string, maxChars: number): { text: string; hasMore: boolean } {
  const full = normalizeText(raw);
  if (full.length <= maxChars) {
    return { text: full, hasMore: false };
  }
  const slice = full.slice(0, maxChars);
  const lastSpace = slice.lastIndexOf(" ");
  const cut = lastSpace > Math.floor(maxChars * 0.6) ? slice.slice(0, lastSpace) : slice;
  return { text: `${cut.trimEnd()}…`, hasMore: true };
}

/**
 * Adapt a raw string into a PreviewText field.
 */
export function adaptPreviewText(
  raw: string | null | undefined,
  field: LineClampField = "description",
): PreviewText {
  const fullText = normalizeText(raw);
  const lineClamp = LINE_CLAMP[field];
  const { text, hasMore } = truncateText(fullText, PREVIEW_CHAR_LIMIT[field]);
  return {
    text,
    fullText,
    hasMore: hasMore || fullText.split(/\n/).length > lineClamp,
    lineClamp,
  };
}

/**
 * Adapt a list into a bounded PreviewList.
 */
export function adaptPreviewList<T>(
  items: readonly T[] | null | undefined,
  maxItems: number,
): PreviewList<T> {
  const source = Array.isArray(items) ? items : [];
  const limit = Math.max(0, maxItems);
  const sliced = source.slice(0, limit);
  return {
    items: sliced,
    totalCount: source.length,
    hasMore: source.length > sliced.length,
    maxItems: limit,
  };
}

/**
 * Adapt a list using the default item budget for a card type.
 */
export function adaptPreviewListForCardType<T>(
  items: readonly T[] | null | undefined,
  cardType: PresentationCardType,
): PreviewList<T> {
  return adaptPreviewList(items, PREVIEW_LIST_LIMIT[cardType]);
}

/**
 * Adapt a title + body narrative block.
 */
export function adaptPreviewBlock(
  title: string | null | undefined,
  body: string | null | undefined,
): PreviewBlock {
  const titlePreview = adaptPreviewText(title, "title");
  const bodyPreview = adaptPreviewText(body, "narrative");
  return {
    title: titlePreview,
    body: bodyPreview,
    hasMore: titlePreview.hasMore || bodyPreview.hasMore,
  };
}

export type InterpretationPreviewModel = {
  readonly executive: PreviewText;
  readonly strengths: PreviewList<string>;
  readonly warnings: PreviewList<string>;
  readonly hasMore: boolean;
};

/**
 * Adapt S08-style interpretation payload for a fixed preview card.
 */
export function adaptInterpretationPreview(input: {
  readonly executiveBody: string;
  readonly strengths: readonly string[];
  readonly warnings: readonly string[];
  readonly cardType?: PresentationCardType;
}): InterpretationPreviewModel {
  const cardType = input.cardType ?? "preview";
  const executive = adaptPreviewText(input.executiveBody, "narrative");
  const strengths = adaptPreviewListForCardType(input.strengths, cardType);
  const warnings = adaptPreviewListForCardType(input.warnings, cardType);
  return {
    executive,
    strengths,
    warnings,
    hasMore: executive.hasMore || strengths.hasMore || warnings.hasMore,
  };
}

export type ReportSummaryPreviewModel = {
  readonly executive: PreviewBlock;
  readonly strengths: PreviewList<string>;
  readonly attention: PreviewList<string>;
  readonly recommendations: PreviewList<string>;
  readonly hasMore: boolean;
};

/**
 * Adapt S11-style report summary payload for a fixed preview card.
 */
export function adaptReportSummaryPreview(input: {
  readonly executiveTitle: string;
  readonly executiveBody: string;
  readonly strengths: readonly string[];
  readonly attention: readonly string[];
  readonly recommendations: readonly string[];
  readonly cardType?: PresentationCardType;
}): ReportSummaryPreviewModel {
  const cardType = input.cardType ?? "preview";
  const executive = adaptPreviewBlock(input.executiveTitle, input.executiveBody);
  const strengths = adaptPreviewListForCardType(input.strengths, cardType);
  const attention = adaptPreviewListForCardType(input.attention, cardType);
  const recommendations = adaptPreviewListForCardType(input.recommendations, cardType);
  return {
    executive,
    strengths,
    attention,
    recommendations,
    hasMore:
      executive.hasMore ||
      strengths.hasMore ||
      attention.hasMore ||
      recommendations.hasMore,
  };
}

export type StrengthPreviewModel = {
  readonly insight: PreviewText;
  readonly factors: PreviewList<{ readonly text: string; readonly tone: string }>;
  readonly hasMore: boolean;
};

/**
 * Adapt S05 strength preview payload.
 */
export function adaptStrengthPreview(input: {
  readonly insight: string;
  readonly factors: readonly { readonly text: string; readonly tone: string }[];
  readonly cardType?: PresentationCardType;
}): StrengthPreviewModel {
  const cardType = input.cardType ?? "preview";
  const insight = adaptPreviewText(input.insight, "summary");
  const factors = adaptPreviewList(
    input.factors,
    Math.max(PREVIEW_LIST_LIMIT[cardType], 4),
  );
  return {
    insight,
    factors,
    hasMore: insight.hasMore || factors.hasMore,
  };
}

/**
 * Resolve card type for a Result section (adapter helper).
 */
export function resolveSectionCardType(section: ResultSectionId): PresentationCardType {
  return CARD_TYPE_BY_SECTION[section];
}
