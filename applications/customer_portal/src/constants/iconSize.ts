/**
 * BTE Portal Design System — Icon Size Tokens (WP01).
 * Pixel sizes for iconography; consume via tokens — never hard-code.
 */

/** Icon size scale (px). */
export const iconSize = {
  xs: 12,
  sm: 16,
  md: 20,
  lg: 24,
  xl: 32,
  "2xl": 40,
} as const;

export type IconSizeKey = keyof typeof iconSize;

/** Format an icon size token as a CSS length. */
export function iconSizePx(key: IconSizeKey): string {
  return `${iconSize[key]}px`;
}
