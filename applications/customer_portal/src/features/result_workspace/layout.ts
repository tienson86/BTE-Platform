/**
 * BZ-UI-01 approved panel arrangement on a 10-column workspace grid.
 * Desktop freeze: 6+4 | 4+3+3 | 4+3+3 | 6+4.
 */

import type {
  TuTruSlotPillar,
  WorkspaceNavItem,
  WorkspacePanelSpec,
} from "./types";

export const WORKSPACE_GRID_COLUMNS = 10;

export const WORKSPACE_BREAKPOINTS = {
  mobile: 640,
  tablet: 1024,
} as const;

/** Empty pillar labels — reserved slot, not bound identity. */
export const EMPTY_TU_TRU_PILLAR: TuTruSlotPillar = {
  stem: "",
  branch: "",
  canChi: "",
  napAm: "",
  cungPhi: "",
};

export const WORKSPACE_PANELS: readonly WorkspacePanelSpec[] = [
  { id: "tu-tru", title: "Tứ Trụ", span: 6, kind: "canonical-tu-tru", row: 1 },
  { id: "overview", title: "Tổng quan lá số", span: 4, kind: "canonical-shell", row: 1 },
  { id: "five-elements", title: "Ngũ Hành", span: 4, kind: "canonical-shell", row: 2 },
  { id: "ten-gods", title: "Thập Thần", span: 3, kind: "canonical-shell", row: 2 },
  { id: "destiny", title: "Mệnh Cục", span: 3, kind: "canonical-shell", row: 2 },
  { id: "shen-sha", title: "Thần Sát", span: 4, kind: "canonical-shell", row: 3 },
  { id: "bone-weight", title: "Cân Xương Đoán Mệnh", span: 3, kind: "canonical-shell", row: 3 },
  { id: "luck-cycles", title: "Đại Vận / Lưu Niên", span: 3, kind: "canonical-shell", row: 3 },
  { id: "interpretation", title: "Luận Giải Tổng Thể", span: 6, kind: "canonical-shell", row: 4 },
  { id: "conclusion", title: "Kết Luận & Hành Động", span: 4, kind: "canonical-shell", row: 4 },
];

export const WORKSPACE_TOP_NAV: readonly WorkspaceNavItem[] = [
  { id: "home", label: "Trang chủ", href: "/dashboard" },
  { id: "analysis", label: "Phân tích", href: "/analyze" },
  { id: "result", label: "Kết quả", href: "/result-workspace", active: true },
  { id: "report", label: "Báo cáo", href: "/reports" },
  { id: "history", label: "Lịch sử", href: "/history" },
  { id: "account", label: "Tài khoản", href: "/profile" },
];

export const WORKSPACE_HEADER_SLOTS = [
  { id: "profile", label: "Hồ sơ" },
  { id: "chart-id", label: "Mã lá số" },
  { id: "status", label: "Trạng thái" },
] as const;
