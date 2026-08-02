import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type ChipGroupProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
  label?: string;
};

/** Shared chip cluster. */
export function ChipGroup({
  children,
  label = "Chips",
  className,
  ...rest
}: ChipGroupProps) {
  return (
    <div
      className={cx("cui-shared-chip-group", "cui-row-list", className)}
      role="group"
      aria-label={label}
      {...rest}
    >
      {children}
    </div>
  );
}
