/**
 * BTE Portal Design System — Color Tokens (WP01).
 * Primary = Emerald, Secondary = Slate (Sprint 01 Design Tokens).
 * Components must consume these tokens — never hard-code hex values.
 */

/** Standard 50–900 scale for a color family. */
export type ColorScale = {
  readonly 50: string;
  readonly 100: string;
  readonly 200: string;
  readonly 300: string;
  readonly 400: string;
  readonly 500: string;
  readonly 600: string;
  readonly 700: string;
  readonly 800: string;
  readonly 900: string;
};

/** Primary brand — Emerald. */
export const primary: ColorScale = {
  50: "#ecfdf5",
  100: "#d1fae5",
  200: "#a7f3d0",
  300: "#6ee7b7",
  400: "#34d399",
  500: "#10b981",
  600: "#059669",
  700: "#047857",
  800: "#065f46",
  900: "#064e3b",
} as const;

/** Secondary — Slate. */
export const secondary: ColorScale = {
  50: "#f8fafc",
  100: "#f1f5f9",
  200: "#e2e8f0",
  300: "#cbd5e1",
  400: "#94a3b8",
  500: "#64748b",
  600: "#475569",
  700: "#334155",
  800: "#1e293b",
  900: "#0f172a",
} as const;

/** Success — Green. */
export const success: ColorScale = {
  50: "#f0fdf4",
  100: "#dcfce7",
  200: "#bbf7d0",
  300: "#86efac",
  400: "#4ade80",
  500: "#22c55e",
  600: "#16a34a",
  700: "#15803d",
  800: "#166534",
  900: "#14532d",
} as const;

/** Warning — Amber. */
export const warning: ColorScale = {
  50: "#fffbeb",
  100: "#fef3c7",
  200: "#fde68a",
  300: "#fcd34d",
  400: "#fbbf24",
  500: "#f59e0b",
  600: "#d97706",
  700: "#b45309",
  800: "#92400e",
  900: "#78350f",
} as const;

/** Error / Danger — Red. */
export const error: ColorScale = {
  50: "#fef2f2",
  100: "#fee2e2",
  200: "#fecaca",
  300: "#fca5a5",
  400: "#f87171",
  500: "#ef4444",
  600: "#dc2626",
  700: "#b91c1c",
  800: "#991b1b",
  900: "#7f1d1d",
} as const;

/** Info — Sky / cool blue. */
export const info: ColorScale = {
  50: "#f0f9ff",
  100: "#e0f2fe",
  200: "#bae6fd",
  300: "#7dd3fc",
  400: "#38bdf8",
  500: "#0ea5e9",
  600: "#0284c7",
  700: "#0369a1",
  800: "#075985",
  900: "#0c4a6e",
} as const;

/**
 * Background scale — page canvas from lightest (50) to darkest (900).
 * Default light UI uses 50–100.
 */
export const background: ColorScale = {
  50: "#fafbfc",
  100: "#f4f6f8",
  200: "#eef1f4",
  300: "#e4e9ef",
  400: "#d5dde6",
  500: "#b8c4d0",
  600: "#8b9aab",
  700: "#5c6b7a",
  800: "#2f3b47",
  900: "#0f1419",
} as const;

/**
 * Surface scale — cards / panels from lightest (50) to darkest (900).
 * Default light UI uses 50–100.
 */
export const surface: ColorScale = {
  50: "#ffffff",
  100: "#f8fafc",
  200: "#f1f5f9",
  300: "#e8eef4",
  400: "#dce4ec",
  500: "#c5d0db",
  600: "#94a3b8",
  700: "#64748b",
  800: "#334155",
  900: "#1e293b",
} as const;

/** Border scale — subtle (50) to strong (900). */
export const border: ColorScale = {
  50: "#f8fafc",
  100: "#f1f5f9",
  200: "#e2e8f0",
  300: "#cbd5e1",
  400: "#94a3b8",
  500: "#64748b",
  600: "#475569",
  700: "#334155",
  800: "#1e293b",
  900: "#0f172a",
} as const;

/** Text / ink scale — muted light (50) to primary dark (900). */
export const text: ColorScale = {
  50: "#f8fafc",
  100: "#f1f5f9",
  200: "#e2e8f0",
  300: "#cbd5e1",
  400: "#94a3b8",
  500: "#64748b",
  600: "#475569",
  700: "#334155",
  800: "#1e293b",
  900: "#0f172a",
} as const;

/** Aggregated color tokens. */
export const colors = {
  primary,
  secondary,
  success,
  warning,
  error,
  info,
  background,
  surface,
  border,
  text,
} as const;

export type ColorFamily = keyof typeof colors;
export type ColorShade = keyof ColorScale;
