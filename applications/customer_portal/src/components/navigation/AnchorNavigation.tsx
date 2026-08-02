import { StickyReadingRail } from "../shared";
import type { NavigationItemViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type AnchorNavigationProps = {
  items: NavigationItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Section anchor navigation — prepared anchors only. */
export function AnchorNavigation({
  items,
  title = "Section Anchors",
  status = "ready",
  className,
}: AnchorNavigationProps) {
  return (
    <div className={cx("cui-nav-anchor-navigation", className)}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading anchors",
          emptyTitle: "No anchors available",
          unavailableTitle: "Anchors unavailable",
          errorTitle: "Unable to load anchors",
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
