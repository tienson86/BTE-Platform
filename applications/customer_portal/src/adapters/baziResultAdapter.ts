/**
 * Analysis API → BaZi Result ViewModel adapter (TASK_003A).
 * Components consume ViewModels only — never raw JSON.
 */

import { customerGenderDisplay, genderDisplayLabel } from "./genderDisplay";
import type { AnalysisDataDto, AnalyzeChartRequest, PillarDto, SeriesItemDto } from "../models";
import {
  BAZI_MOCK_ACTIONS,
  BAZI_RESULT_LABELS,
  buildExecutiveFromResult,
  type BaZiFiveElement,
  type BaZiInterpretationBlock,
  type BaZiKnowledgeItem,
  type BaZiPillar,
  type BaZiProfile,
  type BaZiChartMetadata,
  type BaZiResultMockBundle,
  type BaZiShenShaItem,
  type BaZiSpiritGod,
  type BaZiStrength,
  type BaZiTenGod,
  type PillarKind,
  type PresentationStatus,
} from "../screens/bazi/mockData";
import { shenShaEntriesFromAnalysis } from "./canonicalShenSha";
import {
  UNAVAILABLE_CONCLUSION,
  commercialOrUnavailable,
  extractInterpretationSections,
} from "./contentGuards";
import {
  canonicalStrengthLabel,
  readCanonicalStrengthScore,
} from "./canonicalStrength";
import {
  canonicalFiveElementCounts,
  fiveElementAbsentLabel,
} from "./canonicalFiveElements";
import {
  canonicalFavorableDisplay,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
  canonicalUnfavorableDisplay,
} from "./canonicalUsefulGod";
import {
  asTenGodsPayload,
  hiddenLinesForPillar,
  hiddenLabels,
  stemDisplay,
  tenGodsNote,
  visibleEntryForPillar,
  visibleLabels,
} from "./tenGodsDisplay";
import {
  asNarrativeResult,
  hasUsableNarrativeResult,
} from "./narrativeResultAdapter";

/** Presentation ViewModel — same shape as former mock bundle. */
export type BaZiResultViewModel = BaZiResultMockBundle;

const PILLAR_SPECS: readonly {
  readonly key: keyof Pick<
    NonNullable<AnalysisDataDto["bazi"]>,
    "year_pillar" | "month_pillar" | "day_pillar" | "hour_pillar"
  >;
  readonly kind: PillarKind;
  readonly label: string;
}[] = [
  { key: "year_pillar", kind: "year", label: "Năm" },
  { key: "month_pillar", kind: "month", label: "Tháng" },
  { key: "day_pillar", kind: "day", label: "Ngày" },
  { key: "hour_pillar", kind: "hour", label: "Giờ" },
];

const ELEMENT_ORDER = [
  { id: "kim" as const, name: "Kim" },
  { id: "moc" as const, name: "Mộc" },
  { id: "thuy" as const, name: "Thủy" },
  { id: "hoa" as const, name: "Hỏa" },
  { id: "tho" as const, name: "Thổ" },
];

function asString(value: unknown, fallback = ""): string {
  if (value === null || value === undefined) {
    return fallback;
  }
  return String(value);
}

function pad2(n: number): string {
  return String(n).padStart(2, "0");
}

function formatSolarDate(year: number, month: number, day: number): string {
  return `${pad2(day)}/${pad2(month)}/${year}`;
}

function formatBirthTime(hour: number, minute: number): string {
  return `${pad2(hour)}:${pad2(minute)}`;
}

function normalizeElementName(label: string): string {
  const map: Record<string, string> = {
    kim: "Kim",
    metal: "Kim",
    moc: "Mộc",
    wood: "Mộc",
    "mộc": "Mộc",
    thuy: "Thủy",
    water: "Thủy",
    "thủy": "Thủy",
    hoa: "Hỏa",
    fire: "Hỏa",
    "hỏa": "Hỏa",
    tho: "Thổ",
    earth: "Thổ",
    "thổ": "Thổ",
  };
  const key = label.trim().toLowerCase();
  return map[key] ?? label.trim();
}


