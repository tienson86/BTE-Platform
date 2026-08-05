import type { HTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseProgress } from "../base/BaseProgress";
import { BaseText } from "../base/BaseText";

export type ScoreBarProps = HTMLAttributes<HTMLDivElement> & {
  label?: string;
  value: number;
  max?: number;
};

/** WP02 ScoreBar — labeled progress/score meter. */
export function ScoreBar({
  label,
  value,
  max = 100,
  className,
  ...rest
}: ScoreBarProps) {
  const clamped = Math.max(0, Math.min(value, max));
  return (
    <div className={cx("cui-score-bar", className)} {...rest}>
      {label ? (
        <div className="cui-score-bar__header">
          <BaseText variant="caption">{label}</BaseText>
          <BaseText variant="metadata" tone="muted">
            {clamped}/{max}
          </BaseText>
        </div>
      ) : null}
      <BaseProgress value={clamped} max={max} />
    </div>
  );
}
