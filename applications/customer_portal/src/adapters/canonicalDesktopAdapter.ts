/**
 * Analysis API → Canonical Desktop ViewModel.
 * Calendar / BaZi / Pattern / Score / Strength / Interpretation / Report / Feng Shui.
 */

import { canonicalGender } from "./genderDisplay";
import type { AnalysisDataDto, AnalyzeChartRequest, PillarDto } from "../models";
import {
  CANONICAL_DESKTOP_MOCK,
  type CanonicalDesktopMock,
} from "../screens/canonical_desktop/mockData";
import {
  UNAVAILABLE_CONCLUSION,
  commercialOrUnavailable,
  extractInterpretationSections,
  findSectionBody,
  firstCommercialSnippet,
} from "./contentGuards";
import {
  canonicalStrengthLabel,
  canonicalStrengthMeterPercent,
  formatCanonicalStrengthScore,
  readCanonicalStrengthScore,
} from "./canonicalStrength";
import {
  FIVE_ELEMENT_ROWS,
  FIVE_ELEMENTS_TITLE,
  canonicalFiveElementCounts,
  fiveElementAbsentLabel,
  fiveElementUnitTotal,
  formatFiveElementsCompact,
  formatFiveElementsProvenance,
  publishedFiveElementsMethodNote,
} from "./canonicalFiveElements";
import {
  canonicalFavorableDisplay,
  canonicalClimatePreferenceLabel,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
  canonicalUsefulShortReason,
  canonicalUnfavorableDisplay,
} from "./canonicalUsefulGod";
import {
  asTenGodsPayload,
  hiddenLabels,
  hiddenLinesForPillar,
  tenGodLabel,
  tenGodsNote,
  visibleLabels,
} from "./tenGodsDisplay";
import { shenShaEntriesFromAnalysis } from "./canonicalShenSha";
import {
  patternCustomerLine,
  strengthCustomerSummary,
  stripInternalRuleIds,
  temperatureCustomerLine,
  tenGodsProminenceFromAnalysis,
} from "./customerFacingPresentation";
import {
  asNarrativeResult,
  careerFieldText,
  careerSelectionFromNarrative,
  executiveFromNarrative,
  hasUsableNarrativeResult,
  paragraphByRole,
  primaryRecommendationFromNarrative,
  promotionFieldText,
  promotionReadinessFromNarrative,
  recommendationActions,
  secondaryMilestoneFromNarrative,
  sectionParagraphTexts,
  summaryText,
  type NarrativeResultDto,
} from "./narrativeResultAdapter";

export type CanonicalDesktopStatus = "ready" | "loading" | "error" | "empty";

/**
 * Widen deep fixture literals to runtime-safe primitives.
 * Mock uses `as const`; ViewModels must accept API-derived strings/numbers.
 */
type WidenLiterals<T> = T extends string
  ? string
  : T extends number
    ? number
    : T extends boolean
      ? boolean
      : T extends readonly (infer U)[]
        ? ReadonlyArray<WidenLiterals<U>>
        : T extends object
          ? { readonly [K in keyof T]: WidenLiterals<T[K]> }
          : T;

export type CanonicalDesktopViewModel = {
  readonly header: WidenLiterals<CanonicalDesktopMock["header"]>;
  readonly sidebar: WidenLiterals<CanonicalDesktopMock["sidebar"]>;
  readonly s00: WidenLiterals<CanonicalDesktopMock["s00"]>;
  readonly s01: WidenLiterals<CanonicalDesktopMock["s01"]>;
  readonly s02: WidenLiterals<CanonicalDesktopMock["s02"]>;
  readonly s03: WidenLiterals<CanonicalDesktopMock["s03"]>;
  readonly s04: WidenLiterals<CanonicalDesktopMock["s04"]>;
  readonly s05: WidenLiterals<CanonicalDesktopMock["s05"]>;
  readonly s06: WidenLiterals<CanonicalDesktopMock["s06"]>;
  readonly s07: WidenLiterals<CanonicalDesktopMock["s07"]>;
  readonly s08: WidenLiterals<CanonicalDesktopMock["s08"]>;
  readonly s09: WidenLiterals<CanonicalDesktopMock["s09"]>;
  readonly s10: WidenLiterals<CanonicalDesktopMock["s10"]>;
  readonly s11: WidenLiterals<CanonicalDesktopMock["s11"]>;
  readonly footer: WidenLiterals<CanonicalDesktopMock["footer"]>;
  readonly source: "api" | "mock";
  readonly status: CanonicalDesktopStatus;
  readonly statusMessage?: string;
  /** Pack 05 official commercial narrative (preferred over legacy interpretation). */
  readonly narrativeResult?: NarrativeResultDto | null;
  /** Composed commercial consulting. Customer fields only; ids stay internal. */
  readonly commercialConsulting?: CommercialConsultingView | null;
};

export type CommercialConsultingSectionView = {
  readonly domain: string;
  readonly title: string;
  readonly summary: string;
  readonly meaning: readonly string[];
  readonly recommendations: readonly string[];
  /** Internal trace. Knowledge cards must not render this. */
  readonly sourceUnitIds: readonly string[];
};

export type CommercialConsultingView = {
  readonly visible: boolean;
  readonly status: string;
  readonly sections: readonly CommercialConsultingSectionView[];
};

export type AdaptCanonicalDesktopOptions = {
  readonly request?: AnalyzeChartRequest;
  readonly requestId?: string | null;
  readonly status?: CanonicalDesktopStatus;
  readonly source?: "api" | "mock";
};

type GlyphMeta = { han: string; element: string; tone: string };

