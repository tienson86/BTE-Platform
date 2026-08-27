/**
 * Date Selection presentation types (frontend adapter / view-model).
 */

export type SixStateVm = {
  remainder: number;
  code: string;
  label: string;
};

export type TrachVm = {
  cung: string;
  element_code: string;
  element_label: string;
  trach_group_code: string;
  trach_group_label: string;
};

export type CalendarCellVm = {
  solar_year: number;
  solar_month: number;
  solar_day: number;
  lunar_day: number;
  lunar_month: number;
  weekday: number;
  six_state: SixStateVm;
};

export type KeSlotVm = {
  ke_index: number;
  time_range: string;
  six_state: SixStateVm;
};

export type HourVm = {
  window: { branch: string; time_range: string };
  ganzhi: string;
  six_state: SixStateVm;
  trach: TrachVm | null;
  ke_slots: KeSlotVm[];
};

export type DayVm = {
  calendar: {
    solar_label: string;
    lunar_label: string;
    year_ganzhi: string;
    day_ganzhi: string;
  };
  six_state: SixStateVm;
  trach: TrachVm | null;
  hours: HourVm[];
};

export type PersonVm = {
  full_name: string;
  gender_label: string;
  solar_label: string;
  lunar_label: string;
  ganzhi: string;
  trach: TrachVm;
};

export type RankedDateVm = {
  day: DayVm;
  recommendations: Array<{ time_range: string; primary: boolean }>;
};

export const DATE_SELECTION_NAV = [
  { id: "good-date", label: "Xem ngày tốt/xấu", href: "/good-date" },
  { id: "choose-date", label: "Chọn ngày tốt", href: "/choose-date" },
] as const;

export const HOUR_BRANCHES = [
  "Tý",
  "Sửu",
  "Dần",
  "Mão",
  "Thìn",
  "Tỵ",
  "Ngọ",
  "Mùi",
  "Thân",
  "Dậu",
  "Tuất",
  "Hợi",
] as const;

export const CLOCK_NUMBERS = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] as const;
