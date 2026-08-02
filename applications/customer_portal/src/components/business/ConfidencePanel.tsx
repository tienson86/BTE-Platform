import {
  ConfidenceBadge,
  InformationBox,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { ConfidencePanelViewModel } from "../../view_models/metrics";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { MetricIndicator } from "./MetricIndicator";
import { renderPresentationGate } from "./presentationGate";

export type ConfidencePanelProps = {
  data: ConfidencePanelViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Confidence indicators panel — presentation only. */
export function ConfidencePanel({
  data,
  status = "ready",
  className,
}: ConfidencePanelProps) {
  const title = data.title ?? "Confidence Indicators";

  return (
    <section className={cx("cui-biz-confidence-panel", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading confidence indicators",
          emptyTitle: "No confidence indicators available",
          unavailableTitle: "Confidence indicators unavailable",
          errorTitle: "Unable to load confidence indicators",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader
            title={title}
            level={2}
            actions={<ConfidenceBadge level={data.level} />}
          />
          {data.summary ? (
            <InformationBox title="Confidence Summary">{data.summary}</InformationBox>
          ) : null}
          {data.items && data.items.length > 0 ? (
            <div className="cui-biz-confidence-panel__items">
              {data.items.map((item) => (
                <MetricIndicator key={item.id} data={item} />
              ))}
            </div>
          ) : null}
        </SectionSurface>,
      )}
    </section>
  );
}
