/**
 * PACK_04 — Shared presentation typography with line-clamp.
 */

import type { CSSProperties, HTMLAttributes, ReactNode } from "react";
import {
  LINE_CLAMP,
  type LineClampField,
  type PresentationTypographyRole,
  type PreviewText,
} from "../../presentation";
import { cx } from "../../utils";

export type PresentationTextProps = Omit<HTMLAttributes<HTMLElement>, "role"> & {
  /** Typography role (PACK_04 scale). */
  typeRole?: PresentationTypographyRole;
  /** Line-clamp field preset (overrides lines when set). */
  clamp?: LineClampField | "none";
  /** Explicit line count; wins over clamp preset when provided. */
  lines?: number;
  /** Prefer PreviewText from Presentation Adapter. */
  preview?: PreviewText;
  as?: "p" | "span" | "div" | "h2" | "h3" | "h4";
  children?: ReactNode;
};

/**
 * Typography primitive for PACK_04 Result surfaces.
 */
export function PresentationText({
  typeRole = "body",
  clamp = "none",
  lines,
  preview,
  as = "p",
  className,
  title,
  children,
  ...rest
}: PresentationTextProps): ReactNode {
  const resolvedLines =
    lines ??
    (preview ? preview.lineClamp : clamp !== "none" ? LINE_CLAMP[clamp] : undefined);
  const content = preview ? preview.text : children;
  const fullTitle = title ?? (preview?.hasMore ? preview.fullText : undefined);
  const Component = as;
  const clampStyle: CSSProperties | undefined = resolvedLines
    ? ({ ["--ui-line-clamp"]: String(resolvedLines) } as CSSProperties)
    : undefined;

  return (
    <Component
      className={cx("ui-presentation-text", className)}
      data-presentation="pack04"
      data-type-role={typeRole}
      data-line-clamp={resolvedLines ?? "none"}
      data-has-more={preview?.hasMore ? "true" : "false"}
      title={fullTitle}
      style={clampStyle}
      {...rest}
    >
      {content}
    </Component>
  );
}
