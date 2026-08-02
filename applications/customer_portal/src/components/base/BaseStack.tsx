import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseSpacing } from "./types";

export type BaseStackProps = HTMLAttributes<HTMLDivElement> & {
  gap?: BaseSpacing;
  as?: "div" | "section";
  children?: ReactNode;
};

/** Primitive vertical stack with semantic spacing gap. */
export function BaseStack({
  gap = "paragraph",
  as = "div",
  className,
  children,
  ...rest
}: BaseStackProps) {
  const Component = as;
  return (
    <Component
      className={cx("cui-base-stack", className)}
      data-gap={gap}
      {...rest}
    >
      {children}
    </Component>
  );
}
