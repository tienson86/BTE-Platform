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
      label: "Năm",
      stem: "Giáp",
      stemElement: "Mộc",
      stemYinYang: "Dương",
      branch: "Tý",
      branchElement: "Thủy",
      napAm: "Hải Trung Kim",
      tenGod: "Thiên Ấn",
      hiddenStems: [{ stem: "Quý", tenGod: "Chính Ấn" }],
      truongSinh: "Mộ",
      isDayMaster: false,
    },
    {
      key: "month",
      label: "Tháng",
      stem: "Bính",
      stemElement: "Hỏa",
      stemYinYang: "Dương",
      branch: "Dần",
      branchElement: "Mộc",
      napAm: "Lư Trung Hỏa",
      tenGod: "Thất Sát",
      hiddenStems: [
        { stem: "Giáp", tenGod: "Kiếp Tài" },
        { stem: "Bính", tenGod: "Thất Sát" },
        { stem: "Mậu", tenGod: "Thiên Ấn" },
      ],
      truongSinh: "Trường Sinh",
      isDayMaster: false,
    },
    {
      key: "day",
      label: "Ngày",
      stem: "Mậu",
      stemElement: "Thổ",
      stemYinYang: "Dương",
      branch: "Ngọ",
      branchElement: "Hỏa",
      napAm: "Thiên Hà Thủy",
      tenGod: "Nhật Chủ",
      hiddenStems: [
        { stem: "Đinh", tenGod: "Thiên Tài" },
        { stem: "Kỷ", tenGod: "Tỷ Kiên" },
      ],
      truongSinh: "Đế Vượng",
      isDayMaster: true,
    },
    {
      key: "hour",
      label: "Giờ",
      stem: "Canh",
      stemElement: "Kim",
      stemYinYang: "Dương",
      branch: "Thân",
      branchElement: "Kim",
      napAm: "Tuyền Trung Thủy",
      tenGod: "Thực Thần",
      hiddenStems: [
        { stem: "Canh", tenGod: "Thực Thần" },
        { stem: "Nhâm", tenGod: "Thiên Tài" },
        { stem: "Mậu", tenGod: "Tỷ Kiên" },
      ],
      truongSinh: "Suy",
      isDayMaster: false,
    },
  ],
};
