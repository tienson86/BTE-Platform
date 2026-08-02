import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseTone } from "./types";

export type BaseCalloutProps = HTMLAttributes<HTMLElement> & {
  tone?: BaseTone;
  title?: ReactNode;
  children?: ReactNode;
};

/** Primitive callout / annotation surface. */
export function BaseCallout({
  tone = "neutral",
  title,
  className,
  children,
  ...rest
}: BaseCalloutProps) {
  return (
    <aside
      className={cx("cui-base-callout", className)}
      data-tone={tone}
      {...rest}
    >
      {title ? <p className="cui-base-state__title">{title}</p> : null}
      {children ? <div className="cui-base-state__body">{children}</div> : null}
    </aside>
  );
}
