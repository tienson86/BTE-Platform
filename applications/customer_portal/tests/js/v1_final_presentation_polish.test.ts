/**
 * V1.0 final presentation polish — customer copy only.
 * Does not change Strength / Pattern / Ten Gods / ShenSha calculation.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import {
  buildTenGodsProminence,
  formatShenShaCustomer,
  hasInternalRuleId,
  strengthCustomerSummary,
  stripInternalRuleIds,
  temperatureCustomerEvidence,
  tenGodsProminenceFromAnalysis,
} from "../../src/adapters/customerFacingPresentation";
import { canonicalPatternEvidence } from "../../src/adapters/canonicalPattern";
import { canonicalStrengthEvidence } from "../../src/adapters/canonicalStrength";
import { buildFullReportViewModel, renderFullReportHtml } from "../../src/report/fullReportViewModel";
import { adaptResultPageViewModel } from "../../src/screens/result/adapters/resultPresentationAdapter";
import type { AnalysisDataDto } from "../../src/models";
import type { TenGodsPayload } from "../../src/adapters/tenGodsDisplay";

const DUNG_STRENGTH_EVIDENCE =
  "Hưu khí theo tháng +10 · Vô căn -20 · Ấn tinh sinh thân +10 · Có Chính Ấn +5 · Có Tỷ Kiên +5 · Bị Quan Sát khắc -10 · Có Thất Sát -8 · Thực Thương tiết khí -8 · Tiết khí nặng -10";

const DUNG: AnalysisDataDto = {
  bazi: {
    day_master: "Ất",
    day_master_element: "Mộc",
    year_pillar: { stem: "Nhâm", branch: "Tuất" },
    month_pillar: { stem: "Ất", branch: "Tỵ" },
    day_pillar: { stem: "Ất", branch: "Tỵ" },
    hour_pillar: { stem: "Tân", branch: "Tỵ" },
    shensha_matches: [
      {
        id: "hong_luan",
        canonical_name: "Hồng Loan",
        presence_label: "Có · trụ Tháng · trụ Ngày · trụ Giờ",
        evidence_text: "Nhật chi Tỵ → gặp Tỵ",
        occurrences: [
          { pillar: "month", location: "branch", target_value: "Tỵ" },
          { pillar: "day", location: "branch", target_value: "Tỵ" },
          { pillar: "hour", location: "branch", target_value: "Tỵ" },
        ],
      },
      {
        id: "tian_de",
        canonical_name: "Thiên Đức Quý Nhân",
        presence_label: "Có · trụ Giờ",
        evidence_text: "Nguyệt chi Tỵ → gặp Tân",
        occurrences: [{ pillar: "hour", location: "stem", target_value: "Tân" }],
      },
    ],
  },
  strength: {
    strength_level: "weak",
    strength_score: 0.24,
    reasoning: "Thân nhược",
    evidence_compact: DUNG_STRENGTH_EVIDENCE,
    raw_total: -26,
  },
  pattern: {
    cach_cuc: "Sát Ấn tương sinh",
    winning_rule_id: "com_san_01",
    month_branch: "Tỵ",
    month_main_qi: "Bính",
    evidence_compact:
      "Nguyệt lệnh Tỵ · khí chính Bính · Bính đối với Ất là Thương Quan · rule com_san_01",
  },
  temperature: {
    climate_state: "hot",
    climate_state_label: "Nhiệt",
    balancing_need: "cooling",
    balancing_need_label: "Cần làm mát",
    month_branch: "Tỵ",
    season: "summer",
    evidence_compact: "Nguyệt lệnh Tỵ · mùa Hạ · khí hậu Nhiệt · Cần làm mát · rule cli_001",
  },
  ten_gods: dungTenGods(),
};

function dungTenGods(): TenGodsPayload {
  return {
    visible: [
      { pillar: "year", stem: "Nhâm", ten_god: "Chính Ấn", god_id: "zheng_yin" },
      { pillar: "month", stem: "Ất", ten_god: "Tỷ Kiên", god_id: "bi_jian" },
      { pillar: "day", stem: "Ất", ten_god: "Nhật Chủ", god_id: "day_master" },
      { pillar: "hour", stem: "Tân", ten_god: "Thất Sát", god_id: "qi_sha" },
    ],
    hidden: [
      hidden("year", "Tuất", "Mậu", "Chính Tài"),
      hidden("year", "Tuất", "Tân", "Thất Sát"),
      hidden("year", "Tuất", "Đinh", "Thực Thần"),
      hidden("month", "Tỵ", "Bính", "Thương Quan"),
      hidden("month", "Tỵ", "Canh", "Chính Quan"),
      hidden("month", "Tỵ", "Mậu", "Chính Tài"),
      hidden("day", "Tỵ", "Bính", "Thương Quan"),
      hidden("day", "Tỵ", "Canh", "Chính Quan"),
      hidden("day", "Tỵ", "Mậu", "Chính Tài"),
      hidden("hour", "Tỵ", "Bính", "Thương Quan"),
      hidden("hour", "Tỵ", "Canh", "Chính Quan"),
      hidden("hour", "Tỵ", "Mậu", "Chính Tài"),
    ],
  };
}

function hidden(pillar: string, branch: string, stem: string, tenGod: string) {
  return {
    pillar,
    branch,
    hidden_stem: stem,
    stem,
    ten_god: tenGod,
  };
}

describe("V1 final presentation polish", () => {
  it("strips customer-facing rule IDs from compact evidence", () => {
    const raw = "Nguyệt lệnh Tỵ · khí chính Bính · rule com_san_01";
    expect(stripInternalRuleIds(raw)).toBe("Nguyệt lệnh Tỵ · khí chính Bính");
    expect(hasInternalRuleId(raw)).toBe(true);
    expect(hasInternalRuleId(stripInternalRuleIds(raw))).toBe(false);
    expect(canonicalPatternEvidence(DUNG)).toContain("com_san_01");
    expect(canonicalStrengthEvidence(DUNG)).toContain("-20");
  });

  it("builds a readable Strength summary from canonical evidence, not ±scores", () => {
    const summary = strengthCustomerSummary(DUNG);
    expect(summary).toContain("Vô căn");
    expect(summary).toContain("sinh tháng Tỵ");
    expect(summary).toContain("Thực Thương tiết khí mạnh");
    expect(summary).toContain("Quan Sát gây áp lực");
    expect(summary).toContain("có sinh trợ nhưng không đủ cân lại");
    expect(summary).not.toMatch(/[+\-]\d+/);
    expect(hasInternalRuleId(summary)).toBe(false);
  });

  it("rewrites Điều hậu evidence without climate rule IDs", () => {
    const evidence = temperatureCustomerEvidence(DUNG);
    expect(evidence).toContain("Sinh tháng Tỵ");
    expect(evidence.toLowerCase()).toContain("hạ");
    expect(evidence.toLowerCase()).toContain("nhiệt");
    expect(evidence).not.toContain("cli_");
    expect(evidence).not.toContain("rule ");
  });

  it("ranks Ten Gods deterministically and does not count Nhật Chủ as Tỷ Kiên", () => {
    const summary = tenGodsProminenceFromAnalysis(DUNG);
    const byName = Object.fromEntries(summary.all.map((item) => [item.name, item]));
    expect(byName["Thất Sát"]?.klass).toBe("Lộ rõ");
    expect(byName["Tỷ Kiên"]?.klass).toBe("Lộ rõ");
    expect(byName["Tỷ Kiên"]?.visibleCount).toBe(1);
    expect(byName["Chính Ấn"]?.klass).toBe("Lộ rõ");
    expect(byName["Thương Quan"]?.klass).toBe("Ẩn nổi bật");
    expect(byName["Thương Quan"]?.hiddenCount).toBe(3);
    expect(byName["Chính Tài"]?.klass).toBe("Ẩn nổi bật");
    expect(byName["Chính Quan"]?.klass).toBe("Ẩn nổi bật");
    expect(summary.all.some((item) => item.name === "Nhật Chủ")).toBe(false);
    const hiddenOnly = buildTenGodsProminence(
      {
        visible: [{ pillar: "day", stem: "Ất", ten_god: "Nhật Chủ", god_id: "day_master" }],
        hidden: [
          hidden("month", "Tỵ", "Bính", "Thương Quan"),
          hidden("day", "Tỵ", "Bính", "Thương Quan"),
          hidden("hour", "Tỵ", "Bính", "Thương Quan"),
          hidden("year", "Tuất", "Đinh", "Thực Thần"),
        ],
      },
      "Ất",
    );
    const thuong = hiddenOnly.all.find((item) => item.name === "Thương Quan");
    const thuc = hiddenOnly.all.find((item) => item.name === "Thực Thần");
    expect(thuong?.klass).toBe("Ẩn nổi bật");
    expect(thuc?.klass).toBe("Có ẩn");
    expect(hiddenOnly.all.indexOf(thuong!)).toBeLessThan(hiddenOnly.all.indexOf(thuc!));
    expect(hiddenOnly.all.some((item) => item.name === "Tỷ Kiên")).toBe(false);
  });

  it("preserves visible occurrence over a single hidden occurrence", () => {
    const summary = buildTenGodsProminence(
      {
        visible: [{ pillar: "hour", stem: "Tân", ten_god: "Thất Sát" }],
        hidden: [hidden("year", "Tuất", "Đinh", "Thực Thần")],
      },
      "Ất",
    );
    expect(summary.all[0]?.name).toBe("Thất Sát");
    expect(summary.all[0]?.klass).toBe("Lộ rõ");
  });

  it("highlights ShenSha with multiple occurrences without adding unsupported stars", () => {
    const hongLoan = formatShenShaCustomer(DUNG.bazi!.shensha_matches![0]);
    const thienDuc = formatShenShaCustomer(DUNG.bazi!.shensha_matches![1]);
    expect(hongLoan.presence).toBe("Nổi bật");
    expect(hongLoan.evidence).toBe("Có tại trụ Tháng · Ngày · Giờ");
    expect(thienDuc.presence).toBe("Có");
    expect(thienDuc.evidence).toBe("Có tại trụ Giờ");
    const names = (DUNG.bazi?.shensha_matches ?? []).map((item) => item.canonical_name);
    expect(names).not.toContain("Hoa Cái");
    expect(names).not.toContain("Cô Thần");
    expect(names).not.toContain("Đào Hoa");
    expect(names).not.toContain("Dịch Mã");
  });

  it("keeps Result and Full Report on the same customer summaries", () => {
    const desktop = adaptAnalysisToCanonicalDesktop(DUNG, { source: "api" });
    const report = buildFullReportViewModel(DUNG);
    const html = renderFullReportHtml(report);
    const result = adaptResultPageViewModel(desktop, report);
    const yeuTo = desktop.s01.conditions.rows.find((row) => row.label === "Yếu tố chính");
    const cachCuc = desktop.s01.conditions.rows.find((row) => row.label === "Cách cục");
    const dieuHau = desktop.s01.conditions.rows.find((row) => row.label === "Điều hậu");
    expect(yeuTo?.value).toBe(report.strengthEvidence);
    expect(cachCuc?.value).toContain(report.pattern);
    expect(cachCuc?.value).toContain("Nguyệt lệnh Tỵ");
    expect(dieuHau?.value).toContain("Nhiệt");
    expect(dieuHau?.value).toContain("Cần làm mát");
    expect(result.strength.insight.text).toContain("Vô căn");
    expect(report.strengthEvidence).toContain("Vô căn");
    expect(result.tenGods.title).toMatch(/THẬP THẦN NỔI BẬT/i);
    expect(result.tenGods.gods.items.some((item) => item.name.includes("Thất Sát"))).toBe(true);
    expect(result.shenSha.items.some((item) => item.name === "Hồng Loan" && item.presence === "Nổi bật")).toBe(
      true,
    );
    expect(html).toContain("Yếu tố chính");
    expect(html).not.toContain("Căn cứ chính");
    expect(html).not.toContain("Căn cứ khí hậu");
    expect(html).not.toContain("rule ");
    expect(html).not.toContain("cli_");
    expect(html).not.toContain("com_san_");
    expect(hasInternalRuleId(html)).toBe(false);
    expect(desktop.s01.conditions.rows.some((row) => row.label === "Căn cứ")).toBe(false);
    expect(desktop.s05.factors.some((item) => /[+\-]\d+/.test(item.text))).toBe(false);
  });
});
