/**
 * Shared grid cell for Desktop Row containers.
 * Fixed 12-column spans — no auto-flow / masonry.
 */

import type { ReactNode } from "react";

export type RowSpan = 2 | 3 | 4 | 12;

/**
 * Places one section inside a row-owned 12-column grid.
 */
export function RowGridCell({
  span,
  mapping,
  children,
}: {
  span: RowSpan;
  mapping: string;
  children: ReactNode;
}): ReactNode {
  return (
    <div
      className={`cd-row-cell cd-row-cell--${span}`}
      data-component={mapping}
      data-span={span}
    >
      {children}
    </div>
  );
}
