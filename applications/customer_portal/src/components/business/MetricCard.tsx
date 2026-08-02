import {
  InformationBox,
  MetricCard as SharedMetricCard,
  StatusBadge,
} from "../shared";
import type { MetricItemViewModel } from "../../view_models/metrics";
import { cx } from "../../utils";

export type MetricCardProps = {
  data: MetricItemViewModel;
  className?: string;
};

/**
 * Business MetricCard — Pack 06 WP-0007.
 * Composes Shared MetricCard. Presentation values only.
 */
export function MetricCard({ data, className }: MetricCardProps) {
  return (
    <div className={cx("cui-biz-metric-card", className)} data-metric-id={data.id}>
      <SharedMetricCard
        label={data.label}
        value={data.value}
        hint={data.hint ?? data.rangeLabel}
      />
      {data.tone ? <StatusBadge status={data.tone}>{data.tone}</StatusBadge> : null}
      {data.description ? <InformationBox>{data.description}</InformationBox> : null}
    </div>
  );
}
