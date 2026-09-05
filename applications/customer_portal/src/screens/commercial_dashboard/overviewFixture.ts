/**
 * Phase A visual fixture for Overview. Not production content.
 * Must not be used on the live customer /result path.
 */

import { OVERVIEW_SUBTITLE, OVERVIEW_TITLE } from "./cards";
import type { OverviewView } from "./types";

/** Deterministic presentation-only Overview copy for visual review. */
export const OVERVIEW_VISUAL_FIXTURE: OverviewView = {
  title: OVERVIEW_TITLE,
  subtitle: OVERVIEW_SUBTITLE,
  insight: "Bạn thuộc nhóm Thân vượng, có nội lực tốt và thiên về vai trò dẫn dắt.",
  insightSource: "visual-fixture",
  summary: "",
  summarySource: "visual-fixture",
  conclusion:
    "Đây là lá số có nội lực mạnh. Thành công đến khi biết dùng đúng Hỏa để điều tiết thay vì tiếp tục tăng Kim.",
  conclusionSource: "visual-fixture",
  identity: [
    { key: "day-master", label: "Nhật Chủ", value: "Canh Kim" },
    { key: "strength", label: "Thân", value: "Thân vượng" },
    { key: "pattern", label: "Mệnh Cục", value: "Chính Ấn" },
  ],
  balance: [
    { key: "useful-god", label: "Dụng Thần", value: "Hỏa · Đinh" },
    { key: "favorable-god", label: "Hỷ Thần", value: "Thủy · Nhâm" },
    { key: "avoid-god", label: "Kỵ Thần", value: "Kim · Canh" },
  ],
    focusTitle: "",
    focus: [],
    domainTitle: "",
    domains: [],
  };
