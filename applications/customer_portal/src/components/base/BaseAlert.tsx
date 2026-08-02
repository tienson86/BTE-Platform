import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseTone } from "./types";

export type BaseAlertProps = HTMLAttributes<HTMLDivElement> & {
  tone?: Exclude<BaseTone, "neutral" | "accent"> | "neutral";
  title?: ReactNode;
  children?: ReactNode;
};

/** Primitive inline alert. */
export function BaseAlert({
  tone = "info",
  title,
  className,
  children,
  ...rest
}: BaseAlertProps) {
  return (
    <div
      className={cx("cui-base-alert", className)}
      data-tone={tone}
      role="alert"
      {...rest}
    >
      {title ? <p className="cui-base-state__title">{title}</p> : null}
      {children ? <div className="cui-base-state__body">{children}</div> : null}
    </div>
  );
}
