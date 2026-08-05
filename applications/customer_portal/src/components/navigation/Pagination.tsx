import type { HTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type PaginationProps = HTMLAttributes<HTMLElement> & {
  page: number;
  pageCount: number;
  onPageChange?: (page: number) => void;
  previousLabel?: string;
  nextLabel?: string;
};

/** WP02 Pagination — presentational page controls. */
export function Pagination({
  page,
  pageCount,
  onPageChange,
  previousLabel = "Previous",
  nextLabel = "Next",
  className,
  ...rest
}: PaginationProps) {
  const safeCount = Math.max(1, pageCount);
  const safePage = Math.min(Math.max(1, page), safeCount);
  return (
    <nav
      className={cx("cui-pagination", className)}
      aria-label="Pagination"
      {...rest}
    >
      <BaseButton
        variant="secondary"
        size="sm"
        disabled={safePage <= 1}
        onClick={() => onPageChange?.(safePage - 1)}
      >
        {previousLabel}
      </BaseButton>
      <span className="cui-pagination__status" aria-live="polite">
        {safePage} / {safeCount}
      </span>
      <BaseButton
        variant="secondary"
        size="sm"
        disabled={safePage >= safeCount}
        onClick={() => onPageChange?.(safePage + 1)}
      >
        {nextLabel}
      </BaseButton>
    </nav>
  );
}
