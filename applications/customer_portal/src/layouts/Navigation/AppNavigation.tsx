import type { ReactNode } from "react";
import { SidebarItem } from "../../components/navigation/SidebarItem";
import { cx } from "../../utils";
import { APP_NAV_ITEMS } from "./navItems";

export type AppNavigationProps = {
  activeId?: string;
  collapsed?: boolean;
  onNavigate?: () => void;
  className?: string;
};

/** Portal primary navigation list (WP03). */
export function AppNavigation({
  activeId,
  collapsed = false,
  onNavigate,
  className,
}: AppNavigationProps): ReactNode {
  return (
    <nav
      className={cx("cui-app-nav", className)}
      aria-label="Điều hướng chính"
      data-collapsed={collapsed || undefined}
    >
      <ul className="cui-app-nav__list">
        {APP_NAV_ITEMS.map((item) => (
          <li key={item.id}>
            <SidebarItem
              href={item.href}
              label={collapsed ? item.label.charAt(0) : item.label}
              title={item.label}
              active={activeId === item.id}
              onClick={onNavigate}
            />
          </li>
        ))}
      </ul>
    </nav>
  );
}
