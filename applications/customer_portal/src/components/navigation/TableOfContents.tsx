import { StickyReadingRail } from "../shared";
import type { NavigationItemViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type NavigationTableOfContentsProps = {
  items: NavigationItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/**
 * Pack 06 TableOfContents (navigation layer).
 * Public alias NavigationTableOfContents avoids collision with frozen WP-0009 TOC.
 */
export function TableOfContents({
  items,
  title = "Table of Contents",
  status = "ready",
  className,
}: NavigationTableOfContentsProps) {
  return (
    <div className={cx("cui-nav-table-of-contents", className)}>
      {renderNavigationGate(
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
