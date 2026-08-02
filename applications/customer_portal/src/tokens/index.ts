/**
 * Commercial UI V3 Design Tokens — public barrel.
 * Pack 02 + Pack 04 — WP-0001 Foundation.
 */

export {
  coreGrid,
  coreMotion,
  coreOpacity,
  coreRadius,
  coreSpacing,
  coreTypography,
  coreZIndex,
} from "./core";
export type { CoreGridKey, CoreSpacingKey } from "./core";

export {
  darkThemeColors,
  lightThemeColors,
  themeColorCatalog,
} from "./color";
export type { ThemeColorPalette, ThemeMode } from "./color";

export {
  cssVar,
  cssVarNames,
  semanticMotion,
  semanticRadius,
  semanticSpacing,
  semanticTypography,
} from "./semantic";
export type { CssVarName } from "./semantic";

/** Required semantic CSS variable catalog for validation tests. */
export const REQUIRED_SEMANTIC_CSS_VARS = [
  "--surface-background",
  "--surface-report-paper",
  "--surface-section",
  "--surface-callout",
  "--surface-overlay",
  "--surface-disabled",
  "--text-primary",
  "--text-secondary",
  "--text-muted",
  "--text-inverse",
  "--border-divider",
  "--border-callout",
  "--border-focus",
  "--feedback-success",
  "--feedback-warning",
  "--feedback-danger",
  "--feedback-info",
  "--accent-primary",
  "--space-inline",
  "--space-list",
  "--space-paragraph",
  "--space-block",
  "--space-section",
  "--space-chapter",
  "--space-page",
  "--font-display",
  "--font-page-title",
  "--font-chapter",
  "--font-section",
  "--font-subsection",
  "--font-body-large",
  "--font-body",
  "--font-caption",
  "--font-metadata",
  "--radius-paper",
  "--radius-surface",
  "--radius-callout",
  "--radius-overlay",
  "--elevation-none",
  "--elevation-soft",
  "--elevation-overlay",
  "--elevation-modal",
  "--motion-fast",
  "--motion-normal",
  "--motion-slow",
  "--grid-columns",
  "--grid-margin",
  "--grid-gutter",
  "--grid-report-max-width",
  "--grid-reading-max-width",
  "--grid-wide-max-width",
  "--focus-ring",
  "--touch-target-min",
] as const;
