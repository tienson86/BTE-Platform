import { InformationBox, SectionHeader, SectionSurface } from "../shared";
import type { AnalysisExplanationViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type ExplanationPanelProps = {
  data: AnalysisExplanationViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Explanation / reasoning panel — prepared narrative only. */
export function ExplanationPanel({
  data,
  status = "ready",
  className,
}: ExplanationPanelProps) {
  const title = data.title ?? "Explanation";

  return (
    <section className={cx("cui-biz-explanation-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading explanation",
          emptyTitle: "No explanation available",
          unavailableTitle: "Explanation unavailable",
          errorTitle: "Unable to load explanation",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={3} />
          {data.paragraphs.map((paragraph, index) => (
            <InformationBox key={`explanation-${index}`}>{paragraph}</InformationBox>
          ))}
        </SectionSurface>,
      )}
    </section>
  );
}
