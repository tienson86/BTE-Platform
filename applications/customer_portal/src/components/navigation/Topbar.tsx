import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type TopbarProps = HTMLAttributes<HTMLElement> & {
  brand?: ReactNode;
  start?: ReactNode;
  end?: ReactNode;
};

/** WP02 Topbar — application header strip. */
export function Topbar({ brand, start, end, className, children, ...rest }: TopbarProps) {
  return (
    <header className={cx("cui-topbar", "cui-top-bar", className)} {...rest}>
      {brand ? <div className="cui-topbar__brand">{brand}</div> : null}
      {start ? <div className="cui-topbar__start">{start}</div> : null}
      <div className="cui-topbar__main">{children}</div>
      {end ? <div className="cui-topbar__end">{end}</div> : null}
    </header>
  );
}
