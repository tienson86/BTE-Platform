/**
 * Bind Ten Gods Card from canonical analysis. Copy published fields only.
 */

import type { AnalysisDataDto, BaziDto, PillarDto } from "../../models";
import {
  asTenGodsPayload,
  hiddenEntries,
  tenGodLabel,
} from "../../adapters/tenGodsDisplay";
import { TEN_GODS_TITLE } from "./cards";
import { tenGodCommercialAsset } from "./tenGodsCommercialAssets";
import {
  tenGodCombinationAsset,
  tenGodHiddenCombinationSupport,
} from "./tenGodsCombinationAssets";
import type {
  TenGodCombinationView,
  TenGodCommercialView,
  TenGodDetailedView,
  TenGodEcosystemView,
  TenGodRelationView,
  TenGodsPillarKey,
  TenGodsPlacementView,
  TenGodsPresenceView,
  TenGodsView,
} from "./types";

const PILLAR_KEYS: readonly TenGodsPillarKey[] = ["year", "month", "day", "hour"];
const PILLAR_LABELS: Record<TenGodsPillarKey, string> = {
  year: "Năm",
  month: "Tháng",
  day: "Ngày",
  hour: "Giờ",
};
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
const DAY_MASTER_LABEL = "Nhật Chủ";
const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;

function text(value: unknown): string {
  if (value == null) return "";
  return String(value).trim();
}

