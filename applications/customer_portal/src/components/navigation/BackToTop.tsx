import { FooterNote } from "../shared";
import type { NavigationBackToTopViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type BackToTopProps = {
  data: NavigationBackToTopViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Back to top — visibility supplied by ViewModel. */
export function BackToTop({
  data,
  status = "ready",
  className,
}: BackToTopProps) {
  if (!data.visible) {
    return null;
  }

  return (
    <div className={cx("cui-nav-back-to-top", className)} aria-label={data.label}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading back to top",
          emptyTitle: "Back to top unavailable",
          unavailableTitle: "Back to top unavailable",
          errorTitle: "Unable to load back to top",
        },
        <FooterNote>
          <a href={data.href}>{data.label}</a>
        </FooterNote>,
      )}
    </div>
  );
}
