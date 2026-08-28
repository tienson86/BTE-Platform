/**
 * BZ-UI-03 source map — workspace field ownership.
 *
 * Presentation adapter only. No engine ownership.
 *
 * workspace.person            → analysis.customer + calendar + stored input
 * workspace.four_pillars      → calendar.*_can_chi + pillar nayin_element/cung_phi
 * workspace.overview.strength → strength.strength_level / strength_score
 * workspace.overview.useful_god → useful_god (stems/tokens as published)
 * workspace.five_elements     → five_elements.counts (never score.wuxing_score)
 * workspace.ten_gods          → ten_gods / ten_gods_result / bazi.ten_gods
 * workspace.pattern           → pattern.cach_cuc + temperature (Điều hậu)
 * workspace.shensha           → bazi.shensha_matches / bazi.shensha
 * workspace.bone_weight       → bone_weight / can_xuong if published
 * workspace.luck              → luck.current_cycle + luck.cycles
 * workspace.interpretation    → narrative_result sections
 * workspace.conclusion        → narrative_result conclusion (no invented advice)
 */

export const WORKSPACE_SOURCE_MAP = {
  person: "customer + calendar + analyze input",
  four_pillars: "calendar.*_can_chi + bazi.*_pillar identity",
  overview_strength: "strength",
  overview_useful_god: "useful_god",
  overview_score: "score.total_score",
  five_elements: "five_elements",
  ten_gods: "ten_gods | ten_gods_result | bazi.ten_gods",
  pattern: "pattern + temperature",
  shensha: "bazi.shensha_matches | bazi.shensha",
  bone_weight: "bone_weight | can_xuong",
  luck: "luck",
  interpretation: "narrative_result",
  conclusion: "narrative_result conclusion",
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

export const NAYIN_ELEMENT_ONLY = new Set<string>(FIVE_ELEMENT_NAMES);

export const CONFIDENCE_LABELS: Record<string, string> = {
  high: "Cao",
  medium: "Trung bình",
  low: "Thấp",
};

/**
 * PACK 04 / Narrative section titles → workspace four-block labels.
 * Lý giải (canonical section title) maps to Lý do (workspace slot).
 */
export const INTERPRETATION_SECTION_MAP = {
  observe: /quan sát|observation/i,
  reason: /lý giải|lý do|reasoning|explanation/i,
  impact: /tác động|impact/i,
  advice: /khuyến nghị|recommendation/i,
} as const;

export const CONCLUSION_SECTION_MAP = /kết luận|conclusion|closing/i;
