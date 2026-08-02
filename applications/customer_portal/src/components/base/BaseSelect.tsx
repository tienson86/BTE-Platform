import type { SelectHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseSelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  invalid?: boolean;
  children?: ReactNode;
};

/** Primitive select control. */
export function BaseSelect({
  invalid = false,
  className,
  children,
  ...rest
}: BaseSelectProps) {
  return (
    <select
      className={cx("cui-base-select", "cui-base-control", className)}
      aria-invalid={invalid || undefined}
      {...rest}
    >
      {children}
    </select>
  );
}