function mapStrengthLevel(level: string): { label: string; level: string } {
  const token = level.trim().toLowerCase();
  if (token === "strong" || token.includes("vượng") || token.includes("vuong")) {
    return { label: "Thân vượng", level: "Thân vượng" };
  }
  if (token === "weak" || token.includes("nhược") || token.includes("nhuoc")) {
    return { label: "Thân nhược", level: "Thân nhược" };
  }
  if (token === "balanced" || token.includes("cân") || token.includes("can bang")) {
    return { label: "Thân cân bằng", level: "Thân cân bằng" };
  }
  const fromCanonical = canonicalStrengthLabel({
    strength: { strength_level: token },
  });
  if (fromCanonical) {
    return { label: fromCanonical, level: fromCanonical };
  }
  return { label: "", level: "" };
}

function mapPillar(
  dto: PillarDto | undefined,
  kind: PillarKind,
  label: string,
  payload: ReturnType<typeof asTenGodsPayload>,
): BaZiPillar {
  const hidden = hiddenLinesForPillar(payload, kind);
  const stem = asString(dto?.stem, "—");
  const fromPayload = visibleEntryForPillar(payload, kind);
  const element = asString(dto?.element) || fromPayload?.element || undefined;
  return {
    kind,
    label,
    heavenlyStem: stemDisplay(stem === "—" ? "" : stem, element) || stem,
    earthlyBranch: asString(dto?.branch, "—"),
    hiddenStems: hidden.length
      ? hidden
      : Array.isArray(dto?.hidden_stems)
        ? [...dto.hidden_stems]
        : [],
    naYin: asString(dto?.nap_am, "—"),
    twelveStage: asString(dto?.truong_sinh, "—"),
    tenGod: asString(dto?.ten_god, "—"),
    stemElement: element,
  };
}

function seriesValue(item: SeriesItemDto): number {
  if (typeof item.value === "number") return item.value;
  if (typeof item.count === "number") return item.count;
  if (typeof item.score === "number") return item.score;
  return 0;
}

