/**
 * Layout barrel — Pack helpers + WP03 App Shell (ADR-004).
 */

export {
  layoutClassNames,
  sectionWidthClass,
  sectionWidthRoles,
} from "./legacy";
export type { LayoutClassName, SectionWidthRole } from "./legacy";

export { AppLayout } from "./AppLayout";
export type { AppLayoutProps } from "./AppLayout";

export { AuthLayout } from "./AuthLayout";
export type { AuthLayoutProps } from "./AuthLayout";

export { BlankLayout } from "./BlankLayout";
export type { BlankLayoutProps } from "./BlankLayout";

export { PageWrapper } from "./PageWrapper";
export type { PageWrapperProps } from "./PageWrapper";

export { Header } from "./Header";
export type { HeaderProps } from "./Header";

export { Sidebar } from "./Sidebar";
export type { SidebarProps } from "./Sidebar";

export { Footer } from "./Footer";
export type { FooterProps } from "./Footer";

export { AppBreadcrumb } from "./Breadcrumb";
export type { AppBreadcrumbItem, AppBreadcrumbProps } from "./Breadcrumb";

export {
  APP_NAV_ITEMS,
  AppNavigation,
  resolveActiveNavId,
} from "./Navigation";
export type { AppNavChild, AppNavItem, AppNavigationProps } from "./Navigation";
