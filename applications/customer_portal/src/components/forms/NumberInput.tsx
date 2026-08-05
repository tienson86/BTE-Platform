import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseInput } from "../base/BaseInput";

export type NumberInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  invalid?: boolean;
};

/** WP02 NumberInput. */
export function NumberInput({ className, invalid = false, ...rest }: NumberInputProps) {
  return (
    <BaseInput
      type="number"
      inputMode="decimal"
      invalid={invalid}
      className={cx("cui-number-input", className)}
      {...rest}
    />
  );
}
