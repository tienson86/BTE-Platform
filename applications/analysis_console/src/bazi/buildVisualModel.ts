import type { AnalysisData, ChartData } from "../api/types";
import {
  BRANCH_CLASH,
  BRANCH_COMBINATION_TRIADS,
  BRANCH_INFO,
  DEFAULT_BRANCH_FOR_STEM,
  ELEMENT_ORDER,
  PILLAR_KEYS,
  PILLAR_LABELS,
  STEM_INFO,
  tenGodOf,
  type ElementId,
  type PillarKey,
} from "./knowledge";

export type VisualPillar = {
  key: PillarKey;
  label: string;
  stem: string;
  branch: string;
  stem_element: ElementId | null;
  branch_element: ElementId | null;
  hidden_stems: string[];
  ten_god: string;
  season: string;
};

export type VisualLuckPillar = {
  id: string;
  label: string;
  stem: string;
  branch: string;
  stem_element: ElementId | null;
  meta: string;
  active: boolean;
};

export type VisualRelation = {
  id: string;
  kind: "clash" | "combination";
  label: string;
  pillars: PillarKey[];
};

export type VisualBaZiModel = {
  day_master: string;
  pillars: VisualPillar[];
  elements: Record<ElementId, number>;
  strength: string;
  useful_gods: string[];
  season: string;
  relations: VisualRelation[];
  luck_pillars: VisualLuckPillar[];
  analysis_available: boolean;
};

type DomainSummary = {
  payload_digest?: Record<string, unknown>;
};

function asRecord(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object"
    ? (value as Record<string, unknown>)
    : null;
}

function digestOf(
  summary: Record<string, unknown> | null | undefined,
  key: string,
): Record<string, unknown> {
  const domain = asRecord(summary?.[key]) as DomainSummary | null;
  return asRecord(domain?.payload_digest) ?? {};
}

function resolveBranch(stem: string, provided?: string): string {
  if (provided && BRANCH_INFO[provided]) return provided;
  return DEFAULT_BRANCH_FOR_STEM[stem] ?? "Thìn";
}

export function buildVisualBaZiModel(
  chart: ChartData,
  analysis: AnalysisData | null,
): VisualBaZiModel {
  const dayMaster = chart.chart.day_master;
  const stems = chart.chart.stems ?? {};
  const branches =
    (chart.chart as { branches?: Record<string, string> }).branches ?? {};

  const pillars: VisualPillar[] = PILLAR_KEYS.map((key) => {
    const stem = stems[key] ?? (key === "day" ? dayMaster : "—");
    const branch = resolveBranch(stem, branches[key]);
    const stemInfo = STEM_INFO[stem];
    const branchInfo = BRANCH_INFO[branch];
    return {
      key,
      label: PILLAR_LABELS[key],
      stem,
      branch,
      stem_element: stemInfo?.element ?? null,
      branch_element: branchInfo?.element ?? null,
      hidden_stems: branchInfo?.hidden ?? [],
      ten_god: key === "day" ? "Nhật Chủ" : tenGodOf(dayMaster, stem),
      season: branchInfo?.season ?? "—",
    };
  });

  const elements = Object.fromEntries(
    ELEMENT_ORDER.map((el) => [el, 0]),
  ) as Record<ElementId, number>;

  for (const pillar of pillars) {
    if (pillar.stem_element) elements[pillar.stem_element] += 1;
    if (pillar.branch_element) elements[pillar.branch_element] += 1;
    for (const hidden of pillar.hidden_stems) {
      const info = STEM_INFO[hidden];
      if (info) elements[info.element] += 0.5;
    }
  }

  const monthPillar = pillars.find((p) => p.key === "month");
  const season = monthPillar?.season ?? "—";

  const summary = asRecord(analysis?.summary);
  const strengthDigest = digestOf(summary, "strength_summary");
  const usefulDigest = digestOf(summary, "useful_god_summary");
  const combinationDigest = digestOf(summary, "combination_summary");

  const strength =
    typeof strengthDigest.classification === "string"
      ? strengthDigest.classification
      : analysis
        ? "unknown"
        : "pending";

  const useful_gods = Array.isArray(usefulDigest.useful_gods)
    ? usefulDigest.useful_gods.map(String)
    : [];

  const relations = detectRelations(pillars);
  if (
    Array.isArray(combinationDigest.clashes) &&
    combinationDigest.clashes.length > 0
  ) {
    relations.push({
      id: "analysis-clashes",
      kind: "clash",
      label: `Analysis clashes: ${combinationDigest.clashes.length}`,
      pillars: [],
    });
  }

  const luck = asRecord(chart.chart.luck) ?? {};
  const sequence = Array.isArray(luck.da_yun_sequence)
    ? luck.da_yun_sequence
    : [];
  const currentAge =
    typeof luck.current_age === "number" ? luck.current_age : null;
  const currentIndex =
    currentAge == null
      ? -1
      : sequence.findIndex((item) => {
          const row = asRecord(item);
          if (!row) return false;
          const start = Number(row.start_age ?? Number.NaN);
          const end = Number(row.end_age ?? Number.NaN);
          if (Number.isNaN(start) || Number.isNaN(end)) return false;
          return currentAge >= start && currentAge <= end;
        });

  const luck_pillars: VisualLuckPillar[] = sequence.map((item, index) => {
    const row = asRecord(item) ?? {};
    const stem = String(row.stem ?? "—");
    const branch = String(row.branch ?? "—");
    return {
      id: String(row.label ?? `dy${index}`),
      label: String(row.label ?? `Đại vận ${index}`),
      stem,
      branch,
      stem_element: STEM_INFO[stem]?.element ?? null,
      meta: `Ages ${row.start_age ?? "—"}–${row.end_age ?? "—"}`,
      active: index === currentIndex || Boolean(row.active),
    };
  });

  return {
    day_master: dayMaster,
    pillars,
    elements,
    strength,
    useful_gods,
    season,
    relations,
    luck_pillars,
    analysis_available: Boolean(analysis),
  };
}

function detectRelations(pillars: VisualPillar[]): VisualRelation[] {
  const relations: VisualRelation[] = [];
  for (let i = 0; i < pillars.length; i += 1) {
    for (let j = i + 1; j < pillars.length; j += 1) {
      const a = pillars[i];
      const b = pillars[j];
      if (BRANCH_CLASH[a.branch] === b.branch) {
        relations.push({
          id: `clash-${a.key}-${b.key}`,
          kind: "clash",
          label: `${a.label} ↔ ${b.label} clash (${a.branch}/${b.branch})`,
          pillars: [a.key, b.key],
        });
      }
    }
  }

  const branchSet = new Set(pillars.map((p) => p.branch));
  BRANCH_COMBINATION_TRIADS.forEach((triad, index) => {
    const hit = triad.filter((branch) => branchSet.has(branch));
    if (hit.length >= 2) {
      const keys = pillars
        .filter((p) => hit.includes(p.branch))
        .map((p) => p.key);
      relations.push({
        id: `combo-${index}`,
        kind: "combination",
        label: `Combination signal: ${hit.join(" · ")}`,
        pillars: keys,
      });
    }
  });

  return relations;
}
