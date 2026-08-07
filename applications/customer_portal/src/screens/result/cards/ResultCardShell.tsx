/**
 * Result Zone Card shell — fixed height from parent row token.
 */

import type { HTMLAttributes, ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import { cx } from "../../../utils";

export type ResultCardShellProps = HTMLAttributes<HTMLElement> & {
  title: string;
  titleId: string;
  hasMore?: boolean;
  footer?: ReactNode;
  children?: ReactNode;
};

/**
 * Analytical report card — height locked by `--rp-row-card-height`.
 */
export function ResultCardShell({
  title,
  titleId,
  hasMore = false,
  footer,
  className,
  children,
  ...rest
}: ResultCardShellProps): ReactNode {
  return (
    <article
      className={cx("rp-card", className)}
      data-has-more={hasMore ? "true" : "false"}
      aria-labelledby={titleId}
      {...rest}
    >
      <PresentationText
        as="h2"
        id={titleId}
        typeRole="title"
        clamp="title"
        className="rp-card__title"
      >
        {title}
      </PresentationText>
      <div className="rp-card__body">{children}</div>
      {footer ? <div className="rp-card__footer">{footer}</div> : null}
    </article>
  );
}
