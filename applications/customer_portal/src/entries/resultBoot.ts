/**
 * Result boot helpers — ResultStore → PortalPage props (no side effects).
 */

import {
  adaptAnalysisToCanonicalDesktop,
  createCanonicalDesktopGateViewModel,
  type CanonicalDesktopViewModel,
} from "../adapters";
import type { AnalyzeChartRequest } from "../models";
import { buildFullReportViewModel, type FullReportViewModel } from "../report/fullReportViewModel";
import {
  customerContractMessage,
  customerContractStatus,
} from "../resultState/customerContract";
import {
  historyIdFromSearch,
  resolveCurrentStoredResult,
  type StoredResultRecord,
} from "../resultState/currentResult";

export type StoredResult = StoredResultRecord;

export type ResultBootProps = {
  readonly request: AnalyzeChartRequest | null;
  readonly initialData?: CanonicalDesktopViewModel;
  readonly previewFallback: boolean;
  readonly analysisId?: string;
  readonly resultSource?: "current" | "history" | "empty" | "preview" | "contract";
  readonly fullReport?: FullReportViewModel;
};

/**
 * Map ResultStore birth input → AnalyzeChartRequest.
 */
export function toAnalyzeRequest(
  input: Record<string, unknown> | null | undefined,
): AnalyzeChartRequest | null {
  if (!input) return null;
  const year = Number(input.year);
  const month = Number(input.month);
  const day = Number(input.day);
  if (!Number.isFinite(year) || !Number.isFinite(month) || !Number.isFinite(day)) {
    return null;
  }
  return {
    year,
    month,
    day,
    hour: Number.isFinite(Number(input.hour)) ? Number(input.hour) : 0,
    minute: Number.isFinite(Number(input.minute)) ? Number(input.minute) : 0,
    gender: (input.gender as string | null | undefined) ?? null,
    timezone: typeof input.timezone === "string" ? input.timezone : undefined,
    full_name: (input.full_name as string | null | undefined) ?? null,
    birth_place: (input.birth_place as string | null | undefined) ?? null,
    customer_id: (input.customer_id as string | null | undefined) ?? null,
  };
}

/**
 * Resolve PortalPage props from ResultStore payload + URL.
 * Production empty store → empty gate (never mock fixture).
 * `?preview=1` remains an explicit development preview only.
 */
export function resolveResultBoot(
  stored: StoredResult | null,
  search: string = "",
  historyView: StoredResult | null = null,
): ResultBootProps {
  const params = new URLSearchParams(search);
  const forcePreview = params.get("preview") === "1";
  if (forcePreview) {
    return { request: null, previewFallback: true, resultSource: "preview" };
  }

  const historyId = historyIdFromSearch(search);
  const resolved = resolveCurrentStoredResult({
    current: stored,
    historyView,
    fromHistory: Boolean(historyId),
    historyId,
  });
  const payload = resolved;
  const request = toAnalyzeRequest(payload?.input ?? null);

  if (payload?.data && request) {
    const status = customerContractStatus(payload.data);
    if (status !== "ok") {
      return {
        request: null,
        initialData: createCanonicalDesktopGateViewModel(
          "error",
          customerContractMessage(status),
        ),
        previewFallback: false,
        analysisId: payload.analysisId,
        resultSource: "contract",
      };
    }
    const analysisId = payload.analysisId;
    const fullReport = buildFullReportViewModel(payload.data, {
      input: payload.input,
      analysisId,
    });
    return {
      request: null,
      initialData: adaptAnalysisToCanonicalDesktop(payload.data, {
        request,
        requestId: fullReport.analysisId,
        source: "api",
        status: "ready",
      }),
      previewFallback: false,
      analysisId: fullReport.analysisId,
      resultSource: payload.source,
      fullReport,
    };
  }

  return { request: null, previewFallback: false, resultSource: "empty" };
}
