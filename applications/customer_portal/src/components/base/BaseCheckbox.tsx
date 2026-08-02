import type { InputHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseCheckboxProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  label: ReactNode;
};

/** Primitive checkbox with label. */
export function BaseCheckbox({
  label,
  id,
  className,
  ...rest
}: BaseCheckboxProps) {
  const inputId = id ?? rest.name;
  return (
    <label className={cx("cui-base-check", className)} htmlFor={inputId}>
      <input id={inputId} type="checkbox" {...rest} />
      <span>{label}</span>
    </label>
  );
}
