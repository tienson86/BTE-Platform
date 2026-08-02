/**
 * Application bootstrap hooks for Commercial UI V3 foundation.
 * Theme initialization only — no routing or business rendering (WP-0001).
 */

import { initializeTheme, type ThemeMode } from "../theme";

/** Bootstrap presentation foundation on the document root. */
export function bootstrapFoundation(
  root: HTMLElement | null = typeof document !== "undefined" ? document.documentElement : null,
): { theme: ThemeMode } {
  const theme = initializeTheme(root);
  return { theme };
}
