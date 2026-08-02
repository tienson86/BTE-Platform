import type { HTMLAttributes, ReactNode } from "react";
import { BaseGrid, BaseStack } from "../base";
import { cx } from "../../utils";

export type MetricGroupProps = HTMLAttributes<HTMLDivElement> & {
  columns?: 2 | 3 | 4;
  children?: ReactNode;
  stacked?: boolean;
};

/** Shared group of metric cards/rows. */
export function MetricGroup({
  columns = 2,
  stacked = false,
  className,
  children,
  ...rest
}: MetricGroupProps) {
  if (stacked) {
    return (
      <BaseStack gap="list" className={cx("cui-shared-metric-group", className)} {...rest}>
        {children}
      </BaseStack>
    );
  }
  return (
    <BaseGrid columns={columns} className={cx("cui-shared-metric-group", className)} {...rest}>
      {children}
    </BaseGrid>
  );
}
