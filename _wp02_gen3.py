from pathlib import Path

ROOT = Path("applications/customer_portal/src/components")

def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(path)

# Fix feedback index
w("feedback/index.ts", '''
/**
 * Feedback layer — foundation boundaries + WP02 feedback components.
 */

export { ErrorBoundary } from "./ErrorBoundary";
export type { ErrorBoundaryProps } from "./ErrorBoundary";

export { LoadingBoundary } from "./LoadingBoundary";
export type { LoadingBoundaryProps } from "./LoadingBoundary";

export { logFoundationError } from "./logFoundationError";

export { Alert } from "./Alert";
export type { AlertProps } from "./Alert";

export { Toast } from "./Toast";
export type { ToastProps, ToastTone } from "./Toast";

export { Dialog } from "./Dialog";
export type { DialogProps } from "./Dialog";

export { Drawer } from "./Drawer";
export type { DrawerProps, DrawerSide } from "./Drawer";

export { Loading } from "./Loading";
export type { LoadingProps } from "./Loading";

export { Skeleton } from "./Skeleton";
export type { SkeletonProps } from "./Skeleton";

export { EmptyState } from "./EmptyState";
export type { EmptyStateProps } from "./EmptyState";

export { ErrorState } from "./ErrorState";
export type { ErrorStateProps } from "./ErrorState";
''')

# ---- NAVIGATION WP02 ----
w("navigation/Tabs.tsx", '''
export { TabPanel as Tabs } from "../shared/TabPanel";
export type { TabPanelProps as TabsProps, TabItem as TabsItem } from "../shared/TabPanel";
''')

w("navigation/Breadcrumb.tsx", '''
export { ReadingBreadcrumb as Breadcrumb } from "./ReadingBreadcrumb";
export type { ReadingBreadcrumbProps as BreadcrumbProps } from "./ReadingBreadcrumb";
''')

w("navigation/Pagination.tsx", '''
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
''')

w("navigation/SidebarItem.tsx", '''
import type { AnchorHTMLAttributes, ButtonHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

type Common = {
  label: ReactNode;
  active?: boolean;
  icon?: ReactNode;
  className?: string;
};

export type SidebarItemLinkProps = Common &
  AnchorHTMLAttributes<HTMLAnchorElement> & { href: string };

export type SidebarItemButtonProps = Common &
  ButtonHTMLAttributes<HTMLButtonElement> & { href?: undefined };

export type SidebarItemProps = SidebarItemLinkProps | SidebarItemButtonProps;

/** WP02 SidebarItem — nav row for sidebar/rail. */
export function SidebarItem(props: SidebarItemProps) {
  const { label, active = false, icon, className } = props;
  const classes = cx("cui-sidebar-item", className);
  if ("href" in props && props.href !== undefined) {
    const { href, label: _l, active: _a, icon: _i, className: _c, ...rest } = props;
    return (
      <a
        href={href}
        className={classes}
        data-active={active || undefined}
        aria-current={active ? "page" : undefined}
        {...rest}
      >
        {icon}
        <span>{label}</span>
      </a>
    );
  }
  const { label: _l2, active: _a2, icon: _i2, className: _c2, ...buttonRest } =
    props as SidebarItemButtonProps;
  return (
    <button
      type="button"
      className={classes}
      data-active={active || undefined}
      aria-current={active ? "page" : undefined}
      {...buttonRest}
    >
      {icon}
      <span>{label}</span>
    </button>
  );
}
''')

w("navigation/Topbar.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type TopbarProps = HTMLAttributes<HTMLElement> & {
  brand?: ReactNode;
  start?: ReactNode;
  end?: ReactNode;
};

/** WP02 Topbar — application header strip. */
export function Topbar({ brand, start, end, className, children, ...rest }: TopbarProps) {
  return (
    <header className={cx("cui-topbar", "cui-top-bar", className)} {...rest}>
      {brand ? <div className="cui-topbar__brand">{brand}</div> : null}
      {start ? <div className="cui-topbar__start">{start}</div> : null}
      <div className="cui-topbar__main">{children}</div>
      {end ? <div className="cui-topbar__end">{end}</div> : null}
    </header>
  );
}
''')

w("navigation/Menu.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

export type MenuProps = HTMLAttributes<HTMLUListElement> & {
  children?: ReactNode;
  label?: string;
};

/** WP02 Menu — semantic menu list container. */
export function Menu({ children, label = "Menu", className, ...rest }: MenuProps) {
  return (
    <ul className={cx("cui-menu", className)} role="menu" aria-label={label} {...rest}>
      {children}
    </ul>
  );
}
''')

