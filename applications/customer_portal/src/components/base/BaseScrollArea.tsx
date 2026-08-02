import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseScrollAreaProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
};

/** Primitive scrollable region. */
export function BaseScrollArea({
  className,
  children,
  ...rest
}: BaseScrollAreaProps) {
  return (
    <div className={cx("cui-base-scroll-area", className)} tabIndex={0} {...rest}>
      {children}
    </div>
  );
}
