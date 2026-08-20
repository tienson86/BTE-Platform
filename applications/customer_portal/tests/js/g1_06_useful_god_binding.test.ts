/**
 * G1-06 — Portal copies rich Useful God display. Does not derive Can/Hành.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { adaptAnalysisToBaZiResult } from "../../src/adapters/baziResultAdapter";
import { buildFullReportViewModel, renderFullReportHtml } from "../../src/report/fullReportViewModel";
import {
  canonicalFavorableDisplay,
  canonicalUsefulDisplay,
  canonicalUnfavorableDisplay,
} from "../../src/adapters/canonicalUsefulGod";
import type { AnalysisDataDto } from "../../src/models";

const DISPLAY = "Hỏa · Bính · Thất Sát";
const HY =
  "Hỏa · Bính · Thất Sát / Hỏa · Đinh · Chính Quan / Mộc · Giáp · Thiên Tài";
const KY = "Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan";

const CASE_0001: AnalysisDataDto = {
  bazi: { day_master: "Canh", day_master_element: "Kim" },
  pattern: { cach_cuc: "Chính Ấn", dung_than: "should-not-win" },
  strength: { strength_level: "strong", strength_score: 0.87 },
  temperature: {
    climate_state: "cold",
    climate_state_label: "Hàn",
    balancing_need: "warming",
    balancing_need_label: "Cần ôn ấm",
    temperature_score: 0.72,
  },
  useful_god: {
    useful_god: "Bính",
    useful_ten_god: "Thất Sát",
    useful_stem: "Bính",
    useful_element: "Hỏa",
    useful_display: DISPLAY,
    favorable_gods: ["Bính", "Đinh", "Giáp"],
    unfavorable_gods: ["Nhâm", "Quý"],
    favorable_display: HY,
    unfavorable_display: KY,
    winning_rule_id: "sea_001",
    winning_rule_group: "season",
  },
};

describe("G1-06 canonical Useful God binding", () => {
  it("copies published display and does not reverse-map from Ten God names", () => {
    expect(canonicalUsefulDisplay(CASE_0001.useful_god)).toBe(DISPLAY);
    expect(canonicalFavorableDisplay(CASE_0001.useful_god)).toBe(HY);
    expect(canonicalUnfavorableDisplay(CASE_0001.useful_god)).toBe(KY);
  });

  it("Canonical Desktop S02 shows three-layer Dụng / Hỷ / Kỵ", () => {
    const vm = adaptAnalysisToCanonicalDesktop(CASE_0001, { source: "api" });
    expect(vm.s02.items.find((item) => item.label === "Dụng thần")?.value).toBe(DISPLAY);
    expect(vm.s02.items.find((item) => item.label === "Hỷ thần")?.value).toBe(HY);
    expect(vm.s02.items.find((item) => item.label === "Kỵ thần")?.value).toBe(KY);
    const dieuHau = vm.s01.conditions.rows.find((row) => row.label === "Điều hậu");
    expect(dieuHau?.value).toContain("Hàn");
    expect(dieuHau?.value).toContain("Cần ôn ấm");
  });

  it("Full Report and BaZi adapter stay on the same published strings", () => {
    const report = buildFullReportViewModel(CASE_0001);
    expect(report.usefulGod).toBe(DISPLAY);
    expect(report.hyThan).toBe(HY);
    expect(report.kyThan).toBe(KY);
    const html = renderFullReportHtml(report);
    expect(html).toContain(DISPLAY);
    expect(html).toContain("Hàn");
    expect(html).toContain("Cần ôn ấm");
    const bazi = adaptAnalysisToBaZiResult(CASE_0001);
    expect(bazi.spiritGods.find((row) => row.role === "dung")?.name).toBe(DISPLAY);
    expect(bazi.spiritGods.find((row) => row.role === "hy")?.name).toBe(HY);
    expect(bazi.spiritGods.find((row) => row.role === "ky")?.name).toBe(KY);
  });
});
