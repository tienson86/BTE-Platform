/**
 * Canonical personal Cung Phi / Mệnh Quái / Hành Cung / Nhóm Trạch.
 *
 * Year-palace routing is the source. Gregorian digit-sum and Feng Shui Gua
 * must not win when they disagree with Tứ Trụ Year Cung for the same man.
 */

const EAST = new Set(["Khảm", "Ly", "Chấn", "Tốn"]);
const WEST = new Set(["Càn", "Khôn", "Cấn", "Đoài"]);
const ELEMENT: Record<string, string> = {
  Khảm: "Thủy",
  Ly: "Hỏa",
  Chấn: "Mộc",
  Tốn: "Mộc",
  Càn: "Kim",
  Khôn: "Thổ",
  Cấn: "Thổ",
  Đoài: "Kim",
};
const FEMALE = new Set(["female", "nu", "nữ", "f", "2", "woman", "girl"]);

export type PersonalCungPhiIdentity = {
  readonly cungPhi: string;
  readonly menhQuai: string;
  readonly hanhCung: string;
  readonly nhomTrach: string;
};

function text(value: unknown): string {
  if (value == null) return "";
  return String(value).trim();
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function firstText(...values: unknown[]): string {
  for (const value of values) {
    const next = text(value);
    if (next) return next;
  }
  return "";
}

function isFemale(gender: string): boolean {
  return FEMALE.has(gender.trim().toLowerCase());
}

export function houseGroupForCung(cung: string): string {
  if (EAST.has(cung)) return "Đông Tứ Trạch";
  if (WEST.has(cung)) return "Tây Tứ Trạch";
  return "";
}

export function elementLabelForCung(cung: string): string {
  return ELEMENT[cung] || "";
}

/**
 * Bind personal Cung Phi from analysis payload. Does not look up palaces.
 */
export function bindPersonalCungPhiIdentity(
  data: Record<string, unknown> | null | undefined,
  genderHint = "",
): PersonalCungPhiIdentity {
  const payload = data ?? {};
  const calendar = asRecord(payload.calendar);
  const feng = asRecord(payload.feng_shui);
  const identity = asRecord(payload.identity);
  const person = asRecord(identity.person);
  const four = asRecord(identity.four_pillars);
  const yearCell = asRecord(four.year);
  const bazi = asRecord(payload.bazi);
  const yearPillar = asRecord(bazi.year_pillar);
  const routing = asRecord(calendar.ganzhi_routing);
  const yearRoute = asRecord(routing.year);
  const gender = firstText(genderHint, person.gender, asRecord(payload.customer).gender);
  const yearPalace = firstText(yearRoute.cung_phi, yearPillar.cung_phi, yearCell.cung_phi);
  const calendarPalace = firstText(calendar.cung_phi, calendar.menh_quai);
  // Male (and unknown) personal identity is the year palace. Stale digit-sum
  // calendar.cung_phi (Tốn for 1987) must not override Tứ Trụ Year Khôn.
  const cungPhi = isFemale(gender)
    ? firstText(calendarPalace, yearPalace, feng.cung_phi, feng.gua_name, feng.menh_quai)
    : firstText(yearPalace, calendarPalace, feng.cung_phi, feng.gua_name, feng.menh_quai);
  const derivedGroup = houseGroupForCung(cungPhi);
  const publishedGroup = firstText(
    calendar.nhom_trach,
    calendar.house_group,
    feng.nhom_trach,
    feng.house_group,
  );
  const nhomTrach = derivedGroup || publishedGroup;
  const hanhCung = firstText(elementLabelForCung(cungPhi), calendar.hanh_cung);
  return {
    cungPhi,
    menhQuai: cungPhi,
    hanhCung,
    nhomTrach,
  };
}
