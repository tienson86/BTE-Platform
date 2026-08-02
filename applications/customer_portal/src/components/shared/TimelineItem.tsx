import type { LiHTMLAttributes, ReactNode } from "react";
import { BaseStack, BaseText } from "../base";
import { cx } from "../../utils";

export type TimelineItemProps = LiHTMLAttributes<HTMLLIElement> & {
  title: ReactNode;
  description?: ReactNode;
  meta?: ReactNode;
  children?: ReactNode;
};

/** Shared timeline item. */
export function TimelineItem({
  title,
  description,
  meta,
  className,
  children,
  ...rest
}: TimelineItemProps) {
  return (
    <li className={cx("cui-shared-timeline-item", className)} {...rest}>
      <BaseStack gap="inline">
        <BaseText variant="subsection">{title}</BaseText>
        {meta ? (
          <BaseText variant="metadata" tone="muted">
            {meta}
          </BaseText>
        ) : null}
        {description ? (
          <BaseText variant="body" tone="secondary">
            {description}
          </BaseText>
        ) : null}
        {children}
      </BaseStack>
    </li>
  );
}
