export const GOLDEN_BASIS_TITLE = "Cơ sở đánh giá";

export const GOLDEN_BASIS_HELPER =
  "Kết quả không chỉ dựa trên số lượng Cát và Hung, mà còn xét cường độ, thứ tự, bộ ba kết hợp và trạng thái phần cuối dãy.";

export const GOLDEN_BASIS_PRINCIPLES = [
  "Dựa trên 8 cặp năng lượng chính.",
  "Dựa trên các bộ ba nổi bật.",
  "Dựa trên dòng Tài vận.",
  "Dựa trên năng lượng kết.",
  "Dựa trên điểm minh họa tĩnh.",
] as const;

export const GOLDEN_BASIS_HIGHLIGHTS = [
  { label: "Trường nổi bật", value: "Diên Niên · Thiên Y · Sinh Khí" },
  { label: "Năng lượng kết", value: "86 · Thiên Y" },
  { label: "Tổng cặp", value: "8 cặp · 7 Cát · 1 Hung" },
] as const;

export const GOLDEN_BASIS_EVIDENCE = [
  { group: "Cặp năng lượng", items: ["32 · Họa Hại", "28 / 82 · Sinh Khí", "27 / 86 · Thiên Y", "78 / 87 / 78 · Diên Niên"] },
  { group: "Bộ ba nổi bật", items: ["827 · Sinh Khí → Thiên Y", "278 · Thiên Y → Diên Niên", "786 · Diên Niên → Thiên Y"] },
  { group: "Điểm minh họa tĩnh", items: ["82 / 100 · TỐT"] },
] as const;