const STEM_ENTRIES: { keys: string[]; meta: GlyphMeta }[] = [
  { keys: ["giáp", "giap"], meta: { han: "甲", element: "Mộc Dương", tone: "wood" } },
  { keys: ["ất", "at"], meta: { han: "乙", element: "Mộc Âm", tone: "wood" } },
  { keys: ["bính", "binh"], meta: { han: "丙", element: "Hỏa Dương", tone: "fire" } },
  { keys: ["đinh", "dinh"], meta: { han: "丁", element: "Hỏa Âm", tone: "fire" } },
  { keys: ["mậu", "mau"], meta: { han: "戊", element: "Thổ Dương", tone: "earth" } },
  { keys: ["kỷ", "ky"], meta: { han: "己", element: "Thổ Âm", tone: "earth" } },
  { keys: ["canh"], meta: { han: "庚", element: "Kim Dương", tone: "metal" } },
  { keys: ["tân", "tan"], meta: { han: "辛", element: "Kim Âm", tone: "metal" } },
  { keys: ["nhâm", "nham"], meta: { han: "壬", element: "Thủy Dương", tone: "water" } },
  { keys: ["quý", "quy"], meta: { han: "癸", element: "Thủy Âm", tone: "water" } },
];

const BRANCH_ENTRIES: { keys: string[]; meta: GlyphMeta }[] = [
  { keys: ["tý"], meta: { han: "子", element: "Thủy Dương", tone: "water" } },
  { keys: ["sửu", "suu"], meta: { han: "丑", element: "Thổ Âm", tone: "earth" } },
  { keys: ["dần", "dan"], meta: { han: "寅", element: "Mộc Dương", tone: "wood" } },
  { keys: ["mão", "mao"], meta: { han: "卯", element: "Mộc Âm", tone: "wood" } },
  { keys: ["thìn", "thin"], meta: { han: "辰", element: "Thổ Dương", tone: "earth" } },
  { keys: ["tỵ"], meta: { han: "巳", element: "Hỏa Âm", tone: "fire" } },
  { keys: ["ngọ", "ngo"], meta: { han: "午", element: "Hỏa Dương", tone: "fire" } },
  { keys: ["mùi", "mui"], meta: { han: "未", element: "Thổ Âm", tone: "earth" } },
  { keys: ["thân", "than"], meta: { han: "申", element: "Kim Dương", tone: "metal" } },
  { keys: ["dậu", "dau"], meta: { han: "酉", element: "Kim Âm", tone: "metal" } },
  { keys: ["tuất", "tuat"], meta: { han: "戌", element: "Thổ Dương", tone: "earth" } },
  { keys: ["hợi", "hoi"], meta: { han: "亥", element: "Thủy Âm", tone: "water" } },
];

const TEN_GOD_COLORS: Record<string, string> = {
  "chính quan": "#1565c0",
  "thất sát": "#6a1b9a",
  "chính ấn": "#ef6c00",
  "thiên ấn": "#f9a825",
  "chính tài": "#2e7d32",
  "thiên tài": "#c62828",
  "thực thần": "#5d4037",
  "thương quan": "#455a64",
  "tỷ kiên": "#7b1fa2",
  "kiếp tài": "#00838f",
};


/**
 * Deep-clone fixture for mutation-safe ViewModel bases.
 */
function cloneFixture(): CanonicalDesktopViewModel {
  return {
    ...(JSON.parse(JSON.stringify(CANONICAL_DESKTOP_MOCK)) as CanonicalDesktopMock),
    source: "mock",
    status: "ready",
  };
}

function asString(value: unknown, fallback = ""): string {
  if (value === null || value === undefined) return fallback;
  return String(value);
}

function formatLunarBirth(calendar: AnalysisDataDto["calendar"]): string {
  if (!calendar) return "";
  const lunar = calendar.lunar;
  if (calendar.lunar_date) {
    return asString(calendar.lunar_date);
  }
  const day = lunar?.day ?? calendar.lunar_day;
  const month = lunar?.month ?? calendar.lunar_month;
  const year = lunar?.year ?? calendar.lunar_year;
  if (day == null || month == null || year == null) return "";
  const leap = Boolean(lunar?.is_leap_month ?? lunar?.leap ?? calendar.is_leap_month ?? calendar.leap_month);
  const date = `${pad2(Number(day))}/${pad2(Number(month))}/${Number(year)}`;
  return leap ? `${date} nhuận` : date;
}

function formatLuckCurrent(luck: AnalysisDataDto["luck"]): string {
  const current = luck?.current_cycle;
  if (!current) return UNAVAILABLE_CONCLUSION;
  const gan = asString(current.gan_zhi);
  const years =
    current.year_start != null && current.year_end != null
      ? `${current.year_start}–${current.year_end}`
      : "";
  const text = [gan, years].filter(Boolean).join(" ");
  return text || UNAVAILABLE_CONCLUSION;
}

function formatLuckAgeBand(luck: AnalysisDataDto["luck"]): string {
  const current = luck?.current_cycle;
  if (current?.age_start == null || current?.age_end == null) return "";
  return `${current.age_start}–${current.age_end}`;
}

function formatLuckElements(cycle: NonNullable<AnalysisDataDto["luck"]>["current_cycle"]): string {
  if (!cycle) return "";
  const stem = asString(cycle.stem);
  const branch = asString(cycle.branch);
  const stemEl = asString(cycle.stem_element);
  const branchEl = asString(cycle.branch_element);
  const parts: string[] = [];
  if (stem && stemEl) parts.push(`${stem} · ${stemEl}`);
  if (branch && branchEl) parts.push(`${branch} · ${branchEl}`);
  return parts.join(" / ");
}

