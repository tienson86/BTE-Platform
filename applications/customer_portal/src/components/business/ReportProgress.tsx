import { ReadingProgress } from "../shared";
import { cx } from "../../utils";

export type ReportProgressProps = {
  value?: number;
  className?: string;
};

/** Report reading progress — presentation value only. */
export function ReportProgress({ value, className }: ReportProgressProps) {
  if (typeof value !== "number") {
    return null;
  }

  return (
    <div className={cx("cui-biz-report-progress", className)} aria-label="Reading Progress">
      <ReadingProgress value={value} />
    </div>
  );
}
