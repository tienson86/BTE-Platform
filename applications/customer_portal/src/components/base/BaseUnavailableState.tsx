import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseUnavailableStateProps = HTMLAttributes<HTMLDivElement> & {
  title?: ReactNode;
  description?: ReactNode;
  action?: ReactNode;
  children?: ReactNode;
};

/** Primitive unavailable content state. */
export function BaseUnavailableState({
  title = "Unavailable",
  description,
  action,
  className,
  children,
  ...rest
}: BaseUnavailableStateProps) {
  return (
    <div className={cx("cui-base-state", className)} data-tone="warning" {...rest}>
      <p className="cui-base-state__title">{title}</p>
      {description ? <p className="cui-base-state__body">{description}</p> : null}
      {children}
      {action}
    </div>
  );
}
