/**
 * Canonical workspace catalogs — labels only, not calculated results.
 */

export const OVERVIEW_SLOTS = [
  { id: "strength", label: "Thân vượng" },
  { id: "useful-god", label: "Dụng thần" },
  { id: "favorable-god", label: "Hỷ thần" },
  { id: "avoid-god", label: "Kỵ thần" },
] as const;

export const FIVE_ELEMENTS = [
  { id: "wood", name: "Mộc" },
  { id: "fire", name: "Hỏa" },
  { id: "earth", name: "Thổ" },
  { id: "metal", name: "Kim" },
  { id: "water", name: "Thủy" },
] as const;

export const TEN_GODS = [
  "Tỷ Kiên",
  "Kiếp Tài",
  "Thực Thần",
  "Thương Quan",
  "Thiên Tài",
  "Chính Tài",
  "Thất Sát / Thiên Quan",
  "Chính Quan",
  "Thiên Ấn",
  "Chính Ấn",
] as const;

export const SHEN_SHA_NAMES = [
  "Thiên Đức",
  "Nguyệt Đức",
  "Thiên Ất Quý Nhân",
  "Văn Xương",
  "Đào Hoa",
  "Hồng Loan",
  "Hoa Cái",
  "Dịch Mã",
  "Không Vong",
] as const;

export const INTERPRETATION_BLOCKS = [
  { id: "observe", title: "Quan sát" },
  { id: "reason", title: "Lý do" },
  { id: "impact", title: "Tác động" },
  { id: "advice", title: "Khuyến nghị" },
] as const;

export const ACTION_CHIPS = [
  { id: "career", label: "Công việc" },
  { id: "finance", label: "Tài chính" },
  { id: "relation", label: "Quan hệ" },
  { id: "health", label: "Sức khỏe" },
] as const;

export const EMPTY_COPY = "Chờ dữ liệu";
