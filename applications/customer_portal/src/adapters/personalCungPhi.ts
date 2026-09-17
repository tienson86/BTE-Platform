/**
 * Canonical personal Cung Phi / Mệnh Quái / Hành Cung / Nhóm Trạch.
 *
 * Calendar/Feng Shui personal identity is the source. Per-pillar Ganzhi
 * palaces are technical routing data and must never override gendered Cung Phi.
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
  void firstText(genderHint, person.gender, asRecord(payload.customer).gender);
  const yearPalace = firstText(yearRoute.cung_phi, yearPillar.cung_phi, yearCell.cung_phi);
  const calendarPalace = firstText(calendar.cung_phi, calendar.menh_quai);
  const cungPhi = firstText(
    calendarPalace,
    feng.cung_phi,
    feng.gua_name,
    feng.menh_quai,
    yearPalace,
  );
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
