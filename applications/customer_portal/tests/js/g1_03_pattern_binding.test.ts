/**
 * G1-03 — Cách cục binds PatternResult, does not recompute.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { buildFullReportViewModel } from "../../src/report/fullReportViewModel";
import { canonicalPatternEvidence, canonicalPatternLabel } from "../../src/adapters/canonicalPattern";
import type { AnalysisDataDto } from "../../src/models";

const CASE_0001: AnalysisDataDto = {
  pattern: {
    pattern: "chinh_an",
    cach_cuc: "Chính Ấn",
    winning_rule_id: "pat_ca_01",
    fallback_used: false,
    month_branch: "Sửu",
    month_main_qi: "Kỷ",
    month_main_qi_ten_god: "Chính Ấn",
    evidence_compact:
      "Nguyệt lệnh Sửu · khí chính Kỷ · Kỷ đối với Canh là Chính Ấn · Kỷ không thấu trực tiếp · Mậu Thiên Ấn thấu tại trụ Giờ · rule pat_ca_01",
    penetration_exact: false,
  },
  bazi: { day_master: "Canh", day_master_element: "Kim" },
};

describe("G1-03 canonical Pattern binding", () => {
    it("Canonical Desktop Cách cục is Chính Ấn with customer evidence", () => {
    const vm = adaptAnalysisToCanonicalDesktop(CASE_0001, { source: "api" });
    expect(vm.s01.dayMaster.tags.some((tag) => tag.text.includes("Chính Ấn"))).toBe(true);
    const cachCuc = vm.s01.conditions.rows.find((row) => row.label === "Cách cục");
    expect(cachCuc?.value).toContain("Chính Ấn");
    expect(cachCuc?.value).toContain("Nguyệt lệnh Sửu");
    expect(cachCuc?.value).toContain("khí chính Kỷ");
    expect(cachCuc?.value).not.toContain("thành cách");
    expect(cachCuc?.value).not.toContain("Chính Quan");
    expect(cachCuc?.value).not.toContain("rule ");
    expect(cachCuc?.value).not.toContain("pat_ca_");
  });

  it("Full Report Cách cục uses canonical Pattern without rule IDs", () => {
    const report = buildFullReportViewModel(CASE_0001);
    expect(report.pattern).toBe("Chính Ấn");
    expect(report.patternEvidence).toContain("Kỷ đối với Canh là Chính Ấn");
    expect(canonicalPatternLabel(CASE_0001)).toBe("Chính Ấn");
    expect(canonicalPatternEvidence(CASE_0001)).toContain("Kỷ không thấu trực tiếp");
  });
});
