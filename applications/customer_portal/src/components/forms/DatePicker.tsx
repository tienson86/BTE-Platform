import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseInput } from "../base/BaseInput";

export type DatePickerProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  invalid?: boolean;
};

/** WP02 DatePicker — native date input, token-styled. */
export function DatePicker({ className, invalid = false, ...rest }: DatePickerProps) {
  return (
    <BaseInput
      type="date"
      invalid={invalid}
      className={cx("cui-date-picker", className)}
      {...rest}
    />
  );
}
