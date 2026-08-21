/**
 * G2-06 — customer end-to-end UI acceptance.
 * Presentation/workflow only. Does not recompute Gate-1 engines.
 */

import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { PortalPage } from "../../src/screens/canonical_desktop";
import {
  OFFICIAL_DOCX_LABEL,
  OFFICIAL_PDF_LABEL,
  PRINT_VIEW_LABEL,
  VIEW_REPORT_LABEL,
} from "../../src/export/customerExport";
import {
  CONTRACT_MISMATCH_MESSAGE,
  CORRUPT_HISTORY_MESSAGE,
  CUSTOMER_USEFUL_GOD_CONTRACT,
  MISSING_HISTORY_MESSAGE,
} from "../../src/resultState/customerContract";
import type { AnalysisDataDto } from "../../src/models";
import type { StoredResultRecord } from "../../src/resultState/currentResult";

const CONTRACT = CUSTOMER_USEFUL_GOD_CONTRACT;
const SHOT_DIR = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../../../release/gate_02/screenshots/g2_06",
);
const HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";
const DUNG = "Thủy · Nhâm · Thực Thần";
const TUYEN = "Mộc · Ất · Chính Quan";
const SON = "Hỏa · Đinh · Chính Quan";
const TRUONG = "Kim · Tân · Chính Ấn";

function record(id: string, data: AnalysisDataDto, name: string, birth: Record<string, unknown>): StoredResultRecord {
  return { analysis_id: id, input: { ...birth, full_name: name }, data };
}

function payload(id: string, extra: AnalysisDataDto): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    result_meta: { analysis_id: id, customer_contract: CONTRACT, created_at: "2026-08-21T03:00:00.000Z" },
    narrative_result: { contract: "pack05_narrative_result_v1", status: "ok", summary: { identity: id } },
    ...extra,
  };
}

function collect(node: HTMLElement | null): string {
  return (node?.textContent || "").replace(/\s+/g, " ").trim();
}

function renderBoot(current: StoredResultRecord | null, search = "", history: StoredResultRecord | null = null) {
  const boot = resolveResultBoot(current, search, history);
  const rendered = render(
    <PortalPage
      request={boot.request}
      initialData={boot.initialData}
      previewFallback={boot.previewFallback}
      fullReport={boot.fullReport}
      analysisId={boot.analysisId}
      resultSource={boot.resultSource}
      exportPayload={boot.exportPayload}
      reanalyzeHref={boot.reanalyzeHref}
    />,
  );
  return { ...rendered, boot };
}