function customerLabel(value: string): string {
  const next = text(value);
  if (!next || TECHNICAL_TOKEN.test(next)) return "";
  return next;
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function isPillar(value: string): value is TenGodsPillarKey {
  return (PILLAR_KEYS as readonly string[]).includes(value);
}

function pillarOf(bazi: BaziDto | undefined, key: TenGodsPillarKey): PillarDto | undefined {
  if (!bazi) return undefined;
  if (key === "year") return bazi.year_pillar;
  if (key === "month") return bazi.month_pillar;
  if (key === "day") return bazi.day_pillar;
  return bazi.hour_pillar;
}

function fallbackVisible(bazi: BaziDto | undefined): TenGodsPlacementView[] {
  return PILLAR_KEYS.map((key) => {
    const tenGod = customerLabel(text(pillarOf(bazi, key)?.ten_god));
    if (!tenGod) return null;
    return {
      pillar: key,
      pillarLabel: PILLAR_LABELS[key],
      stem: customerLabel(text(pillarOf(bazi, key)?.stem)),
      tenGod,
      isDayMaster: key === "day" || tenGod === DAY_MASTER_LABEL,
    };
  }).filter((item): item is TenGodsPlacementView => Boolean(item));
}

function bindVisible(payload: ReturnType<typeof asTenGodsPayload>): TenGodsPlacementView[] {
  const visible = payload?.visible ?? [];
  const byPillar = new Map<TenGodsPillarKey, TenGodsPlacementView>();
  for (const item of visible) {
    const record = typeof item === "string" ? { ten_god: item } : asRecord(item);
    const pillarRaw = text(record.pillar);
    const pillar = isPillar(pillarRaw) ? pillarRaw : null;
    if (!pillar || byPillar.has(pillar)) continue;
    const tenGod = customerLabel(tenGodLabel(item));
    if (!tenGod) continue;
    byPillar.set(pillar, {
      pillar,
      pillarLabel: PILLAR_LABELS[pillar],
      stem: customerLabel(text(record.stem)),
      tenGod,
      isDayMaster: pillar === "day" || tenGod === DAY_MASTER_LABEL,
    });
  }
  return PILLAR_KEYS.map((key) => byPillar.get(key)).filter(
    (item): item is TenGodsPlacementView => Boolean(item),
  );
}

function bindHidden(payload: ReturnType<typeof asTenGodsPayload>): TenGodsPlacementView[] {
  return hiddenEntries(payload)
    .map((item) => {
      const pillarRaw = text(item.pillar);
      const pillar = isPillar(pillarRaw) ? pillarRaw : null;
      const tenGod = customerLabel(text(item.ten_god));
      if (!pillar || !tenGod || tenGod === DAY_MASTER_LABEL) return null;
      return {
        pillar,
        pillarLabel: PILLAR_LABELS[pillar],
        stem: customerLabel(text(item.hidden_stem || item.stem)),
        tenGod,
        isDayMaster: false,
      };
    })
    .filter((item): item is TenGodsPlacementView => Boolean(item));
}

function namesInOrder(names: Iterable<string>): string[] {
  const present = new Set(names);
  return TRADITIONAL_ORDER.filter((name) => present.has(name));
}

function bindCombination(visible: readonly TenGodsPlacementView[]): TenGodCombinationView | null {
  const names = visible.filter((item) => !item.isDayMaster).map((item) => item.tenGod);
  const asset = tenGodCombinationAsset(names);
  if (!asset) return null;
  return {
    title: asset.title,
    members: asset.members,
    insight: asset.insight,
    capability: asset.capability,
    income: asset.income,
    career: asset.career,
    leadership: asset.leadership,
    growth: asset.growth,
    risk: asset.risk,
    recommendation: asset.recommendation,
  };
}

function bindHiddenSupport(
  hidden: readonly TenGodsPlacementView[],
  visible: readonly TenGodsPlacementView[],
): string {
  const visibleNames = new Set(visible.map((item) => item.tenGod));
  const hiddenOnly = hidden
    .map((item) => item.tenGod)
    .filter((name) => name && !visibleNames.has(name));
  return tenGodHiddenCombinationSupport(hiddenOnly);
}

function bindCommercial(visible: readonly TenGodsPlacementView[]): TenGodCommercialView[] {
  const seen = new Set<string>();
  const cards: TenGodCommercialView[] = [];
  for (const item of visible) {
    if (item.isDayMaster || seen.has(item.tenGod)) continue;
    const asset = tenGodCommercialAsset(item.tenGod);
    if (!asset) continue;
    seen.add(item.tenGod);
    cards.push({
      name: item.tenGod,
      pillarLabel: item.pillarLabel,
      insight: asset.insight,
      capability: asset.capability,
      income: asset.income,
      career: asset.career,
      risk: asset.risk,
      recommendation: asset.recommendation,
    });
  }
  return cards;
}

function bindDistribution(
  visible: readonly TenGodsPlacementView[],
  hidden: readonly TenGodsPlacementView[],
): TenGodsPresenceView[] {
  const visibleNames = new Set(
    visible.map((item) => item.tenGod).filter((name) => name !== DAY_MASTER_LABEL),
  );
  const hiddenNames = new Set(hidden.map((item) => item.tenGod));
  return namesInOrder([...visibleNames, ...hiddenNames]).map((name) => ({
    name,
    visible: visibleNames.has(name),
    hidden: hiddenNames.has(name),
  }));
}

function bindDetailed(data: AnalysisDataDto | null | undefined): TenGodDetailedView[] {
  const items = data?.ten_gods?.detailed?.items ?? [];
  const cards: TenGodDetailedView[] = [];
  for (const item of items) {
    const name = customerLabel(text(item.name));
    if (!name) continue;
    cards.push({
      name,
      statusLabel: text(item.status_label),
      roleLabel: text(item.role_label),
      positives: (item.positives ?? []).map((value) => text(value)).filter(Boolean),
      risks: (item.risks ?? []).map((value) => text(value)).filter(Boolean),
      conditions: (item.conditions ?? []).map((value) => text(value)).filter(Boolean),
      unresolved: Boolean(item.unresolved),
      fallback: text(item.fallback) || "Chưa đủ dữ liệu để kết luận chi tiết",
    });
  }
  return cards;
}

function bindRelations(data: AnalysisDataDto | null | undefined): TenGodRelationView[] {
  const items = data?.ten_gods?.relations?.items ?? [];
  const rows: TenGodRelationView[] = [];
  for (const item of items) {
    const name = customerLabel(text(item.name));
    if (!name) continue;
    rows.push({
      name,
      stateLabel: text(item.state_label),
      mechanism: text(item.mechanism),
      condition: text(item.condition),
      unresolved: Boolean(item.unresolved),
      fallback: text(item.fallback) || "Chưa đủ dữ liệu để chốt",
    });
  }
  return rows;
}

function bindEcosystemRole(value: { label?: string; unresolved?: boolean } | undefined): {
  readonly label: string;
  readonly unresolved: boolean;
} {
  const unresolved = Boolean(value?.unresolved);
  const label = text(value?.label);
  return {
    label: label || (unresolved ? "Chưa đủ dữ liệu để chốt" : "Không áp dụng"),
    unresolved,
  };
}

function bindEcosystem(data: AnalysisDataDto | null | undefined): TenGodEcosystemView | null {
  const payload = data?.ten_gods?.ecosystem;
  if (!payload) return null;
  return {
    unresolved: Boolean(payload.unresolved),
    fallback: text(payload.fallback) || "Chưa đủ dữ liệu để chốt",
    driver: bindEcosystemRole(payload.driver),
    support: bindEcosystemRole(payload.support),
    bottleneck: bindEcosystemRole(payload.bottleneck),
    blocked: bindEcosystemRole(payload.blocked),
    suppressed: bindEcosystemRole(payload.suppressed),
    excessive: bindEcosystemRole(payload.excessive),
    deficient: bindEcosystemRole(payload.deficient),
    missing: bindEcosystemRole(payload.missing),
    flow: text(payload.flow) || "Chưa đủ dữ liệu để chốt",
    flowQuality: text(payload.flow_quality) || "Chưa đủ dữ liệu để chốt",
  };
}

/**
 * Map published Ten Gods onto the structure card. Does not calculate relationships.
 */
export function adaptTenGodsCard(data: AnalysisDataDto | null | undefined): TenGodsView {
  const payload = asTenGodsPayload(data?.ten_gods) ?? asTenGodsPayload(data?.ten_gods_result);
  const visible = bindVisible(payload);
  const hidden = bindHidden(payload);
  const placements = visible.length ? visible : fallbackVisible(data?.bazi);
  const available = placements.length > 0 || hidden.length > 0;
  const detailed = bindDetailed(data);
  const relations = bindRelations(data);
  const ecosystem = bindEcosystem(data);
  const usePack07 = detailed.length > 0;
  return {
    title: TEN_GODS_TITLE,
    available,
    featured: [],
    visible: placements,
    hidden,
    hiddenNames: namesInOrder(hidden.map((item) => item.tenGod)),
    distribution: bindDistribution(placements, hidden),
    combination: usePack07 ? null : bindCombination(placements),
    hiddenSupport: usePack07 ? "" : bindHiddenSupport(hidden, placements),
    commercial: usePack07 ? [] : bindCommercial(placements),
    detailed,
    relations: usePack07 ? relations : [],
    ecosystem: usePack07 ? ecosystem : null,
    summary: "",
  };
}
