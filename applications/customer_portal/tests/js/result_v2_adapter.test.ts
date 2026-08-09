import { describe, expect, it } from "vitest";
import { adaptPortalResult } from "../../src/features/result_v2/adapter/portalPresentationAdapter";
import { clampSummaryBullets } from "../../src/features/result_v2/utils/clamp";
import { resultV2ReadyReport } from "./result_v2_fixture";

describe("result_v2 adapter", () => {
  it("clamps summary bullets to 5", () => {
    expect(clampSummaryBullets(["a", "b", "c", "d", "e", "f"])).toHaveLength(5);
  });

  it("maps presentation envelope without engine types", () => {
    const model = adaptPortalResult(resultV2ReadyReport);
    expect(model.contract_id).toBe("bte.portal.result_ui.v2");
    expect(model.hero?.name).toBe("Nguyễn Văn An");
    expect(model.summary?.bullets).toHaveLength(5);
    expect(model.page.state).toBe("partial_ready");
    expect(model.recommendations[0]?.reason).toContain("vai trò");
    expect(model.technical.collapsed).toBe(true);
    expect(model.technical.available).toBe(true);
    expect(JSON.stringify(model)).not.toContain("AnalysisResult");
    expect(JSON.stringify(model)).not.toContain("<html>");
  });

  it("returns error when hero is missing", () => {
    const model = adaptPortalResult({
      success: true,
      presentation: {
        identity: { full_name: "A" },
        summary: { bullets: ["Một câu đủ nghĩa."] },
      },
    });
    expect(model.page.state).toBe("error");
    expect(model.hero).toBeNull();
  });

  it("returns empty when presentation is absent and success", () => {
    const model = adaptPortalResult({ success: true });
    expect(model.page.state).toBe("empty");
  });

  it("hides charts when none published", () => {
    const model = adaptPortalResult({
      success: true,
      presentation: {
        identity: {
          full_name: "Lan",
          headline: "Giữ nhịp ổn định",
          one_line_summary: "Ưu tiên hoàn thiện trước khi mở rộng.",
          consultation_status: "ready",
        },
        summary: { bullets: ["Nên hoàn thiện nền tảng trước."] },
        recommendations: [
          {
            id: "r1",
            domain: "career",
            title: "Giữ vai trò rõ",
            reason: "Vì cấu trúc hiện tại cần sự rõ ràng.",
            expected_result: "Giảm phân tán.",
            action: "Từ chối việc ngoài phạm vi chính.",
          },
        ],
        domains: {
          career: { available: true, recommendation_ids: ["r1"] },
          wealth: { available: true, intro: "Giữ chi tiêu ổn." },
          relationship: { available: true, intro: "Ưu tiên lắng nghe." },
          health: { available: true, intro: "Giữ giấc ngủ." },
          luck: { available: true, intro: "Đừng bung sức." },
        },
      },
    });
    expect(model.page.state).toBe("ready");
    expect(model.charts).toHaveLength(0);
    expect(model.nav.items.find((item) => item.target_ui_id === "Charts")?.visible).toBe(false);
  });
});
