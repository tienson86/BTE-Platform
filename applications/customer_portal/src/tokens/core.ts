/**
 * Core design tokens — raw values only.
 * Application code must consume semantic tokens, never these directly.
 * Source: Pack 02 Design System (WP-0001).
 */

/** 8-point spacing scale (px). Pack 02 — 03_SPACING_SYSTEM. */
export const coreSpacing = {
  space_0: 0,
  space_1: 4,
  space_2: 8,
  space_3: 12,
  space_4: 16,
  space_5: 24,
  space_6: 32,
  space_7: 48,
  space_8: 64,
  space_9: 96,
  space_10: 120,
} as const;

/** Grid breakpoints and metrics (px). Pack 02 — 02_GRID_SYSTEM. */
export const coreGrid = {
  breakpoint_mobile_max: 767,
  breakpoint_tablet_min: 768,
  breakpoint_tablet_max: 1279,
  breakpoint_laptop_min: 1280,
  breakpoint_laptop_max: 1439,
  breakpoint_desktop_min: 1440,
  desktop_columns: 12,
  desktop_margin: 48,
  desktop_gutter: 24,
  desktop_report_max_width: 1360,
  desktop_reading_max_width: 760,
  desktop_wide_max_width: 1080,
  laptop_columns: 12,
  laptop_margin: 32,
  laptop_gutter: 20,
  laptop_reading_max_width: 700,
  tablet_columns: 8,
  tablet_margin: 24,
  tablet_gutter: 16,
  mobile_columns: 4,
  mobile_margin: 16,
  mobile_gutter: 12,
} as const;

/** Typography core sizes (rem). Implements Pack 02 — 04_TYPOGRAPHY_SYSTEM hierarchy. */
export const coreTypography = {
  font_family_display:
    '"Source Serif 4", "Iowan Old Style", "Palatino Linotype", Georgia, serif',
  font_family_body:
    '"Source Sans 3", "Segoe UI", system-ui, -apple-system, sans-serif',
  font_family_mono:
    '"Cascadia Code", "SF Mono", Consolas, ui-monospace, monospace',
  size_display: "2.75rem",
  size_page_title: "2.25rem",
  size_chapter: "1.75rem",
  size_section: "1.375rem",
  size_subsection: "1.125rem",
  size_body_large: "1.125rem",
  size_body: "1rem",
  size_caption: "0.875rem",
  size_metadata: "0.75rem",
  weight_regular: 400,
  weight_medium: 500,
  weight_semibold: 600,
  weight_bold: 700,
  line_height_display: 1.15,
  line_height_heading: 1.25,
  line_height_body: 1.7,
  line_height_caption: 1.5,
  letter_spacing_display: "-0.02em",
  letter_spacing_heading: "-0.015em",
  letter_spacing_body: "0",
  letter_spacing_metadata: "0.02em",
} as const;

/** Radius core (px). Pack 02 — 06_ELEVATION_AND_SURFACE. */
export const coreRadius = {
  none: 0,
  paper: 0,
  surface: 4,
  callout: 6,
  overlay: 8,
  control: 6,
} as const;

/** Motion durations (ms). Pack 02 — 08_MOTION_SYSTEM. */
export const coreMotion = {
  instant: 0,
  fast: 120,
  normal: 200,
  slow: 320,
  ease_out: "cubic-bezier(0.22, 1, 0.36, 1)",
  ease_in_out: "cubic-bezier(0.45, 0, 0.55, 1)",
} as const;

/** Opacity core. */
export const coreOpacity = {
  disabled: 0.48,
  muted: 0.72,
  overlay_scrim: 0.48,
  full: 1,
} as const;

/** Z-index layers for foundation shell. */
export const coreZIndex = {
  base: 0,
  sticky: 20,
  rail: 30,
  overlay: 80,
  modal: 100,
  toast: 110,
  focus: 120,
} as const;

export type CoreSpacingKey = keyof typeof coreSpacing;
export type CoreGridKey = keyof typeof coreGrid;
