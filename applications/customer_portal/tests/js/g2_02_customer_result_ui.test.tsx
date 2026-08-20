/**
 * G2-02 — customer Result UI freeze regression.
 * Presentation only. Does not recompute Gate-1 engines.
 */

import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { hasInternalRuleId } from "../../src/adapters/customerFacingPresentation";
import { FIVE_ELEMENTS_DISCLAIMER } from "../../src/adapters/canonicalFiveElements";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { PortalPage } from "../../src/screens/canonical_desktop";
import { adaptResultPageViewModel } from "../../src/screens/result/adapters/resultPresentationAdapter";
import {
  CONTRACT_MISMATCH_MESSAGE,
  CUSTOMER_USEFUL_GOD_CONTRACT,
} from "../../src/resultState/customerContract";
import type { AnalysisDataDto } from "../../src/models";
import type { StoredResultRecord } from "../../src/resultState/currentResult";

const CONTRACT = CUSTOMER_USEFUL_GOD_CONTRACT;
const SHOT_DIR = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../../../release/gate_02/screenshots/g2_02",
);
const HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";
const DUNG_DISPLAY = "Thủy · Nhâm · Thực Thần";
const DUNG_REASON =
  "Nhật chủ Canh Kim thân vượng → cần tiết bớt khí Kim → áp dụng nguyên tắc Tiết theo mô hình cân bằng V1.0 → Kim sinh Thủy → Nhâm đối với Canh là Thực Thần → chọn Thủy · Nhâm · Thực Thần làm Dụng.";

function record(id: string, data: AnalysisDataDto, name: string, birth: Record<string, unknown>): StoredResultRecord {
  return {
    analysis_id: id,
    input: { ...birth, full_name: name },
    data,
  };
}

function baseUseful(extra: Record<string, unknown>): AnalysisDataDto["useful_god"] {
  return {
    useful_god_source: undefined,
    ...extra,
  };
}

function dungData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    bazi: {
      year_pillar: { stem: "Ất", branch: "Sửu" },
      month_pillar: { stem: "Ất", branch: "Dậu" },
      day_pillar: { stem: "Canh", branch: "Thân", ten_god: "Nhật Chủ" },
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
      hy_than: "Thủy · Quý · Thương Quan",
    },
    temperature: { climate_state_label: "Hàn", balancing_need_label: "Cần ôn ấm" },
    useful_god: baseUseful({
      useful_display: DUNG_DISPLAY,
      favorable_display: HY_NEUTRAL,
      short_reason: DUNG_REASON,
      climate_preference_label: "Điều hậu ưu tiên Hỏa",
      unfavorable_display: "Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài",
    }),
    luck: { current_cycle: { gan_zhi: "Tân Tỵ" } },
  };
}

function tuyenData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    bazi: {
      year_pillar: { stem: "Giáp", branch: "Tý" },
      month_pillar: { stem: "Tân", branch: "Mùi" },
      day_pillar: { stem: "Mậu", branch: "Thân", ten_god: "Nhật Chủ" },
      hour_pillar: { stem: "Quý", branch: "Hợi" },
      day_master: "Mậu",
    },
    strength: { strength_level: "strong", strength_score: 0.66 },
    pattern: { cach_cuc: "Kiếp Tài", dung_than: "Tòng Tài" },
    temperature: { climate_state_label: "Nhiệt", balancing_need_label: "Cần làm mát" },
    useful_god: baseUseful({
      useful_display: "Mộc · Ất · Chính Quan",
      favorable_display: HY_NEUTRAL,
      short_reason:
        "Nhật chủ Mậu Thổ thân vượng → có Chính Quan đủ điều kiện Chế → áp dụng nguyên tắc Chế theo mô hình cân bằng V1.0 → Mộc khắc Thổ → Ất đối với Mậu là Chính Quan → chọn Mộc · Ất · Chính Quan làm Dụng.",
      climate_preference_label: "Điều hậu ưu tiên Thủy",
      reason_archetype: "CHẾ",
    }),
  };
}

