import {
  GlossaryEntry,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AppendixGlossaryEntryViewModel } from "../../view_models/appendix";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type GlossarySectionProps = {
  items: AppendixGlossaryEntryViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Glossary section — prepared terms only. */
export function GlossarySection({
  items,
  title = "Glossary",
  status = "ready",
  className,
}: GlossarySectionProps) {
  return (
    <section className={cx("cui-biz-glossary-section", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading glossary",
          emptyTitle: "No glossary available",
          unavailableTitle: "Glossary unavailable",
          errorTitle: "Unable to load glossary",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          {items.length === 0 ? (
            <GlossaryEntry term="Unavailable" definition="No glossary entries." />
          ) : (
            items.map((item) => (
              <GlossaryEntry
                key={item.id}
                term={item.term}
                definition={item.definition}
              />
            ))
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
