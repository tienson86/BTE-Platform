/**
 * G2-01R — canonical result binding repair (routing / identity / contract).
 * Presentation only. Does not recompute Gate-1 engines.
 */

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { canonicalUsefulDisplay, canonicalFavorableDisplay } from "../../src/adapters/canonicalUsefulGod";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { PortalPage } from "../../src/screens/canonical_desktop";
import { buildFullReportViewModel, renderFullReportHtml } from "../../src/report/fullReportViewModel";
import {
  CONTRACT_MISMATCH_MESSAGE,
  CUSTOMER_USEFUL_GOD_CONTRACT,
  customerContractStatus,
} from "../../src/resultState/customerContract";
import {
  historyIdFromSearch,
  resolveCurrentStoredResult,
  type StoredResultRecord,
} from "../../src/resultState/currentResult";
import type { AnalysisDataDto } from "../../src/models";

const CONTRACT = CUSTOMER_USEFUL_GOD_CONTRACT;

const DUNG_DISPLAY = "Thủy · Nhâm · Thực Thần";
const DUNG_HY = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";
const DUNG_REASON =
  "Nhật chủ Canh Kim thân vượng → cần tiết bớt khí Kim → áp dụng nguyên tắc Tiết theo mô hình cân bằng V1.0 → Kim sinh Thủy → Nhâm đối với Canh là Thực Thần → chọn Thủy · Nhâm · Thực Thần làm Dụng.";

const TUYEN_DISPLAY = "Mộc · Ất · Chính Quan";
const TUYEN_HY = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";

function dungPayload(analysisId: string): AnalysisDataDto {
  return {
    analysis_id: analysisId,
    request_id: analysisId,
    useful_god_source: { contract: CONTRACT },
    result_meta: {
      analysis_id: analysisId,
      customer_contract: CONTRACT,
      gate_core_freeze: "G1",
      month_pillar_standard: "BTE-MONTH-PILLAR-LUNAR-V1.0",
    },
    bazi: {
      year_pillar: { stem: "Ất", branch: "Sửu" },
      month_pillar: { stem: "Ất", branch: "Dậu" },
      day_pillar: { stem: "Canh", branch: "Thân" },
      hour_pillar: { stem: "Canh", branch: "Thìn" },
      day_master: "Canh",
    },
    strength: { strength_level: "strong", strength_score: 1.0 },
    pattern: {
      cach_cuc: "Cấu trúc đặc biệt được nhận diện: Giá Sắc",
      detected_special_pattern: "gia_sac",
      qualification_level: 1,
      ug_override_eligible: false,
      dung_than: "should-not-win",
      hy_than: "should-not-win-hy",
    },
    temperature: {
      climate_state_label: "Hàn",
      balancing_need_label: "Cần ôn ấm",
    },
    useful_god: {
      useful_display: DUNG_DISPLAY,
      favorable_display: DUNG_HY,
      short_reason: DUNG_REASON,
      climate_preference_label: "Điều hậu ưu tiên Hỏa",
      hy_role_status: "STATIC_SAME_ELEMENT_SIBLING",
    },
    luck: { current_cycle: { gan_zhi: "Tân Tỵ" } },
  };
}

function tuyenPayload(analysisId: string): AnalysisDataDto {
  return {
    analysis_id: analysisId,
    request_id: analysisId,
    useful_god_source: { contract: CONTRACT },
    result_meta: {
      analysis_id: analysisId,
      customer_contract: CONTRACT,
      gate_core_freeze: "G1",
    },
    bazi: {
      year_pillar: { stem: "Giáp", branch: "Tý" },
      month_pillar: { stem: "Tân", branch: "Mùi" },
      day_pillar: { stem: "Mậu", branch: "Thân" },
      hour_pillar: { stem: "Quý", branch: "Hợi" },
      day_master: "Mậu",
    },
    strength: { strength_level: "strong", strength_score: 0.66 },
    pattern: {
      cach_cuc: "Kiếp Tài",
      dung_than: "should-not-win",
      hy_than: "should-not-win-hy",
    },
    temperature: {
      climate_state_label: "Nhiệt",
      balancing_need_label: "Cần làm mát",
    },
    useful_god: {
      useful_display: TUYEN_DISPLAY,
      favorable_display: TUYEN_HY,
      short_reason: "Nhật chủ Mậu Thổ thân vượng → có Chính Quan đủ điều kiện Chế.",
      climate_preference_label: "Điều hậu ưu tiên Thủy",
      reason_archetype: "CHẾ",
    },
    luck: { current_cycle: { gan_zhi: "Bính Dần" } },
  };
}

