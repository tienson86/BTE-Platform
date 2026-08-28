/**
 * BZ-ID-04A workspace field ownership.
 *
 * Adapter: Identity + Analysis → Workspace View Model.
 * Presentation only. No engine ownership. No frontend identity reconstruction.
 *
 * workspace.person            → identity.person
 * workspace.four_pillars      → identity.four_pillars (year/month/day/hour)
 * workspace.overview.strength → analysis.strength
 * workspace.overview.useful_god → analysis.useful_god
 * workspace.overview.score    → analysis.score
 * workspace.five_elements     → analysis.five_elements
 * workspace.ten_gods          → analysis.ten_gods
 * workspace.pattern           → analysis.pattern + analysis.temperature
 * workspace.shensha           → analysis bazi.shensha (analytical, not identity)
 * workspace.bone_weight       → identity.bone_weight
 * workspace.luck identity     → identity.luck (current cycle / year)
 * workspace.luck.cycles       → analysis.luck.cycles (timeline, not identity)
 * workspace.interpretation ids → identity.interpretation
 * workspace.interpretation body → narrative_result sections by those ids
 * workspace.conclusion        → identity.interpretation.conclusion + action
 */

export const WORKSPACE_SOURCE_MAP = {
  person: "identity.person",
  four_pillars: "identity.four_pillars",
  overview_strength: "analysis.strength",
  overview_useful_god: "analysis.useful_god",
  overview_score: "analysis.score.total_score",
  five_elements: "analysis.five_elements",
  ten_gods: "analysis.ten_gods | ten_gods_result",
  pattern: "analysis.pattern + analysis.temperature",
  shensha: "analysis.bazi.shensha_matches | bazi.shensha",
  bone_weight: "identity.bone_weight",
  luck: "identity.luck (identity fields) + analysis.luck.cycles",
  interpretation: "identity.interpretation ids + narrative_result body",
  conclusion: "identity.interpretation.conclusion + action",
} as const;

/** One owner per identity-backed workspace field. */
export const WORKSPACE_FIELD_OWNERS = {
  "person.name": "identity.person.full_name",
  "person.gender": "identity.person.gender",
  "person.solarDate": "identity.person.solar_birth",
  "person.lunarDate": "identity.person.lunar_birth",
  "person.birthTime": "identity.person.birth_time",
  "person.location": "identity.person.birth_place",
  "person.timezone": "identity.person.timezone",
  "four_pillars.year": "identity.four_pillars.year",
  "four_pillars.month": "identity.four_pillars.month",
  "four_pillars.day": "identity.four_pillars.day",
  "four_pillars.hour": "identity.four_pillars.hour",
  "bone_weight": "identity.bone_weight",
  "luck.current": "identity.luck.current_cycle",
  "luck.ganZhi": "identity.luck.current_cycle_ganzhi",
  "luck.ageRange": "identity.luck.current_cycle_age",
  "luck.currentYear": "identity.luck.current_year",
  "luck.cycles": "analysis.luck.cycles",
  "interpretation.ids": "identity.interpretation",
  "interpretation.body": "narrative_result.sections[id]",
  "conclusion.overall": "identity.interpretation.conclusion",
  "conclusion.action": "identity.interpretation.action",
} as const;

/** Canonical Ten God row names. Aliases preserved centrally. */
export const TEN_GOD_ALIASES: ReadonlyArray<{
  readonly name: string;
  readonly aliases: readonly string[];
}> = [
  { name: "Tỷ Kiên", aliases: ["Tỷ Kiên"] },
  { name: "Kiếp Tài", aliases: ["Kiếp Tài"] },
  { name: "Thực Thần", aliases: ["Thực Thần"] },
  { name: "Thương Quan", aliases: ["Thương Quan"] },
  { name: "Thiên Tài", aliases: ["Thiên Tài"] },
  { name: "Chính Tài", aliases: ["Chính Tài"] },
  {
    name: "Thất Sát / Thiên Quan",
    aliases: ["Thất Sát / Thiên Quan", "Thất Sát", "Thiên Quan"],
  },
  { name: "Chính Quan", aliases: ["Chính Quan"] },
  { name: "Thiên Ấn", aliases: ["Thiên Ấn"] },
  { name: "Chính Ấn", aliases: ["Chính Ấn"] },
];

export const FIVE_ELEMENT_NAMES = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"] as const;

export const CONFIDENCE_LABELS: Record<string, string> = {
  high: "Cao",
  medium: "Trung bình",
  low: "Thấp",
};
