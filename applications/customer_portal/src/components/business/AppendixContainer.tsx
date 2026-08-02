import type { ReactNode } from "react";
import { SectionContainer } from "../shared";
import { cx } from "../../utils";

export type AppendixContainerProps = {
  children?: ReactNode;
  className?: string;
};

/** Appendix document container — lightweight secondary reading shell. */
export function AppendixContainer({ children, className }: AppendixContainerProps) {
  return (
    <SectionContainer
      width="reading"
      gap="section"
      className={cx("cui-biz-appendix-container", className)}
      aria-label="Appendix"
    >
      {children}
    </SectionContainer>
  );
}
