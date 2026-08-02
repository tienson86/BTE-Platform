import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type MetricRowProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  value: ReactNode;
  hint?: ReactNode;
};

/** Shared label/value metric row. */
export function MetricRow({ label, value, hint, className, ...rest }: MetricRowProps) {
  return (
    <div className={cx("cui-shared-metric-row", className)} {...rest}>
      <div>
        <BaseText variant="caption" tone="secondary">
          {label}
        </BaseText>
        {hint ? (
          <BaseText variant="metadata" tone="muted">
            {hint}
          </BaseText>
        ) : null}
      </div>
      <BaseText variant="bodyLarge" className="cui-shared-metric-row__value">
        {value}
      </BaseText>
    </div>
  );
}
