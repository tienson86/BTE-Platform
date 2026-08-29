import type { ReactNode } from "react";
import { cx } from "../../utils";
import { APP_NAV_ITEMS } from "./navItems";

export type PrimaryNavProps = {
  activeId?: string;
  className?: string;
};

/**
 * Canonical top horizontal navigation.
 * Uses existing nav item contract — presentation only.
 */
export function PrimaryNav({
  activeId,
  className,
}: PrimaryNavProps): ReactNode {
  return (
    <nav
      className={cx("cui-primary-nav", className)}
      aria-label="Điều hướng chính"
      data-customer-nav="primary"
    >
      <ul className="cui-primary-nav__list">
        {APP_NAV_ITEMS.map((item) => {
          const active = activeId === item.id;
          if (item.children?.length) {
            return (
              <li key={item.id} className="cui-primary-nav__dropdown">
                <button
                  type="button"
                  className="cui-primary-nav__link"
                  data-active={active || undefined}
                  aria-expanded="false"
                  aria-haspopup="menu"
                >
                  {item.label}
                </button>
                <ul className="cui-primary-nav__menu" role="menu">
                  {item.children.map((child) => (
                    <li key={child.id} role="none">
                      <a
                        href={child.href}
                        className="cui-primary-nav__menu-link"
                        role="menuitem"
                      >
                        {child.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </li>
            );
          }
          return (
            <li key={item.id}>
              <a
                href={item.href}
                className="cui-primary-nav__link"
                data-active={active || undefined}
                aria-current={active ? "page" : undefined}
              >
                {item.label}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
