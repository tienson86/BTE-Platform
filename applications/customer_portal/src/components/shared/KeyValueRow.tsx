import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type KeyValueRowProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  value: ReactNode;
};

/** Shared key/value row. */
export function KeyValueRow({ label, value, className, ...rest }: KeyValueRowProps) {
  return (
    <div className={cx("cui-shared-key-value-row", className)} {...rest}>
      <BaseText variant="caption" tone="secondary">
        {label}
      </BaseText>
      <BaseText variant="body" className="cui-shared-key-value-row__value">
        {value}
      </BaseText>
    </div>
  );
}
