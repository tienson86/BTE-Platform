import { ReadingProgress as SharedReadingProgress } from "../shared";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type NavigationReadingProgressProps = {
  value: number;
  label?: string;
  status?: PresentationStatus;
  className?: string;
};

/**
 * Pack 06 ReadingProgress (navigation layer).
 * Progress value is presentation-ready from NavigationViewModel.
 */
export function ReadingProgress({
  value,
  label = "Reading progress",
  status = "ready",
  className,
}: NavigationReadingProgressProps) {
  return (
    <div className={cx("cui-nav-reading-progress", className)} aria-label={label}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading reading progress",
          emptyTitle: "No reading progress available",
          unavailableTitle: "Reading progress unavailable",
          errorTitle: "Unable to load reading progress",
        },
        <SharedReadingProgress value={value} label={label} />,
      )}
    </div>
  );
}
