/**
 * Production narrative switch monitoring. Operational fields only. No personal data.
 */

export type NarrativeMonitorEvent = {
  readonly provider: string;
  readonly selected: "pack05" | "v2";
  readonly presentation_version: string | null;
  readonly fallback: boolean;
  readonly fallback_reason: string | null;
  readonly fallback_count: number;
  readonly duration_ms: number;
};

export type NarrativeMonitorSink = (event: NarrativeMonitorEvent) => void;

let fallbackCount = 0;
let sink: NarrativeMonitorSink | null = null;

/**
 * Replace the monitor sink. Tests inject a collector. Production uses console.
 */
export function setNarrativeMonitorSink(next: NarrativeMonitorSink | null): void {
  sink = next;
}

/**
 * Reset fallback count. Used by tests and rollback drills.
 */
export function resetNarrativeFallbackCount(): void {
  fallbackCount = 0;
}

/**
 * Current fallback count for this Portal session.
 */
export function getNarrativeFallbackCount(): number {
  return fallbackCount;
}

/**
 * Record a provider selection. Increments fallback_count only on fallback.
 */
export function recordNarrativeSelection(event: {
  readonly provider: string;
  readonly selected: "pack05" | "v2";
  readonly presentationVersion: string | null;
  readonly fallback: boolean;
  readonly fallbackReason: string | null;
  readonly durationMs: number;
}): NarrativeMonitorEvent {
  if (event.fallback) {
    fallbackCount += 1;
  }
  const payload: NarrativeMonitorEvent = {
    provider: event.provider,
    selected: event.selected,
    presentation_version: event.presentationVersion,
    fallback: event.fallback,
    fallback_reason: event.fallbackReason,
    fallback_count: fallbackCount,
    duration_ms: event.durationMs,
  };
  const emit = sink ?? defaultSink;
  emit(payload);
  return payload;
}

function defaultSink(event: NarrativeMonitorEvent): void {
  if (typeof process !== "undefined" && (process.env?.VITEST === "true" || process.env?.VITEST === "1")) {
    return;
  }
  if (typeof console === "undefined" || typeof console.info !== "function") return;
  console.info("narrative.release", payloadWithoutSecrets(event));
}

function payloadWithoutSecrets(event: NarrativeMonitorEvent): NarrativeMonitorEvent {
  return {
    provider: event.provider,
    selected: event.selected,
    presentation_version: event.presentation_version,
    fallback: event.fallback,
    fallback_reason: event.fallback_reason,
    fallback_count: event.fallback_count,
    duration_ms: event.duration_ms,
  };
}
