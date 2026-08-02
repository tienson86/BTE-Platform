import type { HTMLAttributes } from "react";
import { cx } from "../../utils";

export type BaseDividerProps = HTMLAttributes<HTMLHRElement>;

/** Primitive hairline divider. */
export function BaseDivider({ className, ...rest }: BaseDividerProps) {
  return <hr className={cx("cui-base-divider", className)} {...rest} />;
}
