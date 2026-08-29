/**
 * V1.0 Canonical Portal — primary (top) navigation.
 * Presentation routes only — no business logic.
 */

export type AppNavChild = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
};

export type AppNavItem = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
  readonly children?: readonly AppNavChild[];
};

/** Customer Portal V1 primary destinations (Commercial Dashboard 00_NAVIGATION). */
export const APP_NAV_ITEMS: readonly AppNavItem[] = [
  { id: "home", label: "Trang chủ", href: "/good-date" },
  { id: "choose-date", label: "Chọn ngày tốt", href: "/choose-date" },
  { id: "analyze", label: "Xem lá số", href: "/analyze" },
];

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
  if (normalized === "/" || normalized === "" || normalized === "/good-date" || normalized === "/home") {
    return "home";
  }
  if (normalized === "/choose-date") {
    return "choose-date";
  }
  if (
    normalized === "/analyze" ||
    normalized.startsWith("/analyze") ||
    normalized === "/result" ||
    normalized.startsWith("/result") ||
    normalized === "/interpretation" ||
    normalized === "/result-workspace"
  ) {
    return "analyze";
  }
  const exact = APP_NAV_ITEMS.find((item) => item.href === normalized);
  if (exact) {
    return exact.id;
  }
  return undefined;
}
