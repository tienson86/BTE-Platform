/**
 * Phase 08 — Presentation helpers (formatting, sorting, truncation, placeholders).
 * Presentation-only. No BaZi business logic.
 */

import { adaptPreviewText, type PreviewText } from "../../../presentation";
import type { RecommendationPriority } from "../viewModels";

export const RECOMMENDATION_PRIORITY_ORDER: readonly RecommendationPriority[] = [
  "critical",
  "high",
  "medium",
  "low",
] as const;

export const RECOMMENDATION_PRIORITY_LABEL: Record<RecommendationPriority, string> = {
  critical: "Ưu tiên cao",
  high: "Cao",
  medium: "Trung bình",
  low: "Thấp",
};

export const MAX_PRIMARY_RECOMMENDATIONS = 5;

const PRIORITY_RANK: Record<RecommendationPriority, number> = {
  critical: 0,
  high: 1,
  medium: 2,
  low: 3,
};

/**
 * Sort recommendations Critical → Low (stable for equal priority).
 */
export function sortByRecommendationPriority<T extends { readonly priority: RecommendationPriority }>(
  items: readonly T[],
): T[] {
  return [...items].sort((a, b) => PRIORITY_RANK[a.priority] - PRIORITY_RANK[b.priority]);
}

/**
 * Bind placeholder when source text is empty.
 * Prefer commercial unavailable copy for missing narrative fields.
 */
export function bindPlaceholder(
  value: string | null | undefined,
  placeholder = "Chưa đủ dữ liệu để đưa ra kết luận.",
): string {
  const trimmed = (value ?? "").trim();
  return trimmed.length > 0 ? trimmed : placeholder;
}

/**
 * Format a display field with truncation metadata.
 */
export function formatPreviewField(
  value: string | null | undefined,
  field: "title" | "summary" | "description" | "narrative" = "summary",
): PreviewText {
  return adaptPreviewText(bindPlaceholder(value), field);
}

/**
 * Group list items into fixed-size chunks (presentation layout helper).
 */
export function groupItems<T>(items: readonly T[], size: number): T[][] {
  const limit = Math.max(1, size);
  const groups: T[][] = [];
  for (let i = 0; i < items.length; i += limit) {
    groups.push(items.slice(i, i + limit));
  }
  return groups;
}

/**
 * Truncate a list to primary display budget.
 */
export function truncatePrimaryList<T>(
  items: readonly T[],
  maxItems: number,
): { readonly items: readonly T[]; readonly totalCount: number; readonly hasMore: boolean } {
  const limit = Math.max(0, maxItems);
  const sliced = items.slice(0, limit);
  return {
    items: sliced,
    totalCount: items.length,
    hasMore: items.length > sliced.length,
  };
}

/**
 * Map ordinal index → recommendation priority (presentation ranking only).
 */
export function priorityFromIndex(index: number): RecommendationPriority {
  if (index <= 0) return "critical";
  if (index === 1) return "high";
  if (index === 2) return "medium";
  return "low";
}
