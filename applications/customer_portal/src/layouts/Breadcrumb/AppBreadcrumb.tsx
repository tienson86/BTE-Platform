import type { ReactNode } from "react";
import { cx } from "../../utils";

export type AppBreadcrumbItem = {
  readonly id: string;
  readonly label: string;
  readonly href?: string;
};

export type AppBreadcrumbProps = {
  items: readonly AppBreadcrumbItem[];
  className?: string;
};

/** Application breadcrumb trail for Portal shell (WP03). */
export function AppBreadcrumb({ items, className }: AppBreadcrumbProps): ReactNode {
  if (items.length === 0) {
    return null;
  }
  return (
    <nav className={cx("cui-app-breadcrumb", className)} aria-label="Breadcrumb">
      <ol className="cui-app-breadcrumb__list">
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          return (
            <li key={item.id} className="cui-app-breadcrumb__item">
              {item.href && !isLast ? (
                <a href={item.href}>{item.label}</a>
              ) : (
                <span aria-current={isLast ? "page" : undefined}>{item.label}</span>
              )}
              {!isLast ? <span aria-hidden="true"> / </span> : null}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
