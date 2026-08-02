import {
  ConfidenceBadge,
  EvidenceList,
  EvidenceRow,
  HighlightBox,
  InformationBox,
  SectionHeader,
  SectionSurface,
  StatusBadge,
} from "../shared";
import type { InsightSectionViewModel } from "../../view_models/executive_insight";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { renderPresentationGate } from "./presentationGate";

export type InsightSectionProps = {
  data: InsightSectionViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Single insight domain section (strength, career, etc.). */
export function InsightSection({
  data,
  status = "ready",
  className,
}: InsightSectionProps) {
  return (
    <section
      className={cx("cui-biz-insight-section", className)}
      aria-label={data.title}
      data-insight-id={data.id}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: `Loading ${data.title}`,
          emptyTitle: `${data.title} unavailable`,
          unavailableTitle: `${data.title} unavailable`,
          errorTitle: `Unable to load ${data.title}`,
        },
        <SectionSurface gap="paragraph">
          <SectionHeader
            title={data.title}
            level={3}
            actions={
              <>
                {data.priorityLabel ? (
                  <StatusBadge status={data.tone ?? "info"}>
                    {data.priorityLabel}
                  </StatusBadge>
                ) : null}
                {data.confidence ? (
                  <ConfidenceBadge level={data.confidence} />
                ) : null}
              </>
            }
          />
          <HighlightBox title="Conclusion">{data.summary}</HighlightBox>
          {data.body ? <InformationBox>{data.body}</InformationBox> : null}
          {data.evidence && data.evidence.length > 0 ? (
            <EvidenceList>
              {data.evidence.map((item) => (
                <EvidenceRow
                  key={item.id}
                  label={item.label}
                  detail={item.detail}
                  meta={item.meta}
                />
              ))}
            </EvidenceList>
          ) : null}
        </SectionSurface>,
      )}
    </section>
  );
}
