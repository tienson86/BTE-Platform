import type { HTMLAttributes, ReactNode } from "react";
import { BaseHeading, BaseText } from "../base";
import { cx } from "../../utils";

export type SectionHeaderProps = HTMLAttributes<HTMLElement> & {
  title: ReactNode;
  subtitle?: ReactNode;
  actions?: ReactNode;
  level?: 2 | 3 | 4;
};

/** Shared section title row with optional subtitle and actions. */
export function SectionHeader({
  title,
  subtitle,
  actions,
  level = 2,
  className,
  ...rest
}: SectionHeaderProps) {
  return (
    <header className={cx("cui-shared-section-header", className)} {...rest}>
      <div className="cui-shared-section-header__text">
        <BaseHeading level={level}>{title}</BaseHeading>
        {subtitle ? (
          <BaseText variant="caption" tone="secondary">
            {subtitle}
          </BaseText>
        ) : null}
      </div>
      {actions ? <div className="cui-shared-section-header__actions">{actions}</div> : null}
    </header>
  );
}
