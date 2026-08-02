import { Callout, SectionHeader, SectionSurface } from "../shared";
import type { AnalysisConclusionViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ConclusionPanelProps = {
  data: AnalysisConclusionViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Analytical conclusion panel — presentation only. */
export function ConclusionPanel({
  data,
  status = "ready",
  className,
}: ConclusionPanelProps) {
  return (
    <section
      className={cx("cui-biz-conclusion-panel", className)}
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
          <SectionHeader title={data.title} level={3} />
          <Callout tone="info" title="Conclusion">
            {data.body}
          </Callout>
        </SectionSurface>,
      )}
    </section>
  );
}
