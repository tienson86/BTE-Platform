/**
 * Canonical Commercial Dashboard card catalog (UI-03 geometry only).
 */

import type { DashboardCardSpec } from "./types";

/** Customer-facing Vietnamese titles in frozen dashboard order. */
export const DASHBOARD_CARDS: readonly DashboardCardSpec[] = [
  { id: "overview", title: "TỔNG QUAN LÁ SỐ", span: 4 },
  { id: "bazi", title: "BÁT TỰ", span: 8 },
  { id: "five-elements", title: "NGŨ HÀNH", span: 4 },
  { id: "ten-gods", title: "THẬP THẦN", span: 4 },
  { id: "pattern", title: "MỆNH CỤC", span: 4 },
  { id: "shensha", title: "THẦN SÁT", span: 6 },
  { id: "luck", title: "ĐẠI VẬN", span: 6 },
  { id: "interpretation", title: "LUẬN GIẢI TỔNG THỂ", span: 12 },
  { id: "action-plan", title: "KẾ HOẠCH HÀNH ĐỘNG", span: 12 },
];

export const RESULT_PAGE_TITLE = "KẾT QUẢ LUẬN GIẢI BÁT TỰ";

export const OVERVIEW_TITLE = "TỔNG QUAN LÁ SỐ";

export const OVERVIEW_SUBTITLE = "Bức tranh tổng thể về lá số của bạn";

export const BAZI_TITLE = "BÁT TỰ";

export const FIVE_ELEMENTS_TITLE = "NGŨ HÀNH";

export const FIVE_ELEMENTS_HEADING = "PHÂN BỐ NGŨ HÀNH";

export const TEN_GODS_TITLE = "THẬP THẦN";

export const PATTERN_TITLE = "MỆNH CỤC";

export const SHENSHA_TITLE = "THẦN SÁT";

export const SHENSHA_FALLBACK_HEADING = "Thần Sát nổi bật";

export const SHENSHA_SUPPORTING_NOTE =
  "Thần Sát là yếu tố bổ trợ và không quyết định toàn bộ lá số.";

export const LUCK_TITLE = "ĐẠI VẬN";

export const INTERPRETATION_TITLE = "LUẬN GIẢI TỔNG THỂ";

export const INTERPRETATION_EMPTY =
  "Chưa đủ dữ liệu để tạo luận giải tổng thể.";

export const INTERPRETATION_ZONE_LABELS = {
  observation: "Quan sát",
  reasoning: "Lý do",
  impact: "Tác động",
  recommendation: "Khuyến nghị",
} as const;

export const INTERPRETATION_LEAD_LABEL = "Tổng quan";

export const INTERPRETATION_CLOSE_LABEL = "Kết luận";

export const ACTION_PLAN_TITLE = "KẾ HOẠCH HÀNH ĐỘNG";

export const ACTION_PLAN_EMPTY = "Chưa có đủ dữ liệu để tạo kế hoạch hành động.";

export const ACTION_PLAN_LABELS = {
  priority: "Ưu tiên hàng đầu",
  actions: "Việc nên làm",
  warnings: "Điều cần lưu ý",
  watch: "Trong giai đoạn hiện tại",
} as const;
