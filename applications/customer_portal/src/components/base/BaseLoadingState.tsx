import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseSpinner } from "./BaseSpinner";

export type BaseLoadingStateProps = HTMLAttributes<HTMLDivElement> & {
  title?: ReactNode;
  description?: ReactNode;
  children?: ReactNode;
};

/** Primitive loading state with spinner. */
export function BaseLoadingState({
  title = "Loading",
  description,
  className,
  children,
  ...rest
}: BaseLoadingStateProps) {
  return (
    <div
      className={cx("cui-base-state", className)}
      data-tone="info"
      role="status"
      aria-busy="true"
      {...rest}
    >
      <BaseSpinner label={typeof title === "string" ? title : "Loading"} />
      <p className="cui-base-state__title">{title}</p>
      {description ? <p className="cui-base-state__body">{description}</p> : null}
      {children}
    </div>
  );
}
