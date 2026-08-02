import { LabelValueRow, SectionHeader, SectionSurface, StatusBadge } from "../shared";
import type { ReportHeaderViewModel } from "../../view_models/consultation_report";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ReportHeaderProps = {
  data: ReportHeaderViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Consultation report header — presentation metadata only. */
export function ReportHeader({
  data,
  status = "ready",
  className,
}: ReportHeaderProps) {
  return (
    <header className={cx("cui-biz-report-header", className)} aria-label={data.title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading report header",
          emptyTitle: "No report header available",
          unavailableTitle: "Report header unavailable",
          errorTitle: "Unable to load report header",
        },
        <SectionSurface gap="paragraph" variant="paper">
          <SectionHeader
            title={data.title}
            subtitle={data.subtitle}
            level={2}
            actions={<StatusBadge status="info">Consultation Report</StatusBadge>}
          />
          {data.clientLabel ? (
            <LabelValueRow label="Client" value={data.clientLabel} />
          ) : null}
          {data.generatedLabel ? (
            <LabelValueRow label="Generated" value={data.generatedLabel} />
          ) : null}
        </SectionSurface>,
      )}
    </header>
  );
}
