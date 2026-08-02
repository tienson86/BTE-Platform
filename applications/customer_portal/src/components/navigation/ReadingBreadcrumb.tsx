import { InformationBox } from "../shared";
import type { NavigationBreadcrumbItemViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type ReadingBreadcrumbProps = {
  items: NavigationBreadcrumbItemViewModel[];
  status?: PresentationStatus;
  className?: string;
};

/** Reading breadcrumb — prepared trail only. */
export function ReadingBreadcrumb({
  items,
  status = "ready",
  className,
}: ReadingBreadcrumbProps) {
  return (
    <nav
      className={cx("cui-nav-reading-breadcrumb", className)}
      aria-label="Reading Breadcrumb"
    >
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading breadcrumb",
          emptyTitle: "No breadcrumb available",
          unavailableTitle: "Breadcrumb unavailable",
          errorTitle: "Unable to load breadcrumb",
        },
        <InformationBox title="Reading path">
          <ol className="cui-nav-reading-breadcrumb__list">
            {items.map((item, index) => (
              <li key={item.id} className="cui-nav-reading-breadcrumb__item">
                {item.href ? <a href={item.href}>{item.label}</a> : item.label}
                {index < items.length - 1 ? (
                  <span aria-hidden="true"> / </span>
                ) : null}
              </li>
            ))}
          </ol>
        </InformationBox>,
      )}
    </nav>
  );
}
