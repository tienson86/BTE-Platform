import { SectionDivider, SectionHeader, SectionSurface } from "../shared";
import type { AnalysisBlockViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { ConclusionPanel } from "./ConclusionPanel";
import { ConfidencePanel } from "./ConfidencePanel";
import { EvidencePanel } from "./EvidencePanel";
import { ExplanationPanel } from "./ExplanationPanel";
import { KnowledgeReferencePanel } from "./KnowledgeReferencePanel";
import { RecommendationPanel } from "./RecommendationPanel";
import { RuleReferencePanel } from "./RuleReferencePanel";
import { renderPresentationGate } from "./presentationGate";

export type AnalysisSectionProps = {
  data: AnalysisBlockViewModel;
  status?: PresentationStatus;
  className?: string;
};

/**
 * Single analysis block — Pack 06 / Pack 03 explainability contract.
 * Conclusion → Explanation → Evidence → Rule → Confidence → Knowledge → Recommendation
 */
export function AnalysisSection({
  data,
  status = "ready",
  className,
}: AnalysisSectionProps) {
  return (
    <article
      className={cx("cui-biz-analysis-section", className)}
      aria-label={data.title}
      data-analysis-block={data.id}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: `Loading ${data.title}`,
          emptyTitle: `${data.title} unavailable`,
          unavailableTitle: `${data.title} unavailable`,
          errorTitle: `Unable to load ${data.title}`,
        },
        <SectionSurface gap="block" variant="paper">
          <SectionHeader title={data.title} level={2} />
          <SectionDivider />
          <ConclusionPanel data={data.conclusion} />
          <ExplanationPanel data={data.explanation} />
          <EvidencePanel items={data.evidence} />
          <RuleReferencePanel items={data.rules} />
          <ConfidencePanel data={data.confidence} />
          <KnowledgeReferencePanel items={data.knowledge} />
          {data.recommendation ? (
            <RecommendationPanel data={data.recommendation} />
          ) : null}
        </SectionSurface>,
      )}
    </article>
  );
}
