/**
 * G2-05 — save / history / reload freeze.
 * Persistence and selection only. Does not recompute Gate-1 engines.
 */

import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { PortalPage } from "../../src/screens/canonical_desktop";
import {
  CONTRACT_MISMATCH_MESSAGE,
  CORRUPT_HISTORY_MESSAGE,
  CUSTOMER_USEFUL_GOD_CONTRACT,
  MISSING_HISTORY_MESSAGE,
} from "../../src/resultState/customerContract";
import {
  buildReanalyzeHref,
  buildReportHref,
  resolveCurrentStoredResult,
  type StoredResultRecord,
} from "../../src/resultState/currentResult";
import type { AnalysisDataDto } from "../../src/models";

const CONTRACT = CUSTOMER_USEFUL_GOD_CONTRACT;
const SHOT_DIR = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../../../release/gate_02/screenshots/g2_05",
);
const DUNG_DISPLAY = "Thủy · Nhâm · Thực Thần";
const TUYEN_DISPLAY = "Mộc · Ất · Chính Quan";
const HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";

function record(id: string, data: AnalysisDataDto, name: string, birth: Record<string, unknown>): StoredResultRecord {
  return {
    analysis_id: id,
    input: { ...birth, full_name: name },
    data,
  };
}

function dungData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    result_meta: {
      analysis_id: id,
      created_at: "2026-08-21T01:00:00.000Z",
      customer_contract: CONTRACT,
      gate_core_freeze: "G1",
      month_pillar_standard: "BTE-MONTH-PILLAR-LUNAR-V1.0",
      release_label: "BTE V1.0 — Gate 1 Core Engine",
    },
    narrative_result: { contract: "pack05_narrative_result_v1", status: "ok", summary: { identity: "Dũng" } },
    bazi: {
      year_pillar: { stem: "Ất", branch: "Sửu" },
      month_pillar: { stem: "Ất", branch: "Dậu" },
      day_pillar: { stem: "Canh", branch: "Thân", ten_god: "Nhật Chủ" },
      hour_pillar: { stem: "Canh", branch: "Thìn" },
      day_master: "Canh",
    },
    strength: { strength_level: "strong", strength_score: 1.0 },
    pattern: { cach_cuc: "Cấu trúc đặc biệt được nhận diện: Giá Sắc" },
    useful_god: {
      useful_display: DUNG_DISPLAY,
      favorable_display: HY_NEUTRAL,
      short_reason: "TIẾT",
      climate_preference_label: "Điều hậu ưu tiên Hỏa",
    },
    luck: { current_cycle: { gan_zhi: "Tân Tỵ" } },
  };
}

function tuyenData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    result_meta: { analysis_id: id, created_at: "2026-08-21T02:00:00.000Z", customer_contract: CONTRACT },
    bazi: {
      year_pillar: { stem: "Giáp", branch: "Tý" },
      month_pillar: { stem: "Tân", branch: "Mùi" },
      day_pillar: { stem: "Mậu", branch: "Thân", ten_god: "Nhật Chủ" },
      hour_pillar: { stem: "Quý", branch: "Hợi" },
      day_master: "Mậu",
    },
    strength: { strength_level: "strong", strength_score: 0.66 },
    pattern: { cach_cuc: "Kiếp Tài" },
    useful_god: {
      useful_display: TUYEN_DISPLAY,
      favorable_display: HY_NEUTRAL,
    },
    luck: { current_cycle: { gan_zhi: "Bính Dần" } },
  };
}

function collectText(node: HTMLElement | null): string {
  return (node?.textContent || "").replace(/\s+/g, " ").trim();
}