function sonData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    bazi: {
      year_pillar: { stem: "Bính", branch: "Dần" },
      month_pillar: { stem: "Tân", branch: "Sửu" },
      day_pillar: { stem: "Canh", branch: "Ngọ", ten_god: "Nhật Chủ" },
      hour_pillar: { stem: "Mậu", branch: "Dần" },
      day_master: "Canh",
    },
    strength: { strength_level: "strong", strength_score: 0.87 },
    pattern: { cach_cuc: "Chính Ấn" },
    temperature: { climate_state_label: "Hàn", balancing_need_label: "Cần ôn ấm" },
    useful_god: baseUseful({
      useful_display: "Hỏa · Đinh · Chính Quan",
      favorable_display: HY_NEUTRAL,
      short_reason:
        "Nhật chủ Canh Kim thân vượng → có Chính Quan đủ điều kiện Chế → áp dụng nguyên tắc Chế theo mô hình cân bằng V1.0 → Hỏa khắc Kim → Đinh đối với Canh là Chính Quan → chọn Hỏa · Đinh · Chính Quan làm Dụng.",
      climate_preference_label: "Điều hậu ưu tiên Hỏa",
    }),
  };
}

function dungThiData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    bazi: {
      year_pillar: { stem: "Nhâm", branch: "Tuất" },
      month_pillar: { stem: "Ất", branch: "Tỵ" },
      day_pillar: { stem: "Ất", branch: "Tỵ", ten_god: "Nhật Chủ" },
      hour_pillar: { stem: "Tân", branch: "Tỵ" },
      day_master: "Ất",
    },
    strength: { strength_level: "weak", strength_score: 0.24 },
    pattern: { cach_cuc: "Sát Ấn tương sinh — Thất Sát chế bởi Chính Ấn" },
    temperature: { climate_state_label: "Nhiệt", balancing_need_label: "Cần làm mát" },
    useful_god: baseUseful({
      useful_display: "Thủy · Nhâm · Chính Ấn",
      favorable_display: "Mộc · Ất · Tỷ Kiên",
      short_reason:
        "Nhật chủ Ất Mộc thân nhược → cần sinh trợ → dùng nguyên tắc Sinh / Trợ theo mô hình cân bằng V1.0 → hành Thủy có quan hệ Thủy sinh Mộc → Nhâm đối với Ất là Chính Ấn → chọn Thủy · Nhâm · Chính Ấn làm Dụng.",
      climate_preference_label: "Điều hậu ưu tiên Thủy",
    }),
  };
}

function renderBoot(stored: StoredResultRecord | null, search = "", history: StoredResultRecord | null = null) {
  const boot = resolveResultBoot(stored, search, history);
  const view = render(
    <PortalPage
      request={boot.request}
      initialData={boot.initialData}
      previewFallback={boot.previewFallback}
      fullReport={boot.fullReport}
      analysisId={boot.analysisId}
      resultSource={boot.resultSource}
    />,
  );
  return { boot, ...view };
}

function collectText(container: HTMLElement): string {
  return (container.textContent || "").replace(/\s+/g, " ");
}

