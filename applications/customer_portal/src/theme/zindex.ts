/**
 * BTE Portal Design System — Z-Index Scale (WP01).
 * Layered stacking context for portal chrome and overlays.
 */

/** Z-index scale (unitless). */
export const zindex = {
  base: 0,
  raised: 10,
  dropdown: 100,
  sticky: 200,
  header: 300,
  sidebar: 350,
  overlay: 400,
  modal: 500,
  toast: 600,
  tooltip: 700,
  max: 9999,
} as const;

export type ZIndexKey = keyof typeof zindex;
