import type { HTMLAttributes } from "react";
import { cx } from "../../utils";
import type { BaseSize } from "./types";

export type BaseSpinnerProps = HTMLAttributes<HTMLSpanElement> & {
  size?: BaseSize;
  label?: string;
};

/** Primitive loading spinner. */
export function BaseSpinner({
  size = "md",
  label = "Loading",
  className,
  ...rest
}: BaseSpinnerProps) {
  return (
    <span
      className={cx("cui-base-spinner", className)}
      data-size={size}
      role="status"
      aria-label={label}
      {...rest}
    />
  );
}
