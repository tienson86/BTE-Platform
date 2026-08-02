import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type FilterBarProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
  label?: string;
};

/** Shared filter control bar shell. */
export function FilterBar({
  children,
  label = "Filters",
  className,
  ...rest
}: FilterBarProps) {
  return (
    <div
      className={cx("cui-shared-filter-bar", className)}
      role="group"
      aria-label={label}
      {...rest}
    >
      {children}
    </div>
  );
}
