import {
  GlossaryEntry,
  SectionHeader,
  SectionSurface,
  StatusBadge,
  TagGroup,
} from "../shared";
import type { AppendixTerminologyItemViewModel } from "../../view_models/appendix";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type TerminologySectionProps = {
  items: AppendixTerminologyItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Terminology / abbreviations section — prepared entries only. */
export function TerminologySection({
  items,
  title = "Terminology",
  status = "ready",
  className,
}: TerminologySectionProps) {
  return (
    <section className={cx("cui-biz-terminology-section", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading terminology",
          emptyTitle: "No terminology available",
          unavailableTitle: "Terminology unavailable",
          errorTitle: "Unable to load terminology",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {items.length === 0 ? (
            <GlossaryEntry term="Unavailable" definition="No terminology entries." />
          ) : (
            items.map((item) => (
              <div key={item.id} className="cui-biz-terminology-item">
                {item.abbreviation ? (
                  <TagGroup label={`${item.term} abbreviation`}>
                    <StatusBadge status="neutral">{item.abbreviation}</StatusBadge>
                  </TagGroup>
                ) : null}
                <GlossaryEntry term={item.term} definition={item.definition} />
              </div>
            ))
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
