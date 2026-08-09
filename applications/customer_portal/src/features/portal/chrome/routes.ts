export type PortalRoute =
  | "home"
  | "dashboard"
  | "analyze"
  | "analyze-birth"
  | "analyze-chart"
  | "analyze-progress"
  | "results"
  | "result"
  | "knowledge"
  | "profile"
  | "history"
  | "settings"
  | "help"
  | "about"
  | "onboarding"
  | "complete"
  | "premium"
  | "knowledge-article"
  | "notfound"
  | "error"
  | "loading"
  | "empty";

export type PortalNavItem = {
  readonly id: PortalRoute;
  readonly label: string;
  readonly group: "primary" | "secondary";
  readonly icon:
    | "summary"
    | "recommendation"
    | "chart"
    | "appendix"
    | "knowledge"
    | "status"
    | "technical"
    | "empty"
    | "footer"
    | "warning";
};

export const PORTAL_NAV: readonly PortalNavItem[] = [
  { id: "home", label: "Trang chủ", group: "primary", icon: "summary" },
  { id: "dashboard", label: "Tổng quan", group: "primary", icon: "recommendation" },
  { id: "analyze", label: "Phân tích mới", group: "primary", icon: "chart" },
  { id: "results", label: "Kết quả", group: "primary", icon: "appendix" },
  { id: "knowledge", label: "Kiến thức", group: "primary", icon: "knowledge" },
  { id: "history", label: "Lịch sử", group: "secondary", icon: "appendix" },
  { id: "profile", label: "Hồ sơ", group: "secondary", icon: "status" },
  { id: "settings", label: "Cài đặt", group: "secondary", icon: "technical" },
  { id: "help", label: "Trợ giúp", group: "secondary", icon: "empty" },
  { id: "about", label: "Giới thiệu", group: "secondary", icon: "footer" },
] as const;

export const ROUTE_TITLES: Record<PortalRoute, string> = {
  home: "Trang chủ",
  dashboard: "Tổng quan tư vấn",
  analyze: "Phân tích mới",
  "analyze-birth": "Thông tin ngày sinh",
  "analyze-chart": "Thông tin lá số",
  "analyze-progress": "Đang chuẩn bị tư vấn",
  results: "Danh sách kết quả",
  result: "Xem kết quả",
  knowledge: "Trung tâm kiến thức",
  profile: "Hồ sơ",
  history: "Lịch sử",
  settings: "Cài đặt",
  help: "Trợ giúp",
  about: "Giới thiệu",
  onboarding: "Làm quen với BTE",
  complete: "Đã lưu báo cáo",
  premium: "Tư vấn chuyên sâu",
  "knowledge-article": "Bài kiến thức",
  notfound: "Không tìm thấy trang",
  error: "Không thể hiển thị",
  loading: "Đang tải",
  empty: "Chưa có nội dung",
};

const ALIASES: Record<string, PortalRoute> = {
  "": "home",
  home: "home",
  dashboard: "dashboard",
  analyze: "analyze",
  "analyze/birth": "analyze-birth",
  "analyze/chart": "analyze-chart",
  "analyze/progress": "analyze-progress",
  results: "results",
  reports: "results",
  result: "result",
  knowledge: "knowledge",
  profile: "profile",
  history: "history",
  settings: "settings",
  help: "help",
  about: "about",
  onboarding: "onboarding",
  welcome: "onboarding",
  complete: "complete",
  premium: "premium",
  "knowledge/article": "knowledge-article",
  "404": "notfound",
  notfound: "notfound",
  error: "error",
  loading: "loading",
  empty: "empty",
};

export function parsePortalHash(hash: string): PortalRoute {
  const raw = hash.replace(/^#\/?/, "").split("?")[0]?.replace(/\/+$/, "") ?? "";
  return ALIASES[raw] ?? "notfound";
}

export function portalHref(route: PortalRoute): string {
  const path: Record<PortalRoute, string> = {
    home: "#/home",
    dashboard: "#/dashboard",
    analyze: "#/analyze",
    "analyze-birth": "#/analyze/birth",
    "analyze-chart": "#/analyze/chart",
    "analyze-progress": "#/analyze/progress",
    results: "#/results",
    result: "#/result",
    knowledge: "#/knowledge",
    profile: "#/profile",
    history: "#/history",
    settings: "#/settings",
    help: "#/help",
    about: "#/about",
    onboarding: "#/onboarding",
    complete: "#/complete",
    premium: "#/premium",
    "knowledge-article": "#/knowledge/article",
    notfound: "#/404",
    error: "#/error",
    loading: "#/loading",
    empty: "#/empty",
  };
  return path[route];
}

export type PortalCrumb = {
  id: string;
  label: string;
  href?: string;
  route?: PortalRoute;
};

export function breadcrumbsFor(route: PortalRoute): PortalCrumb[] {
  const home: PortalCrumb = { id: "home", label: "Trang chủ", href: portalHref("home"), route: "home" };
  if (route === "home") return [{ id: "home", label: "Trang chủ" }];
  if (route === "analyze-birth") {
    return [home, { id: "analyze", label: "Phân tích mới", href: portalHref("analyze"), route: "analyze" }, { id: "birth", label: "Ngày sinh" }];
  }
  if (route === "analyze-chart") {
    return [home, { id: "analyze", label: "Phân tích mới", href: portalHref("analyze"), route: "analyze" }, { id: "chart", label: "Lá số" }];
  }
  if (route === "analyze-progress") {
    return [home, { id: "analyze", label: "Phân tích mới", href: portalHref("analyze"), route: "analyze" }, { id: "progress", label: "Tiến trình" }];
  }
  if (route === "result") {
    return [home, { id: "results", label: "Kết quả", href: portalHref("results"), route: "results" }, { id: "result", label: "Xem kết quả" }];
  }
  if (route === "knowledge-article") {
    return [
      home,
      { id: "knowledge", label: "Kiến thức", href: portalHref("knowledge"), route: "knowledge" },
      { id: "knowledge-article", label: "Bài kiến thức" },
    ];
  }
  if (route === "complete") {
    return [home, { id: "result", label: "Kết quả", href: portalHref("result"), route: "result" }, { id: "complete", label: "Đã lưu" }];
  }
  return [home, { id: route, label: ROUTE_TITLES[route] }];
}
