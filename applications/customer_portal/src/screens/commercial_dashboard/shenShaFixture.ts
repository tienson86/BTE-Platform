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
          placement: "Năm · Ngày",
          meaning: "Dễ gặp người hỗ trợ khi khó khăn.",
          category: "Quý Nhân & Hỗ trợ",
        },
        {
          name: "Thiên Đức",
          placement: "Tháng",
          meaning: "Yếu tố hỗ trợ ôn hòa.",
          category: "Quý Nhân & Hỗ trợ",
        },
      ],
    },
    {
      heading: "Học tập & Danh tiếng",
      items: [
        {
          name: "Văn Xương",
          placement: "Giờ",
          meaning: "Nghiên cứu và học thuật.",
          category: "Học tập & Danh tiếng",
        },
      ],
    },
    {
      heading: "Quan hệ & Tình cảm",
      items: [
        {
          name: "Hồng Loan",
          placement: "Năm",
          meaning: "Duyên gặp gỡ đáng chú ý.",
          category: "Quan hệ & Tình cảm",
        },
      ],
    },
    {
      heading: "Di chuyển & Biến động",
      items: [
        {
          name: "Dịch Mã",
          placement: "Ngày",
          meaning: "Biến động môi trường.",
          category: "Di chuyển & Biến động",
        },
      ],
    },
    {
      heading: "Điều cần lưu ý",
      items: [
        {
          name: "Không Vong",
          placement: "Giờ",
          meaning: "Cần xem trong ngữ cảnh tổng thể.",
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
  note: SHENSHA_SUPPORTING_NOTE,
};
