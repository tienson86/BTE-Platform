/**
 * Full canonical report composition — tests A–L.
 */

import { describe, expect, it } from "vitest";
import {
  buildFullReportViewModel,
  isFullCustomerReport,
  renderFullReportHtml,
} from "../../src/report/fullReportViewModel";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { resolveCurrentStoredResult } from "../../src/resultState/currentResult";
import type { AnalysisDataDto } from "../../src/models";
import type { StoredResultRecord } from "../../src/resultState/currentResult";

const HUYNH: AnalysisDataDto = {
  analysis_id: "bte-huynh-1966-fresh",
  calendar: {
    lunar_date: "10/08/1966",
    solar_date: "24/09/1966",
    cung_phi: "Đoài",
    menh_quai: "Đoài",
    nhom_trach: "Tây Tứ Trạch",
  },
  bazi: {
    year_pillar: {
      stem: "Bính",
      branch: "Ngọ",
      nap_am: "Thiên Hà Thủy",
      hidden_stems: ["Đinh", "Kỷ"],
      ten_god: "Thiên Tài",
      truong_sinh: "Đế Vượng",
    },
    month_pillar: {
      stem: "Đinh",
      branch: "Dậu",
      nap_am: "Sa Trung Kim",
      hidden_stems: ["Tân"],
      ten_god: "Thiên Ấn",
      truong_sinh: "Lâm Quan",
    },
    day_pillar: {
      stem: "Kỷ",
      branch: "Mùi",
      nap_am: "Lộ Bàng Thổ",
      hidden_stems: ["Kỷ", "Đinh", "Ất"],
      ten_god: "Nhật Chủ",
      truong_sinh: "Mộ",
    },
    hour_pillar: {
      stem: "Bính",
      branch: "Dần",
      nap_am: "Lư Trung Hỏa",
      hidden_stems: ["Giáp", "Bính", "Mậu"],
      ten_god: "Thiên Tài",
      truong_sinh: "Trường Sinh",
    },
    day_master: "Kỷ",
    day_master_element: "Thổ",
    day_master_yin_yang: "Âm",
    ten_gods: ["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"],
    shensha: ["Thiên Ất Quý Nhân", "Hoa Cái"],
  },
  pattern: { cach_cuc: "Chính Tài", than_vuong_nhuoc: "Thân vượng" },
  useful_god: {
    useful_god: "Đinh",
    useful_display: "Đinh",
    favorable_gods: ["Đinh", "Bính", "Ất"],
    favorable_display: "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng",
    unfavorable_gods: ["Canh", "Tân"],
    unfavorable_display: "Canh, Tân",
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
  strength: { strength_level: "strong", strength_score: 0.66 },
  score: {
    total_score: 61.25,
    grade: "C",
    wuxing_series: [{ label: "Ngũ hành", value: 0 }],
    ten_god_series: [{ label: "Thập thần", value: 100 }],
  },
  report: { html: "<p>STALE Trung hòa 54.25 D+</p>", markdown: "STALE" },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    status: "ok",
    sections: [
      { id: "sec-exec", intent: "executive_summary", title: "Executive Summary", paragraphs: [{ text: "Tóm tắt tư vấn từ NarrativeResult." }] },
      { id: "sec-obs", intent: "observation", title: "Observation", paragraphs: [{ text: "Quan sát mệnh cục hiện tại." }] },
      { id: "sec-reason", intent: "reasoning", title: "Reasoning", paragraphs: [{ text: "Lý giải từ Dụng thần Đinh." }] },
      { id: "sec-impact", intent: "impact", title: "Impact", paragraphs: [{ text: "Ảnh hưởng nghề và vận." }] },
      { id: "sec-rec", intent: "recommendation", title: "Recommendation", paragraphs: [{ text: "Ưu tiên Đinh Bính Ất." }] },
      { id: "sec-warn", intent: "warning", title: "Warning", paragraphs: [{ text: "Tránh Canh Tân." }] },
      { id: "sec-end", intent: "conclusion", title: "Conclusion", paragraphs: [{ text: "Kết luận NarrativeResult." }] },
    ],
  },
  customer: { full_name: "Lương Ngọc Huỳnh", gender: "male", birth_place: "Hà Nội" },
};

const FRESH: StoredResultRecord = {
  analysis_id: "bte-huynh-1966-fresh",
  input: { year: 1966, month: 9, day: 24, hour: 4, minute: 15, gender: "male", full_name: "Lương Ngọc Huỳnh" },
  data: HUYNH,
};

function model() {
  return buildFullReportViewModel(HUYNH, {
    input: FRESH.input,
    analysisId: "bte-huynh-1966-fresh",
  });
}

