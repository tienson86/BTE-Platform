import {
  CitationRow,
  ReferenceBlock,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AnalysisKnowledgeReferenceViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type KnowledgeReferencePanelProps = {
  items: AnalysisKnowledgeReferenceViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Knowledge reference panel — prepared knowledge citations only. */
export function KnowledgeReferencePanel({
  items,
  title = "Knowledge Reference",
  status = "ready",
  className,
}: KnowledgeReferencePanelProps) {
  return (
    <section
      className={cx("cui-biz-knowledge-reference-panel", className)}
      aria-label={title}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading knowledge references",
          emptyTitle: "No knowledge references available",
          unavailableTitle: "Knowledge references unavailable",
          errorTitle: "Unable to load knowledge references",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={3} />
          <ReferenceBlock title="Related Knowledge">
            {items.length === 0 ? (
              <CitationRow citation="Unavailable" />
            ) : (
              items.map((item) => (
                <CitationRow
                  key={item.id}
                  citation={item.citation}
                  source={item.source}
                />
              ))
            )}
          </ReferenceBlock>
        </SectionSurface>,
      )}
    </section>
  );
}
