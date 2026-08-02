import type { InputHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseSwitchProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  label: ReactNode;
};

/** Primitive on/off switch. */
export function BaseSwitch({
  label,
  id,
  className,
  ...rest
}: BaseSwitchProps) {
  const inputId = id ?? rest.name;
  return (
    <label className={cx("cui-base-switch", className)} htmlFor={inputId}>
      <input id={inputId} type="checkbox" role="switch" {...rest} />
      <span className="cui-base-switch__track" aria-hidden="true">
        <span className="cui-base-switch__thumb" />
      </span>
      <span>{label}</span>
    </label>
  );
}
