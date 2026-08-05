import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type MenuProps = HTMLAttributes<HTMLUListElement> & {
  children?: ReactNode;
  label?: string;
};

/** WP02 Menu — semantic menu list container. */
export function Menu({ children, label = "Menu", className, ...rest }: MenuProps) {
  return (
    <ul className={cx("cui-menu", className)} role="menu" aria-label={label} {...rest}>
      {children}
    </ul>
  );
}
