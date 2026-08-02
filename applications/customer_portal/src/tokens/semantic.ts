/**
 * Semantic design tokens — meaning-first API for Commercial UI V3.
 * Components and layouts consume these (via CSS variables), never core values.
 * Source: Pack 02 — 01_DESIGN_TOKENS through 08_MOTION_SYSTEM.
 */

import { coreMotion, coreRadius, coreSpacing, coreTypography } from "./core";

/** Semantic spacing → core scale mapping. Pack 02 — 03_SPACING_SYSTEM. */
export const semanticSpacing = {
  inline: coreSpacing.space_2,
  list: coreSpacing.space_3,
  paragraph: coreSpacing.space_5,
  block: coreSpacing.space_7,
  section: coreSpacing.space_9,
  chapter: coreSpacing.space_10,
  page: coreSpacing.space_10,
  field: coreSpacing.space_2,
  control: coreSpacing.space_5,
  table_cell: coreSpacing.space_4,
  table_section: coreSpacing.space_6,
} as const;

/** Semantic typography roles. Pack 02 — 04_TYPOGRAPHY_SYSTEM. */
export const semanticTypography = {
  display: {
    family: coreTypography.font_family_display,
    size: coreTypography.size_display,
    weight: coreTypography.weight_bold,
    lineHeight: coreTypography.line_height_display,
    letterSpacing: coreTypography.letter_spacing_display,
  },
  page_title: {
    family: coreTypography.font_family_display,
    size: coreTypography.size_page_title,
    weight: coreTypography.weight_bold,
    lineHeight: coreTypography.line_height_heading,
    letterSpacing: coreTypography.letter_spacing_heading,
  },
  chapter: {
    family: coreTypography.font_family_display,
    size: coreTypography.size_chapter,
    weight: coreTypography.weight_semibold,
    lineHeight: coreTypography.line_height_heading,
    letterSpacing: coreTypography.letter_spacing_heading,
  },
  section: {
    family: coreTypography.font_family_body,
    size: coreTypography.size_section,
    weight: coreTypography.weight_semibold,
    lineHeight: coreTypography.line_height_heading,
    letterSpacing: coreTypography.letter_spacing_heading,
  },
  subsection: {
    family: coreTypography.font_family_body,
    size: coreTypography.size_subsection,
    weight: coreTypography.weight_semibold,
    lineHeight: coreTypography.line_height_heading,
    letterSpacing: coreTypography.letter_spacing_body,
  },
  body_large: {
    family: coreTypography.font_family_body,
    size: coreTypography.size_body_large,
    weight: coreTypography.weight_regular,
    lineHeight: coreTypography.line_height_body,
    letterSpacing: coreTypography.letter_spacing_body,
  },
  body: {
    family: coreTypography.font_family_body,
    size: coreTypography.size_body,
    weight: coreTypography.weight_regular,
    lineHeight: coreTypography.line_height_body,
    letterSpacing: coreTypography.letter_spacing_body,
  },
  caption: {
    family: coreTypography.font_family_body,
    size: coreTypography.size_caption,
    weight: coreTypography.weight_regular,
    lineHeight: coreTypography.line_height_caption,
    letterSpacing: coreTypography.letter_spacing_body,
  },
  metadata: {
    family: coreTypography.font_family_body,
    size: coreTypography.size_metadata,
    weight: coreTypography.weight_medium,
    lineHeight: coreTypography.line_height_caption,
    letterSpacing: coreTypography.letter_spacing_metadata,
  },
} as const;

/** Semantic radius. Pack 02 — 06_ELEVATION_AND_SURFACE. */
export const semanticRadius = {
  paper: coreRadius.paper,
  surface: coreRadius.surface,
  callout: coreRadius.callout,
  overlay: coreRadius.overlay,
  control: coreRadius.control,
} as const;

