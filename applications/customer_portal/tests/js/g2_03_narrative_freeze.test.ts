/**
 * G2-03 — Interpretation / Narrative release freeze.
 * Presentation consistency only. Does not recompute Gate-1 engines.
 */

import { describe, expect, it } from "vitest";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { hasInternalRuleId } from "../../src/adapters/customerFacingPresentation";
import { hasUsableNarrativeResult } from "../../src/adapters/narrativeResultAdapter";
import { UNAVAILABLE_CONCLUSION } from "../../src/adapters/contentGuards";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { adaptResultPageViewModel } from "../../src/screens/result/adapters/resultPresentationAdapter";
import {
  CONTRACT_MISMATCH_MESSAGE,
  CUSTOMER_USEFUL_GOD_CONTRACT,
  customerContractStatus,
} from "../../src/resultState/customerContract";
import type { AnalysisDataDto } from "../../src/models";
import type { StoredResultRecord } from "../../src/resultState/currentResult";

const CONTRACT = CUSTOMER_USEFUL_GOD_CONTRACT;
const HY_NEUTRAL = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";
const PLACEHOLDER_RE = /\{\{[^}]+\}\}|\$\{[^}]+\}|\bNone\b|\bnull\b|\bundefined\b/;

function dungNarrative(): AnalysisDataDto["narrative_result"] {
  return {
    contract: "pack05_narrative_result_v1",
    run_id: "id-dung",
    status: "complete",
    summary: {
      identity: "Nhật chủ Canh thân vượng. Mô hình V1.0 ưu tiên Thủy để tiết Kim.",
      strengths: ["Thân vượng"],
      weaknesses: [],
      priority_recommendation: "Ưu tiên trục Thủy · Nhâm · Thực Thần theo mô hình cân bằng V1.0.",
    },
    sections: [
      {
        id: "sec-executive_summary",
        title: "Tóm tắt điều hành",
        paragraphs: [{ role: "observation", text: "Cấu trúc đặc biệt được nhận diện: Giá Sắc. Dụng thần chính: Thủy · Nhâm · Thực Thần." }],
      },
      {
        id: "sec-observation",
        title: "Quan sát",
        paragraphs: [{ role: "observation", text: "Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn. Thân vượng." }],
      },
      {
        id: "sec-reasoning",
        title: "Lý giải",
        paragraphs: [{
          role: "explanation",
          text: "Nhật chủ Canh Kim thân vượng → Tiết → Kim sinh Thủy → Nhâm = Thực Thần. Hỷ thần bổ trợ riêng: Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng. Về điều hậu, Hỏa có vai trò ôn ấm, không thay Overall Dụng.",
        }],
      },
      {
        id: "sec-impact",
        title: "Tác động",
        paragraphs: [{ role: "impact", text: "Thập thần ngày là Nhật Chủ; can cùng loại ở trụ khác là Tỷ Kiên." }],
      },
      {
        id: "sec-recommendation",
        title: "Khuyến nghị",
        paragraphs: [{ role: "suggestion", text: "Ưu tiên xem xét tiết khí Kim theo mô hình V1.0." }],
      },
      {
        id: "sec-warning",
        title: "Lưu ý",
        paragraphs: [{ role: "warning", text: "Không chẩn đoán y khoa. Không hứa hiệu quả tài chính." }],
      },
      {
        id: "sec-conclusion",
        title: "Kết luận",
        paragraphs: [{ role: "conclusion", text: "Overall Dụng là Thủy; Điều hậu ưu tiên Hỏa là việc riêng." }],
      },
    ],
  };
}

function dungData(): AnalysisDataDto {
  return {
    analysis_id: "id-dung",
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
    useful_god: {
      useful_display: "Thủy · Nhâm · Thực Thần",
      favorable_display: HY_NEUTRAL,
      short_reason: "Nhật chủ Canh Kim thân vượng → Tiết → Kim sinh Thủy → Nhâm = Thực Thần.",
      climate_preference_label: "Điều hậu ưu tiên Hỏa",
    },
    narrative_result: dungNarrative(),
  };
}