function record(id: string, data: AnalysisDataDto, name: string): StoredResultRecord {
  return {
    analysis_id: id,
    input: { year: 1985, month: 9, day: 18, hour: 8, minute: 0, full_name: name },
    data,
  };
}

function debugBindingFingerprint(data: AnalysisDataDto, analysisId: string) {
  const bazi = data.bazi || {};
  const pillar = (key: "year_pillar" | "month_pillar" | "day_pillar" | "hour_pillar") => {
    const item = bazi[key] || {};
    return `${item.stem || ""} ${item.branch || ""}`.trim();
  };
  return {
    analysis_id: analysisId,
    four_pillars: [pillar("year_pillar"), pillar("month_pillar"), pillar("day_pillar"), pillar("hour_pillar")].join(" / "),
    strength: `${data.strength?.strength_score} ${data.strength?.strength_level}`,
    pattern: String((data.pattern as { cach_cuc?: string } | undefined)?.cach_cuc || ""),
    useful_god: canonicalUsefulDisplay(data.useful_god),
    luck: String((data.luck?.current_cycle as { gan_zhi?: string } | undefined)?.gan_zhi || ""),
  };
}

describe("G2-01R canonical binding", () => {
  it("A. empty /result does not show mock", () => {
    const boot = resolveResultBoot(null, "");
    expect(boot.previewFallback).toBe(false);
    expect(boot.resultSource).toBe("empty");
    const { container } = render(
      <PortalPage
        request={boot.request}
        initialData={boot.initialData}
        previewFallback={boot.previewFallback}
        fullReport={boot.fullReport}
      />,
    );
    expect(screen.getByText("Chưa có kết quả phân tích")).toBeTruthy();
    expect(container.textContent).toContain("Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.");
    expect(container.querySelector(".rp-result-page")).toBeNull();
    expect(container.textContent).not.toContain("BTE-2024-000123");
    expect(container.textContent).not.toContain("Thủy · Nhâm · Thực Thần");
  });

  it("B. server canonical ID persists into Result and Report", () => {
    const id = "req-server-dung";
    const stored = record(id, dungPayload(id), "Ngô Đắc Dũng");
    const boot = resolveResultBoot(stored, "");
    expect(boot.analysisId).toBe(id);
    expect(boot.fullReport?.analysisId).toBe(id);
    expect(renderFullReportHtml(boot.fullReport!)).toContain(`data-analysis-id="${id}"`);
  });

  it("C. fresh current beats history without explicit context", () => {
    const a = record("id-a", dungPayload("id-a"), "A");
    const b = record("id-b", tuyenPayload("id-b"), "B");
    const resolved = resolveCurrentStoredResult({
      current: b,
      historyView: a,
      fromHistory: false,
    });
    expect(resolved?.analysisId).toBe("id-b");
    expect(resolved?.source).toBe("current");
    expect(resolved?.data.useful_god?.useful_display).toBe(TUYEN_DISPLAY);
  });

  it("D. explicit history is isolated", () => {
    const a = record("id-a", dungPayload("id-a"), "A");
    const b = record("id-b", tuyenPayload("id-b"), "B");
    expect(historyIdFromSearch("?from=history&id=id-a")).toBe("id-a");
    const history = resolveCurrentStoredResult({
      current: b,
      historyView: a,
      fromHistory: true,
      historyId: "id-a",
    });
    expect(history?.analysisId).toBe("id-a");
    expect(history?.source).toBe("history");
    expect(history?.data.useful_god?.useful_display).toBe(DUNG_DISPLAY);
  });

  it("E. normal /result never reads implicit history view", () => {
    const a = record("id-a", dungPayload("id-a"), "A");
    const b = record("id-b", tuyenPayload("id-b"), "B");
    const implicit = resolveCurrentStoredResult({
      current: b,
      historyView: a,
      fromHistory: true,
    });
    expect(implicit?.analysisId).toBe("id-b");
    expect(resolveResultBoot(b, "?from=history", a).analysisId).toBe("id-b");
  });

  it("F. @1.5 mismatch does not use legacy Dụng/Hỷ", () => {
    const stale: AnalysisDataDto = {
      pattern: { dung_than: "Thủy", hy_than: "Kim" },
      useful_god: { useful_god: "Thủy" },
    };
    expect(customerContractStatus(stale)).toBe("unversioned");
    expect(canonicalUsefulDisplay(stale.useful_god, "—")).toBe("—");
    expect(canonicalFavorableDisplay(stale.useful_god, "—")).toBe("—");
    const boot = resolveResultBoot(
      { analysis_id: "old", input: { year: 1990, month: 1, day: 1 }, data: stale },
      "",
    );
    expect(boot.resultSource).toBe("contract");
    expect(boot.initialData?.status).toBe("error");
    expect(boot.initialData?.statusMessage).toBe(CONTRACT_MISMATCH_MESSAGE);
    expect(boot.fullReport).toBeUndefined();
  });

  it("G. legacy=1 cannot affect normal result boot", () => {
    const current = record("id-b", tuyenPayload("id-b"), "B");
    const history = record("id-a", dungPayload("id-a"), "A");
    const boot = resolveResultBoot(current, "?legacy=1", history);
    expect(boot.analysisId).toBe("id-b");
    expect(boot.resultSource).toBe("current");
    expect(boot.fullReport?.usefulGod).toBe(TUYEN_DISPLAY);
  });

  it("H. Dũng frozen fields are preserved on bind", () => {
    const id = "req-dung";
    const data = dungPayload(id);
    const vm = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
    expect(vm.s03.pillars.map((p) => `${p.stem.viet} ${p.branch.viet}`).join(" / ")).toBe(
      "Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn",
    );
    expect(vm.s05.score).toBe("1.00");
    expect(vm.s02.items.find((item) => item.label === "Dụng thần")?.value).toBe(DUNG_DISPLAY);
    expect(vm.s02.items.find((item) => item.label === "Hỷ thần")?.value).toBe(DUNG_HY);
    expect(vm.s02.items.find((item) => item.label === "Dụng thần")?.value).not.toBe("should-not-win");
    expect(vm.s02.dungReason).toBe(DUNG_REASON);
    const dieuHau = vm.s01.conditions.rows.find((row) => row.label === "Điều hậu")?.value || "";
    expect(dieuHau).toContain("Cần ôn ấm");
    expect(dieuHau).toContain("Điều hậu ưu tiên Hỏa");
  });

  it("I. Tuyền frozen fields are preserved on bind", () => {
    const data = tuyenPayload("req-tuyen");
    const vm = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
    expect(vm.s03.pillars.map((p) => `${p.stem.viet} ${p.branch.viet}`).join(" / ")).toBe(
      "Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi",
    );
    expect(vm.s05.score).toBe("0.66");
    expect(vm.s02.items.find((item) => item.label === "Dụng thần")?.value).toBe(TUYEN_DISPLAY);
    expect(vm.s02.items.find((item) => item.label === "Hỷ thần")?.value).toBe(TUYEN_HY);
  });

  it("J. Report uses the same analysis ID", () => {
    const id = "req-report";
    const boot = resolveResultBoot(record(id, dungPayload(id), "Dũng"), "");
    const report = buildFullReportViewModel(dungPayload(id), { analysisId: id });
    expect(boot.analysisId).toBe(report.analysisId);
    expect(report.analysisId).toBe(id);
  });

  it("K. Print HTML uses the selected analysis id", () => {
    const selected = "req-print-a";
    const html = renderFullReportHtml(
      buildFullReportViewModel(dungPayload(selected), { analysisId: selected }),
    );
    expect(html).toContain(`data-analysis-id="${selected}"`);
    expect(html).not.toContain("req-print-b");
  });

  it("L. no field mixing across current vs explicit history", () => {
    const a = record("id-a", dungPayload("id-a"), "Dũng");
    const b = record("id-b", tuyenPayload("id-b"), "Tuyền");
    const current = resolveResultBoot(b, "", a);
    const history = resolveResultBoot(b, "?from=history&id=id-a", a);
    expect(current.fullReport?.usefulGod).toBe(TUYEN_DISPLAY);
    expect(history.fullReport?.usefulGod).toBe(DUNG_DISPLAY);
    expect(current.analysisId).toBe("id-b");
    expect(history.analysisId).toBe("id-a");
    const fpA = debugBindingFingerprint(a.data!, "id-a");
    const fpB = debugBindingFingerprint(b.data!, "id-b");
    expect(fpA.analysis_id).toBe("id-a");
    expect(fpA.four_pillars).toContain("Ất Sửu");
    expect(fpA.useful_god).toBe(DUNG_DISPLAY);
    expect(fpB.useful_god).toBe(TUYEN_DISPLAY);
    expect(fpA.luck).toBe("Tân Tỵ");
    expect(fpB.luck).toBe("Bính Dần");
  });
});
