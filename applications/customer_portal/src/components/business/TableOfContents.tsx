import { StickyReadingRail } from "../shared";
import type { ReportTocItemViewModel } from "../../view_models/consultation_report";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type TableOfContentsProps = {
  items: ReportTocItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Report table of contents — presentation navigation metadata only. */
export function TableOfContents({
  items,
  title = "Table of Contents",
  status = "ready",
  className,
}: TableOfContentsProps) {
  return (
    <div className={cx("cui-biz-table-of-contents", className)}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading table of contents",
          emptyTitle: "No table of contents available",
          unavailableTitle: "Table of contents unavailable",
          errorTitle: "Unable to load table of contents",
        },
        <StickyReadingRail
          title={title}
          items={items.map((item) => ({
            id: item.id,
            label: item.label,
            href: item.href,
            active: item.active,
          }))}
        />,
      )}
    </div>
  );
}
