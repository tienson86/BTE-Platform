import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { Card } from "../base/Card";
import { BaseText } from "../base/BaseText";

export type StatCardProps = HTMLAttributes<HTMLElement> & {
  label: ReactNode;
  value: ReactNode;
  hint?: ReactNode;
};

/** WP02 StatCard — compact statistic surface. */
export function StatCard({ label, value, hint, className, ...rest }: StatCardProps) {
  return (
    <Card className={cx("cui-stat-card", className)} {...rest}>
      <BaseText variant="caption" tone="secondary">
        {label}
      </BaseText>
      <BaseText variant="section">{value}</BaseText>
      {hint ? (
        <BaseText variant="metadata" tone="muted">
          {hint}
        </BaseText>
      ) : null}
    </Card>
  );
}
