import {
  InformationBox,
  PropertyGrid,
  PropertyItem,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AppendixCreditsViewModel } from "../../view_models/appendix";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type CreditsSectionProps = {
  data: AppendixCreditsViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Credits section — prepared attribution only. */
export function CreditsSection({
  data,
  status = "ready",
  className,
}: CreditsSectionProps) {
  const title = data.title ?? "Credits";

  return (
    <section className={cx("cui-biz-credits-section", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading credits",
          emptyTitle: "No credits available",
          unavailableTitle: "Credits unavailable",
          errorTitle: "Unable to load credits",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {data.paragraphs.map((paragraph, index) => (
            <InformationBox key={`credits-${index}`}>{paragraph}</InformationBox>
          ))}
          {data.items && data.items.length > 0 ? (
            <PropertyGrid columns={2}>
              {data.items.map((item) => (
                <PropertyItem key={item.id} label={item.label} value={item.value} />
              ))}
            </PropertyGrid>
          ) : null}
        </SectionSurface>,
      )}
    </section>
  );
}
