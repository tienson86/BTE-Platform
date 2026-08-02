import type { HTMLAttributes, ReactNode } from "react";
import { BaseStack } from "../base";
import { cx } from "../../utils";

export type KeyValueGridProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
};

/** Shared stacked key/value grid. */
export function KeyValueGrid({ className, children, ...rest }: KeyValueGridProps) {
  return (
    <BaseStack gap="list" className={cx("cui-shared-key-value-grid", className)} {...rest}>
      {children}
    </BaseStack>
  );
}
