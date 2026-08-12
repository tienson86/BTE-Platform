import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { adaptPortalResult } from "../result_v2/adapter/portalPresentationAdapter";
import type { AnalysisDataDto } from "../../models";
import { adaptLiveAnalysisResult } from "./liveAnalysisResultAdapter";
import ResultViewerPage from "./pages/ResultViewerPage";
import { portalDemoReport } from "./fixtures/demoReport";

afterEach(() => {
  cleanup();
});

const LIVE_ANALYSIS: AnalysisDataDto = {
  pipeline: [
    "calendar",
    "bazi",
    "pattern",
    "score",
    "interpretation",
    "report",
    "narrative",
  ],
  stage: "analyze",
  customer: {
    full_name: "Trần Thị Bình",
    birth_place: "Đà Nẵng",
    timezone: "Asia/Ho_Chi_Minh",
    gender: "female",
  },
  bazi: {
    day_master: "Ất",
    year_pillar: { stem: "Canh", branch: "Ngọ" },
    month_pillar: { stem: "Tân", branch: "Mùi" },
    day_pillar: { stem: "Ất", branch: "Dậu" },
    hour_pillar: { stem: "Giáp", branch: "Thân" },
  },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    status: "complete",
    summary: {
      identity: "Nhật chủ Ất · Cách cục Tài tinh",
      strengths: ["Kiên nhẫn trong công việc", "Phối hợp nhóm tốt"],
      weaknesses: ["Dễ quá tải khi nhận nhiều việc"],
      priority_recommendation: "Ưu tiên môi trường ổn định",
      next_action: "Hoàn thiện một ưu tiên trước khi mở rộng",
      insufficient_flags: [],
    },
    sections: [
      {
        id: "sec-observation",
        intent: "observation",
        title: "Quan sát",
        paragraphs: [
          {
            id: "p1",
            role: "observation",
            text: "Quan sát từ dữ liệu phân tích: Nhật chủ Ất.",
            insufficient_data: false,
          },
        ],
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
      supporting_points: ["Nên chọn vai trò rõ ràng", "Giữ biên an toàn thời gian"],
      conclusion: "Ưu tiên củng cố nền tảng trong giai tháng tới",
      composed_text: "Giữ nhịp ổn định trước khi tăng tốc. Ưu tiên củng cố nền tảng.",
    },
    primary_recommendation: {
      what: "Chọn môi trường có cấu trúc",
      why: "Năng lực phát huy tốt hơn khi kỳ vọng được nói rõ",
      how: "Lọc cơ hội theo mức rõ ràng của vai trò",
      when: "Trong 90 ngày tới",
      expected_outcome: "Giảm hao tổn và tăng độ tin cậy",
      composed_text: "Chọn môi trường có cấu trúc trong 90 ngày tới.",
      capability_label: "Career Selection",
      role: "primary",
    },
    career_selection_assessment: {
      capability_id: "CAP-D1-CA-SEL",
      career_direction: { text: "Hướng chuyên môn sâu" },
      career_risks: { text: "Tránh nhận quá nhiều việc cùng lúc." },
      career_mitigation: { text: "Chỉ nhận thêm việc khi ưu tiên hiện tại đã ổn." },
    },
  },
};

describe("LAUNCH-03 liveAnalysisResultAdapter", () => {
  it("maps live analysis result successfully without fabrication", () => {
    const mapped = adaptLiveAnalysisResult(LIVE_ANALYSIS, {
      analysis_id: "anl_live_03",
    });
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const presentation = mapped.report.presentation;
    expect(presentation?.identity?.full_name).toBe("Trần Thị Bình");
    expect(presentation?.identity?.headline).toContain("ổn định");
    expect(presentation?.identity?.one_line_summary).toContain("nền tảng");
    expect(presentation?.summary?.bullets?.length).toBeGreaterThan(0);
    expect(presentation?.summary?.bullets?.[0]).toContain("vai trò rõ ràng");
    expect(presentation?.technical?.ids).toBe("anl_live_03");
    expect(presentation?.technical?.pillars).toContain("Ất Dậu");
    expect(presentation?.technical?.timezone).toBe("Asia/Ho_Chi_Minh");
    expect(presentation?.recommendations?.[0]?.title).toBe("Chọn môi trường có cấu trúc");
    expect(presentation?.recommendations?.[0]?.domain).toBe("career");
    expect(presentation?.warnings?.[0]?.body).toContain("quá nhiều việc");
    // Root narrative recs without domain are omitted (no invented domain).
    expect(
      presentation?.recommendations?.some((item) => item.id === "rec-1"),
    ).toBe(false);
    // No fabricated knowledge/charts.
    expect(presentation?.knowledge).toEqual([]);
    expect(presentation?.charts).toEqual([]);
  });

  it("preserves narrative content into PortalResultModel via existing adapter", () => {
    const mapped = adaptLiveAnalysisResult(LIVE_ANALYSIS, {
      analysis_id: "anl_live_03",
    });
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const model = adaptPortalResult(mapped.report);
    expect(model.contract_id).toBe("bte.portal.result_ui.v2");
    expect(model.hero?.name).toBe("Trần Thị Bình");
    expect(model.summary?.bullets.length).toBeGreaterThan(0);
    expect(model.page.state === "ready" || model.page.state === "partial_ready").toBe(true);
    expect(model.recommendations[0]?.reason).toContain("kỳ vọng");
    expect(model.technical.ids).toBe("anl_live_03");
  });

  it("returns controlled error for malformed live result", () => {
    const mapped = adaptLiveAnalysisResult(null, { analysis_id: "x" });
    expect(mapped.ok).toBe(false);
    if (mapped.ok) return;
    expect(mapped.error_code).toBe("live_analysis_malformed");
    expect(mapped.error_message).toContain("không hợp lệ");
  });

  it("returns controlled error when narrative is missing", () => {
    const mapped = adaptLiveAnalysisResult(
      { customer: { full_name: "A" }, bazi: {} },
      { analysis_id: "x" },
    );
    expect(mapped.ok).toBe(false);
    if (mapped.ok) return;
    expect(mapped.error_code).toBe("live_analysis_incomplete");
    expect(mapped.error_message).toContain("thiếu nội dung");
  });
});

describe("LAUNCH-03 ResultViewerPage live vs demo", () => {
  it("renders live Result V2 model and does not use demo source", () => {
    render(
      <ResultViewerPage
        analysisId="anl_live_03"
        analysisResult={LIVE_ANALYSIS}
      />,
    );
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-result-map")).toBe("api");
    expect(root?.getAttribute("data-analysis-id")).toBe("anl_live_03");
    expect(screen.getByText("Trần Thị Bình")).toBeTruthy();
    expect(screen.queryByText(portalDemoReport.presentation?.identity?.headline ?? "___")).toBeNull();
  });

  it("shows Vietnamese error for unmappable live session without demo fallback", () => {
    render(
      <ResultViewerPage
        analysisId="anl_bad"
        analysisResult={{ customer: { full_name: "A" } }}
      />,
    );
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-result-map")).toBe("error");
    expect(screen.getByRole("alert")).toBeTruthy();
    expect(screen.getByText("Không thể hiển thị kết quả")).toBeTruthy();
    expect(screen.getByText(/thiếu nội dung tư vấn/)).toBeTruthy();
    expect(screen.queryByText("Nguyễn Văn An")).toBeNull();
  });

  it("preserves demo/preview path when no live analysis id", () => {
    render(<ResultViewerPage />);
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("demo");
    expect(root?.getAttribute("data-result-map")).toBe("demo");
    expect(screen.getByText("Nguyễn Văn An")).toBeTruthy();
  });
});
