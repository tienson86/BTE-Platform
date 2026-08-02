import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";

export type BaseInputProps = InputHTMLAttributes<HTMLInputElement> & {
  invalid?: boolean;
};

/** Primitive text input. */
export function BaseInput({
  invalid = false,
  className,
  ...rest
}: BaseInputProps) {
  return (
    <input
      className={cx("cui-base-input", "cui-base-control", className)}
      aria-invalid={invalid || undefined}
      {...rest}
    />
  );
}
