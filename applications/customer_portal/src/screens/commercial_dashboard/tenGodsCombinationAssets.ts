/**
 * Ten Gods combination knowledge lookup.
 * Reads authored knowledge units. Does not calculate Ten Gods or write copy.
 */

import matrix from "../../../../../knowledge/consulting/ten_gods/combinations/matrix.json";
import hiddenThienTaiChinhAn from "../../../../../knowledge/consulting/ten_gods/combinations/hidden/thien_tai__chinh_an.json";
import tyKienThucThan from "../../../../../knowledge/consulting/ten_gods/combinations/supported/ty_kien__thuc_than.json";
import tyKienChinhTai from "../../../../../knowledge/consulting/ten_gods/combinations/supported/ty_kien__chinh_tai.json";
import kiepTaiThuongQuan from "../../../../../knowledge/consulting/ten_gods/combinations/supported/kiep_tai__thuong_quan.json";
import kiepTaiThienTai from "../../../../../knowledge/consulting/ten_gods/combinations/supported/kiep_tai__thien_tai.json";
import kiepTaiThatSat from "../../../../../knowledge/consulting/ten_gods/combinations/supported/kiep_tai__that_sat.json";
import thucThanThuongQuan from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuc_than__thuong_quan.json";
import thucThanThienTai from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuc_than__thien_tai.json";
import thucThanChinhTai from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuc_than__chinh_tai.json";
import thucThanChinhQuan from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuc_than__chinh_quan.json";
import thucThanThienAn from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuc_than__thien_an.json";
import thucThanThuongQuanChinhQuan from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuc_than__thuong_quan__chinh_quan.json";
import thuongQuanThienTai from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thuong_quan__thien_tai.json";
import thienTaiChinhTai from "../../../../../knowledge/consulting/ten_gods/combinations/supported/thien_tai__chinh_tai.json";
import chinhTaiChinhQuan from "../../../../../knowledge/consulting/ten_gods/combinations/supported/chinh_tai__chinh_quan.json";
import chinhTaiChinhAn from "../../../../../knowledge/consulting/ten_gods/combinations/supported/chinh_tai__chinh_an.json";
import thatSatThienAn from "../../../../../knowledge/consulting/ten_gods/combinations/supported/that_sat__thien_an.json";
import chinhQuanChinhAn from "../../../../../knowledge/consulting/ten_gods/combinations/supported/chinh_quan__chinh_an.json";
import kiepTaiThatSatThienAn from "../../../../../knowledge/consulting/ten_gods/combinations/supported/kiep_tai__that_sat__thien_an.json";

const TRADITIONAL_ORDER = [
  "Tỷ Kiên",
  "Kiếp Tài",
  "Thực Thần",
  "Thương Quan",
  "Thiên Tài",
  "Chính Tài",
  "Thất Sát",
  "Chính Quan",
  "Thiên Ấn",
  "Chính Ấn",
] as const;

export type TenGodCombinationAsset = {
  readonly title: string;
  readonly insight: string;
  readonly capability: string;
  readonly income: string;
  readonly career: string;
  readonly leadership: string;
  readonly growth: string;
  readonly risk: string;
  readonly recommendation: string;
};

export type TenGodCombinationCatalogEntry = {
  readonly members: readonly string[];
  readonly title: string;
};

export type TenGodCombinationStatus =
  | "SUPPORTED"
  | "DUPLICATE"
  | "LOW_VALUE"
  | "CONFLICTING"
  | "NOT_CUSTOMER_SAFE"
  | "DEFERRED"
  | "UNKNOWN";

export type TenGodCombinationClassification = {
  readonly members: readonly string[];
  readonly status: TenGodCombinationStatus;
  readonly reason: string;
};

type KnowledgeUnit = {
  readonly status: string;
  readonly members: readonly string[];
  readonly title: string;
  readonly executive_insight: string;
  readonly capability: string;
  readonly income_model: string;
  readonly career_model: string;
  readonly management_style: string;
  readonly growth_model: string;
  readonly risk_model: string;
  readonly recommendation: string;
};

type MatrixPair = {
  readonly key: string;
  readonly status: string;
  readonly reason: string;
};

const UNITS: readonly KnowledgeUnit[] = [
  tyKienThucThan,
  tyKienChinhTai,
  kiepTaiThuongQuan,
  kiepTaiThienTai,
  kiepTaiThatSat,
  thucThanThuongQuan,
  thucThanThienTai,
  thucThanChinhTai,
  thucThanChinhQuan,
  thucThanThienAn,
  thucThanThuongQuanChinhQuan,
  thuongQuanThienTai,
  thienTaiChinhTai,
  chinhTaiChinhQuan,
  chinhTaiChinhAn,
  thatSatThienAn,
  chinhQuanChinhAn,
  kiepTaiThatSatThienAn,
];

