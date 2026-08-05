/**
 * Analysis API → BaZi Result ViewModel adapter (TASK_003A).
 * Components consume ViewModels only — never raw JSON.
 */

import type { AnalysisDataDto, AnalyzeChartRequest, PillarDto, SeriesItemDto } from "../models";
import {
  BAZI_MOCK_ACTIONS,
  BAZI_MOCK_INTERPRETATION,
  BAZI_MOCK_KNOWLEDGE,
  BAZI_MOCK_SHEN_SHA,
  BAZI_MOCK_SPIRIT_GODS,
  BAZI_RESULT_LABELS,
  buildExecutiveFromResult,
  type BaZiFiveElement,
  type BaZiPillar,
  type BaZiProfile,
  type BaZiChartMetadata,
  type BaZiResultMockBundle,
  type BaZiStrength,
  type BaZiTenGod,
  type PillarKind,
  type PresentationStatus,
} from "../screens/bazi/mockData";

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

function genderLabel(raw: string | null | undefined): string {
  const value = (raw ?? "").toLowerCase();
  if (value === "male" || value === "nam" || value === "m") {
    return "Nam";
  }
  if (value === "female" || value === "nu" || value === "nữ" || value === "f") {
    return "Nữ";
  }
  return raw ? String(raw) : "—";
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

function strengthBand(score: number): string {
  if (score >= 70) return "Mạnh";
  if (score >= 55) return "Khá";
  if (score >= 40) return "Trung bình";
  return "Yếu";
}

function mapStrengthLevel(level: string, score: number): { label: string; level: string } {
  const token = level
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  if (token.includes("vuong") || token.includes("strong") || token.includes("wang")) {
    return { label: "THÂN VƯỢNG", level: "Mạnh" };
  }
  if (token.includes("nhuoc") || token.includes("weak") || token.includes("ruo")) {
    return { label: "THÂN NHƯỢC", level: "Yếu" };
  }
  if (token.includes("balance") || token.includes("can bang") || token.includes("balanced")) {
    return { label: "CÂN BẰNG", level: "Trung bình" };
  }
  if (score >= 60) {
    return { label: "THÂN VƯỢNG", level: "Mạnh" };
  }
  if (score <= 40) {
    return { label: "THÂN NHƯỢC", level: "Yếu" };
  }
  return { label: "CÂN BẰNG", level: "Trung bình" };
}

function mapPillar(dto: PillarDto | undefined, kind: PillarKind, label: string): BaZiPillar {
  return {
    kind,
    label,
    heavenlyStem: asString(dto?.stem, "—"),
    earthlyBranch: asString(dto?.branch, "—"),
    hiddenStems: Array.isArray(dto?.hidden_stems) ? [...dto.hidden_stems] : [],
    naYin: asString(dto?.nap_am, "—"),
    twelveStage: asString(dto?.truong_sinh, "—"),
  };
}

function seriesValue(item: SeriesItemDto): number {
  if (typeof item.value === "number") return item.value;
  if (typeof item.count === "number") return item.count;
  if (typeof item.score === "number") return item.score;
  return 0;
}

function mapFiveElements(data: AnalysisDataDto): readonly BaZiFiveElement[] {
  const series = data.score?.wuxing_series;
  const scores: Record<string, number> = {
    Kim: 0,
    Mộc: 0,
    Thủy: 0,
    Hỏa: 0,
    Thổ: 0,
  };

  if (Array.isArray(series) && series.length > 0) {
    for (const item of series) {
      const name = normalizeElementName(asString(item.label ?? item.element ?? item.name));
      if (name in scores) {
        scores[name] = seriesValue(item);
      }
    }
  }

  const total = Object.values(scores).reduce((sum, n) => sum + n, 0) || 1;

  return ELEMENT_ORDER.map((el) => {
    const score = scores[el.name] ?? 0;
    const percentage = Math.round((score / total) * 100);
    return {
      id: el.id,
      name: el.name,
      score,
      percentage,
      strength: strengthBand(percentage),
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

function mapTenGods(data: AnalysisDataDto): readonly BaZiTenGod[] {
  const series = data.score?.ten_god_series;
  if (Array.isArray(series) && series.length > 0) {
    return series.map((item, index) => {
      const name = asString(item.label ?? item.name, `Thần ${index + 1}`);
      const score = seriesValue(item);
      return {
        id: slugify(name) || `god-${index}`,
        name,
        count: Math.max(1, Math.round(score)),
        score,
        strength: strengthBand(score),
        descriptionPreview: "",
      };
    });
  }

  const counts = new Map<string, number>();
  const fromList = data.bazi?.ten_gods ?? [];
  for (const god of fromList) {
    const name = asString(god).trim();
    if (!name || name === "Nhật Chủ") continue;
    counts.set(name, (counts.get(name) ?? 0) + 1);
  }

  const pillars = [
    data.bazi?.year_pillar,
    data.bazi?.month_pillar,
    data.bazi?.day_pillar,
    data.bazi?.hour_pillar,
  ];
  for (const pillar of pillars) {
    const name = asString(pillar?.ten_god).trim();
    if (!name || name === "Nhật Chủ") continue;
    counts.set(name, (counts.get(name) ?? 0) + 1);
  }

  return Array.from(counts.entries()).map(([name, count]) => ({
    id: slugify(name),
    name,
    count,
    score: count * 25,
    strength: strengthBand(count * 25),
    descriptionPreview: "",
  }));
}

function mapStrength(data: AnalysisDataDto): BaZiStrength {
  const strength = data.strength;
  const scoreRaw = strength?.strength_score ?? data.score?.strength_score ?? 0;
  const score = Math.round(Number(scoreRaw) || 0);
  const mapped = mapStrengthLevel(asString(strength?.strength_level), score);
  const confidenceRaw = strength?.confidence;
  const confidence =
    typeof confidenceRaw === "number"
      ? Math.round(confidenceRaw <= 1 ? confidenceRaw * 100 : confidenceRaw)
      : 0;

  return {
    score,
    maxScore: 100,
    label: mapped.label,
    level: mapped.level,
    confidence,
    summary: asString(strength?.reasoning, data.score?.recommendation ?? ""),
  };
}

function mapProfile(data: AnalysisDataDto, request?: AnalyzeChartRequest): BaZiProfile {
  const customer = data.customer;
  const year = request?.year;
  const month = request?.month;
  const day = request?.day;
  const hour = request?.hour ?? 0;
  const minute = request?.minute ?? 0;

  const lunar =
    [
      data.calendar?.day_can_chi,
      data.calendar?.month_can_chi,
      data.calendar?.year_can_chi,
    ]
      .filter(Boolean)
      .join(" · ") || "—";

  return {
    fullName: asString(customer?.full_name ?? request?.full_name, "—"),
    gender: genderLabel(customer?.gender ?? request?.gender),
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
  const pillars = PILLAR_SPECS.map((spec) =>
    mapPillar(data.bazi?.[spec.key], spec.kind, spec.label),
  );

  const fiveElements = mapFiveElements(data);
  const tenGods = mapTenGods(data);
  const strength = mapStrength(data);

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
    strength,
    executive: buildExecutiveFromResult({
      strength,
      pillars,
      fiveElements,
      tenGods,
    }),
    spiritGods: BAZI_MOCK_SPIRIT_GODS,
    shenSha: BAZI_MOCK_SHEN_SHA,
    interpretation: BAZI_MOCK_INTERPRETATION,
    knowledge: BAZI_MOCK_KNOWLEDGE,
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
