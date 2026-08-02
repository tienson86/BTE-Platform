import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type BaseTooltipProps = HTMLAttributes<HTMLSpanElement> & {
  content: ReactNode;
  open?: boolean;
  children: ReactNode;
};

/** Primitive hover/focus tooltip. Presentation only. */
export function BaseTooltip({
  content,
  open,
  className,
  children,
  ...rest
}: BaseTooltipProps) {
  return (
    <span
      className={cx("cui-base-tooltip", className)}
      data-open={open ? "true" : undefined}
      {...rest}
    >
      {children}
      <span className="cui-base-tooltip__content" role="tooltip">
        {content}
      </span>
    </span>
  );
}
