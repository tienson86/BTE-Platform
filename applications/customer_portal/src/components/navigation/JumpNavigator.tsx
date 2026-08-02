import { StickyReadingRail } from "../shared";
import type { NavigationItemViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type JumpNavigatorProps = {
  items: NavigationItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Jump navigator — direct section jumps from ViewModel. */
export function JumpNavigator({
  items,
  title = "Jump Navigation",
  status = "ready",
  className,
}: JumpNavigatorProps) {
  return (
    <div className={cx("cui-nav-jump-navigator", className)}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading jump navigator",
          emptyTitle: "No jump targets available",
          unavailableTitle: "Jump navigator unavailable",
          errorTitle: "Unable to load jump navigator",
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
