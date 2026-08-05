import type { SelectHTMLAttributes } from "react";
import { cx } from "../../utils";

export type MultiSelectOption = {
  value: string;
  label: string;
  disabled?: boolean;
};

export type MultiSelectProps = Omit<SelectHTMLAttributes<HTMLSelectElement>, "multiple"> & {
  options: MultiSelectOption[];
  invalid?: boolean;
};

/** WP02 MultiSelect — native multiple select (token-styled). */
export function MultiSelect({
  options,
  invalid = false,
  className,
  ...rest
}: MultiSelectProps) {
  return (
    <select
      multiple
      className={cx("cui-base-select", "cui-base-control", "cui-multi-select", className)}
      aria-invalid={invalid || undefined}
      {...rest}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value} disabled={option.disabled}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
