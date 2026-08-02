import { FooterNote } from "../shared";
import { cx } from "../../utils";

export type SectionTransitionProps = {
  label: string;
  href?: string;
  className?: string;
};

/** Natural transition cue between report sections. */
export function SectionTransition({
  label,
  href,
  className,
}: SectionTransitionProps) {
  return (
    <div className={cx("cui-biz-section-transition", className)} aria-label={label}>
      <FooterNote>
        {href ? <a href={href}>{label}</a> : label}
      </FooterNote>
    </div>
  );
}
