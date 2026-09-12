import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { GOLDEN_ASSESSMENT_FLOW, GOLDEN_ASSESSMENT_STORY } from "../../src/features/number_energy/goldenAssessment";
import { GOLDEN_PHONE_PAIRS } from "../../src/features/number_energy/goldenPairs";
import { adaptNumberEnergyPresentation } from "../../src/features/number_energy/presentationAdapter";
import {
  NUMBER_ENERGY_CONTRACT_FREEZE,
  RUNTIME_GAP_STATUS,
  type NumberEnergyRuntimePayload,
} from "../../src/features/number_energy/presentationContract";

const FORBIDDEN_VIEW_TOKENS = [
  "energy_id",
  "source_span",
  "occurrence_id",
  "strength_rank",
  "verified_by_runtime",
  "analysis_body",
  "fixture_id",
  "knowledge_version",
  "DIEN_NIEN",
  "THIEN_Y",
  "HIDDEN",
  "AMPLIFIED",
  "sequence_state",
  "canonical_meaning_key",
  "semantic_key",
  "copy_key",
  "reason_key",
  "narrative.paragraphs",
];

const PAGE_FILES = [
  "NumberEnergyPage.tsx",
  "index.ts",
  "ResultSection.tsx",
  "InputSection.tsx",
] as const;

