import { LabelValueRow, StatusBadge } from "../shared";
import type { MetricIndicatorViewModel } from "../../view_models/metrics";
import { cx } from "../../utils";

export type MetricIndicatorProps = {
  data: MetricIndicatorViewModel;
  className?: string;
};

/** Single supporting metric indicator — presentation only. */
export function MetricIndicator({ data, className }: MetricIndicatorProps) {
  return (
    <div
      className={cx("cui-biz-metric-indicator", className)}
      data-indicator-id={data.id}
    >
      <LabelValueRow label={data.label} value={data.value} />
      {data.statusLabel ? (
        <StatusBadge status={data.tone ?? "info"}>{data.statusLabel}</StatusBadge>
      ) : null}
    </div>
  );
}
