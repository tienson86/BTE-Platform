/**
 * UI-10 Card 07 Luck — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  LUCK_TITLE,
  LUCK_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptLuckCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  luck: {
    direction_label: "Thuận",
    start_age: 5,
    current_cycle: { index: 3, gan_zhi: "Quý Mão", year_start: 2021, year_end: 2030, age_start: 34, age_end: 43 },
    cycles: [
      { index: 0, gan_zhi: "Canh Tý", year_start: 1991, year_end: 2000, age_start: 4, age_end: 13 },
      { index: 1, gan_zhi: "Tân Sửu", year_start: 2001, year_end: 2010, age_start: 14, age_end: 23 },
      { index: 2, gan_zhi: "Nhâm Dần", year_start: 2011, year_end: 2020, age_start: 24, age_end: 33 },
      { index: 3, gan_zhi: "Quý Mão", year_start: 2021, year_end: 2030, age_start: 34, age_end: 43 },
      { index: 4, gan_zhi: "Giáp Thìn", year_start: 2031, year_end: 2040, age_start: 44, age_end: 53 },
      { index: 5, gan_zhi: "Ất Tỵ", year_start: 2041, year_end: 2050, age_start: 54, age_end: 63 },
      { index: 6, gan_zhi: "Bính Ngọ", year_start: 2051, year_end: 2060, age_start: 64, age_end: 73 },
      { index: 7, gan_zhi: "Đinh Mùi", year_start: 2061, year_end: 2070, age_start: 74, age_end: 83 },
    ],
  },
} as AnalysisDataDto;

function renderLive(analysis: AnalysisDataDto = LIVE_ANALYSIS) {
  return render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
}

function luckCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="luck"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

function toggle(container: HTMLElement): HTMLButtonElement {
  const button = luckCard(container).querySelector("button.bte-luck__toggle");
  expect(button).toBeTruthy();
  return button as HTMLButtonElement;
}

afterEach(cleanup);

describe("UI-10 Luck card", () => {
  it("L1 replaces the Luck skeleton with the real component", () => {
    const { container } = renderLive();
    const card = luckCard(container);
    expect(card.getAttribute("data-implemented")).toBe("luck");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("L2 keeps Luck span at 6/12", () => {
    const { container } = renderLive();
    expect(luckCard(container).getAttribute("data-span")).toBe("6");
    expect(luckCard(container).className).toMatch(/bte-cdash__card--span-6/);
  });

  it("L3 shows the customer title ĐẠI VẬN", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(LUCK_TITLE);
    expect(luckCard(container).textContent).not.toMatch(/Luck Engine|Major Luck|Luck Cycles/);
  });

  it("L4 renders the canonical cycle list", () => {
    const { container } = renderLive();
    fireEvent.click(toggle(container));
    expect(luckCard(container).querySelectorAll("[data-luck-cycle]")).toHaveLength(8);
    expect(adaptLuckCard(LIVE_ANALYSIS).cycles.map((cycle) => cycle.ganZhi)).toContain("Quý Mão");
  });

  it("L5 identifies current cycle from the canonical contract", () => {
    expect(adaptLuckCard(LIVE_ANALYSIS).current?.ganZhi).toBe("Quý Mão");
    expect(luckCard(renderLive().container).querySelector("[data-luck-current-name]")?.textContent).toBe("Quý Mão");
  });

  it("L6 marks current cycle with explicit Hiện tại text", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-now]")?.textContent).toBe("Hiện tại");
  });

  it("L7 binds canonical year ranges", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-current-years]")?.textContent).toBe("2021–2030");
  });

  it("L8 shows age range only from canonical cycle ages", () => {
    expect(adaptLuckCard(LIVE_ANALYSIS).current?.ageRange).toBe("34–43 tuổi");
    expect(
      adaptLuckCard({
        luck: { current_cycle: { gan_zhi: "Quý Mão", year_start: 2021, year_end: 2030 } },
      }).current?.ageRange,
    ).toBe("");
  });

  it("L9 shows direction only from a canonical customer label", () => {
    expect(adaptLuckCard(LIVE_ANALYSIS).direction).toBe("Thuận");
    expect(adaptLuckCard({ luck: { direction: "forward", current_cycle: { gan_zhi: "Quý Mão" } } }).direction).toBe("");
  });

  it("L10 shows starting age only from the canonical field", () => {
    expect(adaptLuckCard(LIVE_ANALYSIS).startAge).toBe("5 tuổi");
    expect(adaptLuckCard({ luck: { current_cycle: { gan_zhi: "Quý Mão" } } }).startAge).toBe("");
  });

  it("L11 derives next cycle only from canonical ordered list index", () => {
    expect(adaptLuckCard(LIVE_ANALYSIS).next?.ganZhi).toBe("Giáp Thìn");
    expect(
      adaptLuckCard({
        luck: {
          current_cycle: { index: 0, gan_zhi: "Canh Tý" },
          cycles: [
            { index: 0, gan_zhi: "Canh Tý" },
            { index: 1, gan_zhi: "Tân Sửu" },
          ],
        },
      }).next?.ganZhi,
    ).toBe("Tân Sửu");
  });

  it("L12 does not calculate Luck astrology in the frontend", () => {
    const adapter = readFileSync(resolve(ROOT, "luckAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/Date\.now|birth_year|stem_yin|gender/);
    expect(adapter).not.toMatch(/LuckEngine|luck_engine|engines\//);
  });

  it("L13 does not infer good/bad luck", () => {
    const { container } = renderLive();
    expect(luckCard(container).textContent).not.toMatch(/xấu|bất lợi|Hung|Cát|đại phát/);
  });

  it("L14 does not infer Luck from Useful God", () => {
    const rebound = adaptLuckCard({
      useful_god: { useful_display: "Hỏa" },
      luck: { current_cycle: { gan_zhi: "Bính Ngọ", stem_element: "Hỏa" } },
    });
    expect(JSON.stringify(rebound)).not.toMatch(/đại cát|vận tốt/);
  });

  it("L15 does not show yearly event predictions", () => {
    const { container } = renderLive();
    expect(luckCard(container).textContent).not.toMatch(/năm cưới|năm phát tài|năm tai họa|năm bệnh/);
  });

  it("L16 does not show Lưu Niên content", () => {
    const { container } = renderLive();
    expect(luckCard(container).textContent).not.toMatch(/Lưu Niên|lưu nguyệt/);
    expect(
      adaptLuckCard({
        luck: { current_cycle: { gan_zhi: "Quý Mão" }, luck_summary: "Lưu Niên Bính Ngọ tiếp nhịp" },
      } as AnalysisDataDto).trend,
    ).toBe("");
  });

  it("L17 does not show fake star or traffic-light ratings", () => {
    const { container } = renderLive();
    expect(luckCard(container).textContent).not.toMatch(/★/);
    expect(adaptLuckCard({ luck: { luck_strength: 90, current_cycle: { gan_zhi: "Quý Mão" } } } as AnalysisDataDto).trend).toBe(
      "",
    );
  });

  it("L18 missing data fails cleanly", () => {
    const { container } = renderLive({});
    expect(luckCard(container).querySelector("[data-luck-empty]")?.textContent).toBe("Chưa đủ dữ liệu Đại Vận.");
    expect(luckCard(container).querySelector("[data-luck-section]")).toBeNull();
  });

  it("L19 does not call astrology engines", () => {
    const card = readFileSync(resolve(ROOT, "LuckCard.tsx"), "utf8");
    expect(card).not.toMatch(/engines\/|LuckEngine|luck_engine/);
  });

  it("L20 keeps the canonical grid spans frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("L21 leaves Identity through ShenSha in role", () => {
    const { container } = renderLive();
    expect(container.querySelector("[data-identity-header='true']")).toBeTruthy();
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-implemented")).toBe("overview");
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-implemented")).toBe("bazi");
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-implemented")).toBe(
      "five-elements",
    );
    expect(container.querySelector('[data-card="ten-gods"]')?.getAttribute("data-implemented")).toBe("ten-gods");
    expect(container.querySelector('[data-card="pattern"]')?.getAttribute("data-implemented")).toBe("pattern");
    expect(container.querySelector('[data-card="shensha"]')?.getAttribute("data-implemented")).toBe("shensha");
  });

  it("L22 leaves Interpretation and Action Plan as skeletons", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual(["interpretation", "action-plan"]);
  });

  it("L23 expand/collapse is an accessible button", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector('[data-luck-cycle="Canh Tý"]')).toBeNull();
    const button = toggle(container);
    expect(button.getAttribute("aria-expanded")).toBe("false");
    expect(button.textContent).toBe("Xem toàn bộ Đại Vận");
    fireEvent.click(button);
    expect(toggle(container).getAttribute("aria-expanded")).toBe("true");
    expect(luckCard(container).querySelector('[data-luck-cycle="Canh Tý"]')).toBeTruthy();
  });

  it("L24 mobile structure stays a vertical stacked card", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-section='current']")).toBeTruthy();
    expect(luckCard(container).querySelector("[data-luck-section='timeline']")).toBeTruthy();
  });

  it("L25 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Hỏa" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.luck?.current_cycle?.gan_zhi).toBe("Quý Mão");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("semantic safety: element, Useful God, and score do not become luck verdicts", () => {
    const rebound = adaptLuckCard({
      useful_god: { useful_display: "Hỏa" },
      luck: {
        luck_strength: 88,
        current_cycle: { gan_zhi: "Bính Ngọ", stem_element: "Hỏa", branch_element: "Hỏa" },
        cycles: [
          { gan_zhi: "Bính Ngọ", stem_element: "Hỏa" },
          { gan_zhi: "Tân Dậu", stem_element: "Kim" },
        ],
      },
    } as AnalysisDataDto);
    const blob = JSON.stringify(rebound);
    expect(rebound.current?.ganZhi).toBe("Bính Ngọ");
    expect(blob).not.toMatch(/thuận lợi|phát triển|tốt/);
    expect(blob).not.toMatch(/xấu|bất lợi/);
    expect(blob).not.toMatch(/đại cát|vận tốt|vận xấu/);
    expect(blob).not.toMatch(/★/);
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(luckCard(container).querySelector("[data-luck-current-name]")?.textContent).toBe("Ất Tỵ");
    expect(LUCK_VISUAL_FIXTURE.current?.yearRange).toBe("2022–2031");
    expect(adaptLuckCard(LIVE_ANALYSIS).current?.ganZhi).toBe("Quý Mão");
    const fixture = readFileSync(resolve(ROOT, "luckFixture.ts"), "utf8");
    expect(fixture).not.toContain("Bính");
    expect(fixture).not.toContain("CASE-0001");
    expect(fixture).not.toContain("Quý Mão");
  });
});
