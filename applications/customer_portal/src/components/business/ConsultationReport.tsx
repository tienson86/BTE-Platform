import type { ReactNode } from "react";
import { Callout, SectionDivider } from "../shared";
import type { ConsultationReportReadyViewModel } from "../../view_models/consultation_report";
import { cx } from "../../utils";
import { PrintFooter } from "./PrintFooter";
import { PrintHeader } from "./PrintHeader";
import { ReportContainer } from "./ReportContainer";
import { ReportFooter } from "./ReportFooter";
import { ReportHeader } from "./ReportHeader";
import { ReportProgress } from "./ReportProgress";
import { TableOfContents } from "./TableOfContents";

export type ConsultationReportProps = {
  data: ConsultationReportReadyViewModel;
  children?: ReactNode;
  className?: string;
};

/**
 * Consultation Report shell — Pack 06 WP-0009.
 * Provides report chrome; section screens are composed by the Screen layer.
 */
export function ConsultationReport({
  data,
  children,
  className,
}: ConsultationReportProps) {
  return (
    <ReportContainer className={cx("cui-biz-consultation-report", className)}>
      <PrintHeader title={data.print.headerTitle} />
      <ReportHeader data={data.header} />
      <ReportProgress value={data.progress} />
      <TableOfContents items={data.toc} />
      <SectionDivider />
      {children}
      {data.closing ? (
        <>
          <SectionDivider />
          <section
            className="cui-biz-report-closing"
            aria-label={data.closing.title}
          >
            <Callout tone="info" title={data.closing.title}>
              {data.closing.body}
            </Callout>
          </section>
        </>
      ) : null}
      <SectionDivider />
      <ReportFooter data={data.footer} />
      <PrintFooter note={data.print.footerNote} />
    </ReportContainer>
  );
}
