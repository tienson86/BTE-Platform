import type { HTMLAttributes } from "react";
import { BaseDivider } from "../base";
import { cx } from "../../utils";

export type SectionDividerProps = HTMLAttributes<HTMLHRElement>;

/** Shared section divider. */
export function SectionDivider({ className, ...rest }: SectionDividerProps) {
  return <BaseDivider className={cx(className)} {...rest} />;
}
