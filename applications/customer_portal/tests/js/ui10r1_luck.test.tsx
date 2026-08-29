/**
 * UI-10R1 — compact Luck Card header. Presentation only.
 */

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { CommercialDashboardPage } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const LIVE = {
  luck: {
    direction_label: "Thuận",
    start_age: 5,
    luck_summary: '{"dayun_runtime":{"kind":"dayun"}}',
    current_cycle: {
      index: 2,
      gan_zhi: "Ất Tỵ",
      year_start: 2022,
      year_end: 2031,
      age_start: 35,
      age_end: 44,
    },
    cycles: [
      { index: 0, gan_zhi: "Quý Mão", year_start: 2002, year_end: 2011, age_start: 15, age_end: 24 },
      { index: 1, gan_zhi: "Giáp Thìn", year_start: 2012, year_end: 2021, age_start: 25, age_end: 34 },
      { index: 2, gan_zhi: "Ất Tỵ", year_start: 2022, year_end: 2031, age_start: 35, age_end: 44 },
      { index: 3, gan_zhi: "Bính Ngọ", year_start: 2032, year_end: 2041, age_start: 45, age_end: 54 },
      { index: 4, gan_zhi: "Đinh Mùi", year_start: 2042, year_end: 2051, age_start: 55, age_end: 64 },
      { index: 5, gan_zhi: "Mậu Thân", year_start: 2052, year_end: 2061, age_start: 65, age_end: 74 },
    ],
  },
} as AnalysisDataDto;

function renderLive() {
  return render(
    <CommercialDashboardPage analysis={LIVE} resultSource="current" layoutMode="live" />,
  );
}

function luckCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="luck"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-10R1 Luck compact header", () => {
  it("LP1 current cycle still renders Ất Tỵ", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-current-name]")?.textContent).toBe("Ất Tỵ");
  });

  it("LP2 current cycle still renders 2022–2031", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-current-years]")?.textContent).toBe("2022–2031");
  });

  it("LP3 current cycle still renders 35–44 tuổi", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-current-ages]")?.textContent).toBe("35–44 tuổi");
  });

  it("LP4 desktop presentation groups current cycle into one compact value row", () => {
    const { container } = renderLive();
    const row = luckCard(container).querySelector("[data-luck-current-row]");
    expect(row).toBeTruthy();
    expect(row?.tagName).toBe("P");
    expect(row?.textContent?.replace(/\s+/g, " ").trim()).toBe("Ất Tỵ (2022–2031) · 35–44 tuổi");
    expect(luckCard(container).querySelectorAll("[data-luck-section='current'] p")).toHaveLength(1);
    expect(row?.className).toContain("bte-luck__value-row");
  });

  it("LP5 Khởi vận renders Thuận · 5 tuổi", () => {
    const { container } = renderLive();
    const row = luckCard(container).querySelector("[data-luck-start-row]");
    expect(row?.textContent?.replace(/\s+/g, " ").trim()).toBe("Thuận · 5 tuổi");
    expect(luckCard(container).querySelector("[data-luck-direction]")?.textContent).toBe("Thuận");
    expect(luckCard(container).querySelector("[data-luck-start-age]")?.textContent).toBe("5 tuổi");
    expect(luckCard(container).querySelectorAll("[data-luck-section='start'] p")).toHaveLength(1);
  });

  it("LP6 timeline values unchanged", () => {
    const { container } = renderLive();
    const names = [...luckCard(container).querySelectorAll("[data-luck-cycle]")].map(
      (node) => node.getAttribute("data-luck-cycle"),
    );
    expect(names).toEqual(["Quý Mão", "Giáp Thìn", "Ất Tỵ", "Bính Ngọ", "Đinh Mùi"]);
  });

  it("LP7 current marker unchanged", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-now]")?.textContent).toBe("Hiện tại");
    expect(
      luckCard(container).querySelector('[data-luck-cycle="Ất Tỵ"]')?.getAttribute("data-luck-current"),
    ).toBe("true");
  });

  it("LP8 next cycle unchanged", () => {
    const { container } = renderLive();
    expect(luckCard(container).querySelector("[data-luck-next]")?.textContent).toBe("Bính Ngọ · 2032–2041");
  });

  it("LP9 no raw runtime/debug content", () => {
    const { container } = renderLive();
    const text = luckCard(container).textContent || "";
    expect(text).not.toContain("dayun_runtime");
    expect(text).not.toContain("{");
    expect(text).not.toContain("}");
    expect(text).not.toMatch(/tốt|xấu|thuận lợi|bất lợi|cơ hội|phòng thủ/);
  });

  it("LP10 grid remains 6/12", () => {
    const { container } = renderLive();
    expect(luckCard(container).getAttribute("data-span")).toBe("6");
    expect(luckCard(container).className).toMatch(/bte-cdash__card--span-6/);
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });
});
