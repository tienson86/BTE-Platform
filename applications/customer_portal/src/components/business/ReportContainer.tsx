import type { ReactNode } from "react";
import { SectionContainer } from "../shared";
import { cx } from "../../utils";

export type ReportContainerProps = {
  children?: ReactNode;
  className?: string;
};

/** Commercial report container — reading-width document shell. */
export function ReportContainer({ children, className }: ReportContainerProps) {
  return (
    <SectionContainer
      width="reading"
      gap="chapter"
      className={cx("cui-biz-report-container", className)}
      aria-label="Consultation Report"
    >
      {children}
    </SectionContainer>
  );
}
