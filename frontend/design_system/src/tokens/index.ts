/**
 * Design token constants — mirror CSS custom properties.
 * Components MUST use CSS variables / these tokens — never hard-code hex in UI.
 */
export const colors = {
  primary: "var(--bte-color-primary)",
  primaryHover: "var(--bte-color-primary-hover)",
  primarySoft: "var(--bte-color-primary-soft)",
  secondary: "var(--bte-color-secondary)",
  secondarySoft: "var(--bte-color-secondary-soft)",
  success: "var(--bte-color-success)",
  successSoft: "var(--bte-color-success-soft)",
  warning: "var(--bte-color-warning)",
  warningSoft: "var(--bte-color-warning-soft)",
  danger: "var(--bte-color-danger)",
  dangerSoft: "var(--bte-color-danger-soft)",
  info: "var(--bte-color-info)",
  infoSoft: "var(--bte-color-info-soft)",
  neutral: "var(--bte-color-neutral)",
  bg: "var(--bte-color-bg)",
  bgAccent: "var(--bte-color-bg-accent)",
  panel: "var(--bte-color-panel)",
  card: "var(--bte-color-card)",
  line: "var(--bte-color-line)",
  ink: "var(--bte-color-ink)",
  muted: "var(--bte-color-muted)",
} as const;

export const spacing = {
  1: "var(--bte-space-1)",
  2: "var(--bte-space-2)",
  3: "var(--bte-space-3)",
  4: "var(--bte-space-4)",
  5: "var(--bte-space-5)",
  6: "var(--bte-space-6)",
  8: "var(--bte-space-8)",
  10: "var(--bte-space-10)",
  12: "var(--bte-space-12)",
} as const;

export const typography = {
  fontSans: "var(--bte-font-sans)",
  fontMono: "var(--bte-font-mono)",
  h1: "var(--bte-text-h1)",
  h2: "var(--bte-text-h2)",
  h3: "var(--bte-text-h3)",
  subtitle: "var(--bte-text-subtitle)",
  body: "var(--bte-text-body)",
  caption: "var(--bte-text-caption)",
  metric: "var(--bte-text-metric)",
  label: "var(--bte-text-label)",
} as const;

export const radius = {
  sm: "var(--bte-radius-sm)",
  md: "var(--bte-radius-md)",
  lg: "var(--bte-radius-lg)",
  xl: "var(--bte-radius-xl)",
} as const;

export const shadows = {
  sm: "var(--bte-shadow-sm)",
  md: "var(--bte-shadow-md)",
  lg: "var(--bte-shadow-lg)",
} as const;

export const zIndex = {
  header: "var(--bte-z-header)",
  sidebar: "var(--bte-z-sidebar)",
  dropdown: "var(--bte-z-dropdown)",
  toast: "var(--bte-z-toast)",
  modal: "var(--bte-z-modal)",
  tooltip: "var(--bte-z-tooltip)",
} as const;

export const motion = {
  fast: "var(--bte-motion-fast)",
  base: "var(--bte-motion-base)",
  slow: "var(--bte-motion-slow)",
  ease: "var(--bte-motion-ease)",
} as const;

export const breakpoints = {
  tablet: 900,
  laptop: 1100,
  desktop: 1280,
} as const;

export type StatusTone = "neutral" | "primary" | "success" | "warning" | "danger" | "info";
