/**
 * Result Page layout primitives — PACK_06 Row / Grid architecture.
 */

import type { CSSProperties, HTMLAttributes, ReactNode } from "react";
import { cx } from "../../../utils";
import { HEIGHT_CLASS_PX, type HeightClass } from "./heightClasses";

export type ResultRowProps = HTMLAttributes<HTMLElement> & {
  /** Official row id (01–07). */
  rowId: "01" | "02" | "03" | "04" | "05" | "06" | "07";
  /** Zone responsibility label. */
  zone: string;
  /** Fixed height class for cards in this row (AUTO = content-driven for reading zones). */
  heightClass?: HeightClass | "AUTO";
  /** Layout gallery pattern id (LP-001 …). */
  pattern?: string;
  children?: ReactNode;
};

/**
 * Independent horizontal row — never influences sibling row height.
 */
export function ResultRow({
  rowId,
  zone,
  heightClass = "M",
  pattern,
  className,
  children,
  ...rest
}: ResultRowProps): ReactNode {
  const heightPx =
    heightClass === "AUTO" ? undefined : HEIGHT_CLASS_PX[heightClass];
  const rowStyle: CSSProperties | undefined = heightPx
    ? ({ ["--rp-row-card-height"]: `${heightPx}px` } as CSSProperties)
    : undefined;

  return (
    <section
      className={cx("rp-row", className)}
      data-result-row={rowId}
      data-zone={zone}
      data-height-class={heightClass}
      data-pattern={pattern}
      data-equal-height={heightClass === "AUTO" ? "false" : "true"}
      style={rowStyle}
      {...rest}
    >
      {children}
    </section>
  );
}

export type ResultGridProps = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
};

/**
 * Official 12-column Result grid (PACK_02).
 */
export function ResultGrid({ className, children, ...rest }: ResultGridProps): ReactNode {
  return (
    <div className={cx("rp-grid", className)} data-grid="12" {...rest}>
      {children}
    </div>
  );
}

export type ResultGridCellProps = HTMLAttributes<HTMLDivElement> & {
  span: 2 | 3 | 4 | 6 | 8 | 12;
  children?: ReactNode;
};

/**
 * Grid cell — equal-height stretch within row; card height locked by row token.
 */
export function ResultGridCell({
  span,
  className,
  children,
  ...rest
}: ResultGridCellProps): ReactNode {
  return (
    <div
      className={cx("rp-grid__cell", `rp-grid__cell--${span}`, className)}
      data-span={span}
      {...rest}
    >
      {children}
    </div>
  );
}
