import { LabelValueRow } from "../shared";
import { cx } from "../../utils";

export type LifeStagePanelProps = {
  value?: string;
  label?: string;
  className?: string;
};

/** Twelve Life Stage panel — presentation label only. */
export function LifeStagePanel({
  value,
  label = "Life Stage",
  className,
}: LifeStagePanelProps) {
  return (
    <div className={cx("cui-biz-life-stage", className)}>
      <LabelValueRow label={label} value={value ?? "Unavailable"} />
    </div>
  );
}
