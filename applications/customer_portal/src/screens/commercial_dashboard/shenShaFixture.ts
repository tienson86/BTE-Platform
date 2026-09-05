/**
 * Phase A visual fixture for ShenSha. Not production content.
 */

import { SHENSHA_SUPPORTING_NOTE, SHENSHA_TITLE } from "./cards";
import type { ShenShaGroupView, ShenShaItemView, ShenShaView } from "./types";

function sample(
  name: string,
  placement: string,
  meaning: string,
  chartRelevance: string,
  category: string,
): ShenShaItemView {
  return {
    name,
    placement,
    meaning,
    chartRelevance,
    evidence: "",
    category,
    stateLabel: "",
    explanation: "",
  };
}

const VISUAL_GROUPS: readonly ShenShaGroupView[] = [
  {
    heading: "Quý Nhân & Hỗ trợ",
    items: [
      sample(
        "Thiên Ất Quý Nhân",
        "Trụ Năm · Trụ Ngày",
        "Dễ gặp người hỗ trợ khi khó khăn.",
        "Xuất hiện tại trụ Năm · Ngày.",
        "Quý Nhân & Hỗ trợ",
      ),
      sample(
        "Thiên Đức",
        "Trụ Tháng",
        "Yếu tố hỗ trợ ôn hòa.",
        "Xuất hiện tại trụ Tháng.",
        "Quý Nhân & Hỗ trợ",
      ),
    ],
  },
  {
    heading: "Học tập & Danh tiếng",
    items: [
      sample(
        "Văn Xương",
        "Trụ Giờ",
        "Nghiên cứu và học thuật.",
        "Xuất hiện tại trụ Giờ.",
        "Học tập & Danh tiếng",
      ),
    ],
  },
  {
    heading: "Quan hệ & Tình cảm",
    items: [
      sample(
        "Hồng Loan",
        "Trụ Năm",
        "Duyên gặp gỡ đáng chú ý.",
        "Xuất hiện tại trụ Năm.",
        "Quan hệ & Tình cảm",
      ),
    ],
  },
  {
    heading: "Di chuyển & Biến động",
    items: [
      sample(
        "Dịch Mã",
        "Trụ Ngày",
        "Biến động môi trường.",
        "Xuất hiện tại trụ Ngày.",
        "Di chuyển & Biến động",
      ),
    ],
  },
  {
    heading: "Điều cần lưu ý",
    items: [
      sample(
        "Không Vong",
        "Trụ Giờ",
        "Cần xem trong ngữ cảnh tổng thể.",
        "Xuất hiện tại trụ Giờ.",
        "Điều cần lưu ý",
      ),
    ],
  },
];

/** Deterministic grouped sample. Not a production category map. */
export const SHENSHA_VISUAL_FIXTURE: ShenShaView = {
  title: SHENSHA_TITLE,
  available: true,
  grouped: true,
  groups: VISUAL_GROUPS,
  items: VISUAL_GROUPS.flatMap((group) => group.items),
  summary: "",
  note: `Lưu ý: ${SHENSHA_SUPPORTING_NOTE}`,
  usePack07: false,
  ecosystem: null,
};