function mapFiveElements(data: AnalysisDataDto): readonly BaZiFiveElement[] {
  const fromFacts = canonicalFiveElementCounts(data);
  const scores: Record<string, number> = {
    Kim: 0,
    Mộc: 0,
    Thủy: 0,
    Hỏa: 0,
    Thổ: 0,
  };

  if (fromFacts) {
    Object.assign(scores, fromFacts);
  } else {
    const series = data.score?.wuxing_series;
    if (Array.isArray(series) && series.length > 0) {
      for (const item of series) {
        const name = normalizeElementName(asString(item.label ?? item.element ?? item.name));
        if (name in scores) {
          scores[name] = seriesValue(item);
        }
      }
    }
  }

  const total = Object.values(scores).reduce((sum, n) => sum + n, 0);

  return ELEMENT_ORDER.map((el) => {
    const score = scores[el.name] ?? 0;
    const percentage = total > 0 ? Math.round((score / total) * 100) : 0;
    return {
      id: el.id,
      name: el.name,
      score,
      percentage,
      strength: fiveElementAbsentLabel(score),
    };
  });
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

const TEN_GOD_CATALOG = [
  "Chính Quan",
  "Thất Sát",
  "Chính Tài",
  "Thiên Tài",
  "Chính Ấn",
  "Thiên Ấn",
  "Thực Thần",
  "Thương Quan",
  "Tỷ Kiên",
  "Kiếp Tài",
] as const;

function mapTenGods(data: AnalysisDataDto): readonly BaZiTenGod[] {
  const payload =
    asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  const present = new Set(
    [...visibleLabels(payload), ...hiddenLabels(payload)].filter(Boolean),
  );
  if (!present.size) {
    const fromList = data.bazi?.ten_gods ?? [];
    for (const god of fromList) {
      const name = asString(god).trim();
      if (name && name !== "Nhật Chủ") present.add(name);
    }
    for (const pillar of [
      data.bazi?.year_pillar,
      data.bazi?.month_pillar,
      data.bazi?.day_pillar,
      data.bazi?.hour_pillar,
    ]) {
      const name = asString(pillar?.ten_god).trim();
      if (name && name !== "Nhật Chủ") present.add(name);
    }
  }
  return TEN_GOD_CATALOG.map((name) => {
    const count = present.has(name) ? 1 : 0;
    return {
      id: slugify(name),
      name,
      count,
      score: count,
      strength: count ? "Có" : "Không",
      descriptionPreview: "",
    };
  });
}

function mapStrength(data: AnalysisDataDto): BaZiStrength {
  const strength = data.strength;
  const raw = readCanonicalStrengthScore(data) ?? 0;
  const unitOne = raw >= 0 && raw <= 1;
  const mapped = mapStrengthLevel(String(strength?.strength_level || ""));
  const confidenceRaw = strength?.confidence;
  const confidence =
    typeof confidenceRaw === "number"
      ? Math.round(confidenceRaw <= 1 ? confidenceRaw * 100 : confidenceRaw)
      : 0;
  const summary = commercialOrUnavailable(asString(strength?.reasoning));

  return {
    score: unitOne ? Math.round(raw * 100) / 100 : raw,
    maxScore: unitOne ? 1 : 100,
    label: mapped.label || canonicalStrengthLabel(data),
    level: mapped.level || canonicalStrengthLabel(data),
    confidence,
    summary,
  };
}

function mapInterpretation(data: AnalysisDataDto): BaZiInterpretationBlock {
  const narrative = asNarrativeResult(data.narrative_result);
  if (hasUsableNarrativeResult(narrative) && narrative) {
    const paragraphs = (narrative.sections ?? [])
      .flatMap((section) => section.paragraphs ?? [])
      .filter((paragraph) => !paragraph.insufficient_data)
      .map((paragraph) => commercialOrUnavailable(paragraph.text))
      .filter((body) => body !== UNAVAILABLE_CONCLUSION)
      .slice(0, 6);
    if (paragraphs.length === 0) {
      const summaryBits = [
        narrative.summary?.identity,
        ...(narrative.summary?.strengths ?? []),
        narrative.summary?.priority_recommendation,
      ]
        .map((item) => commercialOrUnavailable(item))
        .filter((body) => body !== UNAVAILABLE_CONCLUSION);
      return {
        title: "Luận Giải",
        paragraphs:
          summaryBits.length > 0 ? summaryBits.slice(0, 6) : [UNAVAILABLE_CONCLUSION],
      };
    }
    return { title: "Luận Giải", paragraphs };
  }

  // Legacy fallback when Pack 05 NarrativeResult is absent.
  const sections = extractInterpretationSections(
    data.interpretation as Record<string, unknown> | undefined,
  );
  const paragraphs = sections
    .map((section) => commercialOrUnavailable(section.body))
    .filter((body) => body !== UNAVAILABLE_CONCLUSION)
    .slice(0, 6);

  return {
    title: "Luận Giải",
    paragraphs:
      paragraphs.length > 0 ? paragraphs : [UNAVAILABLE_CONCLUSION],
  };
}

function mapKnowledge(data: AnalysisDataDto): readonly BaZiKnowledgeItem[] {
  const pattern = data.pattern as Record<string, unknown> | undefined;
  const useful = canonicalUsefulGodPayload(data);
  const items: BaZiKnowledgeItem[] = [];
  const dm = asString(data.bazi?.day_master);
  if (dm) {
    items.push({
      id: "kn-day-master",
      title: "Nhật Chủ",
      reference: dm,
    });
  }
  const cach = asString(pattern?.cach_cuc);
  if (cach) {
    items.push({
      id: "kn-pattern",
      title: "Cách Cục",
      reference: cach,
    });
  }
  const dung = canonicalUsefulDisplay(useful, asString(pattern?.dung_than));
  if (dung) {
    items.push({
      id: "kn-useful-god",
      title: "Dụng Thần",
      reference: dung,
    });
  }
  if (items.length === 0) {
    return [
      {
        id: "kn-unavailable",
        title: "Kiến thức",
        reference: UNAVAILABLE_CONCLUSION,
      },
    ];
  }
  return items;
}

function mapShenSha(data: AnalysisDataDto): readonly BaZiShenShaItem[] {
  const entries = shenShaEntriesFromAnalysis(data);
  if (entries.length === 0) {
    return [
      {
        id: "ss-unavailable",
        name: "Thần Sát",
        tone: "Trung",
        note: UNAVAILABLE_CONCLUSION,
        present: false,
      },
    ];
  }
  return entries.map((item) => ({
    id: item.id,
    name: item.name,
    tone: "Trung" as const,
    note: item.evidence
      ? `${item.presence} · ${item.evidence}`
      : item.presence,
    present: true,
  }));
}

function mapSpiritGods(data: AnalysisDataDto): readonly BaZiSpiritGod[] {
  const pattern = data.pattern as Record<string, unknown> | undefined;
  const useful = canonicalUsefulGodPayload(data);
  const dung = canonicalUsefulDisplay(useful, asString(pattern?.dung_than));
  const hy = canonicalFavorableDisplay(useful, asString(pattern?.hy_than));
  const ky = canonicalUnfavorableDisplay(useful, asString(pattern?.ky_than));

  const rows: BaZiSpiritGod[] = [];
  if (dung) {
    rows.push({
      id: "dung",
      role: "dung",
      roleLabel: "Dụng Thần",
      name: dung,
      element: dung.toLowerCase(),
    });
  }
  if (hy) {
    rows.push({
      id: "hy",
      role: "hy",
      roleLabel: "Hỷ Thần",
      name: hy,
      element: hy.toLowerCase(),
    });
  }
  if (ky) {
    rows.push({
      id: "ky",
      role: "ky",
      roleLabel: "Kỵ Thần",
      name: ky,
      element: ky.toLowerCase(),
    });
  }
  if (rows.length === 0) {
    return [
      {
        id: "sg-unavailable",
        role: "dung",
        roleLabel: "Dụng Thần",
        name: UNAVAILABLE_CONCLUSION,
        element: "—",
      },
    ];
  }
  return rows;
}

function mapProfile(data: AnalysisDataDto, request?: AnalyzeChartRequest): BaZiProfile {
  const customer = data.customer;
  const year = request?.year;
  const month = request?.month;
  const day = request?.day;
  const hour = request?.hour ?? 0;
  const minute = request?.minute ?? 0;

  const lunarObj = data.calendar?.lunar;
  const lunarDate = asString(data.calendar?.lunar_date);
  const lunarParts = [
    lunarObj?.day ?? data.calendar?.lunar_day,
    lunarObj?.month ?? data.calendar?.lunar_month,
    lunarObj?.year ?? data.calendar?.lunar_year,
  ];
  const lunarNumeric = lunarParts.every((part) => part != null)
    ? `${String(lunarParts[0]).padStart(2, "0")}/${String(lunarParts[1]).padStart(2, "0")}/${lunarParts[2]}`
    : "";
  const lunar = lunarDate || lunarNumeric || "—";

  return {
    fullName: asString(customer?.full_name ?? request?.full_name, "—"),
    gender: customerGenderDisplay(customer, request?.gender),
    solarBirthDate:
      year && month && day ? formatSolarDate(year, month, day) : "—",
    lunarBirthDate: lunar,
    birthTime: year ? formatBirthTime(hour, minute) : "—",
    birthPlace: asString(customer?.birth_place ?? request?.birth_place, "—"),
  };
}

function mapMetadata(
  data: AnalysisDataDto,
  requestId: string | null | undefined,
): BaZiChartMetadata {
  const source = data.bazi_source as { engine?: string; rules?: string } | undefined;
  const interp = data.interpretation_source as { version?: string } | undefined;
  const now = new Date();
  const stamp = `${pad2(now.getDate())}/${pad2(now.getMonth() + 1)}/${now.getFullYear()} ${pad2(now.getHours())}:${pad2(now.getMinutes())}`;

  return {
    chartId: asString(requestId, `BZ-${now.getTime()}`),
    createdAt: stamp,
    analyzedAt: stamp,
    engineVersion: asString(source?.engine, "1.0.0"),
    ruleDatabaseVersion: asString(source?.rules, "1.0.0"),
    interpretationVersion: asString(interp?.version, "1.0.0"),
    analysisStatus: "Hoàn tất",
  };
}

export type AdaptBaZiResultOptions = {
  readonly request?: AnalyzeChartRequest;
  readonly requestId?: string | null;
  readonly status?: PresentationStatus;
  readonly errorMessage?: string;
};

/**
 * Adapt analyze `data` into the BaZi Result ViewModel.
 */
export function adaptAnalysisToBaZiResult(
  data: AnalysisDataDto,
  options: AdaptBaZiResultOptions = {},
): BaZiResultViewModel {
  const payload =
    asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  const pillars = PILLAR_SPECS.map((spec) =>
    mapPillar(data.bazi?.[spec.key], spec.kind, spec.label, payload),
  );

  const fiveElements = mapFiveElements(data);
  const tenGods = mapTenGods(data);
  const strength = mapStrength(data);
  const pattern = data.pattern as Record<string, unknown> | undefined;
  const useful = canonicalUsefulGodPayload(data);

  return {
    status: options.status ?? "ready",
    errorMessage: options.errorMessage,
    labels: BAZI_RESULT_LABELS,
    profile: mapProfile(data, options.request),
    metadata: mapMetadata(data, options.requestId),
    actions: BAZI_MOCK_ACTIONS,
    pillars,
    fiveElements,
    tenGods,
    tenGodsVisible: visibleLabels(payload),
    tenGodsHidden: hiddenLabels(payload),
    tenGodsNote: tenGodsNote(payload),
    strength,
    executive: buildExecutiveFromResult({
      strength,
      pillars,
      fiveElements,
      tenGods,
      gender: genderDisplayLabel(options.request?.gender ?? data.customer?.gender),
      yinYang: asString(data.bazi?.day_master_yin_yang) || undefined,
      dungThan: canonicalUsefulDisplay(useful, asString(pattern?.dung_than)) || undefined,
      hyThan: canonicalFavorableDisplay(useful, asString(pattern?.hy_than)) || undefined,
      kyThan: canonicalUnfavorableDisplay(useful, asString(pattern?.ky_than)) || undefined,
      pattern: asString(pattern?.cach_cuc ?? pattern?.pattern) || undefined,
      overallGrade: asString(data.score?.grade) || undefined,
      recommendation:
        asString(data.score?.recommendation) ||
        commercialOrUnavailable(
          extractInterpretationSections(
            data.interpretation as Record<string, unknown> | undefined,
          ).find((s) => /kết luận|dụng thần/i.test(s.title))?.body,
        ),
    }),
    spiritGods: mapSpiritGods(data),
    shenSha: mapShenSha(data),
    interpretation: mapInterpretation(data),
    knowledge: mapKnowledge(data),
  };
}

/** Empty / error ViewModel preserving labels for gates. */
export function createBaZiResultGateViewModel(
  status: PresentationStatus,
  errorMessage?: string,
): BaZiResultViewModel {
  const strength = {
    score: 0,
    maxScore: 100,
    label: "—",
    level: "—",
    confidence: 0,
    summary: "",
  };

  return {
    status,
    errorMessage,
    labels: BAZI_RESULT_LABELS,
    profile: {
      fullName: "—",
      gender: "—",
      solarBirthDate: "—",
      lunarBirthDate: "—",
      birthTime: "—",
      birthPlace: "—",
    },
    metadata: {
      chartId: "—",
      createdAt: "—",
      analyzedAt: "—",
      engineVersion: "—",
      ruleDatabaseVersion: "—",
      interpretationVersion: "—",
      analysisStatus: status === "loading" ? "Đang tải" : "—",
    },
    actions: BAZI_MOCK_ACTIONS,
    pillars: [],
    fiveElements: [],
    tenGods: [],
    strength,
    executive: buildExecutiveFromResult({
      strength,
      pillars: [],
      fiveElements: [],
      tenGods: [],
    }),
    spiritGods: [],
    shenSha: [],
    interpretation: { title: BAZI_RESULT_LABELS.interpretationTitle, paragraphs: [] },
    knowledge: [],
  };
}
