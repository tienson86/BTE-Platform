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