function comboKey(names: readonly string[]): string {
  return names.join("|");
}

function orderedNames(names: readonly string[]): string[] {
  const present = new Set(
    names.map((name) => name.trim()).filter((name) => name && name !== "Nhật Chủ"),
  );
  return TRADITIONAL_ORDER.filter((name) => present.has(name));
}

function asAsset(unit: KnowledgeUnit): TenGodCombinationAsset {
  return {
    title: unit.title,
    insight: unit.executive_insight,
    capability: unit.capability,
    income: unit.income_model,
    career: unit.career_model,
    leadership: unit.management_style,
    growth: unit.growth_model,
    risk: unit.risk_model,
    recommendation: unit.recommendation,
  };
}

const COMBOS: Readonly<Record<string, TenGodCombinationAsset>> = Object.fromEntries(
  UNITS.filter((unit) => unit.status === "SUPPORTED").map((unit) => [
    comboKey(unit.members),
    asAsset(unit),
  ]),
);

const PAIR_ROWS = (matrix.pairs as readonly MatrixPair[]).map((row) => [row.key, row] as const);
const PAIR_BY_KEY = new Map<string, MatrixPair>(PAIR_ROWS);

/**
 * Published combination library. Lookup only. Does not calculate Ten Gods.
 */
export function listTenGodCombinationCatalog(): readonly TenGodCombinationCatalogEntry[] {
  return Object.keys(COMBOS).map((key) => ({
    members: key.split("|"),
    title: COMBOS[key]?.title ?? "",
  }));
}

/**
 * Classify a published visible set. Does not author copy.
 */
export function classifyTenGodCombination(
  names: readonly string[],
): TenGodCombinationClassification {
  const ordered = orderedNames(names);
  if (ordered.length < 2) {
    return { members: ordered, status: "UNKNOWN", reason: "Need at least two visible role gods." };
  }
  if (COMBOS[comboKey(ordered)]) {
    return { members: ordered, status: "SUPPORTED", reason: "Authored knowledge unit." };
  }
  if (ordered.length === 2) {
    const row = PAIR_BY_KEY.get(comboKey(ordered));
    if (row) {
      return {
        members: ordered,
        status: row.status as TenGodCombinationStatus,
        reason: row.reason,
      };
    }
    return { members: ordered, status: "UNKNOWN", reason: "Members are not in the Ten Gods set." };
  }
  return {
    members: ordered,
    status: "DEFERRED",
    reason: "Triple is not an authored model. Use the strongest supported pair plus remaining single-god cards.",
  };
}

/**
 * Copy combination consulting for a published visible set. Omits when no supported unit exists.
 */
export function tenGodCombinationAsset(
  names: readonly string[],
): (TenGodCombinationAsset & { readonly members: readonly string[] }) | null {
  const ordered = orderedNames(names);
  if (ordered.length < 2) return null;
  const exact = COMBOS[comboKey(ordered)];
  if (exact) return { ...exact, members: ordered };
  let bestKey = "";
  let bestLen = 1;
  for (const key of Object.keys(COMBOS)) {
    const members = key.split("|");
    if (members.length <= bestLen) continue;
    if (members.every((name) => ordered.includes(name))) {
      bestKey = key;
      bestLen = members.length;
    }
  }
  if (!bestKey) return null;
  const asset = COMBOS[bestKey];
  return asset ? { ...asset, members: bestKey.split("|") } : null;
}

const HIDDEN_SUPPORT: Readonly<Record<string, string>> = {
  [comboKey(hiddenThienTaiChinhAn.members)]: hiddenThienTaiChinhAn.support_line,
};

/**
 * Quiet support copy for a published hidden set. Does not replace the visible model.
 */
export function tenGodHiddenCombinationSupport(names: readonly string[]): string {
  const ordered = orderedNames(names);
  if (ordered.length < 2) return "";
  const exact = HIDDEN_SUPPORT[comboKey(ordered)];
  if (exact) return exact;
  for (const key of Object.keys(HIDDEN_SUPPORT)) {
    const members = key.split("|");
    if (members.length >= 2 && members.every((name) => ordered.includes(name))) {
      return HIDDEN_SUPPORT[key] ?? "";
    }
  }
  return "";
}
