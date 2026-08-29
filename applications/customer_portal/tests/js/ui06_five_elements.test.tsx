/**
 * UI-06 Card 03 Five Elements — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  FIVE_ELEMENTS_TITLE,
  FIVE_ELEMENTS_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptFiveElementsCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
const BANNED_INFERENCE =
  /Thủy yếu|Thổ mạnh|Thiếu Thủy|Bổ Thủy|Dụng Thần Thủy|Hành mạnh|Hành yếu|Nên bổ|Nên giảm/;

const LIVE_ANALYSIS = {
  five_elements: {
    counts: { wood: 4, fire: 5, earth: 6, metal: 3, water: 1 },
    wood: { count: 4, status: "EXCESS" },
    fire: { count: 5, status: "EXCESS" },
    earth: { count: 6, status: "EXCESS" },
    metal: { count: 3, status: "EXCESS" },
    water: { count: 1, status: "PRESENT" },
    status: "EXCESS",
    dominant: "earth",
    disclaimer:
      "Phân bố Ngũ hành phản ánh số lần xuất hiện trong cấu trúc, không phải mức vượng suy và không trực tiếp quyết định Dụng thần.",
    method_note: "Tính theo Thiên can · bản hành Địa chi · Tàng can",
    unit_total: 19,
  },
  score: { wuxing_score: 0, grade: "D+" },
  strength: { strength_level: "strong", strength_score: 0.87 },
  useful_god: { useful_display: "Hỏa · Đinh · Chính Quan" },
} as AnalysisDataDto;

function renderLive() {
  return render(
    <CommercialDashboardPage analysis={LIVE_ANALYSIS} resultSource="current" layoutMode="live" />,
  );
}

function feCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="five-elements"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-06 Five Elements card", () => {
  it("F1 replaces the Five Elements skeleton with the real component", () => {
    const { container } = renderLive();
    const card = feCard(container);
    expect(card.getAttribute("data-implemented")).toBe("five-elements");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("F2 keeps Five Elements span at 4/12", () => {
    const { container } = renderLive();
    const card = feCard(container);
    expect(card.getAttribute("data-span")).toBe("4");
    expect(card.className).toMatch(/bte-cdash__card--span-4/);
  });

  it("F3 uses the customer title NGŨ HÀNH", () => {
    const { container } = renderLive();
    expect(feCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(
      FIVE_ELEMENTS_TITLE,
    );
    expect(feCard(container).textContent).not.toMatch(/Five Elements|Wuxing Score|Element Score/);
  });

  it("F4 renders exactly five canonical element labels", () => {
    const { container } = renderLive();
    const labels = [...feCard(container).querySelectorAll("[data-fe-row]")].map((node) =>
      node.getAttribute("data-fe-row"),
    );
    expect(labels).toHaveLength(5);
    expect(labels).toEqual(["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]);
  });

  it("F5 keeps stable Mộc/Hỏa/Thổ/Kim/Thủy order", () => {
    const bound = adaptFiveElementsCard(LIVE_ANALYSIS);
    expect(bound.rows.map((row) => row.label)).toEqual(["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]);
  });

  it("F6 binds canonical live values", () => {
    const { container } = renderLive();
    expect(feCard(container).querySelector('[data-fe-count="wood"]')?.textContent).toBe("4");
    expect(feCard(container).querySelector('[data-fe-count="fire"]')?.textContent).toBe("5");
    expect(feCard(container).querySelector('[data-fe-count="earth"]')?.textContent).toBe("6");
    expect(feCard(container).querySelector('[data-fe-count="metal"]')?.textContent).toBe("3");
    expect(feCard(container).querySelector('[data-fe-count="water"]')?.textContent).toBe("1");
    expect(adaptFiveElementsCard(LIVE_ANALYSIS).rows.map((row) => row.count)).toEqual([4, 5, 6, 3, 1]);
  });

  it("F7 does not display Useful God as a card fact", () => {
    const { container } = renderLive();
    const card = feCard(container);
    expect(card.querySelector('[data-evidence="useful-god"]')).toBeNull();
    expect(card.textContent).not.toMatch(/Hỏa · Đinh · Chính Quan/);
    expect(card.textContent).not.toMatch(/Dụng Thần Thủy|Nên bổ Hỏa/);
  });

  it("F8 does not display Hỷ / Kỵ", () => {
    const { container } = renderLive();
    expect(feCard(container).textContent).not.toMatch(/Hỷ Thần|Kỵ Thần|Hỷ thần|Kỵ thần/);
  });

  it("F9 does not display Day Master strength", () => {
    const { container } = renderLive();
    expect(feCard(container).textContent).not.toMatch(/Thân vượng|Thân nhược|0\.87/);
  });

  it("F10 does not infer customer balance from technical status", () => {
    const bound = adaptFiveElementsCard(LIVE_ANALYSIS);
    expect(bound.balanceStatus).toBe("");
    const { container } = renderLive();
    expect(feCard(container).querySelector("[data-fe-status]")).toBeNull();
    expect(feCard(container).textContent).not.toMatch(/CÂN BẰNG|EXCESS|STRONG|MISSING/);
    expect(feCard(container).querySelector("[data-fe-heading]")?.textContent).toBe("PHÂN BỐ NGŨ HÀNH");
  });

  it("F11 does not label raw counts as strong/weak", () => {
    const { container } = renderLive();
    expect(feCard(container).textContent).not.toMatch(/Thổ mạnh|Thủy yếu|Hành mạnh|Hành yếu|Thiếu Thủy/);
  });

  it("F12 chart and textual values agree", () => {
    const { container } = renderLive();
    const card = feCard(container);
    expect(card.querySelector('[data-fe-chart="bars"]')).toBeTruthy();
    expect(card.querySelectorAll(".bte-fe__fill")).toHaveLength(5);
    expect([...card.querySelectorAll("[data-fe-count]")].map((node) => node.textContent)).toEqual([
      "4",
      "5",
      "6",
      "3",
      "1",
    ]);
  });

  it("F13 missing data fails cleanly", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={{}} resultSource="current" layoutMode="live" />,
    );
    const card = feCard(container);
    expect(card.querySelector("[data-fe-empty]")?.textContent).toBe("Chưa đủ dữ liệu Ngũ Hành.");
    expect(card.querySelector("[data-fe-chart]")).toBeNull();
    expect(card.textContent).not.toMatch(/undefined|null|NaN/);
    expect(adaptFiveElementsCard({}).available).toBe(false);
  });

  it("F14 does not call engines from Five Elements", () => {
    const adapter = readFileSync(resolve(ROOT, "fiveElementsAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "FiveElementsCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/engines\./);
    expect(card).not.toMatch(/engines\./);
    expect(adapter).not.toContain("wuxing_score");
    expect(adapter).not.toContain("CASE-0001");
  });

  it("F15 leaves Overview implemented and unchanged in role", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-implemented")).toBe("overview");
    expect(overview?.getAttribute("data-span")).toBe("4");
  });

  it("F16 leaves BaZi implemented and unchanged in role", () => {
    const { container } = renderLive();
    const bazi = container.querySelector('[data-card="bazi"]');
    expect(bazi?.getAttribute("data-implemented")).toBe("bazi");
    expect(bazi?.getAttribute("data-span")).toBe("8");
  });

  it("F17 leaves other Card skeletons unchanged", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual(["action-plan"]);
  });

  it("F18 keeps the canonical grid spans frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("F19 mobile structure stays a vertical stacked card", () => {
    const { container } = renderLive();
    const card = feCard(container);
    expect(card.querySelector(".bte-fe__chart")).toBeTruthy();
    expect(getComputedStyle(card).overflowX === "visible" || card.className.includes("bte-fe")).toBe(
      true,
    );
    expect(card.textContent).toMatch(/Mộc/);
    expect(card.querySelector(".bte-fe__row")).toBeTruthy();
  });

  it("F20 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Hỏa · Đinh · Chính Quan" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.five_elements?.counts?.wood).toBe(4);
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("semantic safety: raw counts cannot become strength or Useful God copy", () => {
    const bound = adaptFiveElementsCard(LIVE_ANALYSIS);
    expect(bound.comment).toMatch(/xuất hiện nhiều nhất/);
    expect(bound.comment).toMatch(/xuất hiện ít nhất/);
    expect(bound.comment).not.toMatch(BANNED_INFERENCE);
    expect(bound.mostPresent).toBe("Thổ");
    expect(bound.leastPresent).toBe("Thủy");
    const { container } = renderLive();
    const text = feCard(container).textContent || "";
    expect(text).not.toMatch(BANNED_INFERENCE);
    const adapter = readFileSync(resolve(ROOT, "fiveElementsAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "FiveElementsCard.tsx"), "utf8");
    expect(adapter + card).not.toMatch(/Thủy yếu|Thiếu Thủy|Bổ Thủy|Dụng Thần Thủy/);
    expect(adapter).not.toMatch(/EXCESS.*mạnh|status.*Yếu/);
  });

  it("does not treat a missing element as zero unless published", () => {
    const bound = adaptFiveElementsCard({
      five_elements: { counts: { wood: 2, fire: 1 } },
    });
    expect(bound.rows.find((row) => row.key === "earth")?.count).toBeNull();
    expect(bound.rows.find((row) => row.key === "wood")?.count).toBe(2);
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(container.querySelector('[data-layout="visual"]')).toBeTruthy();
    expect(screen.getByText(FIVE_ELEMENTS_VISUAL_FIXTURE.balanceStatus)).toBeTruthy();
    expect(adaptFiveElementsCard(LIVE_ANALYSIS).rows.map((row) => row.count)).not.toEqual(
      FIVE_ELEMENTS_VISUAL_FIXTURE.rows.map((row) => row.count),
    );
    const fixture = readFileSync(resolve(ROOT, "fiveElementsFixture.ts"), "utf8");
    expect(fixture).not.toContain("wood: 4");
  });
});
