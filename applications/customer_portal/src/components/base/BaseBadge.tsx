import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseTone } from "./types";

export type BaseBadgeProps = HTMLAttributes<HTMLSpanElement> & {
  tone?: BaseTone;
  children?: ReactNode;
};

/** Primitive status/meta badge. */
export function BaseBadge({
  tone = "neutral",
  className,
  children,
  ...rest
}: BaseBadgeProps) {
  return (
    <span className={cx("cui-base-badge", className)} data-tone={tone} {...rest}>
      {children}
    </span>
  );
}
