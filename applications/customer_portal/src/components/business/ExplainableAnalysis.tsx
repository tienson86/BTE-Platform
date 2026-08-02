import { SectionHeader, SectionSurface } from "../shared";
import type { AnalysisBlockViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { AnalysisSection } from "./AnalysisSection";
import { renderPresentationGate } from "./presentationGate";

export type ExplainableAnalysisProps = {
  blocks: AnalysisBlockViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Explainable Analysis workspace — hosts analysis blocks in contract order. */
export function ExplainableAnalysis({
  blocks,
  title = "Explainable Analysis",
  status = "ready",
  className,
}: ExplainableAnalysisProps) {
  return (
    <section
      className={cx("cui-biz-explainable-analysis", className)}
      aria-label={title}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading explainable analysis",
          emptyTitle: "No explainable analysis available",
          unavailableTitle: "Explainable analysis unavailable",
          errorTitle: "Unable to load explainable analysis",
        },
        <SectionSurface gap="section" variant="paper">
          <SectionHeader title={title} level={2} />
          <div className="cui-biz-explainable-analysis__blocks">
            {blocks.map((block) => (
              <AnalysisSection key={block.id} data={block} />
            ))}
          </div>
        </SectionSurface>,
      )}
    </section>
  );
}
