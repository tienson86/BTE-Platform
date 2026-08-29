/**
 * UI-10R — Luck Card must not leak runtime/debug JSON to customers.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { CommercialDashboardPage, adaptLuckCard } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const RUNTIME_DUMP =
  '{"dayun_runtime":{"earth_layer":{"earthly_branch":"Tỵ","hidden_stems":["Bính","Mậu","Canh"]},"runtime_metadata":{"kind":"dayun"}},"evaluation":{"attack_elements":[],"support_elements":[],"luck_strength":88,"luck_stage":"UNKNOWN"}}';

const LIVE_LEAK = {
  luck: {
    direction_label: "Thuận",
    start_age: 5,
    luck_summary: RUNTIME_DUMP,
    summary: RUNTIME_DUMP,
    luck_strength: 88,
    current_cycle: {
      index: 2,
      gan_zhi: "Ất Tỵ",
      year_start: 2022,
      year_end: 2031,
      age_start: 35,
      age_end: 44,
      stem_element: "Mộc",
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

function renderLeak() {
  return render(
    <CommercialDashboardPage analysis={LIVE_LEAK} resultSource="current" layoutMode="live" />,
  );
}

function luckCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="luck"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-10R Luck customer presentation cleanup", () => {
  it("LR1 raw dayun_runtime never renders", () => {
    const { container } = renderLeak();
    expect(luckCard(container).textContent).not.toContain("dayun_runtime");
    expect(adaptLuckCard(LIVE_LEAK).trend).toBe("");
  });

  it("LR2 no JSON dump braces appear in the Luck Card", () => {
    const { container } = renderLeak();
    expect(luckCard(container).textContent).not.toContain("{");
    expect(luckCard(container).textContent).not.toContain("}");
  });

  it("LR3 no runtime_metadata renders", () => {
    const { container } = renderLeak();
    expect(luckCard(container).textContent).not.toContain("runtime_metadata");
  });

  it("LR4 no evaluation object renders", () => {
    const { container } = renderLeak();
    expect(luckCard(container).textContent).not.toContain("evaluation");
    expect(adaptLuckCard(LIVE_LEAK).trend).toBe("");
  });

  it("LR5 no attack_elements / support_elements / luck_strength debug fields render", () => {
    const { container } = renderLeak();
    const text = luckCard(container).textContent || "";
    expect(text).not.toContain("attack_elements");
    expect(text).not.toContain("support_elements");
    expect(text).not.toContain("luck_strength");
  });

  it("LR6 current cycle still renders", () => {
    const { container } = renderLeak();
    expect(luckCard(container).querySelector("[data-luck-current-name]")?.textContent).toBe("Ất Tỵ");
    expect(luckCard(container).querySelector("[data-luck-current-years]")?.textContent).toBe("2022–2031");
    expect(luckCard(container).querySelector("[data-luck-current-ages]")?.textContent).toBe("35–44 tuổi");
  });

  it("LR7 timeline still renders", () => {
    const { container } = renderLeak();
    expect(luckCard(container).querySelector("[data-luck-section='timeline']")).toBeTruthy();
    expect(luckCard(container).querySelector('[data-luck-cycle="Ất Tỵ"]')).toBeTruthy();
  });

  it("LR8 next cycle still renders", () => {
    const { container } = renderLeak();
    expect(luckCard(container).querySelector("[data-luck-next]")?.textContent).toBe("Bính Ngọ · 2032–2041");
  });

  it("LR9 direction still renders if canonical", () => {
    const { container } = renderLeak();
    expect(luckCard(container).querySelector("[data-luck-direction]")?.textContent).toBe("Thuận");
  });

  it("LR10 starting age still renders if canonical", () => {
    const { container } = renderLeak();
    expect(luckCard(container).querySelector("[data-luck-start-age]")?.textContent).toBe("5 tuổi");
  });

  it("LR11 no good/bad inference introduced", () => {
    const { container } = renderLeak();
    const text = luckCard(container).textContent || "";
    expect(text).not.toMatch(/tốt|xấu|thuận lợi|bất lợi|cơ hội|phòng thủ|đại cát|Hung|Cát/);
    const rebound = adaptLuckCard({
      luck: {
        luck_summary: RUNTIME_DUMP,
        current_cycle: { gan_zhi: "Ất Tỵ" },
      },
    } as AnalysisDataDto);
    expect(JSON.stringify(rebound)).not.toMatch(/tốt|xấu|thuận lợi|bất lợi/);
  });

  it("LR12 does not call or import the luck engine", () => {
    const adapter = readFileSync(resolve(ROOT, "luckAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "LuckCard.tsx"), "utf8");
    for (const source of [adapter, card]) {
      expect(source).not.toMatch(/engines\/|LuckEngine|luck_engine/);
      expect(source).not.toContain("JSON.stringify");
      expect(source).not.toContain("Object.entries");
    }
  });

  it("does not pass luck_summary or object dumps as customer_summary", () => {
    expect(
      adaptLuckCard({
        luck: {
          luck_summary: RUNTIME_DUMP,
          summary: { dayun_runtime: { kind: "dayun" } },
          customer_summary: { evaluation: {} },
          current_cycle: { gan_zhi: "Ất Tỵ" },
        },
      } as AnalysisDataDto).trend,
    ).toBe("");
    expect(
      adaptLuckCard({
        luck: {
          customer_summary: "Đây là giai đoạn có xu hướng phát triển.",
          current_cycle: { gan_zhi: "Ất Tỵ" },
        },
      } as AnalysisDataDto).trend,
    ).toBe("Đây là giai đoạn có xu hướng phát triển.");
  });

  it("expanded view still omits runtime diagnostics", () => {
    const { container } = renderLeak();
    const toggle = luckCard(container).querySelector("button.bte-luck__toggle");
    expect(toggle).toBeTruthy();
    fireEvent.click(toggle as HTMLButtonElement);
    const text = luckCard(container).textContent || "";
    expect(text).not.toContain("dayun_runtime");
    expect(text).not.toContain("{");
    expect(luckCard(container).querySelector('[data-luck-cycle="Mậu Thân"]')).toBeTruthy();
  });
});
