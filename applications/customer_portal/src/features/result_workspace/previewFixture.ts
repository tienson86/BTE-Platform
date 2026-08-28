/**
 * Isolated BZ-UI-02 preview fixture.
 *
 * Presentation-only demo values for visual QA (`?preview=1` or React `preview`).
 * Not engine output. Not runtime analysis. Not production user results.
 */

import type { TuTruSlotPillar } from "./types";

export const PREVIEW_FIXTURE_KIND = "bz-ui-02-preview-only";

export const PREVIEW_TU_TRU: Record<"year" | "month" | "day" | "hour", TuTruSlotPillar> = {
  year: { stem: "Bính", branch: "Ngọ", canChi: "Bính Ngọ", napAm: "Thủy", cungPhi: "Khảm" },
  month: { stem: "Bính", branch: "Thân", canChi: "Bính Thân", napAm: "Hỏa", cungPhi: "Khôn" },
  day: { stem: "Đinh", branch: "Sửu", canChi: "Đinh Sửu", napAm: "Thủy", cungPhi: "Chấn" },
  hour: { stem: "Ất", branch: "Tỵ", canChi: "Ất Tỵ", napAm: "Hỏa", cungPhi: "Khôn" },
};

export const PREVIEW_OVERVIEW = {
  strength: "Thân vượng",
  usefulGod: "Tỷ Kiên",
  favorableGod: "Thực Thần",
  avoidGod: "Thất Sát",
  score: 78,
  scoreMax: 100,
  confidence: "Cao",
} as const;

export const PREVIEW_FIVE_ELEMENTS = {
  wood: 22,
  fire: 18,
  earth: 24,
  metal: 16,
  water: 20,
  observation: "Bản xem trước — chưa phải kết quả phân tích.",
} as const;

export const PREVIEW_TEN_GODS: Record<string, number> = {
  "Tỷ Kiên": 18,
  "Kiếp Tài": 8,
  "Thực Thần": 14,
  "Thương Quan": 6,
  "Thiên Tài": 10,
  "Chính Tài": 12,
  "Thất Sát / Thiên Quan": 7,
  "Chính Quan": 9,
  "Thiên Ấn": 11,
  "Chính Ấn": 5,
};

export const PREVIEW_DESTINY = {
  pattern: "Kiến Lộc dụng Thực",
  climate: "Điều hậu Trung hòa",
  summary: "Khung cấu trúc xem trước — không phải cách cục máy.",
  quality: "Ổn",
} as const;

export const PREVIEW_SHEN_SHA: Record<string, string> = {
  "Thiên Đức": "Có",
  "Nguyệt Đức": "Có",
  "Thiên Ất Quý Nhân": "Có",
  "Văn Xương": "Không",
  "Đào Hoa": "Có",
  "Hồng Loan": "Không",
  "Hoa Cái": "Có",
  "Dịch Mã": "Không",
  "Không Vong": "Có",
};

export const PREVIEW_BONE_WEIGHT = {
  amount: "4 lượng 8 chỉ",
  stars: 4,
  classification: "Thượng cách",
  preview: "Đoạn xem trước — chưa tính cân xương.",
} as const;

export const PREVIEW_LUCK = {
  current: "Đại vận hiện tại",
  ageRange: "32–41",
  ganzhi: "Nhâm Thân",
  year: "2026",
  observation: "Mốc xem trước — không tính vận hạn.",
} as const;

export const PREVIEW_INTERPRETATION: Record<string, string> = {
  executive: "Khối Tổng quan chờ luận giải.",
  observe: "Khối Quan sát chờ luận giải.",
  reason: "Khối Lý do chờ luận giải.",
  impact: "Khối Tác động chờ luận giải.",
  advice: "Khối Khuyến nghị chờ luận giải.",
  summary: "Khối Tóm tắt chờ luận giải.",
};

export const PREVIEW_CONCLUSION = {
  summary: "Tóm tắt xem trước — chưa phải kết luận thật.",
  overall: "Kết luận xem trước — chưa phải khuyến nghị thật.",
} as const;
