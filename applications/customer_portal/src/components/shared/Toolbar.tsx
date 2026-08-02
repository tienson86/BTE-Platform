import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type ToolbarProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
  label?: string;
};

/** Shared toolbar shell. */
export function Toolbar({
  children,
  label = "Toolbar",
  className,
  ...rest
}: ToolbarProps) {
  return (
    <div
      className={cx("cui-shared-toolbar", className)}
      role="toolbar"
      aria-label={label}
      {...rest}
    >
      {children}
    </div>
  );
}
