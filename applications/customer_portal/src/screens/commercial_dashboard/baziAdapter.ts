/**
 * Bind BaZi Card from canonical analysis. Copy published fields only.
 */

import type { AnalysisDataDto, BaziDto, IdentityPillarDto, PillarDto } from "../../models";
import {
  asTenGodsPayload,
  hiddenEntries,
  visibleEntryForPillar,
} from "../../adapters/tenGodsDisplay";
import { BAZI_TITLE } from "./cards";
import type { BaziHiddenStemView, BaziPillarKey, BaziPillarView, BaziStructureView } from "./types";

const PILLAR_KEYS: readonly BaziPillarKey[] = ["year", "month", "day", "hour"];
const PILLAR_LABELS: Record<BaziPillarKey, string> = {
  year: "Năm trụ",
  month: "Tháng trụ",
  day: "Ngày trụ",
  hour: "Giờ trụ",
};
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

function firstText(...values: unknown[]): string {
  for (const value of values) {
    const next = customerLabel(text(value));
    if (next) return next;
  }
  return "";
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function pillarOf(bazi: BaziDto | undefined, key: BaziPillarKey): PillarDto | undefined {
  if (!bazi) return undefined;
  if (key === "year") return bazi.year_pillar;
  if (key === "month") return bazi.month_pillar;
  if (key === "day") return bazi.day_pillar;
  return bazi.hour_pillar;
}

function hiddenFromPillar(pillar: PillarDto | undefined): string[] {
  if (!Array.isArray(pillar?.hidden_stems)) return [];
  return pillar.hidden_stems.map((item) => text(item)).filter(Boolean);
}

function bindHiddenStems(
  key: BaziPillarKey,
  pillar: PillarDto | undefined,
  tenGods: ReturnType<typeof asTenGodsPayload>,
): BaziHiddenStemView[] {
  const stems = hiddenFromPillar(pillar);
  const published = hiddenEntries(tenGods).filter((item) => item.pillar === key);
  if (stems.length) {
    return stems.map((stem) => {
      const match = published.find((item) => text(item.hidden_stem || item.stem) === stem);
      return { stem, tenGod: customerLabel(text(match?.ten_god)) };
    });
  }
  return published
    .map((item) => ({
      stem: firstText(item.hidden_stem, item.stem),
      tenGod: customerLabel(text(item.ten_god)),
    }))
    .filter((item) => item.stem);
}

function bindPillar(
  key: BaziPillarKey,
  identityRaw: IdentityPillarDto | undefined,
  pillar: PillarDto | undefined,
  tenGods: ReturnType<typeof asTenGodsPayload>,
  dayMaster: { readonly stem: string; readonly element: string; readonly yinYang: string },
): BaziPillarView {
  const identity = asRecord(identityRaw);
  const extra = asRecord(pillar);
  const visible = visibleEntryForPillar(tenGods, key);
  const stem = firstText(identity.stem, pillar?.stem);
  const isDay = key === "day";
  return {
    key,
    label: PILLAR_LABELS[key],
    stem,
    stemElement: firstText(
      extra.stem_element,
      pillar?.element,
      visible?.element,
      isDay ? dayMaster.element : "",
    ),
    stemYinYang: firstText(
      extra.stem_yin_yang,
      extra.yin_yang,
      asRecord(visible).yin_yang,
      isDay ? dayMaster.yinYang : "",
    ),
    branch: firstText(identity.branch, pillar?.branch),
    branchElement: firstText(extra.branch_element),
    napAm: firstText(pillar?.nap_am, identity.nayin_element),
    tenGod: firstText(pillar?.ten_god, visible?.ten_god),
    hiddenStems: bindHiddenStems(key, pillar, tenGods),
    truongSinh: firstText(pillar?.truong_sinh, extra.twelve_stage),
    isDayMaster: isDay,
  };
}

/**
 * Map published BaZi fields onto the structure card. Does not calculate astrology.
 */
export function adaptBaziCard(data: AnalysisDataDto | null | undefined): BaziStructureView {
  const payload = data ?? {};
  const identity = asRecord(payload.identity);
  const four = asRecord(identity.four_pillars);
  const bazi = payload.bazi;
  const tenGods = asTenGodsPayload(payload.ten_gods) ?? asTenGodsPayload(payload.ten_gods_result);
  const dayMaster = {
    stem: firstText(bazi?.day_master),
    element: firstText(bazi?.day_master_element),
    yinYang: firstText(bazi?.day_master_yin_yang),
  };
  const pillars = PILLAR_KEYS.map((key) =>
    bindPillar(
      key,
      four[key] as IdentityPillarDto | undefined,
      pillarOf(bazi, key),
      tenGods,
      dayMaster,
    ),
  );
  const available = pillars.some((pillar) => pillar.stem || pillar.branch);
  return { title: BAZI_TITLE, available, pillars };
}