describe("G2-06 customer E2E UI", () => {
  it("export actions are distinct and labeled", () => {
    const stored = record(
      "id-dung",
      payload("id-dung", {
        bazi: { day_pillar: { stem: "Canh", branch: "Thân" } },
        strength: { strength_level: "strong", strength_score: 1 },
        pattern: { cach_cuc: "Cấu trúc đặc biệt được nhận diện: Giá Sắc" },
        useful_god: { useful_display: DUNG, favorable_display: HY_NEUTRAL, short_reason: "TIẾT", climate_preference_label: "Điều hậu ưu tiên Hỏa" },
      }),
      "Ngô Đắc Dũng",
      { year: 1985, month: 9, day: 18, hour: 8 },
    );
    renderBoot(stored);
    expect(screen.getByRole("link", { name: VIEW_REPORT_LABEL })).toBeTruthy();
    expect(screen.getByRole("button", { name: PRINT_VIEW_LABEL })).toBeTruthy();
    expect(screen.getByRole("button", { name: OFFICIAL_PDF_LABEL })).toBeTruthy();
    expect(screen.getByRole("button", { name: OFFICIAL_DOCX_LABEL })).toBeTruthy();
    expect(screen.queryByRole("button", { name: /Xuất PDF/i })).toBeNull();
  });

  it("Dũng / Tuyền / Sơn / Trường core fields stay on one analysis", () => {
    const dung = renderBoot(
      record(
        "dung",
        payload("dung", {
          bazi: {
            year_pillar: { stem: "Ất", branch: "Sửu" },
            month_pillar: { stem: "Ất", branch: "Dậu" },
            day_pillar: { stem: "Canh", branch: "Thân", ten_god: "Nhật Chủ" },
            hour_pillar: { stem: "Canh", branch: "Thìn" },
            day_master: "Canh",
          },
          strength: { strength_level: "strong", strength_score: 1 },
          pattern: { cach_cuc: "Cấu trúc đặc biệt được nhận diện: Giá Sắc", detected_special_pattern: "gia_sac", qualification_level: 1, ug_override_eligible: false },
          useful_god: { useful_display: DUNG, favorable_display: HY_NEUTRAL, short_reason: "Kim sinh Thủy", climate_preference_label: "Điều hậu ưu tiên Hỏa" },
        }),
        "Ngô Đắc Dũng",
        { year: 1985, month: 9, day: 18, hour: 8 },
      ),
    );
    const dungText = collect(dung.container);
    expect(dungText).toContain("Ất");
    expect(dungText).toContain("Canh");
    expect(dungText).toContain(DUNG);
    expect(dungText).toContain(HY_NEUTRAL);
    expect(dungText).not.toContain("Thổ · Mậu · Thiên Ấn");
    expect(dungText).not.toMatch(/\bmale\b|\bfemale\b|\bmock\b|\bfixture\b/);
    dung.unmount();

    const tuyen = renderBoot(
      record(
        "tuyen",
        payload("tuyen", {
          bazi: { day_pillar: { stem: "Mậu", branch: "Thân" }, day_master: "Mậu" },
          strength: { strength_level: "strong", strength_score: 0.66 },
          pattern: { cach_cuc: "Kiếp Tài" },
          useful_god: { useful_display: TUYEN, favorable_display: HY_NEUTRAL, short_reason: "Chế", climate_preference_label: "Điều hậu ưu tiên Thủy" },
        }),
        "Vũ Thị Thanh Tuyền",
        { year: 1984, month: 7, day: 13, hour: 21, minute: 1 },
      ),
    );
    const tuyenText = collect(tuyen.container);
    expect(tuyenText).toContain("0.66");
    expect(tuyenText).toContain("Kiếp Tài");
    expect(tuyenText).toContain(TUYEN);
    expect(tuyenText).not.toContain("Tòng Tài");
    expect(tuyenText).not.toContain("cực nhược");
    tuyen.unmount();

    const son = renderBoot(
      record(
        "son",
        payload("son", {
          strength: { strength_level: "strong", strength_score: 0.87 },
          pattern: { cach_cuc: "Chính Ấn" },
          useful_god: { useful_display: SON, favorable_display: HY_NEUTRAL, climate_preference_label: "Điều hậu ưu tiên Hỏa" },
        }),
        "Nguyễn Tiến Sơn",
        { year: 1987, month: 1, day: 21, hour: 4, minute: 30 },
      ),
    );
    expect(collect(son.container)).toContain(SON);
    son.unmount();

    const truong = renderBoot(
      record(
        "truong",
        payload("truong", {
          strength: { strength_level: "weak", strength_score: 0.34 },
          pattern: { cach_cuc: "Quan Ấn tương sinh — Chính Quan sinh Chính Ấn trợ Nhật chủ" },
          useful_god: { useful_display: TRUONG, favorable_display: "Thủy · Nhâm · Tỷ Kiên", short_reason: "Sinh / Trợ", climate_preference_label: "Điều hậu ưu tiên Thủy" },
        }),
        "Cao Xuân Trường",
        { year: 1989, month: 7, day: 21, hour: 15, minute: 45 },
      ),
    );
    expect(collect(truong.container)).toContain(TRUONG);
    expect(collect(truong.container)).toContain("Thủy · Nhâm · Tỷ Kiên");
    truong.unmount();
  });

  it("empty, missing History, corrupt, and old contract stay safe", () => {
    const empty = renderBoot(null);
    expect(screen.getByText("Chưa có kết quả phân tích")).toBeTruthy();
    expect(empty.container.querySelector('a[href="/analyze"]')).toBeTruthy();
    expect(collect(empty.container)).not.toContain(DUNG);
    empty.unmount();

    const current = record(
      "id-tuyen",
      payload("id-tuyen", { useful_god: { useful_display: TUYEN, favorable_display: HY_NEUTRAL } }),
      "Tuyền",
      { year: 1984, month: 7, day: 13, hour: 21 },
    );
    const missing = renderBoot(current, "?from=history&id=missing-id", null);
    expect(missing.boot.resultSource).toBe("missing");
    expect(collect(missing.container)).toContain(MISSING_HISTORY_MESSAGE);
    expect(collect(missing.container)).not.toContain(TUYEN);
    missing.unmount();

    const corrupt = renderBoot(current, "?from=history&id=bad", { analysis_id: "bad", data: null, corrupt: true });
    expect(collect(corrupt.container)).toContain(CORRUPT_HISTORY_MESSAGE);
    expect(collect(corrupt.container)).not.toContain(TUYEN);
    corrupt.unmount();

    const old = renderBoot(current, "?from=history&id=legacy", {
      analysis_id: "legacy",
      input: { year: 1990, month: 1, day: 1 },
      data: { pattern: { dung_than: "Thủy", hy_than: "Kim" } },
    });
    expect(collect(old.container)).toContain(CONTRACT_MISMATCH_MESSAGE);
    expect(collect(old.container)).not.toContain("Thủy");
    old.unmount();
  });

  it("History Dũng then current Tuyền do not mix", () => {
    const history = record(
      "id-dung",
      payload("id-dung", { useful_god: { useful_display: DUNG, favorable_display: HY_NEUTRAL } }),
      "Ngô Đắc Dũng",
      { year: 1985, month: 9, day: 18, hour: 8 },
    );
    const current = record(
      "id-tuyen",
      payload("id-tuyen", { useful_god: { useful_display: TUYEN, favorable_display: HY_NEUTRAL } }),
      "Vũ Thị Thanh Tuyền",
      { year: 1984, month: 7, day: 13, hour: 21, minute: 1 },
    );
    const hist = renderBoot(current, "?from=history&id=id-dung", history);
    expect(hist.boot.exportPayload?.analysisId).toBe("id-dung");
    expect(collect(hist.container)).toContain(DUNG);
    expect(collect(hist.container)).not.toContain(TUYEN);
    hist.unmount();
    const now = renderBoot(current, "", history);
    expect(now.boot.exportPayload?.analysisId).toBe("id-tuyen");
    expect(collect(now.container)).toContain(TUYEN);
    expect(now.container.querySelector(".rp-history-banner")).toBeNull();
  });

  it("writes G2-06 HTML captures", () => {
    mkdirSync(SHOT_DIR, { recursive: true });
    const write = (file: string, html: string) => {
      writeFileSync(path.join(SHOT_DIR, file), `<!doctype html><meta charset="utf-8"><title>${file}</title>${html}`, "utf8");
    };
    const empty = renderBoot(null);
    write("empty_result.html", empty.container.innerHTML);
    empty.unmount();
    const current = record(
      "id-tuyen",
      payload("id-tuyen", {
        bazi: { day_pillar: { stem: "Mậu", branch: "Thân" } },
        strength: { strength_level: "strong", strength_score: 0.66 },
        pattern: { cach_cuc: "Kiếp Tài" },
        useful_god: { useful_display: TUYEN, favorable_display: HY_NEUTRAL },
      }),
      "Vũ Thị Thanh Tuyền",
      { year: 1984, month: 7, day: 13, hour: 21, minute: 1 },
    );
    const dung = record(
      "id-dung",
      payload("id-dung", {
        bazi: { day_pillar: { stem: "Canh", branch: "Thân" } },
        strength: { strength_level: "strong", strength_score: 1 },
        pattern: { cach_cuc: "Cấu trúc đặc biệt được nhận diện: Giá Sắc" },
        useful_god: { useful_display: DUNG, favorable_display: HY_NEUTRAL },
      }),
      "Ngô Đắc Dũng",
      { year: 1985, month: 9, day: 18, hour: 8 },
    );
    const hist = renderBoot(current, "?from=history&id=id-dung", dung);
    write("history_then_current.html", hist.container.innerHTML);
    hist.unmount();
    const now = renderBoot(current, "", dung);
    write("current_after_history.html", now.container.innerHTML);
    now.unmount();
    expect(true).toBe(true);
  });
});
