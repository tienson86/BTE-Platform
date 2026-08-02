/**
 * Theme color palettes for Light and Dark.
 * Semantic roles only — Pack 02 — 05_COLOR_SYSTEM + 00_VISUAL_LANGUAGE (paper / ink).
 */

export type ThemeColorPalette = {
  surface_background: string;
  surface_report_paper: string;
  surface_section: string;
  surface_callout: string;
  surface_overlay: string;
  surface_disabled: string;
  text_primary: string;
  text_secondary: string;
  text_muted: string;
  text_inverse: string;
  border_divider: string;
  border_callout: string;
  border_focus: string;
  feedback_success: string;
  feedback_success_soft: string;
  feedback_warning: string;
  feedback_warning_soft: string;
  feedback_danger: string;
  feedback_danger_soft: string;
  feedback_info: string;
  feedback_info_soft: string;
  accent_primary: string;
  accent_primary_hover: string;
  accent_primary_soft: string;
  interaction_hover: string;
  interaction_selected: string;
  interaction_disabled: string;
  elevation_soft: string;
  elevation_overlay: string;
  elevation_modal: string;
  focus_ring: string;
};

/**
 * Light theme — cool neutral paper, ink text, restrained navy accent.
 * Avoids decorative saturation; reading remains primary.
 */
export const lightThemeColors: ThemeColorPalette = {
  surface_background: "#EEF0F3",
  surface_report_paper: "#FFFFFF",
  surface_section: "#F7F8FA",
  surface_callout: "#F0F3F7",
  surface_overlay: "#FFFFFF",
  surface_disabled: "#E8EAEE",
  text_primary: "#1A1D23",
  text_secondary: "#4A5568",
  text_muted: "#6B7280",
  text_inverse: "#F8FAFC",
  border_divider: "#E2E5EB",
  border_callout: "#C5D0DE",
  border_focus: "#2B4C7E",
  feedback_success: "#2F6F4E",
  feedback_success_soft: "#EAF5EF",
  feedback_warning: "#9A6700",
  feedback_warning_soft: "#FFF6E5",
  feedback_danger: "#B42318",
  feedback_danger_soft: "#FCEBEA",
  feedback_info: "#2B4C7E",
  feedback_info_soft: "#EAF0F7",
  accent_primary: "#2B4C7E",
  accent_primary_hover: "#1F3A63",
  accent_primary_soft: "#EAF0F7",
  interaction_hover: "rgba(26, 29, 35, 0.06)",
  interaction_selected: "rgba(43, 76, 126, 0.12)",
  interaction_disabled: "rgba(26, 29, 35, 0.38)",
  elevation_soft:
    "0 1px 2px rgba(26, 29, 35, 0.04), 0 4px 16px rgba(26, 29, 35, 0.05)",
  elevation_overlay:
    "0 4px 8px rgba(26, 29, 35, 0.06), 0 12px 32px rgba(26, 29, 35, 0.10)",
  elevation_modal:
    "0 8px 16px rgba(26, 29, 35, 0.08), 0 24px 48px rgba(26, 29, 35, 0.14)",
  focus_ring: "0 0 0 3px rgba(43, 76, 126, 0.32)",
};

/** Dark theme — preserves semantic meaning; does not invert intent. */
export const darkThemeColors: ThemeColorPalette = {
  surface_background: "#0E1116",
  surface_report_paper: "#161A21",
  surface_section: "#1B2028",
  surface_callout: "#1F2630",
  surface_overlay: "#1C222C",
  surface_disabled: "#252B35",
  text_primary: "#E8ECF2",
  text_secondary: "#A8B0BD",
  text_muted: "#8791A0",
  text_inverse: "#0E1116",
  border_divider: "#2A313C",
  border_callout: "#3A4656",
  border_focus: "#7BA0D4",
  feedback_success: "#5FBF8A",
  feedback_success_soft: "#163526",
  feedback_warning: "#E0B354",
  feedback_warning_soft: "#3A2E12",
  feedback_danger: "#F07167",
  feedback_danger_soft: "#3A1816",
  feedback_info: "#7BA0D4",
  feedback_info_soft: "#1A2738",
  accent_primary: "#7BA0D4",
  accent_primary_hover: "#9BB6E0",
  accent_primary_soft: "#1A2738",
  interaction_hover: "rgba(232, 236, 242, 0.06)",
  interaction_selected: "rgba(123, 160, 212, 0.18)",
  interaction_disabled: "rgba(232, 236, 242, 0.38)",
  elevation_soft:
    "0 1px 2px rgba(0, 0, 0, 0.35), 0 8px 24px rgba(0, 0, 0, 0.28)",
  elevation_overlay:
    "0 8px 16px rgba(0, 0, 0, 0.40), 0 16px 40px rgba(0, 0, 0, 0.36)",
  elevation_modal:
    "0 12px 24px rgba(0, 0, 0, 0.48), 0 28px 56px rgba(0, 0, 0, 0.42)",
  focus_ring: "0 0 0 3px rgba(123, 160, 212, 0.40)",
};

export const themeColorCatalog = {
  light: lightThemeColors,
  dark: darkThemeColors,
} as const;

export type ThemeMode = keyof typeof themeColorCatalog;
