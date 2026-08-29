/**
 * Phase A visual fixture for Ten Gods. Not production content.
 */

import { TEN_GODS_TITLE } from "./cards";
import type { TenGodsView } from "./types";

/** Deterministic sample structure. Not the production validation case. */
export const TEN_GODS_VISUAL_FIXTURE: TenGodsView = {
  title: TEN_GODS_TITLE,
  available: true,
  featured: ["Thiên Ấn", "Thất Sát", "Kiếp Tài"],
  visible: [
    { pillar: "year", pillarLabel: "Năm", stem: "Giáp", tenGod: "Thiên Ấn", isDayMaster: false },
    { pillar: "month", pillarLabel: "Tháng", stem: "Ất", tenGod: "Thất Sát", isDayMaster: false },
    { pillar: "day", pillarLabel: "Ngày", stem: "Mậu", tenGod: "Nhật Chủ", isDayMaster: true },
    { pillar: "hour", pillarLabel: "Giờ", stem: "Canh", tenGod: "Kiếp Tài", isDayMaster: false },
  ],
  hidden: [
    { pillar: "year", pillarLabel: "Năm", stem: "Quý", tenGod: "Chính Ấn", isDayMaster: false },
    { pillar: "month", pillarLabel: "Tháng", stem: "Giáp", tenGod: "Thiên Ấn", isDayMaster: false },
    { pillar: "hour", pillarLabel: "Giờ", stem: "Nhâm", tenGod: "Thiên Tài", isDayMaster: false },
  ],
  hiddenNames: ["Thiên Tài", "Thiên Ấn", "Chính Ấn"],
  distribution: [
    { name: "Kiếp Tài", visible: true, hidden: false },
    { name: "Thiên Tài", visible: false, hidden: true },
    { name: "Thất Sát", visible: true, hidden: false },
    { name: "Thiên Ấn", visible: true, hidden: true },
    { name: "Chính Ấn", visible: false, hidden: true },
  ],
  summary: "",
};
