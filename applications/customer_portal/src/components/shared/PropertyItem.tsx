import type { HTMLAttributes, ReactNode } from "react";
import { BaseText } from "../base";
import { cx } from "../../utils";

export type PropertyItemProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  value: ReactNode;
};

/** Shared property item. */
export function PropertyItem({ label, value, className, ...rest }: PropertyItemProps) {
  return (
    <div className={cx("cui-shared-property-item", className)} {...rest}>
      <BaseText variant="caption" tone="secondary">
        {label}
      </BaseText>
      <BaseText variant="body">{value}</BaseText>
    </div>
  );
}
