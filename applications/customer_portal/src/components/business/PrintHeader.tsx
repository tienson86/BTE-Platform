import { SectionHeader } from "../shared";
import { cx } from "../../utils";

export type PrintHeaderProps = {
  title: string;
  className?: string;
};

/** Print-only report header. */
export function PrintHeader({ title, className }: PrintHeaderProps) {
  return (
    <div className={cx("cui-biz-print-header", className)} aria-hidden="true">
      <SectionHeader title={title} level={2} />
    </div>
  );
}
