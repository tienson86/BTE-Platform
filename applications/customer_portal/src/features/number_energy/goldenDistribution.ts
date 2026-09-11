export type EnergyRole = "primary" | "secondary" | "none";

export type GoldenEnergyCount = {
  label: string;
  count: 0 | 1 | 2 | 3;
  role: EnergyRole;
};

export const GOLDEN_ENERGY_DISTRIBUTION: readonly GoldenEnergyCount[] = [
  { label: "Sinh Khí", count: 2, role: "secondary" },
  { label: "Thiên Y", count: 2, role: "secondary" },
  { label: "Diên Niên", count: 3, role: "primary" },
  { label: "Phục Vị", count: 0, role: "none" },
  { label: "Họa Hại", count: 1, role: "none" },
  { label: "Ngũ Quỷ", count: 0, role: "none" },
  { label: "Lục Sát", count: 0, role: "none" },
  { label: "Tuyệt Mệnh", count: 0, role: "none" },
];

export const ENERGY_COUNT_SCALE = 3;

export const ENERGY_ROLE_LABEL: Record<EnergyRole, string> = {
  primary: "Chủ đạo",
  secondary: "Phụ trợ",
  none: "",
};
