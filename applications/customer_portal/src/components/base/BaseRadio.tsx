import type { InputHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseRadioProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  label: ReactNode;
};

/** Primitive radio with label. */
export function BaseRadio({
  label,
  id,
  className,
  ...rest
}: BaseRadioProps) {
  const inputId = id ?? (rest.name && rest.value != null ? `${rest.name}-${String(rest.value)}` : undefined);
  return (
    <label className={cx("cui-base-radio", className)} htmlFor={inputId}>
      <input id={inputId} type="radio" {...rest} />
      <span>{label}</span>
    </label>
  );
}