describe("G2-02 customer Result UI freeze", () => {
  it("reason is visible on /result below Dụng/Hỷ/Kỵ", () => {
    const { container } = renderBoot(
      record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
        year: 1985,
        month: 9,
        day: 18,
        hour: 8,
        minute: 0,
      }),
    );
    expect(container.querySelector('[data-field="dung-reason"]')?.textContent).toContain("Căn cứ chọn Dụng");
    expect(container.querySelector('[data-field="dung-reason"]')?.textContent).toContain("theo mô hình cân bằng V1.0");
    expect(screen.getByText(DUNG_DISPLAY)).toBeTruthy();
  });

  it("Hỷ neutral is visible and does not duplicate Dụng", () => {
    const { container } = renderBoot(
      record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
        year: 1985,
        month: 9,
        day: 18,
        hour: 8,
      }),
    );
    const useful = container.querySelector('[data-card="useful-gods"]')?.textContent || "";
    expect(useful).toContain(HY_NEUTRAL);
    expect(useful).not.toContain("Thủy · Quý");
    const hyValue = [...container.querySelectorAll(".rp-indicators__row")]
      .find((row) => row.textContent?.includes("Hỷ thần"))
      ?.textContent;
    expect(hyValue).toContain(HY_NEUTRAL);
    expect(hyValue).not.toContain(DUNG_DISPLAY);
  });

  it("Điều hậu is a separate card from Dụng", () => {
    const { container } = renderBoot(
      record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
        year: 1985,
        month: 9,
        day: 18,
        hour: 8,
      }),
    );
    const climate = container.querySelector('[data-card="climate"]');
    const useful = container.querySelector('[data-card="useful-gods"]');
    expect(climate).toBeTruthy();
    expect(useful).toBeTruthy();
    expect(climate?.textContent).toContain("Cần ôn ấm");
    expect(climate?.textContent).toContain("Điều hậu ưu tiên Hỏa");
    expect(useful?.textContent).not.toContain("Điều hậu ưu tiên Hỏa");
  });

  it("LEVEL-1 wording is detected, not override-absolute", () => {
    const { container } = renderBoot(
      record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
        year: 1985,
        month: 9,
        day: 18,
        hour: 8,
      }),
    );
    const pattern = container.querySelector('[data-field="pattern"]')?.textContent || "";
    expect(pattern).toContain("Cấu trúc đặc biệt được nhận diện: Giá Sắc");
    expect(pattern).not.toContain("tuyệt đối");
    expect(pattern).not.toContain("Chuyên cách ưu tiên Ấn");
  });

  it("empty /result shows gate, CTA, and no mock fixture", () => {
    const { container } = renderBoot(null);
    expect(screen.getByText("Chưa có kết quả phân tích")).toBeTruthy();
    expect(container.querySelector('a[href="/analyze"]')?.textContent).toContain("Nhập ngày giờ sinh");
    expect(container.querySelector(".rp-result-page")).toBeNull();
    expect(collectText(container)).not.toContain("BTE-2024-000123");
    expect(collectText(container)).not.toContain(DUNG_DISPLAY);
  });

  it("explicit History shows a saved-analysis banner without mixing current data", () => {
    const history = record("id-a", dungData("id-a"), "Dũng", { year: 1985, month: 9, day: 18, hour: 8 });
    const current = record("id-b", tuyenData("id-b"), "Tuyền", { year: 1984, month: 7, day: 13, hour: 21, minute: 1 });
    const { container, boot } = renderBoot(current, "?from=history&id=id-a", history);
    expect(boot.resultSource).toBe("history");
    expect(container.querySelector('[data-result-source="history"]')).toBeTruthy();
    expect(container.querySelector(".rp-history-banner")?.textContent).toContain("kết quả đã lưu");
    expect(collectText(container)).toContain(DUNG_DISPLAY);
    expect(collectText(container)).not.toContain("Mộc · Ất · Chính Quan");
  });

  it("version mismatch shows reanalyze notice without contract id or stale Dụng", () => {
    const stale: StoredResultRecord = {
      analysis_id: "old",
      input: { year: 1990, month: 1, day: 1 },
      data: { pattern: { dung_than: "Thủy", hy_than: "Kim" }, useful_god: { useful_god: "Thủy" } },
    };
    const { container, boot } = renderBoot(stale);
    expect(boot.resultSource).toBe("contract");
    expect(container.querySelector('[data-reason="contract"]')).toBeTruthy();
    expect(screen.getByText("Kết quả cần phân tích lại")).toBeTruthy();
    expect(collectText(container)).toContain(CONTRACT_MISMATCH_MESSAGE);
    expect(collectText(container)).not.toContain("UsefulGodView@1.5");
    expect(collectText(container)).not.toContain("Thủy");
    expect(container.querySelector('[data-card="useful-gods"]')).toBeNull();
  });

  it("does not leak rule IDs or mock labels on a frozen result", () => {
    const { container } = renderBoot(
      record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", { year: 1985, month: 9, day: 18, hour: 8 }),
    );
    const body = container.querySelector(".rp-result-page");
    const text = collectText(body as HTMLElement);
    expect(hasInternalRuleId(text)).toBe(false);
    expect(text).not.toMatch(/\b(male|female|strong|weak|balanced|preview|mock|fixture|debug)\b/i);
    expect(text).not.toContain("str_");
    expect(text).not.toContain("sample");
    expect(container.querySelector(".rp-identity__name")?.textContent).not.toContain("id-dung");
    expect(container.querySelector('[data-card="four-pillars"]')?.textContent).toContain("Nhật Chủ");
    expect(container.querySelector('[data-card="four-pillars"]')?.textContent).toContain("Ất");
    expect(container.querySelector('[data-card="four-pillars"]')?.textContent).toContain("Canh");
  });

  it("Five Elements title and disclaimer stay structural", () => {
    const vm = adaptAnalysisToCanonicalDesktop(dungData("id-fe"), { source: "api" });
    const page = adaptResultPageViewModel(vm);
    expect(page.fiveElements.title).toMatch(/phân bố ngũ hành/i);
    expect(page.fiveElements.summary.fullText).toContain(FIVE_ELEMENTS_DISCLAIMER);
    expect(page.fiveElements.summary.text).toContain("không phải mức vượng suy");
    expect(page.fiveElements.rows.items.every((row) => !/mạnh|yếu|vượng|thiếu/i.test(row.status))).toBe(true);
  });

  it("Tuyền customer UI keeps CHẾ path and separate water climate", () => {
    const { container } = renderBoot(
      record("id-tuyen", tuyenData("id-tuyen"), "Vũ Thị Thanh Tuyền", {
        year: 1984,
        month: 7,
        day: 13,
        hour: 21,
        minute: 1,
      }),
    );
    const text = collectText(container);
    expect(text).toContain("0.66");
    expect(text).toContain("Kiếp Tài");
    expect(text).toContain("Mộc · Ất · Chính Quan");
    expect(text).toContain("Chế");
    expect(text).toContain(HY_NEUTRAL);
    expect(text).not.toContain("Tòng Tài");
    expect(container.querySelector('[data-card="climate"]')?.textContent).toContain("Điều hậu ưu tiên Thủy");
  });

  it("writes freeze HTML captures A–I", () => {
    mkdirSync(SHOT_DIR, { recursive: true });
    const writeShot = (file: string, html: string): void => {
      writeFileSync(
        path.join(SHOT_DIR, file),
        `<!doctype html><meta charset="utf-8"><title>${file}</title>${html}`,
        "utf8",
      );
    };
    const son = renderBoot(record("son", sonData("son"), "Nguyễn Tiến Sơn", { year: 1987, month: 1, day: 21, hour: 4, minute: 30 }));
    writeShot("A_son.html", son.container.innerHTML);
    son.unmount();
    const tuyen = renderBoot(record("tuyen", tuyenData("tuyen"), "Vũ Thị Thanh Tuyền", { year: 1984, month: 7, day: 13, hour: 21, minute: 1 }));
    writeShot("B_tuyen.html", tuyen.container.innerHTML);
    tuyen.unmount();
    const dung = renderBoot(record("dung", dungData("dung"), "Ngô Đắc Dũng", { year: 1985, month: 9, day: 18, hour: 8 }));
    writeShot("C_dung.html", dung.container.innerHTML);
    writeShot("D_hy_neutral.html", dung.container.innerHTML);
    writeShot("F_level1_special.html", dung.container.innerHTML);
    dung.unmount();
    const supported = renderBoot(record("dung-thi", dungThiData("dung-thi"), "Đặng Thị Dung", { year: 1982, month: 5, day: 22, hour: 9, minute: 30 }));
    writeShot("E_hy_supported.html", supported.container.innerHTML);
    supported.unmount();
    const empty = renderBoot(null);
    writeShot("G_empty.html", empty.container.innerHTML);
    empty.unmount();
    const mismatch = renderBoot({
      analysis_id: "old",
      input: { year: 1990, month: 1, day: 1 },
      data: { pattern: { dung_than: "Thủy" } },
    });
    writeShot("H_contract_mismatch.html", mismatch.container.innerHTML);
    mismatch.unmount();
    const hist = renderBoot(
      record("cur", tuyenData("cur"), "Tuyền", { year: 1984, month: 7, day: 13, hour: 21 }),
      "?from=history&id=hist",
      record("hist", dungData("hist"), "Dũng", { year: 1985, month: 9, day: 18, hour: 8 }),
    );
    writeShot("I_history.html", hist.container.innerHTML);
    hist.unmount();
    expect(true).toBe(true);
  });
});
