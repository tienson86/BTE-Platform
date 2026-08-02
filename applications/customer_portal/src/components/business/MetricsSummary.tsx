import {
  InformationBox,
  MetricGroup,
  SectionHeader,
  SectionSurface,
} from "../shared";
import type { MetricsSummaryViewModel } from "../../view_models/metrics";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { MetricCard } from "./MetricCard";
import { renderPresentationGate } from "./presentationGate";

export type MetricsSummaryProps = {
  data: MetricsSummaryViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Executive metrics summary — narrative lead plus key metrics. */
export function MetricsSummary({
  data,
  status = "ready",
  className,
}: MetricsSummaryProps) {
  const title = data.title ?? "Executive Metrics Summary";

  return (
    <section className={cx("cui-biz-metrics-summary", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading metrics summary",
          emptyTitle: "No metrics summary available",
          unavailableTitle: "Metrics summary unavailable",
          errorTitle: "Unable to load metrics summary",
        },
        <SectionSurface gap="paragraph">
          <SectionHeader title={title} level={2} />
          <InformationBox title="Summary">{data.lead}</InformationBox>
          <MetricGroup stacked>
            {data.items.map((item) => (
              <MetricCard key={item.id} data={item} />
            ))}
          </MetricGroup>
        </SectionSurface>,
      )}
    </section>
  );
}
