/**
 * Bind Identity Header from canonical analysis payload. Copy only.
 */

import { genderDisplayLabel } from "../../adapters/genderDisplay";
import type { AnalysisDataDto, AnalyzeChartRequest, PillarDto } from "../../models";
import { CAN_XUONG_DETAIL_HREF, adaptCanXuong } from "./canXuongAdapter";
import type {
  IdentityHeaderView,
  IdentityPillarView,
  IdentityStatusView,
} from "./types";

export type AdaptIdentityOptions = {
  readonly request?: AnalyzeChartRequest | null;
  readonly analysisId?: string | null;
};

const EMPTY_PILLAR: IdentityPillarView = {
  stem: "",
  branch: "",
  canChi: "",
  napAm: "",
  cungPhi: "",
};

function text(value: unknown): string {
  if (value == null) return "";
  return String(value).trim();
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function firstText(...values: unknown[]): string {
  for (const value of values) {
    const next = text(value);
    if (next) return next;
  }
  return "";
}

function splitCanChi(canChi: string): { stem: string; branch: string } {
  const parts = canChi.split(/\s+/).filter(Boolean);
  if (parts.length >= 2) return { stem: parts[0]!, branch: parts[1]! };
  return { stem: canChi, branch: "" };
}

function publishedCanChi(stem: string, branch: string, ...candidates: unknown[]): string {
  const published = firstText(...candidates);
  if (published) return published;
  if (stem && branch) return `${stem} ${branch}`;
  return stem || branch;
}

function bindPillarCung(
  extra: Record<string, unknown>,
  route: Record<string, unknown>,
  cell: Record<string, unknown>,
  ruleVersion: string,
): string {
  const canonical = firstText(extra.cung_phi, route.cung_phi);
  if (canonical) return canonical;
  // G1-10C structured payloads must not fall back to Hạ Nguyên identity palaces.
  if (ruleVersion === "G1-10C" || ruleVersion.startsWith("G1-10")) {
    return "";
  }
  return firstText(cell.cung_phi);
}

function bindPillar(
  identityRaw: unknown,
  baziPillar: PillarDto | undefined,
  routeRaw: unknown,
  ruleVersion: string,
): IdentityPillarView {
  const cell = asRecord(identityRaw);
  const extra = asRecord(baziPillar);
  const route = asRecord(routeRaw);
  const labeled = splitCanChi(text(cell.can_chi));
  const stem = firstText(baziPillar?.stem, cell.stem, labeled.stem);
  const branch = firstText(baziPillar?.branch, cell.branch, labeled.branch);
  if (!stem && !branch && !cell.can_chi && !cell.cung_phi && !extra.cung_phi) return EMPTY_PILLAR;
  return {
    stem,
    branch,
    canChi: publishedCanChi(stem, branch, extra.can_chi, extra.ganzhi, cell.can_chi),
    // Tứ Trụ summary uses published Ngũ Hành only. Full nap_am stays on Bát Tự.
    napAm: firstText(cell.nayin_element),
    cungPhi: bindPillarCung(extra, route, cell, ruleVersion),
  };
}

function solarTermName(calendar: Record<string, unknown>): string {
  const term = calendar.solar_term;
  if (term && typeof term === "object") return text(asRecord(term).name);
  return text(term);
}

function formatAnalyzedAt(raw: string): string {
  if (!raw) return "";
  const parsed = new Date(raw);
  if (Number.isNaN(parsed.getTime())) return raw;
  return new Intl.DateTimeFormat("vi-VN", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(parsed);
}

function bindStatus(
  data: AnalysisDataDto,
  options: AdaptIdentityOptions,
  extra: {
    readonly cungPhi: string;
    readonly menhQuai: string;
    readonly nhomTrach: string;
    readonly tietKhi: string;
    readonly tamNguyen: string;
    readonly cuuVan: string;
  },
): IdentityStatusView {
  const meta = asRecord(data.result_meta);
  const confidence = firstText(data.score?.confidence);
  return {
    analysisId: firstText(options.analysisId, data.analysis_id, meta.analysis_id),
    version: firstText(meta.release_label),
    analyzedAt: formatAnalyzedAt(firstText(meta.created_at, meta.analyzed_at)),
    confidence,
    cungPhi: extra.cungPhi,
    menhQuai: extra.menhQuai,
    nhomTrach: extra.nhomTrach,
    tietKhi: extra.tietKhi,
    tamNguyen: extra.tamNguyen,
    cuuVan: extra.cuuVan,
  };
}

/**
 * Map published analysis fields onto the Identity Header view.
 */
export function adaptIdentityHeader(
  data: AnalysisDataDto | null | undefined,
  options: AdaptIdentityOptions = {},
): IdentityHeaderView {
  const payload = data ?? {};
  const identity = asRecord(payload.identity);
  const person = asRecord(identity.person);
  const customer = payload.customer;
  const calendar = asRecord(payload.calendar);
  const identityCalendar = asRecord(identity.calendar);
  const feng = asRecord(payload.feng_shui);
  const four = asRecord(identity.four_pillars);
  const bazi = payload.bazi;
  const request = options.request;
  const routing = asRecord(calendar.ganzhi_routing);
  const ruleVersion = text(calendar.calendar_rule_version);
  const year = bindPillar(four.year, bazi?.year_pillar, routing.year, ruleVersion);
  const month = bindPillar(four.month, bazi?.month_pillar, routing.month, ruleVersion);
  const day = bindPillar(four.day, bazi?.day_pillar, routing.day, ruleVersion);
  const hour = bindPillar(four.hour, bazi?.hour_pillar, routing.hour, ruleVersion);
  const genderRaw = firstText(person.gender, customer?.gender, request?.gender);
  const canXuong = adaptCanXuong(payload);
  const cungPhi = firstText(calendar.cung_phi, feng.cung_phi, feng.gua_name);
  const menhQuai = firstText(calendar.menh_quai, feng.menh_quai, cungPhi);
  const nhomTrach = firstText(
    calendar.house_group,
    calendar.nhom_trach,
    feng.house_group,
    feng.nhom_trach,
  );
  return {
    person: {
      fullName: firstText(person.full_name, customer?.full_name, request?.full_name),
      gender: genderRaw ? genderDisplayLabel(genderRaw) : "",
      solarBirth: firstText(person.solar_birth, calendar.solar_date, identityCalendar.solar_date),
      lunarBirth: firstText(person.lunar_birth, calendar.lunar_date, identityCalendar.lunar_date),
      birthTime: firstText(person.birth_time, request && `${String(request.hour ?? 0).padStart(2, "0")}:${String(request.minute ?? 0).padStart(2, "0")}`),
      birthPlace: firstText(person.birth_place, customer?.birth_place, request?.birth_place),
    },
    pillars: { year, month, day, hour },
    dayMaster: {
      stem: firstText(bazi?.day_master, day.stem),
      element: firstText(bazi?.day_master_element),
      yinYang: firstText(bazi?.day_master_yin_yang),
    },
    foundation: {
      available: canXuong.available,
      displayWeight: canXuong.displayWeight,
      weight: canXuong.displayWeight,
      classification: canXuong.classification,
      rating: canXuong.rating,
      summary: canXuong.summary,
      interpretation: canXuong.interpretation,
      detailHref: canXuong.detailHref || CAN_XUONG_DETAIL_HREF,
    },
    status: bindStatus(payload, options, {
      cungPhi,
      menhQuai,
      nhomTrach,
      tietKhi: firstText(identityCalendar.solar_term, solarTermName(calendar)),
      tamNguyen: firstText(calendar.tam_nguyen),
      cuuVan: firstText(calendar.cuu_van),
    }),
  };
}

/**
 * True when the pillar stem is the published Day Master.
 */
export function isDayMasterPillar(stem: string, dayMasterStem: string): boolean {
  return Boolean(stem) && Boolean(dayMasterStem) && stem.trim() === dayMasterStem.trim();
}
