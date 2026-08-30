/**
 * UI-15 Information Visualization. Chrome only. NarrativeV2Presentation unchanged.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  VISUALIZATIONS,
  VISUAL_HIERARCHY,
} from "../../src/screens/commercial_dashboard";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");

afterEach(cleanup);

function renderVisual() {
  return render(<CommercialDashboardPage layoutMode="visual" resultSource="preview" />);
}

describe("UI-15 information visualization", () => {
  it("registers the six approved visualization kinds", () => {
    expect(VISUALIZATIONS["five-elements"]).toBe("balance-bars");
    expect(VISUALIZATIONS.luck).toBe("timeline");
    expect(VISUALIZATIONS.pattern).toBe("formation-flow");
    expect(VISUALIZATIONS.bazi).toBe("structure");
    expect(VISUALIZATIONS["ten-gods"]).toBe("relationship");
    expect(VISUALIZATIONS.shensha).toBe("grouped-chips");
    expect(VISUALIZATIONS.overview).toBeUndefined();
  });

  it("marks approved visualizations on the dashboard cards", () => {
    const { container } = renderVisual();
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-viz")).toBe("balance-bars");
    expect(container.querySelector('[data-card="luck"]')?.getAttribute("data-viz")).toBe("timeline");
    expect(container.querySelector('[data-card="pattern"]')?.getAttribute("data-viz")).toBe("formation-flow");
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-viz")).toBe("structure");
    expect(container.querySelector('[data-card="ten-gods"]')?.getAttribute("data-viz")).toBe("relationship");
    expect(container.querySelector('[data-card="shensha"]')?.getAttribute("data-viz")).toBe("grouped-chips");
  });

  it("keeps Five Elements order Mộc Hỏa Thổ Kim Thủy without sorting", () => {
    const { container } = renderVisual();
    const labels = [...container.querySelectorAll("[data-fe-row]")].map((node) => node.getAttribute("data-fe-row"));
    expect(labels).toEqual(["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]);
    expect(container.querySelector('[data-viz-chart="balance-bars"]')).toBeTruthy();
    expect(container.querySelector(".bte-fe__swatch")).toBeTruthy();
  });

  it("renders Luck as an LTR timeline with current highlighted", () => {
    const { container } = renderVisual();
    const timeline = container.querySelector('[data-viz-chart="timeline"]');
    expect(timeline).toBeTruthy();
    expect(timeline?.querySelector("[data-luck-current='true']")).toBeTruthy();
    expect(timeline?.querySelector("[data-luck-now='true']")?.textContent).toBe("Hiện tại");
    expect(timeline?.querySelector(".bte-luck__node")).toBeTruthy();
  });

  it("renders Pattern as a formation flow", () => {
    const { container } = renderVisual();
    expect(container.querySelector('[data-viz-chart="formation-flow"]')).toBeTruthy();
    expect(container.querySelector("[data-pat-section='formation'] .bte-pat__step-text")).toBeTruthy();
  });

  it("renders BaZi as layered structure with stem → branch → hidden → ten god → stage", () => {
    const { container } = renderVisual();
    const bazi = container.querySelector('[data-card="bazi"]');
    expect(bazi?.querySelector('[data-viz-chart="structure"]')).toBeTruthy();
    expect(bazi?.querySelector('[data-bazi-row="stem"]')).toBeTruthy();
    expect(bazi?.querySelector('[data-bazi-row="branch"]')).toBeTruthy();
    expect(bazi?.querySelector('[data-bazi-row="hidden"]')).toBeTruthy();
    expect(bazi?.querySelector('[data-bazi-row="ten-god"]')).toBeTruthy();
    expect(bazi?.querySelector('[data-bazi-row="stage"]')).toBeTruthy();
    expect(bazi?.querySelector("table")).toBeTruthy();
  });

  it("renders Ten Gods as lộ → tàng relationship layout", () => {
    const { container } = renderVisual();
    const tg = container.querySelector('[data-card="ten-gods"]');
    expect(tg?.querySelector('[data-viz-layer="visible"]')).toBeTruthy();
    expect(tg?.querySelector('[data-viz-layer="hidden"]')).toBeTruthy();
  });

  it("renders ShenSha as grouped chips", () => {
    const { container } = renderVisual();
    const ss = container.querySelector('[data-card="shensha"]');
    expect(ss?.querySelector('[data-viz-chart="grouped-chips"]')).toBeTruthy();
    expect(ss?.getAttribute("data-grouped")).toBe("true");
    expect(ss?.querySelectorAll("[data-ss-group]").length).toBeGreaterThan(1);
  });

  it("preserves UI-14 hierarchy and frozen spans", () => {
    expect(VISUAL_HIERARCHY["five-elements"].level).toBe(3);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    const { container } = renderVisual();
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-visual-level")).toBe("3");
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-visual-level")).toBe("1");
    expect(container.querySelector('[data-visual="v2"]')).toBeTruthy();
  });

  it("uses UI-13 tokens and forbids radar, pie, gauge, 3D, heatmap, speedometer", () => {
    expect(CSS).toContain("--feedback-success");
    expect(CSS).toContain("--feedback-info");
    expect(CSS).toContain("--accent-primary");
    expect(CSS).toContain("--space-3");
    expect(CSS).toContain("--font-size-caption");
    expect(CSS).not.toMatch(/#2f6b3a|#b42318|#b8860b|#1d4f91/);
    expect(CSS.toLowerCase()).not.toMatch(/radar|pie-chart|donut|gauge|speedometer|heatmap|3d/);
  });

  it("applies responsive visualization rules without page-level chart scroll", () => {
    expect(CSS).toContain(".bte-luck[data-viz=\"timeline\"] .bte-luck__timeline");
    expect(CSS).toContain("overflow-x: auto");
    expect(CSS).toContain("@media (max-width: 767px)");
    expect(CSS).toContain(".bte-pat[data-viz=\"formation-flow\"] .bte-pat__flow");
    expect(CSS).not.toContain("overflow-x: scroll");
  });

  it("does not edit narrative, runtime, or presentation adapters", () => {
    for (const file of [
      "fiveElementsAdapter.ts",
      "luckAdapter.ts",
      "patternAdapter.ts",
      "baziAdapter.ts",
      "tenGodsAdapter.ts",
      "shenShaAdapter.ts",
      "overviewAdapter.ts",
      "interpretationAdapter.ts",
      "actionPlanAdapter.ts",
    ]) {
      const source = readFileSync(resolve(ROOT, file), "utf8");
      expect(source).not.toContain("vizCatalog");
      expect(source).not.toContain("data-viz");
    }
  });
});
