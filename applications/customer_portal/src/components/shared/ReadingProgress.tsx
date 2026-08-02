import type { HTMLAttributes } from "react";
import { BaseProgress, BaseText } from "../base";
import { cx } from "../../utils";

export type ReadingProgressProps = HTMLAttributes<HTMLDivElement> & {
  value: number;
  max?: number;
  label?: string;
};

/** Shared reading progress indicator. Presentation value only. */
export function ReadingProgress({
  value,
  max = 100,
  label = "Reading progress",
  className,
  ...rest
}: ReadingProgressProps) {
  return (
    <div className={cx("cui-shared-reading-progress", className)} {...rest}>
      <BaseText variant="metadata" tone="muted">
        {label}
      </BaseText>
      <BaseProgress value={value} max={max} label={label} />
    </div>
  );
}
