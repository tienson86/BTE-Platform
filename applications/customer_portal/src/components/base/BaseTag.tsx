import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseTone } from "./types";

export type BaseTagProps = HTMLAttributes<HTMLSpanElement> & {
  tone?: BaseTone;
  children?: ReactNode;
};

/** Primitive categorical tag. */
export function BaseTag({
  tone = "neutral",
  className,
  children,
  ...rest
}: BaseTagProps) {
  return (
    <span className={cx("cui-base-tag", className)} data-tone={tone} {...rest}>
      {children}
    </span>
  );
}