function goldenRuntimePayload(): NumberEnergyRuntimePayload {
  return {
    purpose_context: "phone_number",
    metadata: { input_raw: "0328278786", purpose_context: "phone_number" },
    input_raw: "0328278786",
    pair_occurrences: [
      pair("32", "Họa Hại", "HUNG", "Hung", "Nhẹ", [true, false, false, false]),
      pair("28", "Sinh Khí", "CAT", "Cát", "Nhẹ", [true, false, false, false]),
      pair("82", "Sinh Khí", "CAT", "Cát", "Nhẹ", [true, false, false, false]),
      pair("27", "Thiên Y", "CAT", "Cát", "Nhẹ", [true, false, false, false]),
      pair("78", "Diên Niên", "CAT", "Cát", "Mạnh", [true, true, true, false]),
      pair("87", "Diên Niên", "CAT", "Cát", "Mạnh", [true, true, true, false]),
      pair("78", "Diên Niên", "CAT", "Cát", "Mạnh", [true, true, true, false]),
      pair("86", "Thiên Y", "CAT", "Cát", "Mạnh", [true, true, true, false]),
    ],
    pair_summary: {
      pair_count: 8,
      supportive_pair_count: 7,
      challenging_pair_count: 1,
      primary_energy_label: "Diên Niên",
      terminal_energy_label: "Thiên Y",
      terminal_pair_digits: "86",
    },
    energy_distribution: [
      { energy_label: "Sinh Khí", count: 2 },
      { energy_label: "Thiên Y", count: 2 },
      { energy_label: "Diên Niên", count: 3 },
      { energy_label: "Phục Vị", count: 0 },
      { energy_label: "Họa Hại", count: 1 },
      { energy_label: "Ngũ Quỷ", count: 0 },
      { energy_label: "Lục Sát", count: 0 },
      { energy_label: "Tuyệt Mệnh", count: 0 },
    ],
    triple_occurrences: [
      triple("328", "Họa Hại", "Sinh Khí", "Khẩu tài tốt", "Khả năng giao tiếp và diễn đạt là điểm mạnh của tổ hợp này. Lời nói có giá trị và dễ được người khác lắng nghe, tiếp nhận.", ["Giao tiếp", "Công việc"], "STANDARD"),
      triple("282", "Sinh Khí", "Sinh Khí", "Quý nhân và cơ hội được tăng cường", "Sinh Khí được tiếp nối, làm nổi bật khả năng gặp người hỗ trợ, cơ hội và những mối quan hệ thuận lợi.", ["Quý nhân", "Cơ hội"], "STANDARD"),
      triple("827", "Sinh Khí", "Thiên Y", "Quý nhân mang đến Tài vận", "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.", ["Tài vận", "Quý nhân"], "FEATURED"),
      triple("278", "Thiên Y", "Diên Niên", "Tài đi vào sự nghiệp", "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh hoặc phát triển sự nghiệp.", ["Tài vận", "Công việc"], "FEATURED"),
      triple("787", "Diên Niên", "Diên Niên", "Năng lực nghề nghiệp được tăng cường", "Diên Niên được tiếp nối, làm nổi bật năng lực làm việc, trách nhiệm và khả năng tổ chức.", ["Công việc", "Năng lực"], "COMPACT"),
      triple("878", "Diên Niên", "Diên Niên", "Năng lực nghề nghiệp được tăng cường", "Diên Niên tiếp tục xuất hiện, cho thấy công việc và năng lực nghề nghiệp là chủ đề được duy trì rõ trong dãy.", ["Công việc", "Năng lực"], "COMPACT"),
      triple("786", "Diên Niên", "Thiên Y", "Năng lực nghề nghiệp tạo Tài", "Tài vận chủ yếu đến từ năng lực làm việc, chuyên môn và sự nghiệp.", ["Tài vận", "Công việc"], "FEATURED"),
    ],
    chain: {
      primary_energy_label: "Diên Niên",
      secondary_energy_labels: ["Sinh Khí", "Thiên Y"],
      terminal_energy_label: "Thiên Y",
      terminal_pair_digits: "86",
      terminal_triple_digits: "786",
      terminal_interaction_label: "Diên Niên → Thiên Y",
      dominant_flow_summary: "Diên Niên chủ đạo, kết Thiên Y",
    },
    wealth_flow: {
      stages: [
        {
          id: "WF-01",
          label: "TÀI VẬN",
          headline: "Có Thiên Y",
          evidence: "27 · 86",
          interaction: "",
          narrative: "Dãy xuất hiện hai điểm Thiên Y, vì vậy trục tài vận được hình thành rõ.",
        },
        {
          id: "WF-02",
          label: "TÀI TỪ ĐÂU?",
          headline: "Quý nhân & cơ hội",
          evidence: "827",
          interaction: "Sinh Khí → Thiên Y",
          narrative: "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.",
        },
        {
          id: "WF-03",
          label: "TÀI ĐI ĐÂU?",
          headline: "Sự nghiệp & lập nghiệp",
          evidence: "278",
          interaction: "Thiên Y → Diên Niên",
          narrative: "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh hoặc phát triển sự nghiệp.",
        },
        {
          id: "WF-04",
          label: "HẬU VẬN",
          headline: "Thiên Y",
          evidence: "786",
          interaction: "Diên Niên → Thiên Y",
          narrative:
            "Phần cuối dãy quy về Thiên Y. Diên Niên đứng trước cho thấy năng lực và công việc tiếp tục là nguồn dẫn tới tài vận.",
        },
      ],
    },
    wealth_story: {
      nodes: ["Quý nhân & cơ hội", "Tài", "Sự nghiệp", "Tài"],
      display: "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài",
      synthesis:
        "Dòng tài vận của dãy đi theo hướng: quý nhân và cơ hội mở đường, nguồn lực được đưa vào sự nghiệp, và phần cuối lại quy về khả năng tạo Tài từ chính năng lực nghề nghiệp.",
    },
    domain_insights: [
      domain("Tài vận", "Có đường Tài tương đối rõ"),
      domain("Công việc & sự nghiệp", "Đây là một trong những điểm mạnh nhất của dãy"),
      domain("Tình cảm & quan hệ", "Quan hệ xã hội có yếu tố hỗ trợ"),
      domain("Tính cách & năng lực", "Trách nhiệm và năng lực làm việc khá rõ"),
      domain("Cân bằng trường khí", "Cát tinh giữ vai trò chủ đạo"),
    ],
    strengths: [
      finding("Quý nhân có thể mở đường cho Tài", "Quan hệ, người hỗ trợ hoặc những cơ hội thuận lợi có thể trở thành một trong những con đường hình thành Tài."),
      finding("Năng lực nghề nghiệp nổi bật", "Diên Niên được lặp lại liên tiếp, làm công việc, trách nhiệm và năng lực nghề nghiệp trở thành chủ đề mạnh của dãy."),
      finding("Công việc có khả năng tạo thành quả", "Phần cuối dãy tiếp tục đưa năng lực nghề nghiệp về Thiên Y, làm rõ hơn con đường tạo Tài bằng chuyên môn và công việc."),
      finding("Khẩu tài có thể phát huy tích cực", "Khả năng nói và diễn đạt có giá trị khi được sử dụng đúng cách, đặc biệt trong giao tiếp và công việc với con người."),
    ],
    cautions: [
      finding("Cần chú ý cách sử dụng lời nói", "Họa Hại xuất hiện ở đầu thân số, vì vậy lời nói và cách phản ứng vẫn là một điểm cần tiết chế. Khi dùng tốt, bộ 328 lại phát huy thành khẩu tài."),
      finding("Không nên chỉ nhìn số lượng Cát tinh", "Dãy có nhiều Cát tinh, nhưng giá trị thực tế vẫn nằm ở cách các trường khí nối tiếp và vận động với nhau."),
    ],
    evidence: [
      {
        title: "Cặp năng lượng",
        source: "pair_occurrences",
        items: [
          { source: "pair_occurrences", ref: "32", label: "Họa Hại" },
          { source: "pair_occurrences", ref: "28 / 82", label: "Sinh Khí" },
          { source: "pair_occurrences", ref: "27 / 86", label: "Thiên Y" },
          { source: "pair_occurrences", ref: "78 / 87 / 78", label: "Diên Niên" },
        ],
      },
      {
        title: "Bộ ba nổi bật",
        source: "triple_occurrences",
        items: [
          { source: "triple_occurrences", ref: "827", label: "Sinh Khí → Thiên Y" },
          { source: "triple_occurrences", ref: "278", label: "Thiên Y → Diên Niên" },
          { source: "triple_occurrences", ref: "786", label: "Diên Niên → Thiên Y" },
        ],
      },
    ],
    assessment: {
      title: "Đánh giá tổng thể",
      summary:
        "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y. Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy.",
      story_line: "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI",
      story_nodes: ["QUÝ NHÂN", "TÀI", "SỰ NGHIỆP", "TÀI"],
    },
    recommendation: {
      state: "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG",
      label: "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG",
      summary: "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài.",
      copy_key: "CONTINUE",
    },
    score: {
      total: 82,
      max: 100,
      display: "82 / 100",
      grade: "TỐT",
      verified_by_runtime: true,
      breakdown: [
        { label: "Cấu trúc năng lượng", earned: 21, max: 25 },
        { label: "Dòng tài vận", earned: 22, max: 25 },
        { label: "Công việc & trợ lực", earned: 17, max: 20 },
        { label: "Ổn định & rủi ro", earned: 10, max: 15 },
        { label: "Năng lượng kết", earned: 12, max: 15 },
      ],
      reasons: [
        { title: "Cấu trúc Cát giữ vai trò chủ đạo", summary: "Sinh Khí, Thiên Y và Diên Niên chiếm phần lớn thân số." },
        { title: "Dòng Tài có nguồn rõ", summary: "Sinh Khí → Thiên Y cho thấy quý nhân và cơ hội có khả năng dẫn tới Tài." },
        { title: "Công việc là trục mạnh", summary: "Diên Niên xuất hiện liên tiếp và tiếp tục dẫn tới Thiên Y ở phần cuối dãy." },
        { title: "Họa Hại cần được sử dụng đúng cách", summary: "Họa Hại xuất hiện ở đầu thân số, nhưng tổ hợp tiếp theo là Họa Hại → Sinh Khí, giúp khả năng giao tiếp có hướng phát huy tích cực." },
      ],
    },
    grade: "TỐT",
    verified_by_runtime: true,
  };
}

