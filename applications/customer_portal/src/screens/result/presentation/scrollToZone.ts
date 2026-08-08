/**
 * In-page navigation helpers for Result consulting CTAs.
 * Presentation only — no new routes.
 */

export type ResultZoneId =
  | "context"
  | "summary"
  | "recommendation"
  | "analysis"
  | "interpretation"
  | "visualization"
  | "knowledge";

/**
 * Smooth-scroll to an existing Result zone by data-zone attribute.
 */
export function scrollToResultZone(zone: ResultZoneId): void {
  if (typeof document === "undefined") return;
  const target = document.querySelector(`[data-zone="${zone}"]`);
  if (!(target instanceof HTMLElement)) return;
  target.scrollIntoView({ behavior: "smooth", block: "start" });
}
