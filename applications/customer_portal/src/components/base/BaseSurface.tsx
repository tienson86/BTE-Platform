import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseSurfaceVariant } from "./types";

export type BaseSurfaceProps = HTMLAttributes<HTMLDivElement> & {
  variant?: BaseSurfaceVariant;
  as?: "div" | "section" | "article" | "aside";
  children?: ReactNode;
};

/** Primitive surface following Pack 02 surface hierarchy. */
export function BaseSurface({
  variant = "section",
  as = "div",
  className,
  children,
  ...rest
}: BaseSurfaceProps) {
  const Component = as;
  return (
    <Component
      className={cx("cui-base-surface", className)}
      data-variant={variant}
      {...rest}
    >
      {children}
    </Component>
  );
}
