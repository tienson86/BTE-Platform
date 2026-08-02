import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type TagGroupProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
  label?: string;
};

/** Shared tag cluster. */
export function TagGroup({
  children,
  label = "Tags",
  className,
  ...rest
}: TagGroupProps) {
  return (
    <div
      className={cx("cui-shared-tag-group", "cui-row-list", className)}
      role="group"
      aria-label={label}
      {...rest}
    >
      {children}
    </div>
  );
}
