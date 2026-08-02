import { SectionHeader, StatusBadge } from "../shared";
import type { NavigationCurrentSectionViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type CurrentSectionProps = {
  data: NavigationCurrentSectionViewModel;
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Current section indicator — label from ViewModel only. */
export function CurrentSection({
  data,
  title = "Current Section",
  status = "ready",
  className,
}: CurrentSectionProps) {
  return (
    <div
      className={cx("cui-nav-current-section", className)}
      aria-label={title}
      data-current-section={data.id}
    >
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading current section",
          emptyTitle: "No current section available",
          unavailableTitle: "Current section unavailable",
          errorTitle: "Unable to load current section",
        },
        <SectionHeader
          title={title}
          subtitle={data.label}
          level={3}
          actions={<StatusBadge status="info">{data.label}</StatusBadge>}
        />,
      )}
    </div>
  );
}
