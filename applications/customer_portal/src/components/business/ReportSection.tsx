import type { ReactNode } from "react";
import { SectionDivider, SectionHeader, SectionSurface } from "../shared";
import { cx } from "../../utils";

export type ReportSectionProps = {
  id: string;
  title: string;
  children?: ReactNode;
  className?: string;
};

/** Report section wrapper preserving document reading order. */
export function ReportSection({
  id,
  title,
  children,
  className,
}: ReportSectionProps) {
  return (
    <section
      id={id}
      className={cx("cui-biz-report-section", className)}
      aria-label={title}
      data-report-section={id}
    >
      <SectionSurface gap="block" variant="paper">
        <SectionHeader title={title} level={2} />
        <SectionDivider />
        {children}
      </SectionSurface>
    </section>
  );
}
