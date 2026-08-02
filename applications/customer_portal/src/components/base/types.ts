/**
 * Shared prop contracts for Base Components — WP-0002.
 * Presentation only. No business meaning.
 */

export type BaseSize = "sm" | "md" | "lg";

export type BaseTone =
  | "neutral"
  | "accent"
  | "success"
  | "warning"
  | "danger"
  | "info";

export type BaseSurfaceVariant =
  | "background"
  | "paper"
  | "section"
  | "callout"
  | "overlay";

export type BaseTextVariant =
  | "display"
  | "pageTitle"
  | "chapter"
  | "section"
  | "subsection"
  | "bodyLarge"
  | "body"
  | "caption"
  | "metadata";

export type BaseHeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;

export type BaseSpacing =
  | "inline"
  | "list"
  | "paragraph"
  | "block"
  | "section"
  | "chapter"
  | "none";
