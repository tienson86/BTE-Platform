/**
 * Theme infrastructure barrel — runtime + React ThemeProvider.
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