w("navigation/Dropdown.tsx", '''
import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton } from "../base/BaseButton";

export type DropdownProps = HTMLAttributes<HTMLDivElement> & {
  label: ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children?: ReactNode;
};

/** WP02 Dropdown — disclosure pattern (caller may control open). */
export function Dropdown({
  label,
  open,
  onOpenChange,
  children,
  className,
  ...rest
}: DropdownProps) {
  const uncontrolled = open === undefined;
  return (
    <div className={cx("cui-dropdown", className)} data-open={open || undefined} {...rest}>
      <BaseButton
        variant="secondary"
        size="sm"
        aria-expanded={open ?? undefined}
        aria-haspopup="menu"
        onClick={() => onOpenChange?.(!(open ?? false))}
      >
        {label}
      </BaseButton>
      {(uncontrolled || open) && children ? (
        <div className="cui-dropdown__panel" role="menu">
          {children}
        </div>
      ) : null}
    </div>
  );
}
''')

# Append to navigation index - rewrite with WP02 exports at end
w("navigation/index.ts", '''
/**
 * Navigation Component Library — WP-0011 + WP02.
 * Composes Shared / Base Components. Presentation only.
 */

export { ReadingNavigation } from "./ReadingNavigation";
export type { ReadingNavigationProps } from "./ReadingNavigation";

export { ReadingRail } from "./ReadingRail";
export type { ReadingRailProps } from "./ReadingRail";

export { TableOfContents as NavigationTableOfContents } from "./TableOfContents";
export type { NavigationTableOfContentsProps } from "./TableOfContents";

export { ScrollSpy as NavigationScrollSpy } from "./ScrollSpy";
export type { NavigationScrollSpyProps } from "./ScrollSpy";

export { ReadingProgress as NavigationReadingProgress } from "./ReadingProgress";
export type { NavigationReadingProgressProps } from "./ReadingProgress";

export { CurrentSection } from "./CurrentSection";
export type { CurrentSectionProps } from "./CurrentSection";

export { JumpNavigator } from "./JumpNavigator";
export type { JumpNavigatorProps } from "./JumpNavigator";

export { AnchorNavigation } from "./AnchorNavigation";
export type { AnchorNavigationProps } from "./AnchorNavigation";

export { BackToTop } from "./BackToTop";
export type { BackToTopProps } from "./BackToTop";

export { ReadingBreadcrumb } from "./ReadingBreadcrumb";
export type { ReadingBreadcrumbProps } from "./ReadingBreadcrumb";

export { PrintNavigator } from "./PrintNavigator";
export type { PrintNavigatorProps } from "./PrintNavigator";

export { Tabs } from "./Tabs";
export type { TabsProps, TabsItem } from "./Tabs";

export { Breadcrumb } from "./Breadcrumb";
export type { BreadcrumbProps } from "./Breadcrumb";

export { Pagination } from "./Pagination";
export type { PaginationProps } from "./Pagination";

export { SidebarItem } from "./SidebarItem";
export type { SidebarItemProps } from "./SidebarItem";

export { Topbar } from "./Topbar";
export type { TopbarProps } from "./Topbar";

export { Menu } from "./Menu";
export type { MenuProps } from "./Menu";

export { Dropdown } from "./Dropdown";
export type { DropdownProps } from "./Dropdown";
''')

w("navigation/README.md", '''
# Navigation Components (WP02)

| Component | Props | Notes |
|-----------|-------|-------|
| Tabs | TabsProps | Alias of TabPanel |
| Breadcrumb | BreadcrumbProps | Alias of ReadingBreadcrumb |
| Pagination | PaginationProps | |
| SidebarItem | SidebarItemProps | Link or button |
| Topbar | TopbarProps | Header strip |
| Menu | MenuProps | role=menu |
| Dropdown | DropdownProps | Host may control open |

Existing reading-navigation components remain exported.
''')

print("nav done")
