/**
 * G1-05 — Phân bố Ngũ hành binds data.five_elements.counts, not Score grade.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { adaptAnalysisToBaZiResult } from "../../src/adapters/baziResultAdapter";
import { buildFullReportViewModel, renderFullReportHtml } from "../../src/report/fullReportViewModel";
import { adaptResultPageViewModel } from "../../src/screens/result/adapters/resultPresentationAdapter";
import {
  FIVE_ELEMENTS_ABSENT_LABEL,
  FIVE_ELEMENTS_DISCLAIMER,
  FIVE_ELEMENTS_METHOD_NOTE,
  FIVE_ELEMENTS_TITLE,
  formatFiveElementsCompact,
  canonicalFiveElementCounts,
} from "../../src/adapters/canonicalFiveElements";
import type { AnalysisDataDto } from "../../src/models";

const CASE_0001: AnalysisDataDto = {
  five_elements: {
    wood: { count: 4 },
    fire: { count: 5 },
    earth: { count: 6 },
    metal: { count: 3 },
    water: { count: 1 },
    counts: { wood: 4, fire: 5, earth: 6, metal: 3, water: 1 },
    unit_total: 19,
    method_note: FIVE_ELEMENTS_METHOD_NOTE,
  },
  score: {
    wuxing_score: 0,
    grade: "B+",
    total_score: 72,
    wuxing_series: [
      { label: "Mộc", value: 40 },
      { label: "Hỏa", value: 40 },
      { label: "Thổ", value: 10 },
      { label: "Kim", value: 10 },
      { label: "Thủy", value: 0 },
    ],
  },
  bazi: { day_master: "Canh", day_master_element: "Kim" },
  pattern: { cach_cuc: "Chính Ấn" },
  strength: { strength_level: "strong", strength_score: 0.87 },
};

const ZERO_WATER: AnalysisDataDto = {
  five_elements: {
    counts: { wood: 2, fire: 7, earth: 4, metal: 4, water: 0 },
  },
  score: { wuxing_score: 0, grade: "C" },
};

const FORBIDDEN = ["Mạnh", "Yếu", "Vượng", "Suy", "Thiếu", "Dư", "nổi", "khuyết"];

describe("G1-05 canonical Five Elements distribution binding", () => {
  it("CASE-0001 keeps 4/5/6/3/1 and ignores wuxing_series / grade", () => {
    const counts = canonicalFiveElementCounts(CASE_0001);
    expect(counts).toEqual({ Mộc: 4, Hỏa: 5, Thổ: 6, Kim: 3, Thủy: 1 });
    expect(formatFiveElementsCompact(counts)).toBe("Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1");
    const vm = adaptAnalysisToCanonicalDesktop(CASE_0001, { source: "api" });
    expect(vm.s04.title).toBe(FIVE_ELEMENTS_TITLE);
    expect(vm.s04.rows.map((row) => `${row.name} ${row.count}`)).toEqual([
      "Mộc 4",
      "Hỏa 5",
      "Thổ 6",
      "Kim 3",
      "Thủy 1",
    ]);
    expect(vm.s04.summary).toContain(FIVE_ELEMENTS_METHOD_NOTE);
    expect(vm.s04.summary).toContain("Tổng đơn vị cấu trúc: 19");
    expect(vm.s04.summary).toContain(FIVE_ELEMENTS_DISCLAIMER);
    expect(vm.s04.summary).not.toContain("B+");
    expect(vm.s02.items.find((item) => item.label === "Phân bố Ngũ hành")?.value).toBe(
      "Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1",
    );
    const rendered = `${vm.s04.title} ${vm.s04.rows.map((row) => row.status).join(" ")}`;
    for (const token of FORBIDDEN) {
      expect(rendered).not.toContain(token);
    }
  });

  it("count 0 is structural absence, not Dụng/Hỷ/khuyết", () => {
    const vm = adaptAnalysisToCanonicalDesktop(ZERO_WATER, { source: "api" });
    const water = vm.s04.rows.find((row) => row.name === "Thủy");
    expect(water?.count).toBe(0);
    expect(water?.status).toBe(FIVE_ELEMENTS_ABSENT_LABEL);
    expect(water?.status).not.toContain("Dụng");
    expect(water?.status).not.toContain("Hỷ");
    expect(water?.status).not.toContain("khuyết");
  });

  it("Portal result and Full Report use the same counts", () => {
    const desktop = adaptAnalysisToCanonicalDesktop(CASE_0001, { source: "api" });
    const result = adaptResultPageViewModel(desktop);
    const report = buildFullReportViewModel(CASE_0001);
    const html = renderFullReportHtml(report);
    expect(result.fiveElements.title).toBe(FIVE_ELEMENTS_TITLE);
    expect(result.fiveElements.rows.items.map((row) => row.count)).toEqual([4, 5, 6, 3, 1]);
    expect(report.fiveElements.map((row) => row.count)).toEqual([4, 5, 6, 3, 1]);
    expect(html).toContain("Phân bố Ngũ hành");
    expect(html).toContain(FIVE_ELEMENTS_METHOD_NOTE);
    expect(html).toContain(FIVE_ELEMENTS_DISCLAIMER);
    expect(html).not.toContain("Cân bằng Ngũ hành");
    const bazi = adaptAnalysisToBaZiResult(CASE_0001);
    expect(bazi.fiveElements.find((el) => el.id === "hoa")?.score).toBe(5);
    expect(bazi.fiveElements.every((el) => !["Mạnh", "Yếu", "Khá"].includes(el.strength))).toBe(
      true,
    );
  });
});
