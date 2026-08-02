import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseErrorStateProps = HTMLAttributes<HTMLDivElement> & {
  title?: ReactNode;
  description?: ReactNode;
  action?: ReactNode;
  children?: ReactNode;
};

/** Primitive error state. */
export function BaseErrorState({
  title = "Something went wrong",
  description,
  action,
  className,
  children,
  ...rest
}: BaseErrorStateProps) {
  return (
    <div
      className={cx("cui-base-state", className)}
      data-tone="danger"
      role="alert"
      {...rest}
    >
      <p className="cui-base-state__title">{title}</p>
      {description ? <p className="cui-base-state__body">{description}</p> : null}
      {children}
      {action}
    </div>
  );
}
