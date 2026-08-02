import { FooterNote } from "../shared";
import { cx } from "../../utils";

export type PrintFooterProps = {
  note: string;
  className?: string;
};

/** Print-only report footer. */
export function PrintFooter({ note, className }: PrintFooterProps) {
  return (
    <div className={cx("cui-biz-print-footer", className)} aria-hidden="true">
      <FooterNote>{note}</FooterNote>
    </div>
  );
}
