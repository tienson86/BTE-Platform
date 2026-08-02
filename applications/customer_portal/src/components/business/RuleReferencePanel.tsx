import {
  CitationRow,
  ReferenceBlock,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AnalysisRuleReferenceViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type RuleReferencePanelProps = {
  items: AnalysisRuleReferenceViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Rule reference panel — prepared citations only. */
export function RuleReferencePanel({
  items,
  title = "Rule Reference",
  status = "ready",
  className,
}: RuleReferencePanelProps) {
  return (
    <section className={cx("cui-biz-rule-reference-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading rule references",
          emptyTitle: "No rule references available",
          unavailableTitle: "Rule references unavailable",
          errorTitle: "Unable to load rule references",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={3} />
          <ReferenceBlock title="Governing Rules">
            {items.length === 0 ? (
              <CitationRow citation="Unavailable" />
            ) : (
              items.map((item) => (
                <CitationRow
                  key={item.id}
                  citation={item.citation ?? item.label}
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