/** Semantic motion. Pack 02 — 08_MOTION_SYSTEM. */
export const semanticMotion = {
  instant: `${coreMotion.instant}ms`,
  fast: `${coreMotion.fast}ms`,
  normal: `${coreMotion.normal}ms`,
  slow: `${coreMotion.slow}ms`,
  fade: `${coreMotion.normal}ms`,
  expand: `${coreMotion.normal}ms`,
  collapse: `${coreMotion.fast}ms`,
  ease_out: coreMotion.ease_out,
  ease_in_out: coreMotion.ease_in_out,
} as const;

/** CSS custom property names for semantic tokens (kebab-case). */
export const cssVarNames = {
  surface_background: "--surface-background",
  surface_report_paper: "--surface-report-paper",
  surface_section: "--surface-section",
  surface_callout: "--surface-callout",
  surface_overlay: "--surface-overlay",
  surface_disabled: "--surface-disabled",
  text_primary: "--text-primary",
  text_secondary: "--text-secondary",
  text_muted: "--text-muted",
  text_inverse: "--text-inverse",
  border_divider: "--border-divider",
  border_callout: "--border-callout",
  border_focus: "--border-focus",
  feedback_success: "--feedback-success",
  feedback_success_soft: "--feedback-success-soft",
  feedback_warning: "--feedback-warning",
  feedback_warning_soft: "--feedback-warning-soft",
  feedback_danger: "--feedback-danger",
  feedback_danger_soft: "--feedback-danger-soft",
  feedback_info: "--feedback-info",
  feedback_info_soft: "--feedback-info-soft",
  accent_primary: "--accent-primary",
  accent_primary_hover: "--accent-primary-hover",
  accent_primary_soft: "--accent-primary-soft",
  interaction_hover: "--interaction-hover",
  interaction_selected: "--interaction-selected",
  interaction_disabled: "--interaction-disabled",
  space_inline: "--space-inline",
  space_list: "--space-list",
  space_paragraph: "--space-paragraph",
  space_block: "--space-block",
  space_section: "--space-section",
  space_chapter: "--space-chapter",
  space_page: "--space-page",
  font_display: "--font-display",
  font_page_title: "--font-page-title",
  font_chapter: "--font-chapter",
  font_section: "--font-section",
  font_subsection: "--font-subsection",
  font_body_large: "--font-body-large",
  font_body: "--font-body",
  font_caption: "--font-caption",
  font_metadata: "--font-metadata",
  font_family_display: "--font-family-display",
  font_family_body: "--font-family-body",
  font_family_mono: "--font-family-mono",
  radius_paper: "--radius-paper",
  radius_surface: "--radius-surface",
  radius_callout: "--radius-callout",
  radius_overlay: "--radius-overlay",
  elevation_none: "--elevation-none",
  elevation_soft: "--elevation-soft",
  elevation_overlay: "--elevation-overlay",
  elevation_modal: "--elevation-modal",
  motion_instant: "--motion-instant",
  motion_fast: "--motion-fast",
  motion_normal: "--motion-normal",
  motion_slow: "--motion-slow",
  motion_fade: "--motion-fade",
  motion_expand: "--motion-expand",
  motion_collapse: "--motion-collapse",
  motion_ease_out: "--motion-ease-out",
  motion_ease_in_out: "--motion-ease-in-out",
  grid_columns: "--grid-columns",
  grid_margin: "--grid-margin",
  grid_gutter: "--grid-gutter",
  grid_report_max_width: "--grid-report-max-width",
  grid_reading_max_width: "--grid-reading-max-width",
  grid_wide_max_width: "--grid-wide-max-width",
  focus_ring: "--focus-ring",
  touch_target_min: "--touch-target-min",
} as const;

export type CssVarName = (typeof cssVarNames)[keyof typeof cssVarNames];

/** Helper: wrap a CSS variable name as a `var(...)` reference. */
export function cssVar(name: CssVarName): string {
  return `var(${name})`;
}
