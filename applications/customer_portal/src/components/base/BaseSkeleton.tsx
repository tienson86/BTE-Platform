import type { HTMLAttributes } from "react";
import { cx } from "../../utils";

export type BaseSkeletonProps = HTMLAttributes<HTMLSpanElement> & {
  width?: string;
  height?: string;
};

/** Primitive content placeholder skeleton. */
export function BaseSkeleton({
  width,
  height,
  className,
  style,
  ...rest
}: BaseSkeletonProps) {
  return (
    <span
      className={cx("cui-base-skeleton", className)}
      style={{ width, height, ...style }}
      aria-hidden="true"
      {...rest}
    />
  );
}
