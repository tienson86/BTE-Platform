import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseTextVariant } from "./types";

export type BaseTextTone = "primary" | "secondary" | "muted";

export type BaseTextProps = HTMLAttributes<HTMLParagraphElement> & {
  variant?: BaseTextVariant;
  tone?: BaseTextTone;
  as?: "p" | "span" | "div";
  children?: ReactNode;
};

/** Primitive text. Consumes typography tokens only. */
export function BaseText({
  variant = "body",
  tone = "primary",
  as = "p",
  className,
  children,
  ...rest
}: BaseTextProps) {
  const Component = as;
  return (
    <Component
      className={cx("cui-base-text", className)}
      data-variant={variant}
      data-tone={tone}
      {...rest}
    >
      {children}
    </Component>
  );
}
