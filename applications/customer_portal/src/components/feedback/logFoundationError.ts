/**
 * Placeholder observability hook for foundation errors.
 * Wire to real logging in a later Work Package — presentation only.
 */

export type FoundationErrorLogPayload = {
  error: Error;
  componentStack?: string | null;
  boundary?: string;
};

/**
 * Logs a foundation presentation error.
 * Currently a console placeholder only.
 */
export function logFoundationError(payload: FoundationErrorLogPayload): void {
  if (typeof console !== "undefined" && typeof console.error === "function") {
    console.error("[cui-foundation]", payload.boundary ?? "ErrorBoundary", payload.error, {
      componentStack: payload.componentStack ?? null,
    });
  }
}
