/**
 * BTE Portal Design System — Typography Tokens (WP01).
 * SaaS-oriented hierarchy: Display → Caption.
 */

export type FontWeight = 400 | 500 | 600 | 700;

export type TypeStyle = {
  readonly fontFamily: string;
  readonly fontSize: string;
  readonly fontWeight: FontWeight;
  readonly lineHeight: number;
  readonly letterSpacing: string;
};

/** Font family stacks. */
export const fontFamily = {
  sans: '"Source Sans 3", "Segoe UI", system-ui, -apple-system, sans-serif',
  display: '"Source Sans 3", "Segoe UI", system-ui, -apple-system, sans-serif',
  mono: '"Cascadia Code", "SF Mono", Consolas, ui-monospace, monospace',
} as const;

/** Font size scale (rem). */
export const fontSize = {
  display: "2.5rem",
  h1: "2rem",
  h2: "1.5rem",
  h3: "1.25rem",
  h4: "1.125rem",
  bodyLarge: "1.125rem",
  body: "1rem",
  bodySmall: "0.875rem",
  caption: "0.75rem",
} as const;

/** Font weight scale. */
export const fontWeight = {
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
} as const satisfies Record<string, FontWeight>;

/** Line height scale. */
export const lineHeight = {
  tight: 1.15,
  snug: 1.25,
  normal: 1.5,
  relaxed: 1.7,
} as const;

/** Letter spacing scale. */
export const letterSpacing = {
  tight: "-0.02em",
  snug: "-0.015em",
  normal: "0",
  wide: "0.02em",
} as const;

/** Composed type styles for portal UI. */
export const typography = {
  display: {
    fontFamily: fontFamily.display,
    fontSize: fontSize.display,
    fontWeight: fontWeight.bold,
    lineHeight: lineHeight.tight,
    letterSpacing: letterSpacing.tight,
  },
  h1: {
    fontFamily: fontFamily.display,
    fontSize: fontSize.h1,
    fontWeight: fontWeight.bold,
    lineHeight: lineHeight.snug,
    letterSpacing: letterSpacing.snug,
  },
  h2: {
    fontFamily: fontFamily.display,
    fontSize: fontSize.h2,
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.snug,
    letterSpacing: letterSpacing.snug,
  },
  h3: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.h3,
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.snug,
    letterSpacing: letterSpacing.normal,
  },
  h4: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.h4,
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.snug,
    letterSpacing: letterSpacing.normal,
  },
  bodyLarge: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.bodyLarge,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.relaxed,
    letterSpacing: letterSpacing.normal,
  },
  body: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.body,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.relaxed,
    letterSpacing: letterSpacing.normal,
  },
  bodySmall: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.bodySmall,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.normal,
    letterSpacing: letterSpacing.normal,
  },
  caption: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.caption,
    fontWeight: fontWeight.medium,
    lineHeight: lineHeight.normal,
    letterSpacing: letterSpacing.wide,
  },
} as const satisfies Record<string, TypeStyle>;

export type TypographyRole = keyof typeof typography;
