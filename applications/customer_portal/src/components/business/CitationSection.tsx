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

export type CitationSectionProps = {
  items: AppendixReferenceItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Interpretation / classical citations — prepared only. */
export function CitationSection({
  items,
  title = "Citations",
  status = "ready",
  className,
}: CitationSectionProps) {
  return (
    <section className={cx("cui-biz-citation-section", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading citations",
          emptyTitle: "No citations available",
          unavailableTitle: "Citations unavailable",
          errorTitle: "Unable to load citations",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          <ReferenceBlock title="Interpretation References">
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
