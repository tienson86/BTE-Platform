/**
 * Session carried from wizard submit → result route (LAUNCH-02).
 * Holds the real API identifier and payload; Result V2 mapping is LAUNCH-03.
 */

import type { AnalysisDataDto } from "../../models";

export type PortalAnalysisSession = {
  readonly analysis_id: string;
  readonly request_id: string | null;
  readonly data: AnalysisDataDto;
};

/**
 * Prefer API request_id as the public analysis identifier.
 */
export function resolveAnalysisId(requestId: string | null | undefined): string {
  const trimmed = (requestId ?? "").trim();
  if (trimmed) return trimmed;
  return `local_${Date.now().toString(36)}`;
}
