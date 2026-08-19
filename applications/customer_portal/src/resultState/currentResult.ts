/**
 * Canonical current-result ownership for customer-facing routes.
 *
 * Precedence:
 *   1. fresh analysis in the current session (bte_last_result)
 *   2. explicitly selected history item (?from=history)
 *   3. legacy fallback
 *
 * Fresh successful analyses must never lose to stale history/view keys.
 */

import type { AnalysisDataDto } from "../models";
import { canonicalFiveElementCounts } from "../adapters/canonicalFiveElements";

export const HISTORY_VIEW_QUERY = "from";
export const HISTORY_VIEW_VALUE = "history";

export type StoredResultRecord = {
  readonly input?: Record<string, unknown> | null;
  readonly data?: AnalysisDataDto | null;
  readonly analysis_id?: string | null;
  readonly id?: string | null;
  readonly source?: string | null;
};

export type CurrentResultSource = "current" | "history" | "legacy" | "empty";

export type ResolvedCurrentResult = {
  readonly input: Record<string, unknown>;
  readonly data: AnalysisDataDto;
  readonly analysisId: string;
  readonly source: CurrentResultSource;
};

/**
 * True when the Result page should render an explicit History selection.
 */
export function isHistoryViewSearch(search: string): boolean {
  const params = new URLSearchParams(search.startsWith("?") ? search.slice(1) : search);
  return params.get(HISTORY_VIEW_QUERY) === HISTORY_VIEW_VALUE;
}

/**
 * Stable display identifier for one analysis session.
 */
export function analysisIdOf(record: StoredResultRecord | null | undefined): string | null {
  if (!record) return null;
  const fromRecord = asNonEmpty(record.analysis_id) || asNonEmpty(record.id);
  if (fromRecord) return fromRecord;
  const data = record.data;
  if (data && typeof data === "object") {
    const fromData =
      asNonEmpty(data.analysis_id) ||
      asNonEmpty(data.request_id) ||
      asNonEmpty((data as { case_id?: unknown }).case_id);
    if (fromData) return fromData;
  }
  return null;
}

/**
 * Resolve which stored payload the customer UI should bind.
 *
 * Default /result, Luận giải, Báo cáo, and export use `current`.
 * History/report "open older" uses `from=history`.
 */
export function resolveCurrentStoredResult(options: {
  readonly current: StoredResultRecord | null;
  readonly historyView: StoredResultRecord | null;
  readonly fromHistory: boolean;
}): ResolvedCurrentResult | null {
  if (options.fromHistory && options.historyView?.data) {
    return toResolved(options.historyView, "history");
  }
  if (options.current?.data) {
    return toResolved(options.current, "current");
  }
  if (options.historyView?.data) {
    return toResolved(options.historyView, "legacy");
  }
  return null;
}

/**
 * Structured analysis is present — report screens must not prefer stale HTML/MD.
 */
export function hasStructuredAnalysis(data: AnalysisDataDto | null | undefined): boolean {
  if (!data || typeof data !== "object") return false;
  return Boolean(
    data.calendar ||
      data.five_elements ||
      data.ten_gods ||
      data.luck ||
      data.feng_shui ||
      data.useful_god ||
      data.narrative_result ||
      data.pattern ||
      data.strength,
  );
}

/**
 * Analytical Five Elements counts — never ScoreEngine wuxing_score / wuxing_series.
 */
export function analyticalFiveElementCounts(
  data: AnalysisDataDto | null | undefined,
): Record<"Mộc" | "Hỏa" | "Thổ" | "Kim" | "Thủy", number> | null {
  return canonicalFiveElementCounts(data);
}

/**
 * Analytical Ten Gods labels — never ScoreEngine ten_god_score / ten_god_series.
 */
export function analyticalTenGods(data: AnalysisDataDto | null | undefined): string[] {
  const payload = data?.ten_gods ?? data?.ten_gods_result;
  const labels = payload?.visible_labels;
  if (Array.isArray(labels) && labels.length) {
    return labels.map((item) => String(item).trim()).filter(Boolean);
  }
  const visible = payload?.visible ?? data?.bazi?.ten_gods ?? [];
  return visible
    .map((item) => {
      if (typeof item === "string") return item.trim();
      if (item && typeof item === "object" && "ten_god" in item) {
        return String((item as { ten_god?: string }).ten_god || "").trim();
      }
      return String(item).trim();
    })
    .filter(Boolean);
}

export function analyticalHiddenTenGods(
  data: AnalysisDataDto | null | undefined,
): string[] {
  const payload = data?.ten_gods ?? data?.ten_gods_result;
  const labels = payload?.hidden_labels;
  if (Array.isArray(labels) && labels.length) {
    return [...new Set(labels.map((item) => String(item).trim()).filter(Boolean))];
  }
  const hidden = payload?.hidden ?? [];
  return [
    ...new Set(
      hidden
        .map((item) => {
          if (typeof item === "string") return item.trim();
          if (item && typeof item === "object" && "ten_god" in item) {
            return String((item as { ten_god?: string }).ten_god || "").trim();
          }
          return "";
        })
        .filter(Boolean),
    ),
  ];
}

function toResolved(record: StoredResultRecord, source: CurrentResultSource): ResolvedCurrentResult | null {
  if (!record.data) return null;
  return {
    input: record.input && typeof record.input === "object" ? record.input : {},
    data: record.data,
    analysisId: analysisIdOf(record) || fallbackAnalysisId(record),
    source,
  };
}

function fallbackAnalysisId(record: StoredResultRecord): string {
  const input = record.input || {};
  return ["bte", input.year ?? 0, input.month ?? 0, input.day ?? 0, input.hour ?? 0, input.minute ?? 0]
    .map(String)
    .join("-");
}

function asNonEmpty(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}
