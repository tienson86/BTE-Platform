/**
 * UI-11 Card 08 Interpretation — published narrative, no frontend reasoning.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  INTERPRETATION_TITLE,
  INTERPRETATION_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptInterpretationCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const PACK05 = {
  contract: "pack05_narrative_result_v1",
  sections: [
    {
      intent: "overview",
      title: "Tóm tắt điều hành",
      paragraphs: [{ text: "Người định khung. Lá số cho thấy xu hướng sức gánh cao trên nền Chính Ấn." }],
    },
    {
      intent: "observation",
      title: "Quan sát",
      paragraphs: [
        { text: "Nhật chủ: Canh (Kim)." },
        { text: "Chính Ấn — sinh thuận, dưỡng có khuôn" },
      ],
    },
    {
      intent: "reasoning",
      title: "Lý giải",
      paragraphs: [
        {
          text: "Nền Chính Ấn và trạng thái Thân vượng giải thích vì sao hướng chỉnh là đặt khung trách nhiệm rõ trước khi mở rộng.",
        },
      ],
    },
    {
      intent: "impact",
      title: "Tác động",
      paragraphs: [
        { text: "Sự nghiệp phù hợp hơn khi đặt khung trách nhiệm rõ trước khi mở rộng." },
      ],
    },
    {
      intent: "priority",
      title: "Khuyến nghị",
      paragraphs: [
        { text: "1. Xây: Dựng khung vừa đủ để việc chạy, không chồng lớp kiểm soát." },
        { text: "2. Làm: Hỷ thần bổ trợ riêng: Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng." },
        { text: "3. Củng cố: Giữ một nền học/dưỡng, không bọc mọi việc." },
        { text: "4. Làm: Ra một việc nhỏ sau pha ủ để ấn không kín." },
      ],
    },
    {
      intent: "closing",
      title: "Kết luận",
      paragraphs: [{ text: "Giữ hướng này trên nền Chính Ấn." }],
    },
  ],
};

const LIVE_ANALYSIS = {
  integrated_narrative: {
    status: "complete",
    observation: {
      available: true,
      sentences: ["Nhật chủ được đọc là Thân vượng.", "Điểm lực đã công bố là 0.87."],
    },
    reasoning: { available: true, sentences: ['{"dayun_runtime":{"kind":"x"}}'] },
    impact: {
      available: true,
      sentences: ["Với thế Thân vượng đã công bố, nhịp vận hành nghiêng về chủ động."],
    },
    recommendation: {
      available: true,
      sentences: ["Ưu tiên hướng Dụng thần đã công bố: Hỏa · Đinh · Chính Quan."],
    },
    executive_summary: {
      available: true,
      sentences: ["Cách cục đã công bố là Chính Ấn."],
    },
    summary: { available: true, sentences: ["Điểm lực đã công bố là 0.87."] },
  },
  narrative_result: PACK05,
} as AnalysisDataDto;

const CLEAN_INTEGRATED = {
  integrated_narrative: {
    observation: {
      available: true,
      sentences: ["Điều nổi bật là nền Chính Ấn với nội lực đủ để gánh trách nhiệm."],
    },
    reasoning: {
      available: true,
      sentences: ["Nền tảng này giải thích vì sao cần đặt khung trước khi mở rộng."],
    },
    impact: {
      available: true,
      sentences: ["Cách làm việc thiên về chịu tải trong môi trường có trách nhiệm rõ."],
    },
    recommendation: {
      available: true,
      sentences: ["Giữ khung vừa đủ để việc chạy, không chồng lớp kiểm soát."],
    },
  },
} as AnalysisDataDto;

function renderLive(analysis: AnalysisDataDto = LIVE_ANALYSIS) {
  return render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
}

function intCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="interpretation"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-11 Interpretation card", () => {
  it("I1 replaces the Interpretation skeleton with the real component", () => {
    const { container } = renderLive();
    const card = intCard(container);
    expect(card.getAttribute("data-implemented")).toBe("interpretation");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("I2 keeps Interpretation span at 12/12", () => {
    const { container } = renderLive();
    expect(intCard(container).getAttribute("data-span")).toBe("12");
    expect(intCard(container).className).toMatch(/bte-cdash__card--span-12/);
  });

  it("I3 shows the customer title LUẬN GIẢI TỔNG THỂ", () => {
    const { container } = renderLive();
    expect(intCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(
      INTERPRETATION_TITLE,
    );
    expect(intCard(container).textContent).not.toMatch(/Narrative Engine|AI Analysis|Executive Narrative/);
  });

  it("I4 Quan sát source is canonical", () => {
    const { container } = renderLive(CLEAN_INTEGRATED);
    expect(intCard(container).querySelector('[data-int-zone="observation"]')?.getAttribute("data-int-source")).toBe(
      "integrated_narrative.observation",
    );
    expect(adaptInterpretationCard(LIVE_ANALYSIS).zones.find((zone) => zone.id === "observation")?.source).toBe(
      "narrative_result.observation",
    );
  });

  it("I5 Lý do source is canonical", () => {
    const model = adaptInterpretationCard(LIVE_ANALYSIS);
    expect(model.zones.find((zone) => zone.id === "reasoning")?.source).toBe("narrative_result.reasoning");
    expect(model.zones.find((zone) => zone.id === "reasoning")?.body).toMatch(/đặt khung trách nhiệm/);
  });

  it("I6 Tác động source is canonical", () => {
    const model = adaptInterpretationCard(LIVE_ANALYSIS);
    expect(model.zones.find((zone) => zone.id === "impact")?.source).toBe("narrative_result.impact");
    expect(model.zones.find((zone) => zone.id === "impact")?.body).toMatch(/Sự nghiệp/);
  });

  it("I7 Khuyến nghị source is canonical", () => {
    const model = adaptInterpretationCard(LIVE_ANALYSIS);
    expect(model.zones.find((zone) => zone.id === "recommendation")?.source).toBe(
      "narrative_result.recommendation",
    );
    expect(model.zones.find((zone) => zone.id === "recommendation")?.body).toMatch(/Dựng khung vừa đủ/);
  });

  it("I8 does not perform frontend astrology reasoning", () => {
    const adapter = readFileSync(resolve(ROOT, "interpretationAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "InterpretationCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/\$\{.*strength.*nên/);
    expect(card).not.toMatch(/\$\{.*strength/);
    expect(adapter).not.toContain("useful_god.useful_god");
  });

  it("I9 I10 I11 omit raw engine metadata, JSON, and rule ids", () => {
    const { container } = renderLive();
    const text = intCard(container).textContent || "";
    expect(text).not.toMatch(/dayun_runtime|source_unit_ids|rule_id|pat_ca_01|str_003/);
    expect(text).not.toContain("{");
    expect(text).not.toContain("0.87");
  });

  it("I12 does not duplicate raw data chips", () => {
    const { container } = renderLive();
    expect(intCard(container).textContent).not.toMatch(/Nhật chủ: Canh/);
    expect(intCard(container).textContent).not.toMatch(/4\/5\/6\/3\/1/);
  });

  it("I13 recommendation is not a full Action Plan", () => {
    const { container } = renderLive();
    const rec = intCard(container).querySelector('[data-int-zone="recommendation"]')?.textContent || "";
    expect(rec).not.toMatch(/Top Priorities|action_plan_90d|Kế hoạch 90|90 ngày/);
    expect((rec.match(/\d+\./g) || []).length).toBeLessThanOrEqual(3);
  });

  it("I14 missing narrative fails cleanly", () => {
    const { container } = renderLive({});
    expect(intCard(container).querySelector("[data-int-empty]")?.textContent).toBe(
      "Chưa đủ dữ liệu để tạo luận giải tổng thể.",
    );
  });

  it("I15 does not call engines", () => {
    const adapter = readFileSync(resolve(ROOT, "interpretationAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/engines\.|InterpretationEngine|compose_integrated_narrative/);
  });

  it("I16 I17 grid and upstream cards remain", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    expect(container.querySelector('[data-card="luck"]')?.getAttribute("data-implemented")).toBe("luck");
    expect(container.querySelector('[data-card="shensha"]')?.getAttribute("data-implemented")).toBe("shensha");
  });

  it("I18 no Dashboard skeleton remains", () => {
    const { container } = renderLive();
    expect(container.querySelectorAll("[data-card][data-skeleton='true']")).toHaveLength(0);
    expect(container.querySelector('[data-card="action-plan"]')?.getAttribute("data-implemented")).toBe(
      "action-plan",
    );
  });

  it("I19 expand/collapse is accessible", () => {
    const { container } = renderLive();
    const button = intCard(container).querySelector("button.bte-int__toggle");
    expect(button).toBeTruthy();
    expect(button?.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(button as HTMLButtonElement);
    expect(intCard(container).getAttribute("data-expanded")).toBe("true");
    expect(intCard(container).querySelector("[data-int-closing]")?.textContent).toMatch(/Chính Ấn/);
  });

  it("I20 mobile CSS is single column without page overflow rules", () => {
    const css = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
    expect(css).toMatch(/\.bte-int__zones \{[\s\S]*grid-template-columns: 1fr;/);
    expect(css).toMatch(/overflow-wrap: anywhere/);
  });

  it("semantic safety: raw Strength/Pattern/Useful God/Luck do not create prose", () => {
    const rebound = adaptInterpretationCard({
      strength: { strength_level: "Thân vượng" },
      pattern: { cach_cuc: "Chính Ấn" },
      useful_god: { useful_god: "Hỏa" },
      luck: { current_cycle: { gan_zhi: "Ất Tỵ" } },
    } as AnalysisDataDto);
    expect(rebound.available).toBe(false);
    expect(rebound.zones.every((zone) => zone.body === "")).toBe(true);
    const adapter = readFileSync(resolve(ROOT, "interpretationAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/\$\{strength\} nên|vận tốt|vận xấu/);
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(container.querySelector('[data-layout="visual"]')).toBeTruthy();
    expect(intCard(container).textContent).toContain("nền tảng ổn định");
    expect(INTERPRETATION_VISUAL_FIXTURE.leadSource).toBe("visual-fixture");
  });

  it("canonical routing still resolves visual layout", () => {
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
  });
});
