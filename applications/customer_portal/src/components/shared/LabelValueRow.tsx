import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type LabelValueRowProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  value: ReactNode;
};

/** Shared generic label/value row. */
export function LabelValueRow({ label, value, className, ...rest }: LabelValueRowProps) {
  return (
    <div className={cx("cui-shared-label-value-row", className)} {...rest}>
      <BaseText variant="caption" tone="secondary">
        {label}
      </BaseText>
      <BaseText variant="body" className="cui-shared-label-value-row__value">
        {value}
      </BaseText>
    </div>
  );
}
