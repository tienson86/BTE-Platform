import type { HTMLAttributes, ReactNode } from "react";
import { BaseGrid } from "../base";
import { cx } from "../../utils";

export type PropertyGridProps = HTMLAttributes<HTMLDivElement> & {
  columns?: 2 | 3 | 4;
  children?: ReactNode;
};

/** Shared property grid. */
export function PropertyGrid({
  columns = 2,
  className,
  children,
  ...rest
}: PropertyGridProps) {
  return (
    <BaseGrid columns={columns} className={cx("cui-shared-property-grid", className)} {...rest}>
      {children}
    </BaseGrid>
  );
}
