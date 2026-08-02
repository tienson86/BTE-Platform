import {
  InformationBox,
  MetricGroup,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { MetricSectionViewModel } from "../../view_models/metrics";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { MetricCard } from "./MetricCard";
import { renderPresentationGate } from "./presentationGate";

export type MetricSectionProps = {
  data: MetricSectionViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Grouped metric section (strength, five elements, ten gods, etc.). */
export function MetricSection({
  data,
  status = "ready",
  className,
}: MetricSectionProps) {
  return (
    <section
      className={cx("cui-biz-metric-section", className)}
      aria-label={data.title}
      data-metric-section={data.id}
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
          <SectionHeader title={data.title} level={2} />
          {data.description ? (
            <InformationBox>{data.description}</InformationBox>
          ) : null}
          <MetricGroup stacked>
            {data.metrics.map((metric) => (
              <MetricCard key={metric.id} data={metric} />
            ))}
          </MetricGroup>
        </SectionSurface>,
      )}
    </section>
  );
}
