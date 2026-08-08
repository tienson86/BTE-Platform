/**
 * Stabilization helpers — content quality gates for Result presentation.
 * Presentation-only. Does not invent BaZi conclusions.
 */

/** Shown when commercial narrative is missing or not usable. */
export const UNAVAILABLE_CONCLUSION = "Chưa đủ dữ liệu để đưa ra kết luận.";

const TECHNICAL_MARKERS: readonly RegExp[] = [
  /kích hoạt khi/i,
  /áp dụng bảng/i,
  /ưu tiên xác định/i,
  /matched[_ ]?rules?/i,
  /rule[_ ]?id/i,
  /nếu chưa có tiết khí/i,
  /xác định mùa theo/i,
  /không thay thế kết luận phân tích/i,
  /presentation layer/i,
  /pack[_\s]?\d+/i,
  /knowledge base\s*·/i,
  /\(mock\)/i,
  /placeholder/i,
  /chờ engine/i,
  /sẽ được nối/i,
];

/**
 * Detect rule-description / developer / placeholder prose unsuitable for cards.
 */
export function isTechnicalRuleText(value: string | null | undefined): boolean {
  const text = (value ?? "").trim();
  if (!text) return true;
  return TECHNICAL_MARKERS.some((re) => re.test(text));
}

/**
 * Return trimmed commercial text, or unavailable message when empty/technical.
 */
export function commercialOrUnavailable(
  value: string | null | undefined,
): string {
  const text = (value ?? "").trim();
  if (!text || isTechnicalRuleText(text)) {
    return UNAVAILABLE_CONCLUSION;
  }
  return text;
}

/**
 * First sentence/snippet suitable for card preview.
 */
export function firstCommercialSnippet(
  value: string | null | undefined,
  maxLen = 160,
): string {
  const usable = commercialOrUnavailable(value);
  if (usable === UNAVAILABLE_CONCLUSION) return usable;
  const sentence = usable.split(/[.\n]/)[0]?.trim() || usable;
  if (sentence.length <= maxLen) return sentence;
  return `${sentence.slice(0, maxLen - 1).trimEnd()}…`;
}

/**
 * Normalize engine scores that may be 0–1 or 0–100.
 */
export function normalizeScore100(raw: unknown): number {
  const n = Number(raw ?? 0);
  if (!Number.isFinite(n) || n < 0) return 0;
  if (n > 0 && n <= 1) return Math.round(n * 100);
  return Math.min(100, Math.round(n));
}

export type InterpretationSectionRow = {
  readonly id: string;
  readonly title: string;
  readonly body: string;
};

/**
 * Extract interpretation sections from analyze payload.
 */
export function extractInterpretationSections(
  interpretation: Record<string, unknown> | undefined,
): InterpretationSectionRow[] {
  const raw = interpretation?.sections;
  if (!Array.isArray(raw)) return [];
  return raw
    .filter((item): item is Record<string, unknown> => !!item && typeof item === "object")
    .map((item, index) => ({
      id: String(item.id ?? `section-${index + 1}`),
      title: String(item.title ?? "").trim(),
      body: String(item.body ?? item.content ?? item.text ?? "").trim(),
    }))
    .filter((row) => row.body.length > 0 || row.title.length > 0);
}

/**
 * Find first section whose title matches any of the given patterns.
 */
export function findSectionBody(
  sections: readonly InterpretationSectionRow[],
  titlePatterns: readonly RegExp[],
): string {
  for (const section of sections) {
    const title = section.title.toLowerCase();
    if (titlePatterns.some((re) => re.test(title))) {
      return section.body;
    }
  }
  return "";
}
