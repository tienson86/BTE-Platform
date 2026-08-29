/**
 * UI-12 Card 09 Action Plan — published actions only, no frontend astrology.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  ACTION_PLAN_TITLE,
  ACTION_PLAN_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptActionPlanCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  commercial_consulting: {
    status: "complete",
    catalog_id: "bte.consulting.knowledge.catalog.v1",
    sections: [
      {
        domain: "leadership",
        title: "Lãnh đạo",
        summary: "Dẫn bằng vai trò và ranh giới.",
        recommendations: ["Dựng khung vừa đủ để việc chạy."],
        source_unit_ids: ["ck-leadership-001"],
      },
    ],
  },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    recommendations: [
      { priority: "high", action: "1. Xây: Dựng khung vừa đủ để việc chạy, không chồng lớp kiểm soát." },
      { priority: "medium", action: "2. Làm: Hỷ thần bổ trợ riêng: Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng." },
      { priority: "medium", action: "3. Củng cố: Giữ một nền học/dưỡng, không bọc mọi việc." },
      { priority: "medium", action: "4. Làm: Ra một việc nhỏ sau pha ủ để ấn không kín." },
      { priority: "medium", action: "5. Làm: Mở một kênh thoát có phép và giữ nhịp." },
    ],
    sections: [
      {
        intent: "warning",
        title: "Điều cần lưu ý",
        paragraphs: [
          { text: "Không ôm thêm tải vì còn sức. Ủ có hạn; ra một việc." },
        ],
      },
      {
        intent: "priority",
        title: "Khuyến nghị",
        paragraphs: [
          { text: "1. Xây: Dựng khung vừa đủ để việc chạy, không chồng lớp kiểm soát." },
        ],
      },
    ],
  },
  luck: {
    customer_summary: "Theo dõi nhịp gánh trong giai đoạn hiện tại, giữ khung trước khi mở.",
    current_cycle: { gan_zhi: "Ất Tỵ", stem_element: "Mộc" },
  },
} as AnalysisDataDto;

function renderLive(analysis: AnalysisDataDto = LIVE_ANALYSIS) {
  return render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
}

function apCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="action-plan"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-12 Action Plan card", () => {
  it("A1 replaces the Action Plan skeleton with the real component", () => {
    const { container } = renderLive();
    const card = apCard(container);
    expect(card.getAttribute("data-implemented")).toBe("action-plan");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("A2 keeps Action Plan span at 12/12", () => {
    const { container } = renderLive();
    expect(apCard(container).getAttribute("data-span")).toBe("12");
    expect(apCard(container).className).toMatch(/bte-cdash__card--span-12/);
  });

  it("A3 shows the customer title KẾ HOẠCH HÀNH ĐỘNG", () => {
    const { container } = renderLive();
    expect(apCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(ACTION_PLAN_TITLE);
    expect(apCard(container).textContent).not.toMatch(/Action Plan|Recommendation Engine|Consulting Actions|AI Suggestions/);
  });

  it("A4 all actions come from approved canonical sources", () => {
    const model = adaptActionPlanCard(LIVE_ANALYSIS);
    expect(model.priority?.source).toBe("commercial_consulting.recommendations");
    expect(model.actions.every((item) => item.source.startsWith("narrative_result"))).toBe(true);
    expect(model.warnings[0]?.source).toBe("narrative_result.warning");
    expect(model.watch[0]?.source).toBe("luck.customer_summary");
  });

  it("A5 A6 A7 A8 do not perform frontend astrology reasoning", () => {
    const adapter = readFileSync(resolve(ROOT, "actionPlanAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "ActionPlanCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/useful_god\s*==|hy_than|ky_than|Hong Loan|màu đỏ|hướng Nam/);
    expect(card).not.toMatch(/useful_god|strength_level|gan_zhi/);
    expect(adapter).not.toContain("engines.");
  });

  it("A9 A10 omit source_unit_ids and engine/rule ids", () => {
    const { container } = renderLive();
    const text = apCard(container).textContent || "";
    expect(text).not.toMatch(/ck-leadership-001|source_unit_ids|catalog_id|pat_ca_01|str_003|cli_/);
    expect(text).not.toContain("{");
  });

  it("A11 actions are deduplicated with first approved occurrence winning", () => {
    const model = adaptActionPlanCard(LIVE_ANALYSIS);
    const titles = [model.priority, ...model.actions].map((item) => item?.title.toLowerCase() ?? "");
    expect(titles.filter((title) => title.includes("dựng khung")).length).toBe(1);
    expect(model.priority?.title).toMatch(/Dựng khung vừa đủ để việc chạy/);
  });

  it("A12 source order is preserved", () => {
    const model = adaptActionPlanCard(LIVE_ANALYSIS);
    expect(model.priority?.source).toBe("commercial_consulting.recommendations");
    expect(model.actions.map((item) => item.title)).toEqual([
      "Giữ một nền học/dưỡng, không bọc mọi việc",
      "Ra một việc nhỏ sau pha ủ để ấn không kín",
      "Mở một kênh thoát có phép và giữ nhịp",
    ]);
  });

  it("A13 warning content only from approved warning source", () => {
    const { container } = renderLive({
      useful_god: { useful_god: "Hỏa", ky_than: "Kim" },
      narrative_result: {
        sections: [{ intent: "warning", title: "Lưu ý", paragraphs: [{ text: "Không ôm thêm tải vì còn sức." }] }],
      },
    } as AnalysisDataDto);
    expect(apCard(container).querySelector('[data-ap-section="warnings"]')?.textContent).toMatch(/Không ôm thêm tải/);
    expect(adaptActionPlanCard({ useful_god: { useful_god: "Hỏa" } } as AnalysisDataDto).warnings).toEqual([]);
  });

  it("A14 current-period watch only from approved source", () => {
    const fromLuck = adaptActionPlanCard({
      luck: { customer_summary: "Theo dõi nhịp gánh trong giai đoạn hiện tại và giữ khung." },
    } as AnalysisDataDto);
    expect(fromLuck.watch[0]?.source).toBe("luck.customer_summary");
    const fromCycle = adaptActionPlanCard({
      luck: { current_cycle: { gan_zhi: "Ất Tỵ", stem_element: "Hỏa" } },
    } as AnalysisDataDto);
    expect(fromCycle.watch).toEqual([]);
  });

  it("A15 does not inject generic filler advice", () => {
    const model = adaptActionPlanCard({
      narrative_result: {
        recommendations: [
          { action: "Sống tích cực và cố gắng hơn." },
          { action: "Giữ tinh thần lạc quan mỗi ngày." },
          { action: "Khoanh đúng biên trách nhiệm trong nhóm." },
        ],
      },
    } as AnalysisDataDto);
    expect(model.priority?.title).toMatch(/Khoanh đúng biên trách nhiệm/);
    expect(JSON.stringify(model)).not.toMatch(/sống tích cực|cố gắng hơn|tinh thần lạc quan/);
  });

  it("A16 missing action data fails cleanly", () => {
    const { container } = renderLive({});
    expect(apCard(container).querySelector("[data-ap-empty]")?.textContent).toBe(
      "Chưa có đủ dữ liệu để tạo kế hoạch hành động.",
    );
  });

  it("A17 upstream Cards and grid spans remain", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    expect(container.querySelector('[data-card="interpretation"]')?.getAttribute("data-implemented")).toBe(
      "interpretation",
    );
    expect(container.querySelector('[data-card="luck"]')?.getAttribute("data-implemented")).toBe("luck");
  });

  it("A18 no Dashboard skeleton remains", () => {
    const { container } = renderLive();
    expect(container.querySelectorAll("[data-card][data-skeleton='true']")).toHaveLength(0);
  });

  it("A19 mobile CSS is one column without forcing overflow", () => {
    const css = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
    expect(css).toMatch(/\.bte-ap__list--tiles \{[\s\S]*grid-template-columns: 1fr;/);
    expect(css).toMatch(/\.bte-ap__item-title[\s\S]*overflow-wrap: anywhere/);
  });

  it("A20 ResultStore/routing unchanged", () => {
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
  });

  it("semantic safety: raw Useful God / Kỵ / Hong Loan / Luck / Strength do not create actions", () => {
    const rebound = adaptActionPlanCard({
      useful_god: { useful_god: "Hỏa", hy_than: "Hỏa", ky_than: "Kim" },
      strength: { strength_level: "Thân vượng" },
      pattern: { cach_cuc: "Chính Ấn" },
      shensha: { items: [{ name: "Hồng Loan", label: "Hong Loan" }] },
      luck: { current_cycle: { gan_zhi: "Ất Tỵ", stem_element: "Hỏa" }, luck_summary: "{}" },
    } as AnalysisDataDto);
    expect(rebound.available).toBe(false);
    const blob = JSON.stringify(rebound).toLowerCase();
    expect(blob).not.toMatch(/màu đỏ|bổ hỏa|hướng nam|màu trắng|hướng tây|kết hôn|mở rộng kinh doanh|phòng thủ tài chính|làm lãnh đạo/);
  });

  it("expand shows remaining approved actions", () => {
    const actions = Array.from({ length: 8 }, (_, index) => ({
      action: `Giữ một việc rõ số ${index + 1} trong nhóm chuyên môn.`,
    }));
    const { container } = render(
      <CommercialDashboardPage
        analysis={{ narrative_result: { recommendations: actions } } as AnalysisDataDto}
        resultSource="current"
        layoutMode="live"
      />,
    );
    const card = apCard(container);
    expect(card.querySelector(".bte-ap__toggle")?.textContent).toBe("Xem đầy đủ kế hoạch");
    expect(card.querySelectorAll('[data-ap-section="actions"] .bte-ap__item')).toHaveLength(6);
    fireEvent.click(card.querySelector(".bte-ap__toggle") as HTMLButtonElement);
    expect(card.getAttribute("data-expanded")).toBe("true");
    expect(card.querySelectorAll('[data-ap-section="actions"] .bte-ap__item')).toHaveLength(7);
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(container.querySelector('[data-layout="visual"]')).toBeTruthy();
    expect(apCard(container).textContent).toContain("Dựng khung vận hành vừa đủ để việc chạy");
    expect(ACTION_PLAN_VISUAL_FIXTURE.priority?.source).toBe("visual-fixture");
    expect(adaptActionPlanCard({}).available).toBe(false);
  });
});
