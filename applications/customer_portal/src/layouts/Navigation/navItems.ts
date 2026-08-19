/**
 * V1.0 Canonical Portal — primary (top) navigation.
 * Presentation routes only — no business logic.
 */

export type AppNavItem = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
};

/** Top-bar primary destinations (Canonical Portal UI). */
export const APP_NAV_ITEMS: readonly AppNavItem[] = [
  { id: "dashboard", label: "Trang chủ", href: "/dashboard" },
  { id: "interpretation", label: "Luận giải", href: "/result#interpretation" },
  { id: "result", label: "Kết quả", href: "/result" },
  { id: "reports", label: "Báo cáo", href: "/reports" },
  { id: "history", label: "Lịch sử", href: "/history" },
  { id: "profile", label: "Tài khoản", href: "/profile" },
  { id: "login", label: "Đăng nhập", href: "/login" },
] as const;

export type TocNavItem = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
};

/** Default Result page TOC (MỤC LỤC) — IA Freeze v1.1 (S00 first). */
export const RESULT_TOC_ITEMS: readonly TocNavItem[] = [
  { id: "context", label: "Ngữ cảnh", href: "#ngu-canh" },
  { id: "summary", label: "Tóm tắt", href: "#tom-tat" },
  { id: "overview", label: "Tổng quan", href: "#tong-quan" },
  { id: "pillars", label: "BaZi", href: "#tu-tru" },
  { id: "elements", label: "Phân bố Ngũ hành", href: "#ngu-hanh" },
  { id: "strength", label: "Thân", href: "#than-vuong" },
  { id: "gods", label: "Thập thần", href: "#thap-than" },
  { id: "shensha", label: "Thần sát", href: "#than-sat" },
  { id: "interpretation", label: "Luận giải", href: "#luan-giai" },
  { id: "knowledge", label: "Tri thức", href: "#tri-thuc" },
] as const;

/** Default Dashboard TOC. */
export const DASHBOARD_TOC_ITEMS: readonly TocNavItem[] = [
  { id: "welcome", label: "Tổng quan", href: "#tong-quan" },
  { id: "actions", label: "Thao tác", href: "#thao-tac" },
  { id: "metrics", label: "Chỉ số", href: "#chi-so" },
  { id: "recent", label: "Gần đây", href: "#gan-day" },
  { id: "utility", label: "Tiện ích", href: "#tien-ich" },
] as const;

/** Resolve active primary nav id from a path string. */
export function resolveActiveNavId(pathname: string): string | undefined {
  const normalized = pathname.split("?")[0]?.replace(/\/+$/, "") || "/";
  const exact = APP_NAV_ITEMS.find((item) => item.href === normalized);
  if (exact) {
    return exact.id;
  }
  if (normalized === "/" || normalized === "") {
    return "dashboard";
  }
  if (normalized.startsWith("/analyze")) {
    return "interpretation";
  }
  return APP_NAV_ITEMS.find((item) => normalized.startsWith(item.href))?.id;
}
