import { FooterNote, LabelValueRow, SectionSurface } from "../shared";
import type { ReportFooterViewModel } from "../../view_models/consultation_report";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ReportFooterProps = {
  data: ReportFooterViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Consultation report footer. */
export function ReportFooter({
  data,
  status = "ready",
  className,
}: ReportFooterProps) {
  return (
    <footer className={cx("cui-biz-report-footer", className)} aria-label="Report Footer">
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading report footer",
          emptyTitle: "No report footer available",
          unavailableTitle: "Report footer unavailable",
          errorTitle: "Unable to load report footer",
        },
        <SectionSurface gap="paragraph">
          <FooterNote>{data.note}</FooterNote>
          {data.copyright ? (
            <LabelValueRow label="Copyright" value={data.copyright} />
          ) : null}
        </SectionSurface>,
      )}
    </footer>
  );
}
