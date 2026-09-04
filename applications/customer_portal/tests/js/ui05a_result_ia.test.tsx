/**
 * UI-05A Result information architecture. Presentation / layout only.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
} from "../../src/screens/commercial_dashboard";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
const PAGE = readFileSync(resolve(ROOT, "CommercialDashboardPage.tsx"), "utf8");
const GRID = readFileSync(resolve(ROOT, "DashboardGrid.tsx"), "utf8");
const CARDS = readFileSync(resolve(ROOT, "cards.ts"), "utf8");
const HTML = readFileSync(resolve(PORTAL, "templates/result_desktop.html"), "utf8");

const ADAPTERS = [
  "overviewAdapter.ts",
  "baziAdapter.ts",
  "fiveElementsAdapter.ts",
  "tenGodsAdapter.ts",
  "patternAdapter.ts",
  "shenShaAdapter.ts",
  "luckAdapter.ts",
  "interpretationAdapter.ts",
  "actionPlanAdapter.ts",
  "lifeConsultingAdapter.ts",
  "adapter.ts",
  "canXuongAdapter.ts",
] as const;

const DOM_ORDER = [
  "overview",
  "bazi",
  "five-elements",
  "ten-gods",
  "pattern",
  "shensha",
  "luck",
  "interpretation",
  "action-plan",
] as const;

afterEach(cleanup);

function renderVisual() {
  return render(<CommercialDashboardPage layoutMode="visual" resultSource="preview" />);
}

describe("UI-05A result information architecture", () => {
  it("keeps frozen catalog geometry and semantic DOM order", () => {
    expect(DASHBOARD_CARDS.map((card) => card.id)).toEqual([...DOM_ORDER]);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    const { container } = renderVisual();
    const order = [...container.querySelectorAll("[data-card]")].map((node) => node.getAttribute("data-card"));
    expect(order).toEqual([...DOM_ORDER]);
  });

  it("marks the UI-05A architecture without new substitute cards", () => {
    const { container } = renderVisual();
    expect(container.querySelector("[data-ia='ui05a']")).toBeTruthy();
    expect(container.querySelectorAll("[data-card]")).toHaveLength(9);
    expect(container.querySelector("[data-identity-header='true']")).toBeTruthy();
    expect(container.querySelector("[data-life-consulting]")).toBeTruthy();
    expect(GRID).toContain("DASHBOARD_CARDS.map");
    expect(GRID).not.toMatch(/duplicate|cloneCard/);
  });

  it("places identity then Tứ Trụ / Cân Xương / Cung Phi", () => {
    expect(CSS).toContain('"identity identity identity"');
    expect(CSS).toContain('"pillars foundation status"');
    const { container } = renderVisual();
    const identity = container.querySelector("[data-identity-header='true']");
    expect(identity?.querySelector('[data-region="identity"]')).toBeTruthy();
    expect(identity?.querySelector('[data-region="pillars"]')).toBeTruthy();
    expect(identity?.querySelector('[data-region="foundation"]')).toBeTruthy();
    expect(identity?.querySelector('[data-region="status"]')).toBeTruthy();
  });

  it("uses Chart DNA then summary then consulting then detail visual order", () => {
    expect(CSS).toMatch(/data-card="bazi"][\s\S]*order:\s*10/);
    expect(CSS).toMatch(/data-card="five-elements"][\s\S]*order:\s*20/);
    expect(CSS).toMatch(/data-card="pattern"][\s\S]*order:\s*21/);
    expect(CSS).toMatch(/data-card="overview"] \{ order: 30; \}/);
    expect(CSS).toMatch(/\.bte-cdash__grid > \.bte-life[\s\S]*order:\s*40/);
    expect(CSS).toMatch(/data-card="interpretation"][\s\S]*order:\s*41/);
    expect(CSS).toMatch(/data-card="action-plan"][\s\S]*order:\s*42/);
    expect(CSS).toMatch(/data-card="ten-gods"] \{ order: 50; \}/);
    expect(CSS).toMatch(/data-card="shensha"] \{ order: 51; \}/);
    expect(CSS).toMatch(/data-card="luck"] \{ order: 52; \}/);
    expect(CSS).toMatch(/data-card="five-elements"][\s\S]*grid-column:\s*span 6/);
    expect(CSS).toMatch(/data-card="pattern"][\s\S]*grid-column:\s*span 6/);
    expect(CSS).toMatch(/data-card="bazi"][\s\S]*grid-column:\s*1 \/ -1/);
  });

  it("does not change adapters, engines, or catalog titles", () => {
    expect(CARDS).toContain('title: "TỔNG QUAN LÁ SỐ"');
    expect(CARDS).toContain('title: "BÁT TỰ"');
    expect(CARDS).toContain('title: "MỆNH CỤC"');
    expect(PAGE).not.toMatch(/engines\./);
    expect(GRID).not.toMatch(/engines\./);
    for (const name of ADAPTERS) {
      const src = readFileSync(resolve(ROOT, name), "utf8");
      expect(src).not.toContain("data-ia");
      expect(src).not.toContain("ui05a");
    }
  });

  it("keeps live cache on the production /result shell", () => {
    expect(HTML).toContain("/static/dist/result.js?v=PRUNTIME01-UI05A");
    expect(HTML).toContain("/static/dist/result.css?v=PRUNTIME01-UI05A");
  });
});
