import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseEmptyStateProps = HTMLAttributes<HTMLDivElement> & {
  title?: ReactNode;
  description?: ReactNode;
  action?: ReactNode;
  children?: ReactNode;
};

/** Primitive empty content state. */
export function BaseEmptyState({
  title = "Nothing to show",
  description,
  action,
  className,
  children,
  ...rest
}: BaseEmptyStateProps) {
  return (
    <div className={cx("cui-base-state", className)} data-tone="neutral" {...rest}>
      <p className="cui-base-state__title">{title}</p>
      {description ? <p className="cui-base-state__body">{description}</p> : null}
      {children}
      {action}
    </div>
  );
}
