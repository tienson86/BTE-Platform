import type { ReactNode } from "react";
import { cx } from "../utils";

export type BlankLayoutProps = {
  children?: ReactNode;
  className?: string;
};

/** Blank canvas layout — no chrome (WP03 / ADR-004). */
export function BlankLayout({ children, className }: BlankLayoutProps): ReactNode {
  return <div className={cx("cui-blank-layout", className)}>{children}</div>;
}
