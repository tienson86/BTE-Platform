import { LabelValueRow, StatusBadge } from "../shared";
import type { HeavenlyStemCellViewModel } from "../../view_models/four_pillars";
import { cx } from "../../utils";

export type HeavenlyStemCellProps = {
  data: HeavenlyStemCellViewModel;
  className?: string;
};

/** Heavenly Stem cell — presentation only. */
export function HeavenlyStemCell({ data, className }: HeavenlyStemCellProps) {
  const value = data.symbol ? `${data.symbol} · ${data.label}` : data.label;

  return (
    <div className={cx("cui-biz-stem-cell", className)}>
      <LabelValueRow label="Heavenly Stem" value={value} />
      {data.elementLabel ? (
        <StatusBadge status="neutral">{data.elementLabel}</StatusBadge>
      ) : null}
      {data.tenGodLabel ? (
        <StatusBadge status="info">{data.tenGodLabel}</StatusBadge>
      ) : null}
    </div>
  );
}
