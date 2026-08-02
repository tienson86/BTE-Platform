import { LabelValueRow } from "../shared";
import { cx } from "../../utils";

export type NaYinPanelProps = {
  value?: string;
  label?: string;
  className?: string;
};

/** Na Yin panel — presentation label only. */
export function NaYinPanel({
  value,
  label = "Na Yin",
  className,
}: NaYinPanelProps) {
  return (
    <div className={cx("cui-biz-nayin", className)}>
      <LabelValueRow label={label} value={value ?? "Unavailable"} />
    </div>
  );
}
