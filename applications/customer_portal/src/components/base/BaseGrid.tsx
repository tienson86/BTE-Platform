import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseGridColumns = 2 | 3 | 4 | "auto";

export type BaseGridProps = HTMLAttributes<HTMLDivElement> & {
  columns?: BaseGridColumns;
  children?: ReactNode;
};

/** Primitive responsive content grid. */
export function BaseGrid({
  columns = "auto",
  className,
  children,
  ...rest
}: BaseGridProps) {
  return (
    <div
      className={cx("cui-base-grid", className)}
      data-columns={columns === "auto" ? undefined : columns}
      {...rest}
    >
      {children}
    </div>
  );
}
