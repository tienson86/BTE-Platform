import type { ReactNode } from "react";
import { cx } from "../../utils";
import { BaseSurface, type BaseSurfaceProps } from "./BaseSurface";

export type CardProps = BaseSurfaceProps & {
  title?: ReactNode;
  footer?: ReactNode;
};

/** WP02 Card — elevated surface container. */
export function Card({
  title,
  footer,
  children,
  className,
  variant = "section",
  ...rest
}: CardProps) {
  return (
    <BaseSurface
      variant={variant}
      className={cx("cui-card", className)}
      data-elevation="soft"
      {...rest}
    >
      {title ? <div className="cui-card__title">{title}</div> : null}
      <div className="cui-card__body">{children}</div>
      {footer ? <div className="cui-card__footer">{footer}</div> : null}
    </BaseSurface>
  );
}
