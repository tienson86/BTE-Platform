/** Traditional BaZi display knowledge for the Visual Chart (rule tables only). */

export type ElementId = "Wood" | "Fire" | "Earth" | "Metal" | "Water";
export type YinYang = "yang" | "yin";

export type StemInfo = {
  id: string;
  element: ElementId;
  yin_yang: YinYang;
};

export type BranchInfo = {
  id: string;
  element: ElementId;
  yin_yang: YinYang;
  season: string;
  hidden: string[];
};

export const STEM_INFO: Record<string, StemInfo> = {
  Giáp: { id: "Giáp", element: "Wood", yin_yang: "yang" },
  Ất: { id: "Ất", element: "Wood", yin_yang: "yin" },
  Bính: { id: "Bính", element: "Fire", yin_yang: "yang" },
  Đinh: { id: "Đinh", element: "Fire", yin_yang: "yin" },
  Mậu: { id: "Mậu", element: "Earth", yin_yang: "yang" },
  Kỷ: { id: "Kỷ", element: "Earth", yin_yang: "yin" },
  Canh: { id: "Canh", element: "Metal", yin_yang: "yang" },
  Tân: { id: "Tân", element: "Metal", yin_yang: "yin" },
  Nhâm: { id: "Nhâm", element: "Water", yin_yang: "yang" },
  Quý: { id: "Quý", element: "Water", yin_yang: "yin" },
};

export const BRANCH_INFO: Record<string, BranchInfo> = {
  Tý: { id: "Tý", element: "Water", yin_yang: "yang", season: "Winter", hidden: ["Quý"] },
  Sửu: {
    id: "Sửu",
    element: "Earth",
    yin_yang: "yin",
    season: "Winter",
    hidden: ["Kỷ", "Quý", "Tân"],
  },
  Dần: {
    id: "Dần",
    element: "Wood",
    yin_yang: "yang",
    season: "Spring",
    hidden: ["Giáp", "Bính", "Mậu"],
  },
  Mão: { id: "Mão", element: "Wood", yin_yang: "yin", season: "Spring", hidden: ["Ất"] },
  Thìn: {
    id: "Thìn",
    element: "Earth",
    yin_yang: "yang",
    season: "Spring",
    hidden: ["Mậu", "Ất", "Quý"],
  },
  Tỵ: {
    id: "Tỵ",
    element: "Fire",
    yin_yang: "yin",
    season: "Summer",
    hidden: ["Bính", "Mậu", "Canh"],
  },
  Ngọ: {
    id: "Ngọ",
    element: "Fire",
    yin_yang: "yang",
    season: "Summer",
    hidden: ["Đinh", "Kỷ"],
  },
  Mùi: {
    id: "Mùi",
    element: "Earth",
    yin_yang: "yin",
    season: "Summer",
    hidden: ["Kỷ", "Đinh", "Ất"],
  },
  Thân: {
    id: "Thân",
    element: "Metal",
    yin_yang: "yang",
    season: "Autumn",
    hidden: ["Canh", "Nhâm", "Mậu"],
  },
  Dậu: { id: "Dậu", element: "Metal", yin_yang: "yin", season: "Autumn", hidden: ["Tân"] },
  Tuất: {
    id: "Tuất",
    element: "Earth",
    yin_yang: "yang",
    season: "Autumn",
    hidden: ["Mậu", "Tân", "Đinh"],
  },
  Hợi: {
    id: "Hợi",
    element: "Water",
    yin_yang: "yin",
    season: "Winter",
    hidden: ["Nhâm", "Giáp"],
  },
};

/** Stem → companion branch fallback when chart has no branches. */
export const DEFAULT_BRANCH_FOR_STEM: Record<string, string> = {
  Giáp: "Dần",
  Ất: "Mão",
  Bính: "Ngọ",
  Đinh: "Tỵ",
  Mậu: "Thìn",
  Kỷ: "Sửu",
  Canh: "Thân",
  Tân: "Dậu",
  Nhâm: "Hợi",
  Quý: "Tý",
};

export const ELEMENT_ORDER: ElementId[] = [
  "Wood",
  "Fire",
  "Earth",
  "Metal",
  "Water",
];

export const ELEMENT_COLOR: Record<ElementId, { fill: string; stroke: string }> = {
  Wood: { fill: "#1f7a5c", stroke: "#145c44" },
  Fire: { fill: "#c45c3e", stroke: "#9b3b2f" },
  Earth: { fill: "#c4a35a", stroke: "#8b7340" },
  Metal: { fill: "#7a8790", stroke: "#4f5b63" },
  Water: { fill: "#3b6ea5", stroke: "#2a4f78" },
};

const STEM_CYCLE = [
  "Giáp",
  "Ất",
  "Bính",
  "Đinh",
  "Mậu",
  "Kỷ",
  "Canh",
  "Tân",
  "Nhâm",
  "Quý",
] as const;

const TEN_GOD_NAMES = [
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

/**
 * Resolve Ten God of `other` stem relative to day master.
 * Same polarity → even index in generation cycle; opposite → odd.
 */
export function tenGodOf(dayMaster: string, other: string): string {
  const dm = STEM_CYCLE.indexOf(dayMaster as (typeof STEM_CYCLE)[number]);
  const ot = STEM_CYCLE.indexOf(other as (typeof STEM_CYCLE)[number]);
  if (dm < 0 || ot < 0) return "—";
  const dmEl = Math.floor(dm / 2);
  const otEl = Math.floor(ot / 2);
  const relation = (otEl - dmEl + 5) % 5;
  const samePolarity = dm % 2 === ot % 2;
  const index = relation * 2 + (samePolarity ? 0 : 1);
  return TEN_GOD_NAMES[index] ?? "—";
}

export const BRANCH_CLASH: Record<string, string> = {
  Tý: "Ngọ",
  Ngọ: "Tý",
  Sửu: "Mùi",
  Mùi: "Sửu",
  Dần: "Thân",
  Thân: "Dần",
  Mão: "Dậu",
  Dậu: "Mão",
  Thìn: "Tuất",
  Tuất: "Thìn",
  Tỵ: "Hợi",
  Hợi: "Tỵ",
};

export const BRANCH_COMBINATION_TRIADS: string[][] = [
  ["Dần", "Ngọ", "Tuất"],
  ["Tỵ", "Dậu", "Sửu"],
  ["Thân", "Tý", "Thìn"],
  ["Hợi", "Mão", "Mùi"],
];

export const PILLAR_KEYS = ["year", "month", "day", "hour"] as const;
export type PillarKey = (typeof PILLAR_KEYS)[number];

export const PILLAR_LABELS: Record<PillarKey, string> = {
  year: "Year",
  month: "Month",
  day: "Day",
  hour: "Hour",
};
