import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseContainerWidth = "report" | "reading" | "medium" | "wide";

export type BaseContainerProps = HTMLAttributes<HTMLDivElement> & {
  width?: BaseContainerWidth;
  as?: "div" | "section" | "main";
  children?: ReactNode;
};

/** Primitive max-width container using grid tokens. */
export function BaseContainer({
  width = "report",
  as = "div",
  className,
  children,
  ...rest
}: BaseContainerProps) {
  const Component = as;
  return (
    <Component
      className={cx("cui-base-container", className)}
      data-width={width === "report" ? undefined : width}
      {...rest}
    >
      {children}
    </Component>
  );
}
