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
    >
      <ul className="cui-primary-nav__list">
        {APP_NAV_ITEMS.map((item) => {
          const active = activeId === item.id;
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
