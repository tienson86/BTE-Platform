import { LabelValueRow, StatusBadge } from "../shared";
import type { EarthlyBranchCellViewModel } from "../../view_models/four_pillars";
import { cx } from "../../utils";

export type EarthlyBranchCellProps = {
  data: EarthlyBranchCellViewModel;
  className?: string;
};

/** Earthly Branch cell — presentation only. */
export function EarthlyBranchCell({ data, className }: EarthlyBranchCellProps) {
  const value = data.symbol ? `${data.symbol} · ${data.label}` : data.label;

  return (
    <div className={cx("cui-biz-branch-cell", className)}>
      <LabelValueRow label="Earthly Branch" value={value} />
      {data.animalLabel ? (
        <StatusBadge status="neutral">{data.animalLabel}</StatusBadge>
      ) : null}
      {data.elementLabel ? (
        <StatusBadge status="neutral">{data.elementLabel}</StatusBadge>
      ) : null}
    </div>
  );
}
