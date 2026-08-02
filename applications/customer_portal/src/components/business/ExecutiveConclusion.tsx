import {
  Callout,
  ConfidenceBadge,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { ExecutiveConclusionViewModel } from "../../view_models/executive_insight";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ExecutiveConclusionProps = {
  data: ExecutiveConclusionViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Executive conclusion — lead consulting statement. */
export function ExecutiveConclusion({
  data,
  status = "ready",
  className,
}: ExecutiveConclusionProps) {
  return (
    <section
      className={cx("cui-biz-executive-conclusion", className)}
      aria-label={data.title}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading conclusion",
          emptyTitle: "No conclusion available",
          unavailableTitle: "Conclusion unavailable",
          errorTitle: "Unable to load conclusion",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader
            title={data.title}
            level={2}
            actions={
              data.confidence ? (
                <ConfidenceBadge level={data.confidence} />
              ) : undefined
            }
          />
          <Callout tone="info" title="Executive Conclusion">
            {data.body}
          </Callout>
        </SectionSurface>,
      )}
    </section>
  );
}
