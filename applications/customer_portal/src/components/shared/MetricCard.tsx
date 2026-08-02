import type { HTMLAttributes, ReactNode } from "react";
import { BaseSurface, BaseText } from "../base";
import { cx } from "../../utils";

export type MetricCardProps = HTMLAttributes<HTMLElement> & {
  label: ReactNode;
  value: ReactNode;
  hint?: ReactNode;
};

/** Shared metric card surface. */
export function MetricCard({ label, value, hint, className, ...rest }: MetricCardProps) {
  return (
    <BaseSurface
      as="article"
      variant="section"
      className={cx("cui-shared-metric-card", className)}
      {...rest}
    >
      <BaseText variant="caption" tone="secondary">
        {label}
      </BaseText>
      <BaseText variant="section">{value}</BaseText>
      {hint ? (
        <BaseText variant="metadata" tone="muted">
          {hint}
        </BaseText>
      ) : null}
    </BaseSurface>
  );
}
