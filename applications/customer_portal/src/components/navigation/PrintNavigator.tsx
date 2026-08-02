import { Callout, FooterNote } from "../shared";
import type { NavigationPrintViewModel } from "../../view_models/navigation";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderNavigationGate } from "./navigationGate";

export type PrintNavigatorProps = {
  data: NavigationPrintViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Print navigation options — presentation only. */
export function PrintNavigator({
  data,
  status = "ready",
  className,
}: PrintNavigatorProps) {
  return (
    <div className={cx("cui-nav-print-navigator", className)} aria-label={data.label}>
      {renderNavigationGate(
        status,
        {
          loadingTitle: "Loading print navigator",
          emptyTitle: "No print navigator available",
          unavailableTitle: "Print navigator unavailable",
          errorTitle: "Unable to load print navigator",
        },
        <>
          <Callout tone="info" title={data.label}>
            {data.note ?? data.label}
          </Callout>
          {data.href ? (
            <FooterNote>
              <a href={data.href}>{data.label}</a>
            </FooterNote>
          ) : null}
        </>,
      )}
    </div>
  );
}
