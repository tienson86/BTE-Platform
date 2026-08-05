import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseInput } from "../base/BaseInput";

export type PasswordInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  invalid?: boolean;
};

/** WP02 PasswordInput. */
export function PasswordInput({ className, invalid = false, ...rest }: PasswordInputProps) {
  return (
    <BaseInput
      type="password"
      autoComplete="current-password"
      invalid={invalid}
      className={cx("cui-password-input", className)}
      {...rest}
    />
  );
}
