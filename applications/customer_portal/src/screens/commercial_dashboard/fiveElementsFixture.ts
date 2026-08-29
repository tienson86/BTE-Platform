/**
 * Phase A visual fixture for Five Elements. Not production content.
 */

import { FIVE_ELEMENTS_HEADING, FIVE_ELEMENTS_TITLE } from "./cards";
import type { FiveElementsView } from "./types";

/** Deterministic sample distribution. Not the production validation case. */
export const FIVE_ELEMENTS_VISUAL_FIXTURE: FiveElementsView = {
  title: FIVE_ELEMENTS_TITLE,
  available: true,
  sectionHeading: FIVE_ELEMENTS_HEADING,
  balanceStatus: "MẤT CÂN BẰNG NHẸ",
  rows: [
    { key: "wood", label: "Mộc", count: 3 },
    { key: "fire", label: "Hỏa", count: 2 },
    { key: "earth", label: "Thổ", count: 4 },
    { key: "metal", label: "Kim", count: 2 },
    { key: "water", label: "Thủy", count: 3 },
  ],
  mostPresent: "Thổ",
  leastPresent: "Hỏa",
  comment:
    "Phân bố cấu trúc cho thấy Thổ xuất hiện nhiều nhất và Hỏa xuất hiện ít nhất. Phân bố Ngũ Hành phản ánh cấu trúc xuất hiện, không trực tiếp quyết định Dụng Thần.",
};