describe("full canonical report composition", () => {
  it("A. structured current data exists AND narrative sections are rendered", () => {
    const report = model();
    const html = renderFullReportHtml(report);
    expect(report.fiveElements.map((row) => row.count)).toEqual([2, 7, 4, 4, 0]);
    expect(html).toContain("data-narrative=\"pack05\"");
    expect(html).toContain("Tóm tắt tư vấn từ NarrativeResult.");
  });

  it("B. full report does not collapse to facts-only when structured data exists", () => {
    const report = model();
    const html = renderFullReportHtml(report);
    expect(report.factsOnly).toBe(false);
    expect(isFullCustomerReport(report)).toBe(true);
    expect(html).toContain("Tứ trụ / Bát Tự");
    expect(html).toContain("Luận giải");
    expect(html).not.toMatch(/<table>[\s\S]*analysis_id[\s\S]*<\/table>\s*<\/body>/);
  });

  it("C. all 7 NarrativeResult sections survive into full report", () => {
    const titles = model().narrative.map((section) => section.title);
    expect(titles).toEqual([
      "Tóm tắt điều hành",
      "Quan sát",
      "Lý giải",
      "Tác động",
      "Khuyến nghị",
      "Lưu ý",
      "Kết luận",
    ]);
    expect(model().narrative.every((section) => section.present)).toBe(true);
  });

  it("D. Four Pillars survive", () => {
    const pillars = model().pillars;
    expect(pillars).toHaveLength(4);
    expect(pillars.map((pillar) => pillar.stem)).toEqual(["Bính", "Đinh", "Kỷ", "Bính"]);
    expect(pillars[0].napAm).toBe("Thiên Hà Thủy");
    expect(pillars[2].hiddenStems).toContain("Kỷ");
    expect(pillars[3].growthStage).toBe("Trường Sinh");
  });

  it("E. Shen Sha survive", () => {
    expect(model().shenSha.map((item) => item.name)).toEqual(["Thiên Ất Quý Nhân", "Hoa Cái"]);
    expect(renderFullReportHtml(model())).toContain("Thiên Ất Quý Nhân");
  });

  it("F. Da Yun 10 cycles survive", () => {
    expect(model().luckCycles).toHaveLength(10);
    expect(model().luckCurrent).toContain("Quý Mão");
    expect(model().luckCurrent).toContain("2021–2030");
    expect(renderFullReportHtml(model())).toContain("Mậu Tuất");
  });

  it("G. Feng Shui survives", () => {
    expect(model().cungPhi).toBe("Đoài");
    expect(model().menhQuai).toBe("Đoài");
    expect(model().nhomTrach).toBe("Tây Tứ Trạch");
  });

  it("H. P0/P1 values remain correct", () => {
    const report = model();
    expect(report.strengthLabel).toBe("Thân vượng");
    expect(report.usefulGod).toBe("Đinh");
    expect(report.hyThan).toBe("Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng");
    expect(report.kyThan).toBe("Canh, Tân");
    expect(report.fiveElements.map((row) => row.count)).toEqual([2, 7, 4, 4, 0]);
    expect(report.tenGods).toEqual(["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"]);
    expect(report.lunarDate).toBe("10/08/1966");
    expect(report.scoreLabel).toBe("61.25 / C");
    expect(report.pattern).toBe("Chính Tài");
  });

  it("I. export uses real analysis ID, not last-result", () => {
    const fromStorageKey = buildFullReportViewModel(HUYNH, {
      input: FRESH.input,
      analysisId: "last-result",
    });
    expect(fromStorageKey.analysisId).toBe("bte-huynh-1966-fresh");
    expect(fromStorageKey.analysisId).not.toMatch(/last-result/i);
    expect(renderFullReportHtml(fromStorageKey)).not.toContain("last-result");
  });

  it("J. no stale report HTML overrides current structured truth", () => {
    const html = renderFullReportHtml(model());
    expect(html).not.toContain("STALE");
    expect(html).not.toContain("Trung hòa");
    expect(html).not.toContain("54.25");
    expect(html).toContain("Thân vượng");
    expect(html).toContain("61.25 / C");
  });

  it("K. current-result route consistency remains intact", () => {
    const stale: StoredResultRecord = {
      analysis_id: "bte-stale-old",
      input: { year: 1990, month: 1, day: 1 },
      data: { report: { html: "legacy" }, pattern: { than_vuong_nhuoc: "Trung hòa" } },
    };
    const current = resolveCurrentStoredResult({
      current: FRESH,
      historyView: stale,
      fromHistory: false,
    });
    const boot = resolveResultBoot(FRESH, "", stale);
    expect(current?.analysisId).toBe("bte-huynh-1966-fresh");
    expect(boot.fullReport?.analysisId).toBe("bte-huynh-1966-fresh");
    expect(boot.fullReport?.strengthLabel).toBe("Thân vượng");
  });

  it("L. legacy path remains compatibility-only", () => {
    const html = renderFullReportHtml(model());
    expect(html).toContain("data-report=\"canonical-full\"");
    expect(html).toContain("data-facts-only=\"false\"");
    expect(HUYNH.report?.html).toContain("STALE");
    expect(html.includes(String(HUYNH.report?.html))).toBe(false);
  });
});
