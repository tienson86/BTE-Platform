/**
 * G1-04 — Điều hậu binds Temperature climate_state, not pattern.dieu_hau.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { buildFullReportViewModel, renderFullReportHtml } from "../../src/report/fullReportViewModel";
import {
  canonicalBalancingNeedLabel,
  canonicalClimateStateLabel,
  canonicalTemperatureEvidence,
} from "../../src/adapters/canonicalTemperature";
import type { AnalysisDataDto } from "../../src/models";

const CASE_0001: AnalysisDataDto = {
  pattern: {
    pattern: "chinh_an",
    cach_cuc: "Chính Ấn",
    dieu_hau: "Đắc lệnh",
    evidence_compact: "Nguyệt lệnh Sửu · khí chính Kỷ",
  },
  bazi: { day_master: "Canh", day_master_element: "Kim" },
  strength: { strength_level: "strong", strength_score: 0.87 },
  temperature: {
    temperature_level: "cold",
    climate_state: "cold",
    climate_state_label: "Hàn",
    balancing_need: "warming",
    balancing_need_label: "Cần ôn ấm",
    evidence_compact: "Nguyệt lệnh Sửu · mùa Đông · khí hậu Hàn · Cần ôn ấm · rule cli_002",
    month_branch: "Sửu",
    season: "winter",
    temperature_score: 0.72,
    score_semantic: "imbalance_intensity",
  },
  useful_god: { useful_god: "Thực Thần" },
};

describe("G1-04 canonical Temperature / Điều hậu binding", () => {
  it("does not treat pattern.dieu_hau as Điều hậu", () => {
    expect(canonicalClimateStateLabel(CASE_0001)).toBe("Hàn");
    expect(canonicalBalancingNeedLabel(CASE_0001)).toBe("Cần ôn ấm");
    expect(canonicalTemperatureEvidence(CASE_0001)).toContain("Nguyệt lệnh Sửu");
    expect(canonicalClimateStateLabel(CASE_0001)).not.toBe("Đắc lệnh");
  });

  it("Canonical Desktop shows climate rows, not pattern Đắc lệnh as Điều hậu", () => {
    const vm = adaptAnalysisToCanonicalDesktop(CASE_0001, { source: "api" });
    const climate = vm.s01.conditions.rows.find((row) => row.label === "Trạng thái khí hậu");
    const need = vm.s01.conditions.rows.find((row) => row.label === "Nhu cầu điều hòa");
    const evidence = vm.s01.conditions.rows.find((row) => row.label === "Căn cứ khí hậu");
    expect(climate?.value).toBe("Hàn");
    expect(need?.value).toBe("Cần ôn ấm");
    expect(evidence?.value).toContain("Nguyệt lệnh Sửu");
    expect(vm.s01.conditions.rows.some((row) => row.label === "Điều hậu" && row.value === "Đắc lệnh")).toBe(
      false,
    );
  });

  it("Full Report binds climate/need/evidence and does not emit —", () => {
    const report = buildFullReportViewModel(CASE_0001);
    expect(report.climateState).toBe("Hàn");
    expect(report.balancingNeed).toBe("Cần ôn ấm");
    expect(report.climateEvidence).toContain("mùa Đông");
    const html = renderFullReportHtml(report);
    expect(html).toContain("Hàn");
    expect(html).toContain("Cần ôn ấm");
    expect(html).not.toContain("Điều hậu</span><strong>—</strong>");
    expect(html).not.toContain("Đắc lệnh");
  });
});
