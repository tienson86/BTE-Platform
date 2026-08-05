/**
 * BTE Portal Design System — Breakpoint Tokens (WP01).
 * Aligned with Sprint 01 WP10 responsive ranges; adds `wide`.
 *
 * mobile  0 – 767
 * tablet  768 – 1023
 * laptop  1024 – 1439
 * desktop 1440 – 1919
 * wide    1920+
 */

/** Breakpoint minimum widths (px). */
export const breakpoints = {
  mobile: 0,
  tablet: 768,
  laptop: 1024,
  desktop: 1440,
  wide: 1920,
} as const;

export type BreakpointName = keyof typeof breakpoints;

/** Max width for each range (px). `wide` has no upper bound. */
export const breakpointMax = {
  mobile: 767,
  tablet: 1023,
  laptop: 1439,
  desktop: 1919,
  wide: Number.POSITIVE_INFINITY,
} as const;

/** Resolve breakpoint name from viewport width (px). */
export function resolveBreakpoint(widthPx: number): BreakpointName {
  if (widthPx < breakpoints.tablet) {
    return "mobile";
  }
  if (widthPx < breakpoints.laptop) {
    return "tablet";
  }
  if (widthPx < breakpoints.desktop) {
    return "laptop";
  }
  if (widthPx < breakpoints.wide) {
    return "desktop";
  }
  return "wide";
}

/** CSS media-query helpers (min-width). */
export const mediaQueries = {
  mobile: `(min-width: ${breakpoints.mobile}px)`,
  tablet: `(min-width: ${breakpoints.tablet}px)`,
  laptop: `(min-width: ${breakpoints.laptop}px)`,
  desktop: `(min-width: ${breakpoints.desktop}px)`,
  wide: `(min-width: ${breakpoints.wide}px)`,
} as const;