function collectNarrative(data: AnalysisDataDto): string {
  const vm = adaptAnalysisToCanonicalDesktop(data, {
    request: { year: 1985, month: 9, day: 18, hour: 8, full_name: "Ngô Đắc Dũng" },
    requestId: "id-dung",
    source: "api",
  });
  const page = adaptResultPageViewModel(vm);
  const parts = [
    page.executive.headline.text,
    ...page.executive.points.items,
    ...page.interpretation.blocks.flatMap((block) => [
      block.title,
      block.observation.text,
      block.explanation.text,
    ]),
  ];
  return parts.join(" ");
}

describe("G2-03 narrative freeze", () => {
  it("uses the same analysis ID on Result, narrative, and report model", () => {
    const stored: StoredResultRecord = {
      analysis_id: "id-dung",
      input: { year: 1985, month: 9, day: 18, hour: 8, full_name: "Ngô Đắc Dũng" },
      data: dungData(),
    };
    const boot = resolveResultBoot(stored, "");
    expect(boot.analysisId).toBe("id-dung");
    expect(boot.fullReport?.analysisId).toBe("id-dung");
    expect(boot.initialData?.narrativeResult?.run_id).toBe("id-dung");
  });

  it("does not contradict Strength, Pattern, Dụng, or Hỷ", () => {
    const blob = collectNarrative(dungData());
    expect(blob).toMatch(/Thân vượng|thân vượng/);
    expect(blob).not.toMatch(/Nhật chủ suy nhược|cực nhược/);
    expect(blob).toContain("Giá Sắc");
    expect(blob).not.toMatch(/chuyên cách hoàn chỉnh|ưu tiên Ấn vì chuyên cách/);
    expect(blob).toContain("Thủy · Nhâm · Thực Thần");
    expect(blob).not.toContain("Thổ · Mậu · Thiên Ấn");
    expect(blob).toContain(HY_NEUTRAL);
    expect(blob).not.toMatch(/Hỷ thần là/);
    expect(blob).not.toContain("Tòng Tài");
  });

  it("keeps Điều hậu separate from Overall Dụng", () => {
    const blob = collectNarrative(dungData());
    expect(blob).toMatch(/Điều hậu|ôn ấm/);
    expect(blob).not.toMatch(/Hỏa chính là Overall|Hỏa chính là Dụng/);
  });

  it("does not leak rule IDs, placeholders, or mock narrative", () => {
    const blob = collectNarrative(dungData());
    expect(hasInternalRuleId(blob)).toBe(false);
    expect(blob).not.toMatch(PLACEHOLDER_RE);
    expect(blob).not.toMatch(/\b(preview|mock|fixture)\b/i);
  });

  it("does not fabricate chart-specific narrative when narrative_result is missing", () => {
    const data: AnalysisDataDto = {
      analysis_id: "empty-n",
      useful_god_source: { contract: CONTRACT },
      useful_god: { useful_display: "Thủy · Nhâm · Thực Thần", favorable_display: HY_NEUTRAL },
      strength: { strength_level: "strong", strength_score: 1 },
    };
    const vm = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
    expect(hasUsableNarrativeResult(vm.narrativeResult)).toBe(false);
    const page = adaptResultPageViewModel(vm);
    const interp = page.interpretation.blocks.map((block) => block.observation.text).join(" ");
    expect(interp).toContain(UNAVAILABLE_CONCLUSION);
    expect(interp).not.toMatch(/Giá Sắc|Thủy · Nhâm · Thực Thần/);
  });

  it("does not treat unversioned History as current V1.0 narrative truth", () => {
    const stored: StoredResultRecord = {
      analysis_id: "legacy-1",
      input: { year: 1985, month: 9, day: 18, hour: 8, full_name: "Ngô Đắc Dũng" },
      data: {
        analysis_id: "legacy-1",
        useful_god: { useful_display: "Thủy · Nhâm · Thực Thần" },
        narrative_result: dungNarrative(),
      },
    };
    expect(customerContractStatus(stored.data)).toBe("unversioned");
    const boot = resolveResultBoot(stored, "");
    expect(boot.resultSource).toBe("contract");
    expect(boot.initialData?.statusMessage).toBe(CONTRACT_MISMATCH_MESSAGE);
    expect(hasUsableNarrativeResult(boot.initialData?.narrativeResult)).toBe(false);
  });
});
