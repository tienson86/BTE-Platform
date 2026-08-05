/**
 * BTE Portal Design System — Border Radius Tokens (WP01).
 * Default commercial radius is 12px (Sprint 01 Design Tokens).
 */

/** Border radius scale (px). */
export const radius = {
  0: 0,
  4: 4,
  8: 8,
  12: 12,
  16: 16,
  20: 20,
  24: 24,
  9999: 9999,
} as const;

/** Semantic aliases — `md` maps to Sprint default 12px. */
export const radiusAlias = {
  none: radius[0],
  sm: radius[4],
  md: radius[12],
  lg: radius[16],
  xl: radius[24],
  full: radius[9999],
} as const;

export type RadiusKey = keyof typeof radius;
export type RadiusAliasKey = keyof typeof radiusAlias;

/** Format a radius token as a CSS length. */
export function radiusPx(key: RadiusKey): string {
  return `${radius[key]}px`;
}