function formatLuckSequence(luck: AnalysisDataDto["luck"]): string {
  const cycles = luck?.cycles ?? [];
  if (!cycles.length) return UNAVAILABLE_CONCLUSION;
  return cycles
    .map((cycle) => {
      const gan = asString(cycle.gan_zhi);
      const years =
        cycle.year_start != null && cycle.year_end != null
          ? `${cycle.year_start}–${cycle.year_end}`
          : "";
      const elements = formatLuckElements(cycle);
      return [gan, years, elements].filter(Boolean).join(" ");
    })
    .filter(Boolean)
    .join(" | ");
}


function pad2(n: number): string {
  return String(n).padStart(2, "0");
}

function normKey(raw: string): string {
  return raw
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function genderMeta(raw: string | null | undefined): { symbol: string; label: string } {
  const canonical = canonicalGender(raw);
  if (canonical === "male") {
    return { symbol: "♂", label: "Nam" };
  }
  if (canonical === "female") {
    return { symbol: "♀", label: "Nữ" };
  }
  return { symbol: "•", label: "—" };
}

function matchGlyph(
  viet: string,
  entries: { keys: string[]; meta: GlyphMeta }[],
): GlyphMeta | null {
  const raw = viet.trim().toLowerCase();
  for (const entry of entries) {
    if (entry.keys.some((candidate) => candidate.toLowerCase() === raw)) {
      return entry.meta;
    }
  }
  const key = normKey(viet);
  for (const entry of entries) {
    if (entry.keys.some((candidate) => normKey(candidate) === key)) {
      return entry.meta;
    }
  }
  return null;
}

function lookupStem(viet: string): { han: string; viet: string; element: string; tone: string } {
  const hit = matchGlyph(viet, STEM_ENTRIES);
  const label = viet.trim() || "—";
  if (hit) {
    return { han: hit.han, viet: label, element: hit.element, tone: hit.tone };
  }
  return { han: label, viet: label, element: "—", tone: "metal" };
}

function lookupBranch(viet: string): { han: string; viet: string; element: string; tone: string } {
  const hit = matchGlyph(viet, BRANCH_ENTRIES);
  const label = viet.trim() || "—";
  if (hit) {
    return { han: hit.han, viet: label, element: hit.element, tone: hit.tone };
  }
  return { han: label, viet: label, element: "—", tone: "metal" };
}

function normalizeElement(label: string): string {
  const map: Record<string, string> = {
    kim: "Kim",
    metal: "Kim",
    moc: "Mộc",
    wood: "Mộc",
    thuy: "Thủy",
    water: "Thủy",
    hoa: "Hỏa",
    fire: "Hỏa",
    tho: "Thổ",
    earth: "Thổ",
  };
  return map[normKey(label)] ?? label.trim();
}


function pickStr(obj: Record<string, unknown> | undefined, keys: string[]): string {
  if (!obj) return "";
  for (const key of keys) {
    const v = obj[key];
    if (typeof v === "string" && v.trim()) return v.trim();
  }
  return "";
}

function pickList(obj: Record<string, unknown> | undefined, keys: string[]): string[] {
  if (!obj) return [];
  for (const key of keys) {
    const v = obj[key];
    if (Array.isArray(v)) {
      return v.map((x) => asString(x).trim()).filter(Boolean);
    }
    if (typeof v === "string" && v.trim()) {
      return v.split(/[,;/|]+/).map((s) => s.trim()).filter(Boolean);
    }
  }
  return [];
}

function mapPillarGlyph(
  dto: PillarDto | undefined,
  title: string,
  stamp: string,
  highlight: boolean,
  tenGod: string,
  hiddenLines: readonly string[],
): CanonicalDesktopViewModel["s03"]["pillars"][number] {
  const stem = lookupStem(asString(dto?.stem, "—"));
  const branch = lookupBranch(asString(dto?.branch, "—"));
  return {
    title,
    stem,
    branch,
    stamp,
    highlight,
    tenGod,
    hiddenLines: [...hiddenLines],
  };
}

function mapS00(
  data: AnalysisDataDto,
  request: AnalyzeChartRequest | undefined,
  requestId: string | null | undefined,
): CanonicalDesktopViewModel["s00"] {
  const base = cloneFixture().s00;
  const gender = genderMeta(
    data.customer?.gender_label ?? data.customer?.gender ?? request?.gender,
  );
  const year = request?.year;
  const month = request?.month;
  const day = request?.day;
  const hour = request?.hour ?? 0;
  const minute = request?.minute ?? 0;
  const lunarText = formatLunarBirth(data.calendar);
  const now = new Date();

  return {
    ...base,
    profile: {
      ...base.profile,
      name: asString(data.customer?.full_name ?? request?.full_name, base.profile.name),
      genderSymbol: gender.symbol,
      meta: `${gender.label} • ${asString(data.bazi?.day_master_yin_yang, gender.label)}`,
    },
    birth: {
      ...base.birth,
      date:
        year && month && day
          ? `${pad2(day)}/${pad2(month)}/${year}`
          : base.birth.date,
      lunar: lunarText ? `(${lunarText})` : base.birth.lunar,
      time:
        year !== undefined
          ? `${pad2(hour)}:${pad2(minute)} (${asString(data.customer?.timezone ?? request?.timezone, "GMT+7")})`
          : base.birth.time,
    },
    chartId: {
      ...base.chartId,
      value: asString(requestId || data.analysis_id, ""),
    },
    analyzedAt: {
      ...base.analyzedAt,
      value: `${pad2(now.getDate())}/${pad2(now.getMonth() + 1)}/${now.getFullYear()} ${pad2(now.getHours())}:${pad2(now.getMinutes())}:${pad2(now.getSeconds())}`,
      relative: "Vừa xong",
    },
    status: {
      ...base.status,
      value: "Hoàn tất",
    },
  };
}

function mapS01(data: AnalysisDataDto): CanonicalDesktopViewModel["s01"] {
  const base = cloneFixture().s01;
  const dm = asString(data.bazi?.day_master, base.dayMaster.value);
  const element = normalizeElement(asString(data.bazi?.day_master_element));
  const yy = asString(data.bazi?.day_master_yin_yang);
  const pattern = data.pattern as Record<string, unknown> | undefined;
  const strengthScore = readCanonicalStrengthScore(data) ?? 0;
  const score = canonicalStrengthMeterPercent(strengthScore);
  const level = canonicalStrengthLabel(data);
  const cachCuc = pickStr(pattern, ["cach_cuc", "pattern"]);
  const than = level;
  const season = asString(
    (data.calendar?.solar_term as { name?: string } | null | undefined)?.name,
  );
  const sections = extractInterpretationSections(
    data.interpretation as Record<string, unknown> | undefined,
  );
  const narrative = asNarrativeResult(data.narrative_result);
  const useNarrative = hasUsableNarrativeResult(narrative);
  const career = careerSelectionFromNarrative(narrative);
  const promotion = promotionReadinessFromNarrative(narrative);
  const executive = executiveFromNarrative(narrative);
  const primaryRec = primaryRecommendationFromNarrative(narrative);
  const secondary = secondaryMilestoneFromNarrative(narrative);
  const careerDirection = careerFieldText(career, "career_direction");
  const careerStrengths = careerFieldText(career, "career_strengths");
  const whoBody = useNarrative
    ? (executive?.central_message ||
        summaryText(narrative?.summary, "identity") ||
        careerDirection)
    : findSectionBody(sections, [/^tính cách$/i, /tổng quan/i]);
  const strengthBody = useNarrative
    ? (executive?.supporting_points?.length
        ? executive.supporting_points.join(" ")
        : careerStrengths || summaryText(narrative?.summary, "strengths"))
    : findSectionBody(sections, [/điểm mạnh/i, /thế mạnh/i]);
  const primaryAction =
    primaryRec?.composed_text ||
    careerFieldText(career, "action_plan_90d") ||
    summaryText(narrative?.summary, "priority_recommendation") ||
    summaryText(narrative?.summary, "next_action");
  const secondaryAction =
    secondary?.composed_text ||
    (promotion
      ? `Promotion Readiness Assessment (mốc nghề phụ): ${promotionFieldText(promotion, "promotion_readiness")}`
      : "");
  const actionBody = useNarrative
    ? [primaryAction, secondaryAction].filter(Boolean).join(" ")
    : findSectionBody(sections, [
        /dụng thần/i,
        /kết luận/i,
        /hành động/i,
        /khuyến/i,
      ]);
  const useful = canonicalUsefulGodPayload(data);
  const dung = canonicalUsefulDisplay(useful);
  const whoFallback = [dm && `Nền tảng ngày ${dm}`, cachCuc && `Cấu trúc nghề ${cachCuc}`, than]
    .filter(Boolean)
    .join(" · ");
  const strengthFallback = [cachCuc && `Cấu trúc nghề ${cachCuc}`, than]
    .filter(Boolean)
    .join(". ");
  const actionFallback = dung
    ? `Ưu tiên phát huy trục hỗ trợ: ${dung}. ${asString(data.score?.recommendation)}`.trim()
    : asString(data.score?.recommendation);

  const strengthTone =
    score >= 60 ? ("danger" as const) : score >= 40 ? ("warning" as const) : ("success" as const);

  return {
    ...base,
    dayMaster: {
      ...base.dayMaster,
      value: element ? `${dm}`.replace(/\s+/g, " ").trim() || `${dm}` : dm,
      subtype: yy && element ? `${yy} ${element}`.trim() : yy || element || base.dayMaster.subtype,
      tags: [
        {
          text: than || (element ? `${element} ${score >= 55 ? "vượng" : "cân"}` : "—"),
          tone: strengthTone,
        },
        {
          text: `Mệnh cục: ${cachCuc || level || "—"}`,
          tone: "neutral" as const,
        },
      ],
    },
    conditions: {
      ...base.conditions,
      rows: [
        {
          label: "Mùa sinh",
          value: season || UNAVAILABLE_CONCLUSION,
          tag: season ? "Tiết khí" : "—",
          tone: "neutral" as const,
        },
        {
          label: "Yếu tố chính",
          value: strengthCustomerSummary(data) || UNAVAILABLE_CONCLUSION,
          tag: than || "—",
          tone: strengthTone,
        },
        {
          label: "Cách cục",
          value: patternCustomerLine(data) || cachCuc || UNAVAILABLE_CONCLUSION,
          tag: than || "Nhận diện",
          tone: strengthTone === "danger" ? ("warning" as const) : strengthTone,
        },
        {
          label: "Điều hậu",
          value: [
            temperatureCustomerLine(data),
            canonicalClimatePreferenceLabel(canonicalUsefulGodPayload(data)),
          ]
            .filter(Boolean)
            .join(" · ") || UNAVAILABLE_CONCLUSION,
          tag: "Điều hậu",
          tone: "neutral" as const,
        },
        {
          label: "Thân cư",
          value: pickStr(pattern, ["tong_cach", "than"]) || than || UNAVAILABLE_CONCLUSION,
          tag: score >= 55 ? "Tốt" : "Theo dõi",
          tone: score >= 55 ? ("success" as const) : ("warning" as const),
        },
        {
          label: "Đại vận",
          value: formatLuckCurrent(data.luck),
          tag: formatLuckAgeBand(data.luck) || "—",
          tone: "neutral" as const,
        },
        {
          label: "Chiều vận",
          value: asString(data.luck?.direction_label) || UNAVAILABLE_CONCLUSION,
          tag: "Đại vận",
          tone: "neutral" as const,
        },
        {
          label: "Tuổi khởi vận",
          value: data.luck?.start_age != null ? String(data.luck.start_age) : UNAVAILABLE_CONCLUSION,
          tag: "Đại vận",
          tone: "neutral" as const,
        },
        {
          label: "Căn cứ Đại vận",
          value: stripInternalRuleIds(asString(data.luck?.evidence)) || UNAVAILABLE_CONCLUSION,
          tag: "Đại vận",
          tone: "neutral" as const,
        },
        {
          label: "Phương pháp V1.0",
          value: asString(data.luck?.method_note) || UNAVAILABLE_CONCLUSION,
          tag: "Đại vận",
          tone: "neutral" as const,
        },
        {
          label: "Lộ trình Đại vận",
          value: formatLuckSequence(data.luck),
          tag: data.luck?.cycles?.length ? `${data.luck.cycles.length} vận` : "—",
          tone: "neutral" as const,
        },
      ],
    },
    decisions: [
      {
        icon: "target" as const,
        question: "BẠN LÀ AI?",
        answer: commercialOrUnavailable(whoBody || whoFallback),
      },
      {
        icon: "bulb" as const,
        question: "THẾ MẠNH CỦA BẠN?",
        answer: commercialOrUnavailable(strengthBody || strengthFallback),
      },
      {
        icon: "compass" as const,
        question: "BẠN NÊN LÀM GÌ?",
        answer: commercialOrUnavailable(
          actionBody || actionFallback || asString(data.score?.recommendation),
        ),
      },
    ],
  };
}

function mapS02(data: AnalysisDataDto): CanonicalDesktopViewModel["s02"] {
  const base = cloneFixture().s02;
  const useful = canonicalUsefulGodPayload(data);
  const distribution = formatFiveElementsCompact(canonicalFiveElementCounts(data));
  const yy = asString(data.bazi?.day_master_yin_yang, "—");
  const than = canonicalStrengthLabel(data) || "—";
  const dung = canonicalUsefulDisplay(useful, "—");
  const hy = canonicalFavorableDisplay(useful, "—");
  const ky = canonicalUnfavorableDisplay(useful, "—");

  return {
    ...base,
    dungReason: canonicalUsefulShortReason(useful),
    items: [
      {
        icon: "fire" as const,
        label: "Phân bố Ngũ hành",
        value: distribution || "—",
        color: "earth",
      },
      {
        icon: "yinyang" as const,
        label: "Âm dương",
        value: yy,
        color: "water",
      },
      {
        icon: "scale" as const,
        label: "Thế cục",
        value: than,
        color: "earth",
      },
      {
        icon: "drop" as const,
        label: "Dụng thần",
        value: dung,
        color: "water",
      },
      {
        icon: "spark" as const,
        label: "Hỷ thần",
        value: hy,
        color: "metal",
      },
      {
        icon: "leaf" as const,
        label: "Kỵ thần",
        value: ky,
        color: "wood",
      },
    ],
  };
}

function mapS03(
  data: AnalysisDataDto,
  request: AnalyzeChartRequest | undefined,
): CanonicalDesktopViewModel["s03"] {
  const base = cloneFixture().s03;
  const hour = request?.hour ?? 0;
  const minute = request?.minute ?? 0;
  const payload =
    asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  return {
    ...base,
    pillars: [
      mapPillarGlyph(
        data.bazi?.year_pillar,
        "NĂM TRỤ",
        asString(request?.year, base.pillars[0].stamp),
        false,
        asString(data.bazi?.year_pillar?.ten_god),
        hiddenLinesForPillar(payload, "year"),
      ),
      mapPillarGlyph(
        data.bazi?.month_pillar,
        "THÁNG TRỤ",
        request?.month ? pad2(request.month) : base.pillars[1].stamp,
        false,
        asString(data.bazi?.month_pillar?.ten_god),
        hiddenLinesForPillar(payload, "month"),
      ),
      mapPillarGlyph(
        data.bazi?.day_pillar,
        "NGÀY TRỤ (NHẬT CHỦ)",
        asString(request?.day, base.pillars[2].stamp),
        true,
        asString(data.bazi?.day_pillar?.ten_god),
        hiddenLinesForPillar(payload, "day"),
      ),
      mapPillarGlyph(
        data.bazi?.hour_pillar,
        "GIỜ TRỤ",
        request ? `${pad2(hour)}:${pad2(minute)}` : base.pillars[3].stamp,
        false,
        asString(data.bazi?.hour_pillar?.ten_god),
        hiddenLinesForPillar(payload, "hour"),
      ),
    ],
  };
}

function mapS04(data: AnalysisDataDto): CanonicalDesktopViewModel["s04"] {
  const base = cloneFixture().s04;
  const counts = canonicalFiveElementCounts(data);
  const total = fiveElementUnitTotal(counts);
  const rows = FIVE_ELEMENT_ROWS.map((row) => {
    const count = counts?.[row.name] ?? 0;
    const pct = total > 0 ? Math.round((count / total) * 100) : 0;
    return {
      name: row.name,
      element: row.element,
      pct,
      count,
      status: fiveElementAbsentLabel(count),
    };
  });
  return {
    ...base,
    title: FIVE_ELEMENTS_TITLE,
    rows,
    summary: counts
      ? formatFiveElementsProvenance(total) || publishedFiveElementsMethodNote(data)
      : "",
  };
}

function mapS05(data: AnalysisDataDto): CanonicalDesktopViewModel["s05"] {
  const base = cloneFixture().s05;
  const strengthScore = readCanonicalStrengthScore(data);
  const scoreLabel =
    strengthScore == null ? "—" : formatCanonicalStrengthScore(strengthScore);
  const percent =
    strengthScore == null ? 0 : canonicalStrengthMeterPercent(strengthScore);
  const level = canonicalStrengthLabel(data);
  const summary = strengthCustomerSummary(data);
  const reasoning = commercialOrUnavailable(asString(data.strength?.reasoning));
  const factors = summary
    .split(/\s·\s/)
    .map((s) => s.trim())
    .filter(Boolean)
    .filter((text) => commercialOrUnavailable(text) !== UNAVAILABLE_CONCLUSION)
    .slice(0, 6)
    .map((text, i) => ({
      text,
      tone: (i < 2 ? "positive" : i === 2 ? "neutral" : "negative") as
        | "positive"
        | "neutral"
        | "negative",
    }));

  return {
    ...base,
    title: "Điểm thân",
    level: level || "—",
    score: scoreLabel,
    percent: Math.min(100, Math.max(0, percent)),
    insight: summary || reasoning,
    factors:
      factors.length > 0
        ? factors
        : [{ text: UNAVAILABLE_CONCLUSION, tone: "neutral" as const }],
  };
}

function toGodRows(names: readonly string[]): CanonicalDesktopViewModel["s06"]["gods"] {
  return names.filter(Boolean).map((name) => {
    const key = name.toLowerCase();
    const color =
      Object.entries(TEN_GOD_COLORS).find(([k]) => key.includes(k))?.[1] ?? "#5c6570";
    return {
      name,
      short: name.length > 8 ? `${name.slice(0, 6)}.` : name,
      score: "",
      color,
    };
  });
}

function mapS06(data: AnalysisDataDto): CanonicalDesktopViewModel["s06"] {
  const base = cloneFixture().s06;
  const payload =
    asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  const prominence = tenGodsProminenceFromAnalysis(data);
  const visible = visibleLabels(payload);
  const hidden = hiddenLabels(payload);
  if (prominence.featured.length) {
    return {
      ...base,
      title: "THẬP THẦN NỔI BẬT",
      gods: prominence.featured.map((item) => ({
        name: `${item.name} — ${item.klass}`,
        short: item.klass,
        score: item.evidence,
        color:
          Object.entries(TEN_GOD_COLORS).find(([k]) =>
            item.name.toLowerCase().includes(k),
          )?.[1] ?? "#5c6570",
      })),
      hiddenGods: toGodRows(hidden),
      note: prominence.othersLine || tenGodsNote(payload),
    };
  }
  if (visible.length || hidden.length) {
    return {
      ...base,
      gods: toGodRows(visible),
      hiddenGods: toGodRows(hidden),
      note: tenGodsNote(payload),
    };
  }
  const fallback = (data.bazi?.ten_gods ?? [])
    .map((item) => tenGodLabel(item) || asString(item).trim())
    .filter(Boolean);
  if (!fallback.length) {
    return {
      ...base,
      gods: [
        {
          name: UNAVAILABLE_CONCLUSION,
          short: "—",
          score: "",
          color: "#5c6570",
        },
      ],
      hiddenGods: [],
    };
  }
  return {
    ...base,
    gods: toGodRows(fallback),
    hiddenGods: [],
  };
}

function mapS07(data: AnalysisDataDto): CanonicalDesktopViewModel["s07"] {
  const base = cloneFixture().s07;
  const entries = shenShaEntriesFromAnalysis(data);
  if (entries.length === 0) {
    return {
      ...base,
      executive: {
        line1: UNAVAILABLE_CONCLUSION,
        line2: "",
      },
      items: [],
      footerSummary: {
        line1: UNAVAILABLE_CONCLUSION,
        line2: "",
      },
    };
  }
  return {
    ...base,
    executive: {
      line1: `Có ${entries.length} Thần Sát`,
      line2: "",
    },
    items: entries.map((item) => ({
      name: item.name,
      presence: item.presence,
      evidence: item.evidence,
    })),
    footerSummary: {
      line1: "",
      line2: "",
    },
  };
}

function mapS08(data: AnalysisDataDto): CanonicalDesktopViewModel["s08"] {
  const base = cloneFixture().s08;
  const narrative = asNarrativeResult(data.narrative_result);
  if (hasUsableNarrativeResult(narrative) && narrative) {
    const career = careerSelectionFromNarrative(narrative);
    const promotion = promotionReadinessFromNarrative(narrative);
    const executive = executiveFromNarrative(narrative);
    const primaryRec = primaryRecommendationFromNarrative(narrative);
    const secondary = secondaryMilestoneFromNarrative(narrative);
    const careerStrengths = careerFieldText(career, "career_strengths");
    const careerRisks = careerFieldText(career, "career_risks");
    const careerMitigation = careerFieldText(career, "career_mitigation");
    const strengths = (
      executive?.supporting_points?.length
        ? [...executive.supporting_points]
        : careerStrengths
          ? [careerStrengths]
          : (narrative.summary?.strengths ?? []).map((item) =>
              firstCommercialSnippet(item),
            )
    )
      .filter((item) => item !== UNAVAILABLE_CONCLUSION)
      .slice(0, 3);
    const warnings = (
      careerRisks || careerMitigation
        ? [careerRisks, careerMitigation].filter(Boolean)
        : (narrative.summary?.weaknesses ?? []).map((item) =>
            firstCommercialSnippet(item),
          )
    )
      .filter((item) => item !== UNAVAILABLE_CONCLUSION)
      .slice(0, 4);
    const primaryAction =
      primaryRec?.composed_text ||
      careerFieldText(career, "action_plan_90d") ||
      recommendationActions(narrative)[0] ||
      "";
    const secondaryAction =
      secondary?.composed_text ||
      (promotion
        ? `Promotion Readiness Assessment (mốc nghề phụ): ${promotionFieldText(promotion, "promotion_readiness")}`
        : "");
    const actions = [primaryAction, secondaryAction]
      .filter((item) => item && item !== UNAVAILABLE_CONCLUSION)
      .slice(0, 4);
    const overview =
      executive?.central_message ||
      executive?.composed_text ||
      summaryText(narrative.summary, "identity") ||
      paragraphByRole(narrative, "observation") ||
      sectionParagraphTexts(narrative, /observation|overview|executive/i)[0] ||
      careerFieldText(career, "career_direction") ||
      "";
    return {
      ...base,
      executive: {
        ...base.executive,
        body: commercialOrUnavailable(overview),
      },
      strengths: {
        ...base.strengths,
        items: strengths.length > 0 ? strengths : [UNAVAILABLE_CONCLUSION],
      },
      warnings: {
        ...base.warnings,
        items: warnings.length > 0 ? warnings : [UNAVAILABLE_CONCLUSION],
      },
      actions: {
        ...base.actions,
        items: actions.length > 0 ? actions : [UNAVAILABLE_CONCLUSION],
      },
    };
  }

  // Legacy fallback — only when Pack 05 NarrativeResult is absent.
  const sections = extractInterpretationSections(
    data.interpretation as Record<string, unknown> | undefined,
  );

  const strengths: string[] = [];
  const warnings: string[] = [];
  const actions: string[] = [];
  for (const section of sections) {
    const title = section.title.toLowerCase();
    const snippet = firstCommercialSnippet(section.body);
    if (snippet === UNAVAILABLE_CONCLUSION) continue;
    if (/điểm mạnh|thế mạnh|ưu điểm|strength/.test(title)) {
      strengths.push(snippet);
    } else if (/điểm cần lưu ý|lưu ý|nhược|warning|risk|yếu tố/.test(title)) {
      warnings.push(snippet);
    } else if (/hành động|khuyến|recommend|gợi ý|dụng thần|kết luận/.test(title)) {
      actions.push(snippet);
    }
  }

  const overviewBody =
    findSectionBody(sections, [/^tính cách$/i, /^kết luận$/i, /tổng quan/i]) ||
    asString(data.score?.recommendation);
  const dung = canonicalUsefulDisplay(canonicalUsefulGodPayload(data), "");
  if (actions.length === 0 && dung) {
    actions.push(`Ưu tiên phát huy Dụng thần: ${dung}`);
  }
  if (actions.length === 0) {
    const rec = asString(data.score?.recommendation).trim();
    if (rec) actions.push(rec);
  }

  const strengthItems =
    strengths.length > 0 ? strengths.slice(0, 4) : [UNAVAILABLE_CONCLUSION];
  const warningItems =
    warnings.length > 0 ? warnings.slice(0, 4) : [UNAVAILABLE_CONCLUSION];
  const actionItems =
    actions.length > 0 ? actions.slice(0, 4) : [UNAVAILABLE_CONCLUSION];

  return {
    ...base,
    executive: {
      ...base.executive,
      body: commercialOrUnavailable(overviewBody),
    },
    strengths: {
      ...base.strengths,
      items: strengthItems,
    },
    warnings: {
      ...base.warnings,
      items: warningItems,
    },
    actions: {
      ...base.actions,
      items: actionItems,
    },
  };
}

function mapS10(): CanonicalDesktopViewModel["s10"] {
  const base = cloneFixture().s10;
  return {
    ...base,
    stars: 0,
    weight: "—",
    grade: UNAVAILABLE_CONCLUSION,
    insight: UNAVAILABLE_CONCLUSION,
    verse: {
      ...base.verse,
      lines: [UNAVAILABLE_CONCLUSION],
    },
    interpretation: {
      ...base.interpretation,
      body: UNAVAILABLE_CONCLUSION,
    },
  };
}

function mapS09(data: AnalysisDataDto): CanonicalDesktopViewModel["s09"] {
  const base = cloneFixture().s09;
  const cal = data.calendar ?? {};
  const feng =
    data.feng_shui && typeof data.feng_shui === "object"
      ? (data.feng_shui as Record<string, unknown>)
      : {};
  const cung = asString(
    cal.cung_phi ?? feng.cung_phi ?? feng.gua_name ?? cal.gua_name ?? feng.menh_quai ?? cal.menh_quai,
    base.quai.center,
  );
  const menh = asString(cal.menh_quai ?? feng.menh_quai ?? cal.cung_phi ?? feng.cung_phi, cung);
  const nhom = asString(cal.house_group ?? cal.nhom_trach ?? feng.house_group ?? feng.nhom_trach, "");
  const guaName = asString(feng.gua_name ?? cal.gua_name, menh);
  const guaNumber = asString(cal.gua_number ?? feng.gua_number, "");
  const numberMatch = guaNumber.match(/\d+/) ?? guaName.match(/\d+/) ?? menh.match(/\d+/);
  const tamNguyen = asString(cal.tam_nguyen);
  const cuuVan = asString(cal.cuu_van);
  const bullets = [
    `Cung mệnh: ${cung || menh}`,
    nhom ? `Nhóm trạch: ${nhom}` : base.quai.bullets[1],
    tamNguyen ? `Tam Nguyên: ${tamNguyen}` : asString(cal.group_label, base.quai.bullets[2]),
    cuuVan ? `Cửu Vận: ${cuuVan}` : asString(cal.avoid_label, base.quai.bullets[3]),
  ].filter(Boolean);

  return {
    ...base,
    quai: {
      center: guaName || menh || base.quai.center,
      number: numberMatch?.[0] ?? base.quai.number,
      bullets: bullets.length >= 2 ? bullets : base.quai.bullets,
    },
  };
}

function mapS11(data: AnalysisDataDto): CanonicalDesktopViewModel["s11"] {
  const base = cloneFixture().s11;
  const narrative = asNarrativeResult(data.narrative_result);
  const s08 = mapS08(data);

  if (hasUsableNarrativeResult(narrative) && narrative) {
    const closing =
      sectionParagraphTexts(narrative, /conclusion|closing|kết luận/i)[0] ||
      summaryText(narrative.summary, "identity");
    const actions = recommendationActions(narrative);
    return {
      ...base,
      executive: {
        ...base.executive,
        body: commercialOrUnavailable(closing),
      },
      strengths: {
        ...base.strengths,
        items: s08.strengths.items.slice(0, 4),
      },
      attention: {
        ...base.attention,
        items: s08.warnings.items.slice(0, 3),
      },
      recommendations: {
        ...base.recommendations,
        items:
          actions.length > 0
            ? actions.slice(0, 4)
            : s08.actions.items.slice(0, 4),
      },
    };
  }

  const report = data.report as Record<string, unknown> | undefined;
  const deliveryNarrative = data.narrative as Record<string, unknown> | undefined;
  const markdown = asString(report?.markdown ?? deliveryNarrative?.markdown ?? report?.html);
  const firstPara =
    markdown
      .replace(/<[^>]+>/g, " ")
      .split(/\n+/)
      .map((l) => l.replace(/^#+\s*/, "").trim())
      .find((l) => l.length > 40) ?? "";

  return {
    ...base,
    executive: {
      ...base.executive,
      body: commercialOrUnavailable(firstPara || s08.executive.body),
    },
    strengths: {
      ...base.strengths,
      items: s08.strengths.items.slice(0, 4),
    },
    attention: {
      ...base.attention,
      items: s08.warnings.items.slice(0, 3),
    },
    recommendations: {
      ...base.recommendations,
      items: s08.actions.items.slice(0, 4),
    },
  };
}

/**
 * Map full orchestrator analysis payload → Canonical Desktop ViewModel.
 */
export function adaptAnalysisToCanonicalDesktop(
  data: AnalysisDataDto,
  options: AdaptCanonicalDesktopOptions = {},
): CanonicalDesktopViewModel {
  const fixture = cloneFixture();
  const request = options.request;

  return {
    ...fixture,
    header: {
      ...fixture.header,
      user: {
        ...fixture.header.user,
        name: asString(data.customer?.full_name ?? request?.full_name, fixture.header.user.name),
        initials: asString(data.customer?.full_name ?? request?.full_name, "NV")
          .split(/\s+/)
          .filter(Boolean)
          .slice(-2)
          .map((p) => p[0]?.toUpperCase() ?? "")
          .join("")
          .slice(0, 2) || fixture.header.user.initials,
      },
    },
    s00: mapS00(data, request, options.requestId),
    s01: mapS01(data),
    s02: mapS02(data),
    s03: mapS03(data, request),
    s04: mapS04(data),
    s05: mapS05(data),
    s06: mapS06(data),
    s07: mapS07(data),
    s08: mapS08(data),
    s09: mapS09(data),
    // S10 — bone-weight engine not in production pipeline; no fixture leakage.
    s10: mapS10(),
    s11: mapS11(data),
    footer: fixture.footer,
    narrativeResult: asNarrativeResult(data.narrative_result),
    commercialConsulting: mapCommercialConsulting(data.commercial_consulting),
    source: options.source ?? "api",
    status: options.status ?? "ready",
  };
}

function asStringList(value: unknown): readonly string[] {
  if (typeof value === "string") {
    const text = value.trim();
    return text ? [text] : [];
  }
  if (!Array.isArray(value)) return [];
  return value.map((item) => String(item).trim()).filter(Boolean);
}

function mapCommercialConsulting(
  payload: AnalysisDataDto["commercial_consulting"],
): CommercialConsultingView | null {
  if (!payload || typeof payload !== "object") return null;
  const status = asString(payload.status, "insufficient");
  const sections = (payload.sections ?? [])
    .map((item) => {
      const title = asString(item?.title);
      const summary = asString(item?.summary);
      const meaning = asStringList(item?.meaning);
      const recommendations = asStringList(item?.recommendations);
      if (!title || !(summary || meaning.length || recommendations.length)) {
        return null;
      }
      return {
        domain: asString(item?.domain),
        title,
        summary,
        meaning,
        recommendations,
        sourceUnitIds: asStringList(item?.source_unit_ids),
      };
    })
    .filter((item): item is CommercialConsultingSectionView => item !== null);
  if (status !== "complete" || sections.length === 0) {
    return { visible: false, status: "insufficient", sections: [] };
  }
  return { visible: true, status: "complete", sections };
}

/**
 * Gate / preview ViewModels.
 */
export function createCanonicalDesktopGateViewModel(
  status: CanonicalDesktopStatus,
  message?: string,
): CanonicalDesktopViewModel {
  const base = cloneFixture();
  return {
    ...base,
    status,
    statusMessage: message,
    source: "mock",
    narrativeResult: null,
    commercialConsulting: null,
    header: {
      ...base.header,
      user: { initials: "", name: "", role: "" },
      notifications: 0,
    },
    s00: {
      ...base.s00,
      profile: { ...base.s00.profile, name: "", meta: "" },
      birth: { ...base.s00.birth, date: "", lunar: "", time: "" },
      chartId: { ...base.s00.chartId, value: "" },
    },
  };
}

/** Fixture ViewModel for tests / dashboard-preview without network. */
export function createCanonicalDesktopMockViewModel(): CanonicalDesktopViewModel {
  return {
    ...cloneFixture(),
    status: "ready",
    source: "mock",
    narrativeResult: null,
    commercialConsulting: null,
  };
}
