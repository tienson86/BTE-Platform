import type { ReactNode } from "react";
import { cx } from "../../utils";
import { AppNavigation } from "../Navigation/AppNavigation";

export type SidebarProps = {
  activeId?: string;
  collapsed?: boolean;
  open?: boolean;
  onNavigate?: () => void;
  onClose?: () => void;
  className?: string;
};

/** Application sidebar / drawer navigation (WP03). */
export function Sidebar({
  activeId,
  collapsed = false,
  open = false,
  onNavigate,
  onClose,
  className,
}: SidebarProps): ReactNode {
  return (
    <>
      {open ? (
        <button
          type="button"
          className="cui-app-sidebar-backdrop"
          aria-label="Đóng menu điều hướng"
          onClick={onClose}
        />
      ) : null}
      <aside
        className={cx("cui-app-sidebar", className)}
        aria-label="Thanh điều hướng"
        data-collapsed={collapsed || undefined}
        data-open={open || undefined}
      >
        <div className="cui-app-sidebar__brand">
          <span className="cui-app-sidebar__brand-text">
            {collapsed ? "BTE" : "BTE Portal"}
          </span>
        </div>
        <AppNavigation
          activeId={activeId}
          collapsed={collapsed}
          onNavigate={onNavigate}
        />
      </aside>
    </>
  );
}
