import {
  CitationRow,
  ReferenceBlock,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AppendixReferenceItemViewModel } from "../../view_models/appendix";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type KnowledgeReferenceSectionProps = {
  items: AppendixReferenceItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Knowledge references — prepared citations only. */
export function KnowledgeReferenceSection({
  items,
  title = "Knowledge References",
  status = "ready",
  className,
}: KnowledgeReferenceSectionProps) {
  return (
    <section
      className={cx("cui-biz-knowledge-reference-section", className)}
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
          <SectionHeader title={title} level={2} />
          <ReferenceBlock title="Knowledge Sources">
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
