/**
 * Theme barrel — Design System (ADR-002) + WP01 tokens.
 * Runtime theme infrastructure and design token scales.
 */

export {
  THEME_ATTRIBUTE,
  THEME_MODES,
  THEME_STORAGE_KEY,
  applyThemeMode,
  getThemePalette,
  initializeTheme,
  loadThemePreference,
  persistThemePreference,
  readThemeMode,
  resolveThemeMode,
  toggleThemeMode,
} from "./runtime";
export type { ThemePreference } from "./runtime";
export type { ThemeMode } from "../tokens/color";

export { ThemeProvider, useTheme } from "./ThemeProvider";
export type { ThemeContextValue, ThemeProviderProps } from "./ThemeProvider";

export {
  background,
  border,
  colors,
  error,
  info,
  primary,
  secondary,
  success,
  surface,
  text,
  warning,
} from "./colors";
export type { ColorFamily, ColorScale, ColorShade } from "./colors";

export { spacing, spacingPx } from "./spacing";
export type { SpacingKey } from "./spacing";

export {
  fontFamily,
  fontSize,
  fontWeight,
  letterSpacing,
  lineHeight,
  typography,
} from "./typography";
export type { FontWeight, TypeStyle, TypographyRole } from "./typography";

export { radius, radiusAlias, radiusPx } from "./radius";
export type { RadiusAliasKey, RadiusKey } from "./radius";

export { shadows } from "./shadows";
export type { ShadowKey } from "./shadows";

export {
  breakpointMax,
  breakpoints as designBreakpoints,
  mediaQueries,
  resolveBreakpoint as resolveDesignBreakpoint,
} from "./breakpoints";
export type { BreakpointName as DesignBreakpointName } from "./breakpoints";

export {
  motion as designMotion,
  motionDuration,
  motionEasing,
  transition,
} from "./motion";
export type { MotionSpeed } from "./motion";

export { zindex } from "./zindex";
export type { ZIndexKey } from "./zindex";

import { colors } from "./colors";
import { spacing } from "./spacing";
import { typography } from "./typography";
import { radius, radiusAlias } from "./radius";
import { shadows } from "./shadows";
import { breakpoints as designBreakpoints } from "./breakpoints";
import { motion as designMotion } from "./motion";
import { zindex } from "./zindex";

/** Aggregated WP01 design-token object. */
export const designTokens = {
  colors,
  spacing,
  typography,
  radius,
  radiusAlias,
  shadows,
  breakpoints: designBreakpoints,
  motion: designMotion,
  zindex,
} as const;