function pair(
  pair_digits: string,
  display_name: string,
  category: string,
  category_label: string,
  strength_label: string,
  strength_visual: boolean[],
): Record<string, unknown> {
  return { pair_digits, display_name, category, category_label, strength_label, strength_visual };
}

function triple(
  digits: string,
  left_energy_label: string,
  right_energy_label: string,
  customer_title: string,
  customer_summary: string,
  domains: string[],
  priority: string,
): Record<string, unknown> {
  return {
    digits,
    left_energy_label,
    right_energy_label,
    customer_title,
    customer_summary,
    domains,
    priority,
    interpretation_status: "DEFINED",
  };
}

function domain(name: string, conclusion: string): Record<string, unknown> {
  return { domain: name, conclusion, narrative: `${name} — ${conclusion}`, caution: "" };
}

function finding(title: string, summary: string): Record<string, unknown> {
  return { title, summary, semantic_key: "omit-from-view" };
}

function featureSource(fileName: string): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, `../../src/features/number_energy/${fileName}`), "utf8");
}

function entrySource(): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, "../../src/entries/numberEnergyApp.tsx"), "utf8");
}

describe("Number Energy RB06 presentation adapter", () => {
  it("maps Golden runtime payload to Static Golden Fixture values", () => {
    const result = adaptNumberEnergyPresentation(goldenRuntimePayload());
    const { view, slotSource } = result;
    expect(result.freezeLabel).toBe(NUMBER_ENERGY_CONTRACT_FREEZE);
    expect(result.gaps).toEqual([]);
    expect(view.hero.displayValue).toBe("0328 278 786");
    expect(view.hero.scoreDisplay).toBe("82 / 100");
    expect(view.hero.grade).toBe("TỐT");
    expect(view.hero.primaryEnergy).toBe("Diên Niên");
    expect(view.hero.terminalEnergy).toBe("Thiên Y");
    expect(view.hero.analysisTypeLabel).toBe("Số điện thoại");
    expect(view.pairs.map((item) => item.digits)).toEqual(["32", "28", "82", "27", "78", "87", "78", "86"]);
    expect(view.pairs.map((item) => item.categoryLabel)).toEqual(
      GOLDEN_PHONE_PAIRS.map((item) => item.categoryLabel),
    );
    expect(view.quick_structure.favorableValue).toBe("7 cặp");
    expect(view.quick_structure.challengingValue).toBe("1 cặp");
    expect(view.quick_structure.primaryValue).toBe("Diên Niên");
    expect(view.quick_structure.terminalValue).toBe("Thiên Y");
    expect(view.wealth_flow.stages).toHaveLength(4);
    expect(view.wealth_flow.stages.map((item) => item.id)).toEqual(["WF-01", "WF-02", "WF-03", "WF-04"]);
    expect(view.wealth_flow.stages.map((item) => item.headline)).toEqual([
      "Có Thiên Y",
      "Quý nhân & cơ hội",
      "Sự nghiệp & lập nghiệp",
      "Thiên Y",
    ]);
    expect(view.triples).toHaveLength(7);
    expect(view.triples.map((item) => item.digits)).toEqual(["328", "282", "827", "278", "787", "878", "786"]);
    expect(view.triples.filter((item) => item.priority === "featured")).toHaveLength(3);
    expect(view.distribution).toHaveLength(8);
    expect(view.distribution.map((item) => item.count)).toEqual([2, 2, 3, 0, 1, 0, 0, 0]);
    expect(view.distribution.find((item) => item.label === "Diên Niên")?.role).toBe("primary");
    expect(view.domains).toHaveLength(5);
    expect(view.findings.strengths).toHaveLength(4);
    expect(view.findings.cautions).toHaveLength(2);
    expect(view.score.totalDisplay).toBe("82 / 100");
    expect(view.score.grade).toBe("TỐT");
    expect(view.score.breakdown).toHaveLength(5);
    expect(view.assessment.story).toEqual([...GOLDEN_ASSESSMENT_STORY]);
    expect(view.assessment.flow).toEqual([...GOLDEN_ASSESSMENT_FLOW]);
    expect(view.assessment.recommendationState).toBe("PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG");
    expect(view.assessment.recommendationSupporting).toBe(
      "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài.",
    );
    expect(view.expert_seam).toEqual({ visible: false, hidden: true, ariaHidden: true });
    expect(slotSource["P-S11"]).toBe("GOLDEN_FIXTURE");
    for (const slot of ["P-S00", "P-S01", "P-S02", "P-S03", "P-S04", "P-S05", "P-S06", "P-S07", "P-S08", "P-S09", "P-S10"] as const) {
      expect(slotSource[slot]).toBe("RUNTIME");
    }
  });

  it("falls back to Golden fixture and records RUNTIME_GAP when a required field is missing", () => {
    const payload = goldenRuntimePayload();
    delete payload.pair_occurrences;
    const result = adaptNumberEnergyPresentation(payload);
    expect(result.slotSource["P-S01"]).toBe("GOLDEN_FIXTURE");
    expect(result.slotSource["P-S00"]).toBe("RUNTIME");
    expect(result.view.pairs.map((item) => item.digits)).toEqual(["32", "28", "82", "27", "78", "87", "78", "86"]);
    expect(result.gaps.some((item) => item.id === "G19" && item.status === RUNTIME_GAP_STATUS)).toBe(true);
    expect(result.gaps.every((item) => item.status === RUNTIME_GAP_STATUS)).toBe(true);
  });

  it("keeps score and hero on Golden fixture when verified_by_runtime is not true", () => {
    const payload = goldenRuntimePayload();
    payload.verified_by_runtime = false;
    if (payload.score && typeof payload.score === "object") {
      (payload.score as { verified_by_runtime: boolean }).verified_by_runtime = false;
    }
    const result = adaptNumberEnergyPresentation(payload);
    expect(result.slotSource["P-S08"]).toBe("GOLDEN_FIXTURE");
    expect(result.slotSource["P-S00"]).toBe("GOLDEN_FIXTURE");
    expect(result.view.score.totalDisplay).toBe("82 / 100");
    expect(result.view.score.note).toContain("minh họa");
    expect(result.gaps.some((item) => item.id === "G20")).toBe(true);
  });

  it("does not expose forbidden technical tokens in the Customer view", () => {
    const result = adaptNumberEnergyPresentation(goldenRuntimePayload());
    const blob = JSON.stringify(result.view);
    for (const token of FORBIDDEN_VIEW_TOKENS) {
      expect(blob).not.toContain(token);
    }
    expect(blob).not.toContain('"CAT"');
    expect(blob).not.toContain('"HUNG"');
    expect(blob).not.toContain("FEATURED");
    expect(JSON.stringify(result)).not.toContain("verified_by_runtime");
  });

  it("maps motorbike_plate to the motorcycle customer label", () => {
    const payload = goldenRuntimePayload();
    payload.purpose_context = "motorbike_plate";
    const result = adaptNumberEnergyPresentation(payload);
    expect(result.view.hero.analysisTypeLabel).toBe("Biển số xe máy");
  });

  it("unwraps an API envelope without changing Golden mapping", () => {
    const result = adaptNumberEnergyPresentation({ data: goldenRuntimePayload() });
    expect(result.view.hero.displayValue).toBe("0328 278 786");
    expect(result.slotSource["P-S01"]).toBe("RUNTIME");
  });

  it("omits UNDEFINED triple narrative instead of composing from left/right", () => {
    const payload = goldenRuntimePayload();
    payload.triple_occurrences = [
      {
        digits: "999",
        left_energy_label: "Họa Hại",
        right_energy_label: "Họa Hại",
        interpretation_status: "UNDEFINED",
        priority: "STANDARD",
        domains: [],
      },
    ];
    const result = adaptNumberEnergyPresentation(payload);
    expect(result.slotSource["P-S04"]).toBe("RUNTIME");
    expect(result.view.triples).toEqual([
      {
        digits: "999",
        sourceLabel: "Họa Hại",
        targetLabel: "Họa Hại",
        title: "",
        narrative: "",
        domains: "",
        priority: "standard",
      },
    ]);
  });

  it("is not imported by the frozen page, barrel, or app entry", () => {
    for (const fileName of PAGE_FILES) {
      expect(featureSource(fileName)).not.toContain("presentationAdapter");
    }
    expect(entrySource()).not.toContain("presentationAdapter");
    expect(entrySource()).not.toContain("adaptNumberEnergyPresentation");
  });
});
