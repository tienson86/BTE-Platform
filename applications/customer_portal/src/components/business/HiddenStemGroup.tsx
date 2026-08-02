import { LabelValueRow, StatusBadge, TagGroup } from "../shared";
import type { HiddenStemItemViewModel } from "../../view_models/four_pillars";
import { cx } from "../../utils";

export type HiddenStemGroupProps = {
  items: HiddenStemItemViewModel[];
  title?: string;
  className?: string;
};

/** Hidden stems group for a pillar. */
export function HiddenStemGroup({
  items,
  title = "Hidden Stems",
  className,
}: HiddenStemGroupProps) {
  if (items.length === 0) {
    return (
      <div className={cx("cui-biz-hidden-stems", className)}>
        <LabelValueRow label={title} value="Unavailable" />
      </div>
    );
  }

  return (
    <div className={cx("cui-biz-hidden-stems", className)}>
      <LabelValueRow label={title} value={`${items.length} stem(s)`} />
      <TagGroup label={title}>
        {items.map((item) => (
          <StatusBadge key={item.id} status="neutral">
            {item.tenGodLabel ? `${item.label} · ${item.tenGodLabel}` : item.label}
          </StatusBadge>
        ))}
      </TagGroup>
    </div>
  );
}
