import { StickyReadingRail } from "../shared";
import type { NavigationItemViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type ReadingRailProps = {
  items: NavigationItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Reading rail — active section comes from ViewModel. */
export function ReadingRail({
  items,
  title = "Reading Rail",
  status = "ready",
  className,
}: ReadingRailProps) {
  return (
    <div className={cx("cui-nav-reading-rail", className)}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading reading rail",
          emptyTitle: "No reading rail available",
          unavailableTitle: "Reading rail unavailable",
          errorTitle: "Unable to load reading rail",
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
