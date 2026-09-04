/**
 * P-003C Ten Gods consulting layout recomposition.
 * Presentation only. Copy, calculation, and combination knowledge stay frozen.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  adaptTenGodsCard,
  tenGodCombinationAsset,
  tenGodCommercialAsset,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const REPO = resolve(PORTAL, "../..");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
const CARD = readFileSync(resolve(ROOT, "TenGodsCard.tsx"), "utf8");
const ADAPTER = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
const COMMERCIAL = readFileSync(resolve(ROOT, "tenGodsCommercialAssets.ts"), "utf8");
const COMBINATION = readFileSync(resolve(ROOT, "tenGodsCombinationAssets.ts"), "utf8");
const HTML = readFileSync(resolve(PORTAL, "templates/result_desktop.html"), "utf8");
const KNOWLEDGE = resolve(REPO, "knowledge/consulting/ten_gods/combinations");

const CASE_0001 = {
  analysis_id: "ana-p003c-0001",
  identity: {
    person: { full_name: "Nguyễn Tiến Sơn", gender: "male", solar_birth: "1987-01-21" },
  },
  bazi: {
    day_master: "Canh",
    year_pillar: { stem: "Bính", ten_god: "Thất Sát" },
    month_pillar: { stem: "Tân", ten_god: "Kiếp Tài" },
    day_pillar: { stem: "Canh", ten_god: "Nhật Chủ" },
    hour_pillar: { stem: "Mậu", ten_god: "Thiên Ấn" },
  },
  ten_gods: {
    visible: [
      { pillar: "year", stem: "Bính", ten_god: "Thất Sát" },
      { pillar: "month", stem: "Tân", ten_god: "Kiếp Tài" },
      { pillar: "day", stem: "Canh", ten_god: "Nhật Chủ" },
      { pillar: "hour", stem: "Mậu", ten_god: "Thiên Ấn" },
    ],
    hidden: [
      { pillar: "year", hidden_stem: "Giáp", ten_god: "Thiên Tài" },
      { pillar: "month", hidden_stem: "Kỷ", ten_god: "Chính Ấn" },
    ],
    visible_labels: ["Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"],
  },
} as AnalysisDataDto;

afterEach(cleanup);

function renderLive(analysis: AnalysisDataDto = CASE_0001) {
  return render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
}

function tgCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="ten-gods"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

describe("P-003C Ten Gods consulting layout", () => {
  it("TG-L01 Ten Gods module full-width desktop", () => {
    const { container } = renderLive();
    const card = tgCard(container);
    expect(card.getAttribute("data-span")).toBe("4");
    expect(card.className).toMatch(/bte-cdash__card--span-4/);
    expect(card.getAttribute("data-tg-layout")).toBe("consulting-v1");
    expect(CSS).toMatch(/data-card="ten-gods"] \{ order: 22; \}/);
    expect(CSS).toMatch(/data-card="ten-gods"][\s\S]*grid-column:\s*1 \/ -1/);
  });

  it("TG-L02 Combination renders before single cards", () => {
    const { container } = renderLive();
    const sections = [...tgCard(container).querySelectorAll("[data-tg-section]")].map((node) =>
      node.getAttribute("data-tg-section"),
    );
    expect(sections.indexOf("combination")).toBeGreaterThanOrEqual(0);
    expect(sections.indexOf("combination")).toBeLessThan(sections.indexOf("commercial"));
    expect(tgCard(container).querySelector("[data-tg-hero='combination']")).toBeTruthy();
  });

  it("TG-L03 Three gods → three-column desktop grid", () => {
    const { container } = renderLive();
    const list = tgCard(container).querySelector(".bte-tg__consult-list");
    expect(list?.getAttribute("data-tg-count")).toBe("3");
    expect([...tgCard(container).querySelectorAll("[data-tg-commercial]")].map((node) =>
      node.getAttribute("data-tg-commercial"),
    )).toEqual(["Thất Sát", "Kiếp Tài", "Thiên Ấn"]);
    expect(CSS).toContain('.bte-tg__consult-list[data-tg-count="3"] { --tg-cols: 3; }');
  });

  it("TG-L04 Single cards compact by default", () => {
    const { container } = renderLive();
    const first = tgCard(container).querySelector('[data-tg-commercial="Thất Sát"]');
    expect(first?.getAttribute("data-tg-open")).toBe("false");
    expect(first?.querySelector('[data-tg-field="capability"]')).toBeTruthy();
    expect(first?.querySelector('[data-tg-field="income"]')).toBeTruthy();
    expect(first?.querySelector("[data-tg-detail]")?.hasAttribute("hidden")).toBe(true);
    expect(tgCard(container).querySelector("[data-tg-combo-detail]")?.hasAttribute("hidden")).toBe(true);
    expect(CSS).toContain(".bte-tg__consult-grid[hidden]");
  });

  it("TG-L05 Detail expansion preserves full copy", () => {
    const bound = adaptTenGodsCard(CASE_0001);
    const thatSat = tenGodCommercialAsset("Thất Sát");
    const combo = tenGodCombinationAsset(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
    const { container } = renderLive();
    const card = tgCard(container).querySelector('[data-tg-commercial="Thất Sát"]');
    fireEvent.click(card?.querySelector("button.bte-tg__more") as HTMLButtonElement);
    expect(card?.querySelector('[data-tg-field="career"]')?.textContent).toContain(thatSat?.career ?? "");
    expect(card?.querySelector('[data-tg-field="risk"]')?.textContent).toContain(thatSat?.risk ?? "");
    expect(card?.querySelector('[data-tg-field="recommendation"]')?.textContent).toContain(
      thatSat?.recommendation ?? "",
    );
    expect(card?.querySelector('[data-tg-field="insight"]')?.textContent).toBe(thatSat?.insight);
    expect(tgCard(container).querySelector("[data-tg-combination] [data-tg-field='insight']")?.textContent).toBe(
      bound.combination?.insight,
    );
    expect(combo?.title).toBe(bound.combination?.title);
  });

  it("TG-L06 Only selected detail expands", () => {
    const { container } = renderLive();
    const thatSat = tgCard(container).querySelector('[data-tg-commercial="Thất Sát"]');
    const kiep = tgCard(container).querySelector('[data-tg-commercial="Kiếp Tài"]');
    fireEvent.click(thatSat?.querySelector("button.bte-tg__more") as HTMLButtonElement);
    expect(thatSat?.getAttribute("data-tg-open")).toBe("true");
    expect(kiep?.getAttribute("data-tg-open")).toBe("false");
    expect(thatSat?.querySelector("[data-tg-detail]")?.hasAttribute("hidden")).toBe(false);
    expect(kiep?.querySelector("[data-tg-detail]")?.hasAttribute("hidden")).toBe(true);
    fireEvent.click(kiep?.querySelector("button.bte-tg__more") as HTMLButtonElement);
    expect(thatSat?.getAttribute("data-tg-open")).toBe("false");
    expect(kiep?.getAttribute("data-tg-open")).toBe("true");
  });

  it("TG-L07 Hidden support remains secondary", () => {
    const { container } = renderLive();
    const hidden = tgCard(container).querySelector('[data-tg-section="hidden-summary"]');
    expect(hidden?.textContent).toMatch(/Tàng Can hỗ trợ/);
    expect(hidden?.textContent).toMatch(/Thiên Tài/);
    expect(hidden?.textContent).toMatch(/Chính Ấn/);
    expect(tgCard(container).querySelector('[data-tg-commercial="Thiên Tài"]')).toBeNull();
    expect(CSS).toContain('[data-tg-section="hidden-summary"]');
  });

  it("TG-L08 No copy changes", () => {
    expect(CARD).not.toContain("Giá trị của bạn đến từ");
    expect(CARD).not.toContain("Gánh việc khó theo cách linh hoạt");
    const thatSat = tenGodCommercialAsset("Thất Sát");
    const { container } = renderLive();
    expect(tgCard(container).querySelector('[data-tg-commercial="Thất Sát"] [data-tg-field="insight"]')?.textContent).toBe(
      thatSat?.insight,
    );
    expect(tgCard(container).querySelector("[data-tg-combination] .bte-tg__combo-title")?.textContent).toBe(
      tenGodCombinationAsset(["Kiếp Tài", "Thất Sát", "Thiên Ấn"])?.title,
    );
  });

  it("TG-L09 No Ten Gods calculation changes", () => {
    expect(ADAPTER).not.toMatch(/engines\./);
    expect(CARD).not.toMatch(/engines\./);
    expect(ADAPTER).not.toMatch(/ten_god_name\(|map_stem_to_ten_god|LABEL_TO_GOD_ID/);
    expect(ADAPTER).not.toContain("CASE-0001");
  });

  it("TG-L10 No Combination Knowledge changes", () => {
    expect(COMBINATION).toContain("knowledge/consulting/ten_gods/combinations/");
    expect(CARD).not.toContain("tenGodsCombinationAssets");
    expect(CARD).not.toContain("matrix.json");
    const matrix = readFileSync(resolve(KNOWLEDGE, "matrix.json"), "utf8");
    expect(matrix).toContain("Kiếp Tài");
    expect(COMMERCIAL).toContain("Thất Sát");
  });

  it("TG-L11 Tablet layout valid", () => {
    expect(CSS).toContain("@media (max-width: 1199px) and (min-width: 768px)");
    expect(CSS).toContain('.bte-tg__consult-list[data-tg-count="3"]');
    expect(CSS).toContain("--tg-cols: 2");
    const two = {
      ten_gods: {
        visible: [
          { pillar: "year", ten_god: "Thất Sát" },
          { pillar: "day", ten_god: "Nhật Chủ" },
          { pillar: "hour", ten_god: "Thiên Ấn" },
        ],
      },
    } as AnalysisDataDto;
    const { container } = renderLive(two);
    expect(tgCard(container).querySelector(".bte-tg__consult-list")?.getAttribute("data-tg-count")).toBe("2");
  });

  it("TG-L12 Mobile stack valid", () => {
    expect(CSS).toContain("@media (max-width: 767px)");
    expect(CSS).toMatch(
      /@media \(max-width: 767px\)[\s\S]*\.bte-tg__consult-list\[data-tg-count="3"\][\s\S]*--tg-cols:\s*1/,
    );
    const { container } = renderLive();
    expect(tgCard(container).getAttribute("data-mobile-order")).toBe("8");
    expect(tgCard(container).querySelector(".bte-tg__more")?.textContent).toBe("Xem mô hình chi tiết");
  });

  it("TG-L13 No horizontal overflow", () => {
    expect(CSS).toContain(".bte-tg__consult-list");
    expect(CSS).toContain("minmax(0, 1fr)");
    expect(CSS).toContain("min-width: 0");
    expect(CSS).toContain("overflow-x: clip");
    expect(CSS).not.toMatch(/\.bte-tg[^{]*\{[^}]*overflow-x:\s*scroll/);
  });

  it("TG-L14 Live /result verified", () => {
    expect(HTML).toContain("/static/dist/result.js?v=PRUNTIME01-P003C2");
    expect(HTML).toContain("/static/dist/result.css?v=PRUNTIME01-P003C2");
    const entry = readFileSync(resolve(PORTAL, "src/entries/resultApp.tsx"), "utf8");
    expect(entry).toContain("CommercialDashboardPage");
    const capture = readFileSync(resolve(PORTAL, "scripts/capture_p003c_live.py"), "utf8");
    expect(capture).toContain("/result");
    expect(capture).toContain('[data-card="ten-gods"]');
  });
});
