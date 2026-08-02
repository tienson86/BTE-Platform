import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseHeadingLevel, BaseTextVariant } from "./types";

const LEVEL_VARIANT: Record<BaseHeadingLevel, BaseTextVariant> = {
  1: "pageTitle",
  2: "chapter",
  3: "section",
  4: "subsection",
  5: "bodyLarge",
  6: "body",
};

export type BaseHeadingProps = HTMLAttributes<HTMLHeadingElement> & {
  level?: BaseHeadingLevel;
  variant?: BaseTextVariant;
  tone?: "primary" | "secondary" | "muted";
  children?: ReactNode;
};

/** Primitive heading with semantic level. */
export function BaseHeading({
  level = 2,
  variant,
  tone = "primary",
  className,
  children,
  ...rest
}: BaseHeadingProps) {
  const Tag = `h${level}` as "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
  return (
    <Tag
      className={cx("cui-base-heading", className)}
      data-variant={variant ?? LEVEL_VARIANT[level]}
      data-tone={tone}
      {...rest}
    >
      {children}
    </Tag>
  );
}
