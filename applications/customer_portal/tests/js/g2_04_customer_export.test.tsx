/**
 * G2-04 — customer export actions, official PDF vs Print, history isolation.
 */

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { PortalPage } from "../../src/screens/canonical_desktop";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  OFFICIAL_DOCX_LABEL,
  OFFICIAL_PDF_LABEL,
  PRINT_VIEW_LABEL,
  VIEW_REPORT_LABEL,
  customerExportBlockMessage,
  customerExportReady,
} from "../../src/export/customerExport";
import { filenameFromDisposition } from "../../src/api/types";
import {
  CONTRACT_MISMATCH_MESSAGE,
  CUSTOMER_USEFUL_GOD_CONTRACT,
  EMPTY_RESULT_MESSAGE,
} from "../../src/resultState/customerContract";
import type { AnalysisDataDto } from "../../src/models";
import type { StoredResultRecord } from "../../src/resultState/currentResult";

const CONTRACT = CUSTOMER_USEFUL_GOD_CONTRACT;
const HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";

function record(id: string, data: AnalysisDataDto, name: string): StoredResultRecord {
  return {
    analysis_id: id,
    input: { year: 1985, month: 9, day: 18, hour: 8, minute: 0, gender: "male", full_name: name },
    data,
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
    pattern: { cach_cuc: "Cấu trúc đặc biệt được nhận diện: Giá Sắc" },
    useful_god: {
      useful_display: "Thủy · Nhâm · Thực Thần",
      favorable_display: HY_NEUTRAL,
      short_reason: "TIẾT",
      climate_preference_label: "Điều hậu ưu tiên Hỏa",
    },
  };
}

function tuyenData(id: string): AnalysisDataDto {
  return {
    analysis_id: id,
    useful_god_source: { contract: CONTRACT },
    bazi: {
      day_pillar: { stem: "Mậu", branch: "Thân", ten_god: "Nhật Chủ" },
      day_master: "Mậu",
    },
    strength: { strength_level: "strong", strength_score: 0.66 },
    pattern: { cach_cuc: "Kiếp Tài" },
    useful_god: {
      useful_display: "Mộc · Ất · Chính Quan",
      favorable_display: HY_NEUTRAL,
    },
  };
}

describe("G2-04 customer export", () => {
  it("labels official PDF, DOCX, Print view, and Full Report separately", () => {
    const stored = record("dung-current", dungData("dung-current"), "Ngô Đắc Dũng");
    const boot = resolveResultBoot(stored, "");
    render(
      <PortalPage
        request={boot.request}
        initialData={boot.initialData}
        previewFallback={boot.previewFallback}
        fullReport={boot.fullReport}
        analysisId={boot.analysisId}
        resultSource={boot.resultSource}
        exportPayload={boot.exportPayload}
      />,
    );
    const reportLink = screen.getByRole("link", { name: VIEW_REPORT_LABEL });
    expect(reportLink.getAttribute("href")).toBe("/reports");
    expect(screen.getByRole("button", { name: PRINT_VIEW_LABEL })).toBeTruthy();
    expect(screen.getByRole("button", { name: OFFICIAL_PDF_LABEL })).toBeTruthy();
    expect(screen.getByRole("button", { name: OFFICIAL_DOCX_LABEL })).toBeTruthy();
    expect(screen.queryByRole("button", { name: /Xuất PDF/i })).toBeNull();
  });

  it("history boot exports the selected history analysis, not current", () => {
    const current = record("dung-current", dungData("dung-current"), "Ngô Đắc Dũng");
    const history = record("tuyen-hist", tuyenData("tuyen-hist"), "Vũ Thị Thanh Tuyền");
    const boot = resolveResultBoot(current, "?from=history&id=tuyen-hist", history);
    expect(boot.exportPayload?.analysisId).toBe("tuyen-hist");
    expect(boot.exportPayload?.source).toBe("history");
    expect(boot.exportPayload?.data.useful_god?.useful_display).toBe("Mộc · Ất · Chính Quan");
  });

  it("current boot does not keep a previous history selection", () => {
    const current = record("dung-current", dungData("dung-current"), "Ngô Đắc Dũng");
    const history = record("tuyen-hist", tuyenData("tuyen-hist"), "Vũ Thị Thanh Tuyền");
    const boot = resolveResultBoot(current, "", history);
    expect(boot.exportPayload?.analysisId).toBe("dung-current");
    expect(boot.exportPayload?.source).toBe("current");
    expect(boot.exportPayload?.data.useful_god?.useful_display).toBe("Thủy · Nhâm · Thực Thần");
  });

  it("blocks unofficial or empty payloads", () => {
    expect(customerExportReady(null)).toBe(false);
    expect(customerExportBlockMessage(null)).toBe(EMPTY_RESULT_MESSAGE);
    expect(
      customerExportBlockMessage({
        analysisId: "old",
        source: "history",
        data: { analysis_id: "old", pattern: { cach_cuc: "Chính Ấn" } },
      }),
    ).toBe(CONTRACT_MISMATCH_MESSAGE);
  });

  it("parses RFC 5987 download filenames", () => {
    const header =
      'attachment; filename="BTE_BaoCao_NgoDacDung_19850918_V1.pdf"; filename*=UTF-8\'\'BTE_BaoCao_NgoDacDung_19850918_V1.pdf';
    expect(filenameFromDisposition(header, "fallback.pdf")).toBe(
      "BTE_BaoCao_NgoDacDung_19850918_V1.pdf",
    );
  });
});
