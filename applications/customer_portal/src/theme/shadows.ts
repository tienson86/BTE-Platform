/**
 * BTE Portal Design System — Shadow Tokens (WP01).
 * Soft elevation stack for SaaS surfaces.
 */

/** Soft shadow scale (CSS box-shadow values). */
export const shadows = {
  xs: "0 1px 2px rgba(15, 23, 42, 0.04)",
  sm: "0 1px 2px rgba(15, 23, 42, 0.05), 0 2px 8px rgba(15, 23, 42, 0.04)",
  md: "0 2px 4px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.06)",
  lg: "0 4px 8px rgba(15, 23, 42, 0.05), 0 16px 40px rgba(15, 23, 42, 0.08)",
  xl: "0 8px 16px rgba(15, 23, 42, 0.06), 0 24px 56px rgba(15, 23, 42, 0.12)",
} as const;

export type ShadowKey = keyof typeof shadows;
