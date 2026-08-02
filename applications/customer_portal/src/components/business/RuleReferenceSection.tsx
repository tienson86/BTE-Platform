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

export type RuleReferenceSectionProps = {
  items: AppendixReferenceItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Rule references — prepared citations only. */
export function RuleReferenceSection({
  items,
  title = "Rule References",
  status = "ready",
  className,
}: RuleReferenceSectionProps) {
  return (
    <section
      className={cx("cui-biz-rule-reference-section", className)}
      aria-label={title}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading rule references",
          emptyTitle: "No rule references available",
          unavailableTitle: "Rule references unavailable",
          errorTitle: "Unable to load rule references",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          <ReferenceBlock title="Governing Rules">
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
