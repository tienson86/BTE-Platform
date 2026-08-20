/**
 * Canonical Five Elements V1.0 presentation helpers.
 * Customer fact = structural distribution from data.five_elements.counts.
 * Does not recompute. Does not bind score.wuxing_score / wuxing_series.
 */

import type { AnalysisDataDto } from "../models";

export const FIVE_ELEMENTS_TITLE = "PHÂN BỐ NGŨ HÀNH";
export const FIVE_ELEMENTS_SECTION_TITLE = "Phân bố Ngũ hành";
export const FIVE_ELEMENTS_METHOD_NOTE =
  "Tính theo Thiên can · bản hành Địa chi · Tàng can";
export const FIVE_ELEMENTS_DISCLAIMER =
  "Phân bố Ngũ hành phản ánh số lần xuất hiện trong cấu trúc, không phải mức vượng suy và không trực tiếp quyết định Dụng thần.";
export const FIVE_ELEMENTS_ABSENT_LABEL =
  "Không xuất hiện trong phân bố cấu trúc";

export const FIVE_ELEMENT_ROWS: ReadonlyArray<{
  name: "Mộc" | "Hỏa" | "Thổ" | "Kim" | "Thủy";
  element: "wood" | "fire" | "earth" | "metal" | "water";
  key: "wood" | "fire" | "earth" | "metal" | "water";
}> = [
  { name: "Mộc", element: "wood", key: "wood" },
  { name: "Hỏa", element: "fire", key: "fire" },
  { name: "Thổ", element: "earth", key: "earth" },
  { name: "Kim", element: "metal", key: "metal" },
  { name: "Thủy", element: "water", key: "water" },
];

export type FiveElementName = (typeof FIVE_ELEMENT_ROWS)[number]["name"];

export type CanonicalFiveElementCounts = Record<FiveElementName, number>;

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function numericCount(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (value && typeof value === "object" && "count" in value) {
    const count = Number((value as { count?: unknown }).count);
    return Number.isFinite(count) ? count : null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

/**
 * Read published structural counts. Never Score Engine series or grade.
 */
export function canonicalFiveElementCounts(
  data: Pick<AnalysisDataDto, "five_elements"> | null | undefined,
): CanonicalFiveElementCounts | null {
  const facts = data?.five_elements;
  if (!facts) return null;
  const out: CanonicalFiveElementCounts = {
    Mộc: 0,
    Hỏa: 0,
    Thổ: 0,
    Kim: 0,
    Thủy: 0,
  };
  let found = false;
  const record = asRecord(facts);
  const counts = asRecord(record.counts);
  for (const row of FIVE_ELEMENT_ROWS) {
    const fromKey = numericCount(record[row.key]);
    const fromCounts = numericCount(counts[row.key]);
    const count = fromKey ?? fromCounts;
    if (count != null) {
      out[row.name] = count;
      found = true;
    }
  }
  return found ? out : null;
}

export function fiveElementUnitTotal(
  counts: CanonicalFiveElementCounts | null | undefined,
): number {
  if (!counts) return 0;
  return FIVE_ELEMENT_ROWS.reduce((sum, row) => sum + (counts[row.name] ?? 0), 0);
}

export function formatFiveElementsCompact(
  counts: CanonicalFiveElementCounts | null | undefined,
): string {
  if (!counts) return "";
  return FIVE_ELEMENT_ROWS.map((row) => `${row.name} ${counts[row.name]}`).join(" · ");
}

export function formatFiveElementsProvenance(total: number): string {
  if (total > 0) {
    return `${FIVE_ELEMENTS_METHOD_NOTE}. Tổng đơn vị cấu trúc: ${total}. ${FIVE_ELEMENTS_DISCLAIMER}`;
  }
  return `${FIVE_ELEMENTS_METHOD_NOTE}. ${FIVE_ELEMENTS_DISCLAIMER}`;
}

export function publishedFiveElementsDisclaimer(
  data: Pick<AnalysisDataDto, "five_elements"> | null | undefined,
): string {
  const facts = asRecord(data?.five_elements);
  const note = String(facts.disclaimer || "").trim();
  return note || FIVE_ELEMENTS_DISCLAIMER;
}

export function fiveElementAbsentLabel(count: number): string {
  return count === 0 ? FIVE_ELEMENTS_ABSENT_LABEL : "";
}

export function publishedFiveElementsMethodNote(
  data: Pick<AnalysisDataDto, "five_elements"> | null | undefined,
): string {
  const facts = asRecord(data?.five_elements);
  const note = String(facts.method_note || "").trim();
  return note || FIVE_ELEMENTS_METHOD_NOTE;
}
