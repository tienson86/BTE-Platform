/**
 * Result boot helpers — ResultStore → PortalPage props (no side effects).
 */

import {
  adaptAnalysisToCanonicalDesktop,
  type CanonicalDesktopViewModel,
} from "../adapters";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../models";

export type StoredResult = {
  readonly input?: Record<string, unknown> | null;
  readonly data?: AnalysisDataDto | null;
};

export type ResultBootProps = {
  readonly request: AnalyzeChartRequest | null;
  readonly initialData?: CanonicalDesktopViewModel;
  readonly previewFallback: boolean;
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
 * Production: request/data present → engine ViewModel.
 * Preview: no request → fixture.
 */
export function resolveResultBoot(
  stored: StoredResult | null,
  search: string = "",
): ResultBootProps {
  const params = new URLSearchParams(search);
  const forcePreview = params.get("preview") === "1";
  if (forcePreview) {
    return { request: null, previewFallback: true };
  }

  const request = toAnalyzeRequest(stored?.input ?? null);

  if (stored?.data && request) {
    return {
      request: null,
      initialData: adaptAnalysisToCanonicalDesktop(stored.data, {
        request,
        source: "api",
        status: "ready",
      }),
      previewFallback: false,
    };
  }

  if (request) {
    return { request, previewFallback: false };
  }

  return { request: null, previewFallback: true };
}
