/**
 * Dashboard ViewModel types + mock fixture (WP04 / ADR-006).
 * Main flow uses DashboardService → Adapter (TASK_003A).
 * Mock remains for tests and `BTE_DATA_SOURCE=mock` only.
 * Shortcuts / announcement stay static until CMS API exists.
 */

export type DashboardStat = {
  readonly id: string;
  readonly label: string;
  readonly value: string;
  readonly hint?: string;
};

export type DashboardRecentAnalysis = {
  readonly id: string;
  readonly fullName: string;
  readonly createdAt: string;
  readonly status: "ready" | "draft" | "processing";
  readonly href: string;
};

export type DashboardQuickAction = {
  readonly id: string;
  readonly label: string;
  readonly href: string;
};

export type DashboardShortcut = {
  readonly id: string;
  readonly title: string;
  readonly description: string;
  readonly href: string;
};

export type DashboardAnnouncement = {
  readonly id: string;
  readonly title: string;
  readonly body: string;
};

export const DASHBOARD_QUICK_ACTIONS: readonly DashboardQuickAction[] = [
  { id: "new-chart", label: "Lập Lá Số Mới", href: "/analyze" },
  { id: "view-result", label: "Xem Kết Quả", href: "/result" },
  { id: "interpretation", label: "Luận Giải", href: "/interpretation" },
  { id: "reports", label: "Báo Cáo", href: "/reports" },
] as const;

export const DASHBOARD_STATS: readonly DashboardStat[] = [
  { id: "charts", label: "Tổng số lá số", value: "24", hint: "Mock" },
  { id: "analyses", label: "Số lần phân tích", value: "58", hint: "Mock" },
  { id: "reports", label: "Báo cáo đã tạo", value: "12", hint: "Mock" },
  { id: "activity", label: "Hoạt động gần đây", value: "7 ngày", hint: "Mock" },
] as const;

export const DASHBOARD_RECENT: readonly DashboardRecentAnalysis[] = [
  {
    id: "ra-1",
    fullName: "Nguyễn Văn A",
    createdAt: "2026-08-04",
    status: "ready",
    href: "/result?id=ra-1",
  },
  {
    id: "ra-2",
    fullName: "Trần Thị B",
    createdAt: "2026-08-03",
    status: "draft",
    href: "/result?id=ra-2",
  },
  {
    id: "ra-3",
    fullName: "Lê Minh C",
    createdAt: "2026-08-01",
    status: "processing",
    href: "/result?id=ra-3",
  },
] as const;

export const DASHBOARD_SHORTCUTS: readonly DashboardShortcut[] = [
  {
    id: "sc-profile",
    title: "Hồ Sơ",
    description: "Cập nhật thông tin tài khoản.",
    href: "/profile",
  },
  {
    id: "sc-settings",
    title: "Cài Đặt",
    description: "Tuỳ chỉnh giao diện và thông báo.",
    href: "/settings",
  },
] as const;

export const DASHBOARD_ANNOUNCEMENT: DashboardAnnouncement = {
  id: "ann-1",
  title: "Thông báo hệ thống",
  body: "Đây là khu vực thông báo placeholder. Nội dung CMS sẽ được tích hợp sau.",
};
