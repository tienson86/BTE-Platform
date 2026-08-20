/**
 * G1-08 addendum: internal male/female never leak on customer surfaces.
 */

import { describe, expect, it } from "vitest";
import {
  canonicalGender,
  customerGenderDisplay,
  genderDisplayLabel,
} from "../../src/adapters/genderDisplay";
import { adaptAnalysisToBaZiResult } from "../../src/adapters/baziResultAdapter";
import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { adaptLiveAnalysisResult } from "../../src/features/portal/liveAnalysisResultAdapter";
import { draftToAnalyzeRequest } from "../../src/features/portal/wizardAnalyzeRequest";
import { buildFullReportViewModel, renderFullReportHtml } from "../../src/report/fullReportViewModel";
import type { AnalysisDataDto } from "../../src/models";
import type { WizardDraft } from "../../src/features/portal/pages/AnalysisWizard";

const NARRATIVE = {
  contract: "pack05_narrative_result_v1",
  status: "complete",
  summary: {
    identity: "Nhật chủ Ất · Cách cục Tài tinh",
    priority_recommendation: "Ưu tiên môi trường ổn định",
    next_action: "Hoàn thiện một ưu tiên trước khi mở rộng",
    insufficient_flags: [],
  },
  sections: [
    {
      id: "sec-observation",
      intent: "observation",
      title: "Quan sát",
      paragraphs: [{ id: "p1", role: "observation", text: "Quan sát từ dữ liệu phân tích.", insufficient_data: false }],
    },
  ],
  recommendations: [
    {
      id: "rec-1",
      priority: "high",
      action: "Ưu tiên phát huy Mộc",
      reason: "Dụng thần Mộc",
      benefit: "",
      insufficient_data: false,
    },
  ],
  commercial_executive_summary: {
    central_message: "Giữ nhịp ổn định trước khi tăng tốc",
    supporting_points: ["Nên chọn vai trò rõ ràng"],
    conclusion: "Ưu tiên củng cố nền tảng trong giai tháng tới",
    composed_text: "Giữ nhịp ổn định trước khi tăng tốc.",
  },
  primary_recommendation: {
    what: "Chọn môi trường có cấu trúc",
    why: "Năng lực phát huy tốt hơn khi kỳ vọng được nói rõ",
    how: "Lọc cơ hội theo mức rõ ràng của vai trò",
    when: "Trong 90 ngày tới",
    expected_outcome: "Giảm hao tổn và tăng độ tin cậy",
    composed_text: "Chọn môi trường có cấu trúc trong 90 ngày tới.",
  },
};

function analysis(gender: "male" | "female"): AnalysisDataDto {
  return {
    pipeline: ["calendar", "bazi", "pattern", "score", "interpretation", "report"],
    customer: { full_name: "Nguyễn Văn An", gender, birth_place: "Hà Nội" },
    bazi: {
      day_master: "Canh",
      day_master_yin_yang: "Dương",
      year_pillar: { stem: "Bính", branch: "Dần" },
      month_pillar: { stem: "Tân", branch: "Sửu" },
      day_pillar: { stem: "Canh", branch: "Ngọ" },
      hour_pillar: { stem: "Mậu", branch: "Dần" },
    },
    narrative_result: NARRATIVE,
  };
}

function draft(overrides: Partial<WizardDraft> = {}): WizardDraft {
  return {
    name: "Nguyễn Văn An",
    place: "Hà Nội",
    year: "1987",
    month: "1",
    day: "21",
    hour: "4",
    minute: "30",
    gender: "male",
    calendar: "solar",
    ...overrides,
  };
}

describe("G1-08 gender display", () => {
  it("maps internal male to Nam and female to Nữ", () => {
    expect(genderDisplayLabel("male")).toBe("Nam");
    expect(genderDisplayLabel("female")).toBe("Nữ");
    expect(canonicalGender("male")).toBe("male");
    expect(canonicalGender("female")).toBe("female");
  });

  it("does not echo English gender labels", () => {
    expect(genderDisplayLabel("unknown")).toBe("—");
    expect(genderDisplayLabel("")).toBe("—");
    expect(genderDisplayLabel(null)).toBe("—");
    expect(customerGenderDisplay({ gender: "male" })).toBe("Nam");
    expect(customerGenderDisplay({ gender: "female", gender_label: "Nữ" })).toBe("Nữ");
  });

  it("blocks wizard analyze when gender is missing or invalid", () => {
    expect(draftToAnalyzeRequest(draft({ gender: "" }))).toBeNull();
    expect(draftToAnalyzeRequest(draft({ gender: "unknown" }))).toBeNull();
    expect(draftToAnalyzeRequest(draft({ gender: "male" }))?.gender).toBe("male");
    expect(draftToAnalyzeRequest(draft({ gender: "female" }))?.gender).toBe("female");
  });

  it("localizes Result, Canonical Desktop, Technical Info, and Full Report", () => {
    const male = analysis("male");
    const female = analysis("female");
    const request = {
      year: 1987,
      month: 1,
      day: 21,
      hour: 4,
      minute: 30,
      gender: "male" as const,
      full_name: "Nguyễn Văn An",
    };

    expect(adaptAnalysisToBaZiResult(male, { request }).profile.gender).toBe("Nam");
    expect(
      adaptAnalysisToBaZiResult(female, { request: { ...request, gender: "female" } }).profile.gender,
    ).toBe("Nữ");

    const desktop = adaptAnalysisToCanonicalDesktop(male, { request });
    expect(desktop.s00.profile.meta).toContain("Nam");
    expect(desktop.s00.profile.meta).not.toMatch(/\bmale\b/i);

    const live = adaptLiveAnalysisResult(female, { analysis_id: "anl_g108" });
    expect(live.ok).toBe(true);
    if (!live.ok) return;
    expect(live.report.presentation?.technical?.metadata?.gender).toBe("Nữ");
    expect(String(live.report.presentation?.technical?.metadata?.gender)).not.toMatch(/female/i);

    const model = buildFullReportViewModel(male, { input: request });
    expect(model.gender).toBe("Nam");
    const html = renderFullReportHtml(model);
    expect(html).toContain("Giới tính");
    expect(html).toContain("Nam");
    expect(html).not.toMatch(/\b(male|female)\b/i);
  });
});
