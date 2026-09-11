export type GoldenPairCard = {
  digits: string;
  energyLabel: string;
  categoryLabel: "Cát" | "Hung";
  strengthLabel: "Nhẹ" | "Mạnh";
  strengthDots: readonly [boolean, boolean, boolean, boolean];
  keywords: string;
};

export const GOLDEN_PHONE_PAIRS: readonly GoldenPairCard[] = [
  {
    digits: "32",
    energyLabel: "Họa Hại",
    categoryLabel: "Hung",
    strengthLabel: "Nhẹ",
    strengthDots: [true, false, false, false],
    keywords: "Giao tiếp · Khẩu tài",
  },
  {
    digits: "28",
    energyLabel: "Sinh Khí",
    categoryLabel: "Cát",
    strengthLabel: "Nhẹ",
    strengthDots: [true, false, false, false],
    keywords: "Quý nhân · Cơ hội",
  },
  {
    digits: "82",
    energyLabel: "Sinh Khí",
    categoryLabel: "Cát",
    strengthLabel: "Nhẹ",
    strengthDots: [true, false, false, false],
    keywords: "Quý nhân · Cơ hội",
  },
  {
    digits: "27",
    energyLabel: "Thiên Y",
    categoryLabel: "Cát",
    strengthLabel: "Nhẹ",
    strengthDots: [true, false, false, false],
    keywords: "Tài vận · Tài nguyên",
  },
  {
    digits: "78",
    energyLabel: "Diên Niên",
    categoryLabel: "Cát",
    strengthLabel: "Mạnh",
    strengthDots: [true, true, true, false],
    keywords: "Công việc · Năng lực",
  },
  {
    digits: "87",
    energyLabel: "Diên Niên",
    categoryLabel: "Cát",
    strengthLabel: "Mạnh",
    strengthDots: [true, true, true, false],
    keywords: "Công việc · Năng lực",
  },
  {
    digits: "78",
    energyLabel: "Diên Niên",
    categoryLabel: "Cát",
    strengthLabel: "Mạnh",
    strengthDots: [true, true, true, false],
    keywords: "Công việc · Năng lực",
  },
  {
    digits: "86",
    energyLabel: "Thiên Y",
    categoryLabel: "Cát",
    strengthLabel: "Mạnh",
    strengthDots: [true, true, true, false],
    keywords: "Tài vận · Thành quả",
  },
];
