/**
 * BTE Portal Design System — Motion Tokens (WP01).
 * Unified transition durations; Normal = 200ms (Sprint 01).
 */

/** Duration tokens (ms). */
export const motionDuration = {
  fast: 120,
  normal: 200,
  slow: 320,
} as const;

/** Easing curves. */
export const motionEasing = {
  standard: "cubic-bezier(0.22, 1, 0.36, 1)",
  emphasized: "cubic-bezier(0.45, 0, 0.55, 1)",
  linear: "linear",
} as const;

/** Aggregated motion tokens for transitions. */
export const motion = {
  fast: `${motionDuration.fast}ms`,
  normal: `${motionDuration.normal}ms`,
  slow: `${motionDuration.slow}ms`,
  easing: motionEasing.standard,
  easingEmphasized: motionEasing.emphasized,
} as const;

export type MotionSpeed = "fast" | "normal" | "slow";

/**
 * Build a unified CSS transition value.
 * Example: `transition("opacity", "normal")` → `opacity 200ms cubic-bezier(...)`.
 */
export function transition(
  property: string,
  speed: MotionSpeed = "normal",
): string {
  return `${property} ${motion[speed]} ${motion.easing}`;
}
