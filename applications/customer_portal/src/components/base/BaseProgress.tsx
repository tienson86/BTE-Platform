import type { HTMLAttributes } from "react";
import { cx } from "../../utils";

export type BaseProgressProps = HTMLAttributes<HTMLDivElement> & {
  value: number;
  max?: number;
  label?: string;
};

/** Primitive determinate progress bar. */
export function BaseProgress({
  value,
  max = 100,
  label = "Progress",
  className,
  ...rest
}: BaseProgressProps) {
  const clamped = Math.max(0, Math.min(value, max));
  const percent = max === 0 ? 0 : (clamped / max) * 100;
  return (
    <div
      className={cx("cui-base-progress", className)}
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={clamped}
      {...rest}
    >
      <div className="cui-base-progress__bar" style={{ width: `${percent}%` }} />
    </div>
  );
}
