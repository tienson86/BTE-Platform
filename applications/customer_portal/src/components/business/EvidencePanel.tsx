import {
  EvidenceList,
  EvidenceRow,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { AnalysisEvidenceItemViewModel } from "../../view_models/explainable_analysis";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type EvidencePanelProps = {
  items: AnalysisEvidenceItemViewModel[];
  title?: string;
  status?: PresentationStatus;
  className?: string;
};

/** Evidence panel — displays prepared evidence only. */
export function EvidencePanel({
  items,
  title = "Evidence",
  status = "ready",
  className,
}: EvidencePanelProps) {
  return (
    <section className={cx("cui-biz-evidence-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading evidence",
          emptyTitle: "No evidence available",
          unavailableTitle: "Evidence unavailable",
          errorTitle: "Unable to load evidence",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={3} />
          {items.length === 0 ? (
            <EvidenceList>
              <EvidenceRow label="Unavailable" />
            </EvidenceList>
          ) : (
            <EvidenceList>
              {items.map((item) => (
                <EvidenceRow
                  key={item.id}
                  label={item.label}
                  detail={item.detail}
                  meta={item.meta}
                />
              ))}
            </EvidenceList>
          )}
        </SectionSurface>,
      )}
    </section>
  );
}
