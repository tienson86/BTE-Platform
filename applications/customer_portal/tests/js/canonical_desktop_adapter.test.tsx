/**
 * Canonical Desktop adapter — maps orchestrator analysis → S00–S11 ViewModel.
 */

import { describe, expect, it } from "vitest";
import {
  adaptAnalysisToCanonicalDesktop,
  createCanonicalDesktopMockViewModel,
} from "../../src/adapters/canonicalDesktopAdapter";
import type { AnalysisDataDto } from "../../src/models";

const SAMPLE: AnalysisDataDto = {
  pipeline: ["calendar", "bazi", "pattern", "score", "interpretation", "report"],
  calendar: {
    day_can_chi: "Bính Dần",
    month_can_chi: "Giáp Ngọ",
    year_can_chi: "Canh Ngọ",
    hour_can_chi: "Tân Tỵ",
    solar_term: { name: "Lập Thu" },
    cung_phi: "Ly",
    menh_quai: "Ly Hỏa",
    nhom_trach: "Đông tứ mệnh",
  },
  bazi: {
    year_pillar: { stem: "Canh", branch: "Ngọ", nap_am: "Lộ Bàng Thổ" },
    month_pillar: { stem: "Giáp", branch: "Ngọ", nap_am: "Sa Trung Kim" },
    day_pillar: { stem: "Bính", branch: "Dần", nap_am: "Lư Trung Hỏa" },
    hour_pillar: { stem: "Tân", branch: "Tỵ", nap_am: "Bích Thượng Thổ" },
    day_master: "Bính",
    day_master_element: "Hỏa",
    day_master_yin_yang: "Dương",
    ten_gods: ["Chính Ấn", "Thiên Ấn", "Thực Thần"],
    shensha: ["Thiên Ất Quý Nhân", "Kiếp Sát", "Văn Xương"],
  },
  pattern: {
    cach_cuc: "Thực Thương",
    than_vuong_nhuoc: "Thân vượng",
    dung_than: "Thủy",
    hy_than: "Kim",
    ky_than: "Mộc",
  },
  useful_god: {
    useful_god: "Thủy",
    favorable_gods: ["Kim", "Thủy"],
    unfavorable_gods: ["Mộc", "Hỏa"],
  },
  strength: {
    strength_level: "strong",
    strength_score: 78,
    reasoning: "Nhật chủ được sinh trợ. Hỏa vượng trong cục.",
  },
  score: {
    grade: "B+",
    wuxing_series: [
      { label: "Mộc", value: 20 },
      { label: "Hỏa", value: 40 },
      { label: "Thổ", value: 15 },
      { label: "Kim", value: 15 },
      { label: "Thủy", value: 10 },
    ],
    ten_god_series: [
      { label: "Chính Ấn", value: 1.2 },
      { label: "Thiên Ấn", value: 1.0 },
      { label: "Thực Thần", value: 0.8 },
    ],
  },
  interpretation: {
    sections: [
      { title: "Tổng quan", body: "Bạn có tố chất lãnh đạo và nhiệt huyết rõ." },
      { title: "Điểm mạnh", body: "Quyết đoán và tinh thần trách nhiệm cao." },
    ],
  },
  report: {
    markdown: "# Kết luận\n\nNền tảng mệnh cục ổn định nếu duy trì cân bằng cảm xúc.",
  },
  customer: {
    full_name: "Nguyễn Văn Test",
    gender: "male",
  },
};

describe("adaptAnalysisToCanonicalDesktop", () => {
  it("maps Calendar + BaZi pillars into S03 with Han glyphs", () => {
    const vm = adaptAnalysisToCanonicalDesktop(SAMPLE, {
      request: {
        year: 1990,
        month: 8,
        day: 15,
        hour: 10,
        minute: 30,
        gender: "male",
        full_name: "Nguyễn Văn Test",
      },
      requestId: "req-1",
      source: "api",
    });

    expect(vm.source).toBe("api");
    expect(vm.s03.pillars).toHaveLength(4);
    expect(vm.s03.pillars[0].stem.han).toBe("庚");
    expect(vm.s03.pillars[0].stem.viet).toBe("Canh");
    expect(vm.s03.pillars[2].highlight).toBe(true);
    expect(vm.s00.profile.name).toBe("Nguyễn Văn Test");
  });

  it("maps Score / Pattern / Feng Shui / ShenSha / Report slices", () => {
    const vm = adaptAnalysisToCanonicalDesktop(SAMPLE, { source: "api" });

    expect(vm.s04.rows.find((r) => r.name === "Hỏa")?.pct).toBeGreaterThan(30);
    expect(vm.s02.items.find((i) => i.label === "Dụng thần")?.value).toBe("Thủy");
    expect(vm.s09.quai.center).toContain("Ly");
    expect(vm.s07.good.items).toContain("Thiên Ất Quý Nhân");
    expect(vm.s07.bad.items).toContain("Kiếp Sát");
    expect(vm.s05.percent).toBe(78);
    expect(vm.s11.executive.body.length).toBeGreaterThan(10);
  });

  it("prefers Pack 05 narrative_result over legacy interpretation text", () => {
    const withNarrative = {
      ...SAMPLE,
      interpretation: {
        sections: [
          { title: "Tổng quan", body: "Kích hoạt khi xác định Chính Cách." },
        ],
      },
      narrative_result: {
        contract: "pack05_narrative_result_v1",
        status: "partial_insufficient",
        summary: {
          identity: "Nhật chủ Bính · Cách cục Thực Thương",
          strengths: ["Quyết đoán có nguồn chứng"],
          weaknesses: ["Cần cân bằng cảm xúc"],
          priority_recommendation: "Ưu tiên phát huy Thủy",
          next_action: "Ưu tiên phát huy Thủy",
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
                text: "Quan sát từ dữ liệu phân tích: Nhật chủ Bính.",
                insufficient_data: false,
              },
            ],
          },
        ],
        recommendations: [
          {
            id: "rec-1",
            priority: "high",
            action: "Ưu tiên phát huy Thủy",
            reason: "Dụng thần Thủy",
            benefit: "",
            insufficient_data: false,
          },
        ],
      },
    };
    const vm = adaptAnalysisToCanonicalDesktop(withNarrative, { source: "api" });
    expect(vm.narrativeResult?.contract).toBe("pack05_narrative_result_v1");
    expect(vm.s08.executive.body).toContain("Nhật chủ Bính");
    expect(vm.s08.executive.body).not.toContain("Kích hoạt khi");
    expect(vm.s08.strengths.items[0]).toContain("Quyết đoán");
    expect(vm.s11.recommendations.items[0]).toContain("Thủy");
  });

  it("keeps fixture ViewModel for preview/tests", () => {
    const vm = createCanonicalDesktopMockViewModel();
    expect(vm.source).toBe("mock");
    expect(vm.s03.pillars).toHaveLength(4);
  });
});
