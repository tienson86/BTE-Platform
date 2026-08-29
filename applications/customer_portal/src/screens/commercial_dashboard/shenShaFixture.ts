/**
 * Phase A visual fixture for ShenSha. Not production content.
 */

import { SHENSHA_SUPPORTING_NOTE, SHENSHA_TITLE } from "./cards";
import type { ShenShaGroupView, ShenShaView } from "./types";

const VISUAL_GROUPS: readonly ShenShaGroupView[] = [
    {
      heading: "Quý Nhân & Hỗ trợ",
      items: [
        {
          name: "Thiên Ất Quý Nhân",
          placement: "Trụ Năm · Trụ Ngày",
          meaning: "Dễ gặp người hỗ trợ khi khó khăn.",
          chartRelevance: "Xuất hiện tại trụ Năm · Ngày.",
          evidence: "",
          category: "Quý Nhân & Hỗ trợ",
        },
        {
          name: "Thiên Đức",
          placement: "Trụ Tháng",
          meaning: "Yếu tố hỗ trợ ôn hòa.",
          chartRelevance: "Xuất hiện tại trụ Tháng.",
          evidence: "",
          category: "Quý Nhân & Hỗ trợ",
        },
      ],
    },
    {
      heading: "Học tập & Danh tiếng",
      items: [
        {
          name: "Văn Xương",
          placement: "Trụ Giờ",
          meaning: "Nghiên cứu và học thuật.",
          chartRelevance: "Xuất hiện tại trụ Giờ.",
          evidence: "",
          category: "Học tập & Danh tiếng",
        },
      ],
    },
    {
      heading: "Quan hệ & Tình cảm",
      items: [
        {
          name: "Hồng Loan",
          placement: "Trụ Năm",
          meaning: "Duyên gặp gỡ đáng chú ý.",
          chartRelevance: "Xuất hiện tại trụ Năm.",
          evidence: "",
          category: "Quan hệ & Tình cảm",
        },
      ],
    },
    {
      heading: "Di chuyển & Biến động",
      items: [
        {
          name: "Dịch Mã",
          placement: "Trụ Ngày",
          meaning: "Biến động môi trường.",
          chartRelevance: "Xuất hiện tại trụ Ngày.",
          evidence: "",
          category: "Di chuyển & Biến động",
        },
      ],
    },
    {
      heading: "Điều cần lưu ý",
      items: [
        {
          name: "Không Vong",
          placement: "Trụ Giờ",
          meaning: "Cần xem trong ngữ cảnh tổng thể.",
          chartRelevance: "Xuất hiện tại trụ Giờ.",
          evidence: "",
          category: "Điều cần lưu ý",
        },
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
};
