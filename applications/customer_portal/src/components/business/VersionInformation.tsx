import {
  PropertyGrid,
  PropertyItem,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AppendixVersionViewModel } from "../../view_models/appendix";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type VersionInformationProps = {
  data: AppendixVersionViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Version information — prepared metadata only. */
export function VersionInformation({
  data,
  status = "ready",
  className,
}: VersionInformationProps) {
  const title = data.title ?? "Version Information";

  return (
    <section className={cx("cui-biz-version-information", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading version information",
          emptyTitle: "No version information available",
          unavailableTitle: "Version information unavailable",
          errorTitle: "Unable to load version information",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          <PropertyGrid columns={2}>
            {data.items.length === 0 ? (
              <PropertyItem label="Version" value="Unavailable" />
            ) : (
              data.items.map((item) => (
                <PropertyItem key={item.id} label={item.label} value={item.value} />
              ))
            )}
          </PropertyGrid>
        </SectionSurface>,
      )}
    </section>
  );
}
