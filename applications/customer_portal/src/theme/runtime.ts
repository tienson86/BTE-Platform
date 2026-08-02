/**
 * Theme DOM / persistence runtime — no React.
 * Themes override token values; they never redefine component rules.
 */

import {
  themeColorCatalog,
  type ThemeMode,
} from "../tokens/color";

export const THEME_STORAGE_KEY = "bte-cui-theme";
export const THEME_ATTRIBUTE = "data-theme";
export const THEME_MODES = ["light", "dark"] as const satisfies readonly ThemeMode[];

export type ThemePreference = ThemeMode | "system";

/** Resolve effective theme from preference + optional media query. */
export function resolveThemeMode(
  preference: ThemePreference,
  prefersDark = false,
): ThemeMode {
  if (preference === "system") {
    return prefersDark ? "dark" : "light";
  }
  return preference;
}

/** Apply theme mode to a document element. */
export function applyThemeMode(
  mode: ThemeMode,
  root: HTMLElement | null = typeof document !== "undefined" ? document.documentElement : null,
): void {
  if (!root) {
    return;
  }
  root.setAttribute(THEME_ATTRIBUTE, mode);
  root.style.colorScheme = mode;
}

/** Read current theme from DOM. */
export function readThemeMode(
  root: HTMLElement | null = typeof document !== "undefined" ? document.documentElement : null,
): ThemeMode {
  const value = root?.getAttribute(THEME_ATTRIBUTE);
  if (value === "dark" || value === "light") {
    return value;
  }
  return "light";
}

/** Persist preference (localStorage when available). */
export function persistThemePreference(preference: ThemePreference): void {
  if (typeof localStorage === "undefined") {
    return;
  }
  localStorage.setItem(THEME_STORAGE_KEY, preference);
}

/** Load persisted preference. */
export function loadThemePreference(): ThemePreference {
  if (typeof localStorage === "undefined") {
    return "system";
  }
  const stored = localStorage.getItem(THEME_STORAGE_KEY);
  if (stored === "light" || stored === "dark" || stored === "system") {
    return stored;
  }
  return "system";
}

/** Initialize theme from storage + system preference. */
export function initializeTheme(
  root: HTMLElement | null = typeof document !== "undefined" ? document.documentElement : null,
): ThemeMode {
  const preference = loadThemePreference();
  const prefersDark =
    typeof window !== "undefined" &&
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;
  const mode = resolveThemeMode(preference, prefersDark);
  applyThemeMode(mode, root);
  return mode;
}

/** Toggle between light and dark. */
export function toggleThemeMode(
  root: HTMLElement | null = typeof document !== "undefined" ? document.documentElement : null,
): ThemeMode {
  const next: ThemeMode = readThemeMode(root) === "dark" ? "light" : "dark";
  applyThemeMode(next, root);
  persistThemePreference(next);
  return next;
}

/** Palette accessor for tests and tooling. */
export function getThemePalette(mode: ThemeMode) {
  return themeColorCatalog[mode];
}

export type { ThemeMode };
