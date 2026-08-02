import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type TimelineProps = HTMLAttributes<HTMLOListElement> & {
  children?: ReactNode;
};

/** Shared vertical timeline list. */
export function Timeline({ className, children, ...rest }: TimelineProps) {
  return (
    <ol className={cx("cui-shared-timeline", className)} {...rest}>
      {children}
    </ol>
  );
}
