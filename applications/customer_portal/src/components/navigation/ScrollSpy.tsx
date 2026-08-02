import { StickyReadingRail } from "../shared";
import type { NavigationItemViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type NavigationScrollSpyProps = {
  items: NavigationItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/**
 * Pack 06 ScrollSpy (navigation layer) — presentation only.
 * Active section is supplied by NavigationViewModel (no derived observation).
 */
export function ScrollSpy({
  items,
  title = "Scroll Spy",
  status = "ready",
  className,
}: NavigationScrollSpyProps) {
  return (
    <div className={cx("cui-nav-scroll-spy", className)} aria-label={title}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading scroll spy",
          emptyTitle: "No scroll spy available",
          unavailableTitle: "Scroll spy unavailable",
          errorTitle: "Unable to load scroll spy",
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
