/**
 * V1.0 Portal navigation items (WP03).
 * Presentation routes only — no business logic.
 */

export type AppNavItem = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
};

export const APP_NAV_ITEMS: readonly AppNavItem[] = [
  { id: "dashboard", label: "Dashboard", href: "/dashboard" },
  { id: "analyze", label: "Lập Lá Số", href: "/analyze" },
  { id: "result", label: "Kết Quả Bát Tự", href: "/result" },
  { id: "interpretation", label: "Luận Giải", href: "/interpretation" },
  { id: "reports", label: "Báo Cáo", href: "/reports" },
  { id: "profile", label: "Hồ Sơ", href: "/profile" },
  { id: "settings", label: "Cài Đặt", href: "/settings" },
] as const;

/** Resolve active nav id from a path string. */
export function resolveActiveNavId(pathname: string): string | undefined {
  const normalized = pathname.split("?")[0]?.replace(/\/+$/, "") || "/";
  const exact = APP_NAV_ITEMS.find((item) => item.href === normalized);
  if (exact) {
    return exact.id;
  }
  if (normalized === "/" || normalized === "") {
    return "dashboard";
  }
  return APP_NAV_ITEMS.find((item) => normalized.startsWith(item.href))?.id;
}
