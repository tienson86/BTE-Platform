/**
 * Canonical current-result routing — tests A–L.
 */

import { describe, expect, it } from "vitest";
import {
  adaptAnalysisToCanonicalDesktop,
} from "../../src/adapters/canonicalDesktopAdapter";
import { adaptResultPageViewModel } from "../../src/screens/result/adapters/resultPresentationAdapter";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  analyticalFiveElementCounts,
  analyticalTenGods,
  hasStructuredAnalysis,
  isHistoryViewSearch,
  resolveCurrentStoredResult,
  type StoredResultRecord,
} from "../../src/resultState/currentResult";
import type { AnalysisDataDto } from "../../src/models";

const HUYNH: AnalysisDataDto = {
  analysis_id: "bte-huynh-1966-fresh",
  calendar: {
    lunar_date: "10/08/1966",
    lunar: { year: 1966, month: 8, day: 10, is_leap_month: false },
    year_can_chi: "Bính Ngọ",
  },
  bazi: {
    year_pillar: { stem: "Bính", branch: "Ngọ" },
    month_pillar: { stem: "Đinh", branch: "Dậu" },
    day_pillar: { stem: "Kỷ", branch: "Mùi" },
    hour_pillar: { stem: "Bính", branch: "Dần" },
    day_master: "Kỷ",
    ten_gods: ["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"],
  },
  pattern: {
    cach_cuc: "Chính Tài",
    than_vuong_nhuoc: "Thân vượng",
  },
  useful_god: {
    useful_god: "Đinh",
    favorable_gods: ["Đinh", "Bính", "Ất"],
    unfavorable_gods: ["Canh", "Tân"],
  },
  five_elements: {
    wood: { count: 2 },
    fire: { count: 7 },
    earth: { count: 4 },
    metal: { count: 4 },
    water: { count: 0 },
    counts: { wood: 2, fire: 7, earth: 4, metal: 4, water: 0 },
  },
  ten_gods: { visible: ["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"] },
  luck: {
    available: true,
    start_age: 5,
    current_cycle: { gan_zhi: "Quý Mão", year_start: 2021, year_end: 2030 },
    cycles: [
      { gan_zhi: "Mậu Tuất", year_start: 1971, year_end: 1980 },
      { gan_zhi: "Kỷ Hợi", year_start: 1981, year_end: 1990 },
      { gan_zhi: "Canh Tý", year_start: 1991, year_end: 2000 },
      { gan_zhi: "Tân Sửu", year_start: 2001, year_end: 2010 },
      { gan_zhi: "Nhâm Dần", year_start: 2011, year_end: 2020 },
      { gan_zhi: "Quý Mão", year_start: 2021, year_end: 2030 },
      { gan_zhi: "Giáp Thìn", year_start: 2031, year_end: 2040 },
      { gan_zhi: "Ất Tỵ", year_start: 2041, year_end: 2050 },
      { gan_zhi: "Bính Ngọ", year_start: 2051, year_end: 2060 },
      { gan_zhi: "Đinh Mùi", year_start: 2061, year_end: 2070 },
    ],
  },
  feng_shui: {
    cung_phi: "Đoài",
    menh_quai: "Đoài",
    nhom_trach: "Tây Tứ Trạch",
  },
  strength: { strength_level: "strong", strength_score: 0.66 },
  score: {
    total_score: 61.25,
    grade: "C",
    wuxing_series: [{ label: "Ngũ hành", value: 0 }],
    ten_god_series: [{ label: "Thập thần", value: 100 }],
  },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    status: "ok",
    summary: {
      identity: "Nhật chủ Kỷ · Cách cục Chính Tài",
      strengths: ["Thân vượng"],
      weaknesses: [],
      priority_recommendation: "Ưu tiên Đinh",
      next_action: "Ưu tiên Đinh",
    },
    sections: [
      { id: "sec-exec", intent: "executive_summary", title: "Executive Summary", paragraphs: [{ role: "observation", text: "Tóm tắt tư vấn từ NarrativeResult." }] },
      { id: "sec-obs", intent: "observation", title: "Observation", paragraphs: [{ role: "observation", text: "Quan sát mệnh cục hiện tại." }] },
      { id: "sec-reason", intent: "reasoning", title: "Reasoning", paragraphs: [{ role: "explanation", text: "Lý giải từ Dụng thần Đinh." }] },
      { id: "sec-impact", intent: "impact", title: "Impact", paragraphs: [{ role: "impact", text: "Ảnh hưởng nghề và vận." }] },
      { id: "sec-rec", intent: "recommendation", title: "Recommendation", paragraphs: [{ role: "suggestion", text: "Ưu tiên Đinh Bính Ất." }] },
      { id: "sec-warn", intent: "warning", title: "Warning", paragraphs: [{ role: "warning", text: "Tránh Canh Tân." }] },
      { id: "sec-end", intent: "conclusion", title: "Conclusion", paragraphs: [{ role: "conclusion", text: "Kết luận NarrativeResult." }] },
    ],
  },
  customer: { full_name: "Lương Ngọc Huỳnh", gender: "male" },
};

