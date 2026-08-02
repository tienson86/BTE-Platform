import type { ReactNode } from "react";
import { SectionSurface } from "../shared";
import { cx } from "../../utils";

export type HeroBackgroundProps = {
  children?: ReactNode;
  className?: string;
};

/** Decorative reading surface for the Executive Hero. */
export function HeroBackground({ children, className }: HeroBackgroundProps) {
  return (
    <SectionSurface
      variant="paper"
      gap="block"
      className={cx("cui-biz-hero-background", className)}
    >
      {children}
    </SectionSurface>
  );
}
