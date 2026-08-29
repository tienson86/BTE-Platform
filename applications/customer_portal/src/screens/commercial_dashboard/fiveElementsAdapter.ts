/**
 * Bind Five Elements Card from canonical analysis. Copy published counts only.
 */

import type { AnalysisDataDto } from "../../models";
import { FIVE_ELEMENTS_HEADING, FIVE_ELEMENTS_TITLE } from "./cards";
import type { FiveElementKey, FiveElementRowView, FiveElementsView } from "./types";

const ELEMENT_ORDER: readonly { readonly key: FiveElementKey; readonly label: string }[] = [
  { key: "wood", label: "Mộc" },
  { key: "fire", label: "Hỏa" },
  { key: "earth", label: "Thổ" },
  { key: "metal", label: "Kim" },
  { key: "water", label: "Thủy" },
];

const TRUSTED_BALANCE = new Set(["CÂN BẰNG", "MẤT CÂN BẰNG NHẸ", "LỆCH RÕ"]);
const TECHNICAL_STATUS = /^(missing|present|strong|excess|warming|cold|balanced)$/i;
const APPROVED_DISCLAIMER =
  "Phân bố Ngũ Hành phản ánh cấu trúc xuất hiện, không trực tiếp quyết định Dụng Thần.";

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
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }
  return null;
}

function copyCount(facts: Record<string, unknown>, key: FiveElementKey): number | null {
  const counts = asRecord(facts.counts);
  const fromCounts = numericCount(counts[key]);
  if (fromCounts != null) return fromCounts;
  return numericCount(facts[key]);
}

function occurrenceExtremes(rows: readonly FiveElementRowView[]): {
  readonly mostPresent: string;
  readonly leastPresent: string;
} {
  const numbered = rows.filter((row) => row.count != null) as Array<
    FiveElementRowView & { count: number }
  >;
  if (numbered.length < 2) return { mostPresent: "", leastPresent: "" };
  const max = Math.max(...numbered.map((row) => row.count));
  const min = Math.min(...numbered.map((row) => row.count));
  if (max === min) return { mostPresent: "", leastPresent: "" };
  return {
    mostPresent: numbered.find((row) => row.count === max)?.label ?? "",
    leastPresent: numbered.find((row) => row.count === min)?.label ?? "",
  };
}

function trustedBalance(value: unknown): string {
  const next = String(value ?? "").trim();
  if (!next || TECHNICAL_STATUS.test(next) || !TRUSTED_BALANCE.has(next)) return "";
  return next;
}

function publishedComment(facts: Record<string, unknown>): string {
  const summary = String(facts.summary || facts.comment || "").trim();
  if (summary) return summary;
  const disclaimer = String(facts.disclaimer || "").trim();
  return disclaimer || APPROVED_DISCLAIMER;
}

function composeComment(
  mostPresent: string,
  leastPresent: string,
  published: string,
): string {
  const comparison =
    mostPresent && leastPresent
      ? `Phân bố cấu trúc cho thấy ${mostPresent} xuất hiện nhiều nhất và ${leastPresent} xuất hiện ít nhất.`
      : "";
  return [comparison, published].filter(Boolean).join(" ");
}

/**
 * Map published Five Elements counts onto the card. Does not score or infer balance.
 */
export function adaptFiveElementsCard(data: AnalysisDataDto | null | undefined): FiveElementsView {
  const facts = asRecord(data?.five_elements);
  const rows = ELEMENT_ORDER.map((item) => ({
    key: item.key,
    label: item.label,
    count: copyCount(facts, item.key),
  }));
  const available = rows.some((row) => row.count != null);
  const { mostPresent, leastPresent } = occurrenceExtremes(rows);
  return {
    title: FIVE_ELEMENTS_TITLE,
    available,
    sectionHeading: FIVE_ELEMENTS_HEADING,
    balanceStatus: trustedBalance(facts.balance_status),
    rows,
    mostPresent,
    leastPresent,
    comment: available ? composeComment(mostPresent, leastPresent, publishedComment(facts)) : "",
  };
}
