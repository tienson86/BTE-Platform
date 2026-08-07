/**
 * PACK_04 — Equal-height independent card grid.
 */

import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type PresentationGridProps = HTMLAttributes<HTMLDivElement> & {
  /** CSS grid template columns (default: equal flexible columns). */
  columns?: string;
  children?: ReactNode;
};

/**
 * Grid that keeps equal-height independent presentation cards.
 */
export function PresentationGrid({
  columns,
  className,
  style,
  children,
  ...rest
}: PresentationGridProps): ReactNode {
  return (
    <div
      className={cx("ui-presentation-grid", className)}
      data-presentation="pack04"
      data-equal-height="true"
      style={{
        ...style,
        ...(columns ? { gridTemplateColumns: columns } : null),
      }}
      {...rest}
    >
      {children}
    </div>
  );
}

export type PresentationGridCellProps = HTMLAttributes<HTMLDivElement> & {
  /** Optional span hint for 12-column layouts. */
  span?: 2 | 3 | 4 | 12;
  children?: ReactNode;
};

/**
 * Cell wrapper that stretches to equal row height without letting content expand siblings.
 */
export function PresentationGridCell({
  span,
  className,
  children,
  ...rest
}: PresentationGridCellProps): ReactNode {
  return (
    <div
      className={cx(
        "ui-presentation-grid__cell",
        span ? `ui-presentation-grid__cell--${span}` : null,
        className,
      )}
      data-presentation="pack04"
      data-span={span}
      {...rest}
    >
      {children}
    </div>
  );
}