const FRESH: StoredResultRecord = {
  analysis_id: "bte-huynh-1966-fresh",
  input: { year: 1966, month: 9, day: 24, hour: 4, minute: 15, gender: "male", full_name: "Lương Ngọc Huỳnh" },
  data: HUYNH,
};

const STALE: StoredResultRecord = {
  analysis_id: "bte-stale-old",
  input: { year: 1990, month: 1, day: 1, hour: 0, minute: 0, full_name: "Stale" },
  data: {
    calendar: { lunar_date: "01/01/1990" },
    pattern: { than_vuong_nhuoc: "Trung hòa" },
    score: { total_score: 54.25, grade: "D+", wuxing_series: [{ label: "Ngũ hành", value: 0 }], ten_god_series: [{ label: "Thập thần", value: 100 }] },
    report: { html: "<p>legacy stale</p>", markdown: "legacy stale" },
  },
};

function pageModel(record: StoredResultRecord) {
  const boot = resolveResultBoot(record, "", null);
  expect(boot.initialData).toBeDefined();
  return adaptResultPageViewModel(boot.initialData!, boot.fullReport);
}

describe("canonical current-result routing", () => {
  it("A. fresh analyze response becomes canonical current result", () => {
    const resolved = resolveCurrentStoredResult({
      current: FRESH,
      historyView: STALE,
      fromHistory: false,
    });
    expect(resolved?.analysisId).toBe("bte-huynh-1966-fresh");
    expect(resolved?.source).toBe("current");
    expect(resolved?.data.useful_god?.useful_god).toBe("Đinh");
  });

  it("B. /result reads current result, not stale history", () => {
    expect(isHistoryViewSearch("")).toBe(false);
    const boot = resolveResultBoot(FRESH, "", STALE);
    expect(boot.analysisId).toBe("bte-huynh-1966-fresh");
    expect(boot.initialData?.s05.level).toBe("Thân vượng");
    expect(boot.initialData?.s00.birth.lunar).toContain("10/08/1966");
  });

  it("C. Luận giải uses same analysis ID as /result", () => {
    const resultBoot = resolveResultBoot(FRESH, "", null);
    const luanGiaiBoot = resolveResultBoot(FRESH, "", null);
    expect(luanGiaiBoot.analysisId).toBe(resultBoot.analysisId);
    const vm = adaptResultPageViewModel(luanGiaiBoot.initialData!);
    expect(vm.interpretation.blocks.map((block) => block.title)).toEqual(
      expect.arrayContaining([
        "Tóm tắt điều hành",
        "Quan sát",
        "Lý giải",
        "Tác động",
        "Khuyến nghị",
        "Lưu ý",
        "Kết luận",
      ]),
    );
  });

  it("D. Báo cáo uses same analysis ID as /result", () => {
    const resultId = resolveResultBoot(FRESH, "", null).analysisId;
    expect(hasStructuredAnalysis(FRESH.data)).toBe(true);
    expect(FRESH.analysis_id).toBe(resultId);
  });

  it("E. export uses same analysis ID / current result", () => {
    const resolved = resolveCurrentStoredResult({
      current: FRESH,
      historyView: STALE,
      fromHistory: false,
    });
    expect(resolved?.analysisId).toBe("bte-huynh-1966-fresh");
    expect(STALE.data?.report?.html).toContain("legacy stale");
    expect(hasStructuredAnalysis(resolved?.data)).toBe(true);
    expect(resolved?.data.report).toBeUndefined();
  });

  it("F. Five Elements uses analytical distribution, not wuxing_score", () => {
    const counts = analyticalFiveElementCounts(HUYNH);
    expect(counts).toEqual({ Mộc: 2, Hỏa: 7, Thổ: 4, Kim: 4, Thủy: 0 });
    const vm = pageModel(FRESH);
    expect(vm.fiveElements.rows.items.map((row) => `${row.name} ${row.count}`)).toEqual([
      "Mộc 2",
      "Hỏa 7",
      "Thổ 4",
      "Kim 4",
      "Thủy 0",
    ]);
    expect(vm.fiveElements.rows.items.some((row) => row.count === 0 && row.name === "Thủy")).toBe(true);
    expect(vm.fiveElements.rows.items.every((row) => row.count !== 100)).toBe(true);
  });

  it("G. Ten Gods uses analytical values, not ten_god_score", () => {
    expect(analyticalTenGods(HUYNH)).toEqual(["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"]);
    const vm = pageModel(FRESH);
    expect(vm.tenGods.gods.items.map((god) => god.name)).toEqual(
      expect.arrayContaining(["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"]),
    );
    expect(vm.tenGods.gods.items.some((god) => god.score === "100" || god.name === "Thập thần")).toBe(false);
  });

  it("H. Luck survives route navigation", () => {
    const resultVm = pageModel(FRESH);
    const reportVm = pageModel(FRESH);
    expect(resultVm.analysisId).toBe(reportVm.analysisId);
    expect(resultVm.timeline.stages.items).toHaveLength(10);
    expect(resultVm.timeline.summary.text).toContain("Quý Mão");
    expect(resultVm.timeline.summary.text).toContain("2021");
    expect(reportVm.timeline.stages.items.map((stage) => stage.label).join(" ")).toContain("Mậu Tuất");
  });

  it("I. Feng Shui survives route navigation", () => {
    const resultVm = pageModel(FRESH);
    const reportVm = pageModel(FRESH);
    expect(resultVm.context.cungPhi).toContain("Đoài");
    expect(resultVm.context.menhQuai).toContain("Đoài");
    expect(resultVm.context.nhomTrach).toContain("Tây Tứ Trạch");
    expect(reportVm.context.cungPhi).toBe(resultVm.context.cungPhi);
  });

  it("J. Lunar date survives route navigation", () => {
    const resultVm = pageModel(FRESH);
    const luanVm = pageModel(FRESH);
    expect(resultVm.context.birthLunar).toContain("10/08/1966");
    expect(luanVm.context.birthLunar).toBe(resultVm.context.birthLunar);
    expect(resultVm.context.birthLunar).not.toMatch(/10\/08\/Bính|Kỷ Mùi/);
  });

  it("K. NarrativeResult remains the narrative source", () => {
    const vm = pageModel(FRESH);
    expect(vm.interpretation.blocks.some((block) => block.observation.text.includes("NarrativeResult"))).toBe(true);
    const desktop = adaptAnalysisToCanonicalDesktop(HUYNH, {
      request: { year: 1966, month: 9, day: 24, hour: 4, minute: 15, gender: "male" },
      source: "api",
    });
    expect(desktop.narrativeResult?.contract).toBe("pack05_narrative_result_v1");
    expect(desktop.s08.executive.body).not.toContain("Career Selection Assessment");
  });

  it("L. explicit History selection still works without overriding fresh current", () => {
    const current = resolveCurrentStoredResult({
      current: FRESH,
      historyView: STALE,
      fromHistory: false,
    });
    const history = resolveCurrentStoredResult({
      current: FRESH,
      historyView: STALE,
      fromHistory: true,
    });
    expect(isHistoryViewSearch("?from=history")).toBe(true);
    expect(current?.analysisId).toBe("bte-huynh-1966-fresh");
    expect(history?.analysisId).toBe("bte-stale-old");
    expect(history?.source).toBe("history");
    const currentAfterHistoryFlag = resolveCurrentStoredResult({
      current: FRESH,
      historyView: STALE,
      fromHistory: false,
    });
    expect(currentAfterHistoryFlag?.analysisId).toBe("bte-huynh-1966-fresh");
  });
});
