import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseTone } from "./types";

export type BaseChipProps = HTMLAttributes<HTMLSpanElement> & {
  tone?: BaseTone;
  children?: ReactNode;
};

/** Primitive compact chip. */
export function BaseChip({
  tone = "neutral",
  className,
  children,
  ...rest
}: BaseChipProps) {
  return (
    <span className={cx("cui-base-chip", className)} data-tone={tone} {...rest}>
      {children}
    </span>
  );
}
