import type { ReactNode } from "react";
import { StickyReadingRail } from "../../components/shared";
import { useTheme } from "../../theme";
import { cx } from "../../utils";
import type { TocNavItem } from "../Navigation/navItems";
import { RESULT_TOC_ITEMS } from "../Navigation/navItems";

export type SidebarProps = {
  /** @deprecated App routes moved to Header PrimaryNav — kept for compat. */
  activeId?: string;
  tocItems?: readonly TocNavItem[];
  tocTitle?: string;
  tocActiveId?: string;
  collapsed?: boolean;
  open?: boolean;
  onNavigate?: () => void;
  onClose?: () => void;
  className?: string;
};

/**
 * Canonical sidebar — page Table of Contents (MỤC LỤC).
 * Primary app destinations live in Header.
 */
export function Sidebar({
  tocItems = RESULT_TOC_ITEMS,
  tocTitle = "MỤC LỤC",
  tocActiveId,
  collapsed = false,
  open = false,
  onClose,
  className,
}: SidebarProps): ReactNode {
  const { mode, toggleMode } = useTheme();

  return (
    <>
      {open ? (
        <button
          type="button"
          className="cui-app-sidebar-backdrop"
          aria-label="Đóng mục lục"
          onClick={onClose}
        />
      ) : null}
      <aside
        className={cx("cui-app-sidebar", className)}
        aria-label={tocTitle}
        data-collapsed={collapsed || undefined}
        data-open={open || undefined}
      >
        <StickyReadingRail
          className="cui-app-toc"
          title={collapsed ? "Mục" : tocTitle}
          items={tocItems.map((item) => ({
            id: item.id,
            label: collapsed ? item.label.charAt(0) : item.label,
            href: item.href,
            active: tocActiveId === item.id,
          }))}
        />
        {!collapsed ? (
          <div className="cui-app-sidebar__footer">
            <button
              type="button"
              className="cui-app-sidebar__theme"
              onClick={toggleMode}
            >
              {mode === "dark" ? "Giao diện tối" : "Giao diện sáng"}
            </button>
            <p className="cui-app-sidebar__version">BTE Platform v1.0.0</p>
          </div>
        ) : null}
      </aside>
    </>
  );
}
