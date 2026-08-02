import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseSize } from "./types";

export type BaseIconProps = HTMLAttributes<HTMLSpanElement> & {
  size?: BaseSize;
  label?: string;
  children?: ReactNode;
};

/** Primitive icon wrapper. Decorative unless `label` is provided. */
export function BaseIcon({
  size = "md",
  label,
  className,
  children,
  ...rest
}: BaseIconProps) {
  const decorative = !label;
  return (
    <span
      className={cx("cui-base-icon", className)}
      data-size={size}
      role={decorative ? undefined : "img"}
      aria-label={label}
      aria-hidden={decorative ? true : undefined}
      {...rest}
    >
      {children}
    </span>
  );
}