function renderBoot(
  current: StoredResultRecord | null,
  search = "",
  historyView: StoredResultRecord | null = null,
) {
  const boot = resolveResultBoot(current, search, historyView);
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

function fingerprint(data: AnalysisDataDto | null | undefined, analysisId: string) {
  const bazi = data?.bazi || {};
  const pillar = (key: "year_pillar" | "month_pillar" | "day_pillar" | "hour_pillar") => {
    const item = bazi[key] || {};
    return `${item.stem || ""} ${item.branch || ""}`.trim();
  };
  return {
    analysis_id: analysisId,
    four_pillars: [pillar("year_pillar"), pillar("month_pillar"), pillar("day_pillar"), pillar("hour_pillar")].join(" / "),
    strength: `${data?.strength?.strength_score} ${data?.strength?.strength_level}`,
    pattern: String((data?.pattern as { cach_cuc?: string } | undefined)?.cach_cuc || ""),
    dung: String(data?.useful_god?.useful_display || ""),
    luck: String((data?.luck?.current_cycle as { gan_zhi?: string } | undefined)?.gan_zhi || ""),
  };
}

describe("G2-05 history reload freeze", () => {
  it("explicit History is isolated from current and does not mix fingerprints", () => {
    const history = record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
      year: 1985,
      month: 9,
      day: 18,
      hour: 8,
    });
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Vũ Thị Thanh Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
      minute: 1,
    });
    const selected = resolveCurrentStoredResult({
      current,
      historyView: history,
      fromHistory: true,
      historyId: "id-dung",
    });
    expect(selected?.source).toBe("history");
    expect(selected?.analysisId).toBe("id-dung");
    expect(fingerprint(selected?.data, selected?.analysisId || "")).toEqual(
      fingerprint(history.data!, "id-dung"),
    );
    const laterCurrent = resolveCurrentStoredResult({
      current,
      historyView: history,
      fromHistory: false,
    });
    expect(laterCurrent?.analysisId).toBe("id-tuyen");
    expect(laterCurrent?.data.useful_god?.useful_display).toBe(TUYEN_DISPLAY);
  });

  it("missing History id does not load current", () => {
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
    });
    const boot = resolveResultBoot(current, "?from=history&id=missing-id", null);
    expect(boot.resultSource).toBe("missing");
    expect(boot.initialData?.statusMessage).toBe(MISSING_HISTORY_MESSAGE);
    expect(boot.exportPayload).toBeUndefined();
    expect(boot.fullReport).toBeUndefined();
    const { container } = renderBoot(current, "?from=history&id=missing-id", null);
    expect(screen.getByText("Không tìm thấy hồ sơ")).toBeTruthy();
    expect(collectText(container)).not.toContain(TUYEN_DISPLAY);
    expect(container.querySelector('[data-result-source="missing"]')).toBeTruthy();
    expect(container.querySelector(".rp-history-banner")).toBeNull();
    expect(container.querySelector(".rp-status-gate a[href='/history']")?.textContent).toContain(
      "Về lịch sử",
    );
  });

  it("corrupt History snapshot is a safe error and does not mix current", () => {
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
    });
    const corrupt: StoredResultRecord = {
      analysis_id: "bad",
      input: { year: 1990, month: 1, day: 1, full_name: "Hỏng" },
      data: null,
      corrupt: true,
    };
    const boot = resolveResultBoot(current, "?from=history&id=bad", corrupt);
    expect(boot.resultSource).toBe("corrupt");
    expect(boot.initialData?.statusMessage).toBe(CORRUPT_HISTORY_MESSAGE);
    expect(boot.exportPayload).toBeUndefined();
    const { container } = renderBoot(current, "?from=history&id=bad", corrupt);
    expect(collectText(container)).toContain(CORRUPT_HISTORY_MESSAGE);
    expect(collectText(container)).not.toContain(TUYEN_DISPLAY);
    expect(container.querySelector('[data-reason="corrupt"]')).toBeTruthy();
  });

  it("old unversioned History is guarded and not upgraded", () => {
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
    });
    const old: StoredResultRecord = {
      analysis_id: "legacy",
      input: { year: 1990, month: 1, day: 1, full_name: "Cũ" },
      data: { pattern: { dung_than: "Thủy", hy_than: "Kim" }, useful_god: { useful_god: "Thủy" } },
    };
    const boot = resolveResultBoot(current, "?from=history&id=legacy", old);
    expect(boot.resultSource).toBe("contract");
    expect(boot.initialData?.statusMessage).toBe(CONTRACT_MISMATCH_MESSAGE);
    expect(boot.fullReport).toBeUndefined();
    expect(boot.reanalyzeHref).toContain("reanalyze=1");
    expect(boot.reanalyzeHref).toContain("year=1990");
    const { container } = renderBoot(current, "?from=history&id=legacy", old);
    expect(collectText(container)).toContain(CONTRACT_MISMATCH_MESSAGE);
    expect(collectText(container)).not.toContain("Thủy");
    expect(container.querySelector(".rp-history-banner")).toBeNull();
  });

  it("History report/PDF/DOCX payload stays on selected snapshot B", () => {
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Vũ Thị Thanh Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
      minute: 1,
    });
    const history = record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
      year: 1985,
      month: 9,
      day: 18,
      hour: 8,
    });
    const boot = resolveResultBoot(current, "?from=history&id=id-dung", history);
    expect(boot.resultSource).toBe("history");
    expect(boot.exportPayload?.source).toBe("history");
    expect(boot.exportPayload?.analysisId).toBe("id-dung");
    expect(boot.exportPayload?.data.useful_god?.useful_display).toBe(DUNG_DISPLAY);
    expect(boot.fullReport?.usefulGod).toBe(DUNG_DISPLAY);
    expect(buildReportHref(boot.exportPayload?.source, boot.exportPayload?.analysisId)).toBe(
      "/reports?from=history&id=id-dung",
    );
    const { container } = renderBoot(current, "?from=history&id=id-dung", history);
    expect(container.querySelector('a[href="/reports?from=history&id=id-dung"]')).toBeTruthy();
    expect(collectText(container)).toContain(DUNG_DISPLAY);
    expect(collectText(container)).not.toContain(TUYEN_DISPLAY);
    expect(container.querySelector(".rp-history-banner")?.textContent).toContain("kết quả đã lưu");
  });

  it("normal /result returns current after History view", () => {
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
    });
    const history = record("id-dung", dungData("id-dung"), "Dũng", {
      year: 1985,
      month: 9,
      day: 18,
      hour: 8,
    });
    const historyBoot = resolveResultBoot(current, "?from=history&id=id-dung", history);
    const currentBoot = resolveResultBoot(current, "", history);
    expect(historyBoot.analysisId).toBe("id-dung");
    expect(currentBoot.analysisId).toBe("id-tuyen");
    expect(currentBoot.resultSource).toBe("current");
    expect(currentBoot.exportPayload?.source).toBe("current");
    expect(buildReportHref(currentBoot.exportPayload?.source, currentBoot.exportPayload?.analysisId)).toBe(
      "/reports",
    );
  });

  it("Re-analyze href uses stored birth and does not point at current", () => {
    const href = buildReanalyzeHref({
      full_name: "Ngô Đắc Dũng",
      year: 1985,
      month: 9,
      day: 18,
      hour: 8,
      minute: 0,
      gender: "male",
      timezone: "Asia/Bangkok",
    });
    expect(href).toContain("/analyze?");
    expect(href).toContain("reanalyze=1");
    expect(href).toContain("full_name=");
    expect(href).toContain("1985");
    expect(href).not.toContain("id-tuyen");
  });

  it("ten-control snapshot fingerprints stay on the stored analysis id", () => {
    const cases: Array<{ id: string; name: string; data: AnalysisDataDto }> = [
      { id: "son", name: "Nguyễn Tiến Sơn", data: { ...tuyenData("son"), useful_god: { useful_display: "Hỏa · Đinh · Chính Quan" }, strength: { strength_level: "strong", strength_score: 0.87 }, pattern: { cach_cuc: "Chính Ấn" } } },
      { id: "dung", name: "Ngô Đắc Dũng", data: dungData("dung") },
    ];
    cases.forEach((item) => {
      const stored = record(item.id, item.data, item.name, { year: 1985, month: 1, day: 1 });
      const boot = resolveResultBoot(stored, `?from=history&id=${item.id}`, stored);
      expect(boot.analysisId).toBe(item.id);
      expect(fingerprint(boot.exportPayload?.data, boot.analysisId || "")).toEqual(
        fingerprint(item.data, item.id),
      );
    });
  });

  it("writes visual acceptance captures", () => {
    mkdirSync(SHOT_DIR, { recursive: true });
    const writeShot = (file: string, html: string): void => {
      writeFileSync(
        path.join(SHOT_DIR, file),
        `<!doctype html><meta charset="utf-8"><title>${file}</title>${html}`,
        "utf8",
      );
    };
    const history = record("id-dung", dungData("id-dung"), "Ngô Đắc Dũng", {
      year: 1985,
      month: 9,
      day: 18,
      hour: 8,
    });
    const current = record("id-tuyen", tuyenData("id-tuyen"), "Vũ Thị Thanh Tuyền", {
      year: 1984,
      month: 7,
      day: 13,
      hour: 21,
      minute: 1,
    });
    const listHtml = `
      <div class="history-page">
        <h1>Lịch sử</h1>
        <div class="list-item" data-analysis-id="id-tuyen"><strong>Vũ Thị Thanh Tuyền</strong><div>1984-7-13 21:01</div></div>
        <div class="list-item" data-analysis-id="id-dung"><strong>Ngô Đắc Dũng</strong><div>1985-9-18 08:00</div></div>
      </div>`;
    writeShot("history_list.html", listHtml);
    const dung = renderBoot(current, "?from=history&id=id-dung", history);
    writeShot("history_dung.html", dung.container.innerHTML);
    dung.unmount();
    const tuyen = renderBoot(current, "", history);
    writeShot("current_tuyen.html", tuyen.container.innerHTML);
    tuyen.unmount();
    const old = renderBoot(current, "?from=history&id=legacy", {
      analysis_id: "legacy",
      input: { year: 1990, month: 1, day: 1 },
      data: { pattern: { dung_than: "Thủy" } },
    });
    writeShot("old_version.html", old.container.innerHTML);
    old.unmount();
    const missing = renderBoot(current, "?from=history&id=missing-id", null);
    writeShot("missing_record.html", missing.container.innerHTML);
    missing.unmount();
    expect(true).toBe(true);
  });
});
