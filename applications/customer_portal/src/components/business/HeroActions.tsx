import type { ReactNode } from "react";
import { Toolbar } from "../shared";
import { cx } from "../../utils";

export type HeroActionsProps = {
  children?: ReactNode;
  label?: string;
  className?: string;
};

/** Action cluster for Executive Hero. Presentation slot only. */
export function HeroActions({
  children,
  label = "Hero actions",
  className,
}: HeroActionsProps) {
  return (
    <Toolbar label={label} className={cx("cui-biz-hero-actions", className)}>
      {children}
    </Toolbar>
  );
}
