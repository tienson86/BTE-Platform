/**
 * Phase A visual fixture for BaZi Card. Not production content.
 */

import { BAZI_TITLE } from "./cards";
import type { BaziStructureView } from "./types";

/** Deterministic sample structure. Not the production validation case. Not live runtime. */
export const BAZI_VISUAL_FIXTURE: BaziStructureView = {
  title: BAZI_TITLE,
  available: true,
  pillars: [
    {
      key: "year",
      label: "Năm trụ",
      stem: "Giáp",
      stemElement: "Mộc",
      stemYinYang: "Dương",
      branch: "Tý",
      branchElement: "Thủy",
      napAm: "Hải Trung Kim",
      tenGod: "Thiên Ấn",
      hiddenStems: [{ stem: "Quý", element: "Thủy", tenGod: "Chính Ấn" }],
      truongSinh: "Mộ",
      tamHop: "",
      shenSha: [],
      isDayMaster: false,
    },
    {
      key: "month",
      label: "Tháng trụ",
      stem: "Bính",
      stemElement: "Hỏa",
      stemYinYang: "Dương",
      branch: "Dần",
      branchElement: "Mộc",
      napAm: "Lư Trung Hỏa",
      tenGod: "Thất Sát",
      hiddenStems: [
        { stem: "Giáp", element: "Mộc", tenGod: "Kiếp Tài" },
        { stem: "Bính", element: "Hỏa", tenGod: "Thất Sát" },
        { stem: "Mậu", element: "Thổ", tenGod: "Thiên Ấn" },
      ],
      truongSinh: "Trường Sinh",
      tamHop: "",
      shenSha: [],
      isDayMaster: false,
    },
    {
      key: "day",
      label: "Ngày trụ",
      stem: "Mậu",
      stemElement: "Thổ",
      stemYinYang: "Dương",
      branch: "Ngọ",
      branchElement: "Hỏa",
      napAm: "Thiên Hà Thủy",
      tenGod: "Nhật Chủ",
      hiddenStems: [
        { stem: "Đinh", element: "Hỏa", tenGod: "Thiên Tài" },
        { stem: "Kỷ", element: "Thổ", tenGod: "Tỷ Kiên" },
      ],
      truongSinh: "Đế Vượng",
      tamHop: "",
      shenSha: [],
      isDayMaster: true,
    },
    {
      key: "hour",
      label: "Giờ trụ",
      stem: "Canh",
      stemElement: "Kim",
      stemYinYang: "Dương",
      branch: "Thân",
      branchElement: "Kim",
      napAm: "Tuyền Trung Thủy",
      tenGod: "Thực Thần",
      hiddenStems: [
        { stem: "Canh", element: "Kim", tenGod: "Thực Thần" },
        { stem: "Nhâm", element: "Thủy", tenGod: "Thiên Tài" },
        { stem: "Mậu", element: "Thổ", tenGod: "Tỷ Kiên" },
      ],
      truongSinh: "Suy",
      tamHop: "",
      shenSha: [],
      isDayMaster: false,
    },
  ],
};
