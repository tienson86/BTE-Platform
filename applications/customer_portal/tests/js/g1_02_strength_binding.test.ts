/**
 * G1-02 — Điểm thân must bind StrengthResult, never Score Engine.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { adaptAnalysisToBaZiResult } from "../../src/adapters/baziResultAdapter";
import { buildFullReportViewModel } from "../../src/report/fullReportViewModel";
import type { AnalysisDataDto } from "../../src/models";

const CASE_0001: AnalysisDataDto = {
  strength: {
    strength_level: "strong",
    strength_score: 0.87,
    confidence: 1.0,
    reasoning: "Thân vượng",
    evidence_compact:
      "Tướng địa theo tháng +25 · Có căn khí +12 · Đồng hành trợ thân +8 · Bị Quan Sát khắc -10 · Có Thất Sát -8 · Ấn mùa lạnh +10",
    raw_total: 37,
  },
  score: {
    strength_score: 45.0,
    total_score: 51.25,
    grade: "D+",
  },
  pattern: {
    than_vuong_nhuoc: "Thân vượng",
    than: "Kim",
    cach_cuc: "Chính Ấn",
  },
  bazi: { day_master: "Canh", day_master_element: "Kim" },
};

describe("G1-02 canonical Strength binding", () => {
  it("Canonical Desktop Điểm thân uses 0.87, not Score 45 or 51.25/D+", () => {
    const vm = adaptAnalysisToCanonicalDesktop(CASE_0001, { source: "api" });
    expect(vm.s05.level).toBe("Thân vượng");
    expect(vm.s05.score).toBe("0.87");
    expect(vm.s05.score).not.toContain("45");
    expect(vm.s05.score).not.toContain("51.25");
    expect(vm.s05.score).not.toContain("D+");
    expect(vm.s05.percent).toBe(87);
    expect(vm.s05.factors.some((item) => item.text.includes("Ấn mùa lạnh"))).toBe(true);
  });

  it("Full Report Điểm thân uses 0.87", () => {
    const report = buildFullReportViewModel(CASE_0001);
    expect(report.strengthLabel).toBe("Thân vượng");
    expect(report.strengthScore).toBe("0.87");
    const html = report.strengthScore;
    expect(html).not.toBe("45.0");
    expect(html).not.toBe("51.25");
  });

  it("BaZi Strength card ignores Score Engine 45.0", () => {
    const vm = adaptAnalysisToBaZiResult(CASE_0001);
    expect(vm.strength.label).toBe("Thân vượng");
    expect(vm.strength.score).toBe(0.87);
    expect(vm.strength.maxScore).toBe(1);
  });
});
