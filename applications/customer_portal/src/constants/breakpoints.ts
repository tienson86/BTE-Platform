/**
 * Breakpoint constants — Pack 02 — 02_GRID_SYSTEM.
 * Responsive foundations only; no screen behaviour.
 */

import { coreGrid } from "../tokens/core";

export const breakpoints = {
  mobileMax: coreGrid.breakpoint_mobile_max,
  tabletMin: coreGrid.breakpoint_tablet_min,
  tabletMax: coreGrid.breakpoint_tablet_max,
  laptopMin: coreGrid.breakpoint_laptop_min,
  laptopMax: coreGrid.breakpoint_laptop_max,
  desktopMin: coreGrid.breakpoint_desktop_min,
} as const;

export type BreakpointName = "mobile" | "tablet" | "laptop" | "desktop";

/** Resolve breakpoint name from viewport width (px). */
export function resolveBreakpoint(widthPx: number): BreakpointName {
  if (widthPx <= breakpoints.mobileMax) {
    return "mobile";
  }
  if (widthPx <= breakpoints.tabletMax) {
    return "tablet";
  }
  if (widthPx <= breakpoints.laptopMax) {
    return "laptop";
  }
  return "desktop";
}

/**
 * Responsive spacing scale factors.
 * Pack 02 — 03_SPACING_SYSTEM §16.
 */
export const spacingScaleFactor: Record<BreakpointName, number> = {
  desktop: 1,
  laptop: 0.9,
  tablet: 0.8,
  mobile: 0.7,
};
