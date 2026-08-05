/**
 * BTE Portal Design System — Spacing Tokens (WP01).
 * 8px grid foundation. Values are pixel numbers for TS consumers.
 */

/** 8px-grid spacing scale (px). */
export const spacing = {
  0: 0,
  4: 4,
  8: 8,
  12: 12,
  16: 16,
  20: 20,
  24: 24,
  32: 32,
  40: 40,
  48: 48,
  64: 64,
  80: 80,
  96: 96,
} as const;

export type SpacingKey = keyof typeof spacing;

/** Format a spacing token as a CSS length. */
export function spacingPx(key: SpacingKey): string {
  return `${spacing[key]}px`;
}
