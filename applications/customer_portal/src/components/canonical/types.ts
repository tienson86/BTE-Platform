/**
 * Canonical Tứ Trụ panel contracts.
 * Presentation only — callers supply already-resolved labels.
 */

export type TuTruPillar = {
  canChi: string;
  napAm: string;
  cungPhi: string;
};

export type TuTruPanelProps = {
  year: TuTruPillar;
  month: TuTruPillar;
  day: TuTruPillar;
  hour: TuTruPillar;
  className?: string;
};

export const TU_TRU_TITLE = "TỨ TRỤ";

export const TU_TRU_COLUMNS = ["Can Chi", "Nạp âm", "Cung Phi"] as const;

export const TU_TRU_ROWS = [
  { key: "year", label: "Năm" },
  { key: "month", label: "Tháng" },
  { key: "day", label: "Ngày" },
  { key: "hour", label: "Giờ" },
] as const;

export type TuTruRowKey = (typeof TU_TRU_ROWS)[number]["key"];
