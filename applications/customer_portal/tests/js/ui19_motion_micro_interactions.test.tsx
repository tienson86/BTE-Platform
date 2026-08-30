/**
 * UI-19 Motion & Micro-interactions. Chrome only. No Narrative / Presentation / Runtime edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  INTERPRETATION_VISUAL_FIXTURE,
  MOBILE_VISUAL_ORDER,
  MOTION_DURATIONS,
  MOTION_EASING,
  OVERVIEW_VISUAL_FIXTURE,
  VISUAL_HIERARCHY,
  VISUALIZATIONS,
} from "../../src/screens/commercial_dashboard";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const SCREEN = resolve(PORTAL, "src/screens/executive_report");
const REPO = resolve(PORTAL, "../..");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
const MOBILE_CSS = readFileSync(resolve(ROOT, "mobile/mobileExperience.css"), "utf8");
const MOTION_CSS = readFileSync(resolve(ROOT, "motion/motionExperience.css"), "utf8");
const TOKENS = readFileSync(resolve(PORTAL, "src/styles/tokens.css"), "utf8");
const PRINT_CSS = readFileSync(resolve(SCREEN, "print/print.css"), "utf8");

const ADAPTERS = [
  "overviewAdapter.ts",
  "interpretationAdapter.ts",
  "actionPlanAdapter.ts",
  "baziAdapter.ts",
  "fiveElementsAdapter.ts",
  "tenGodsAdapter.ts",
  "patternAdapter.ts",
  "shenShaAdapter.ts",
  "luckAdapter.ts",
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

function read(rel: string): string {
  return readFileSync(resolve(REPO, rel), "utf8");
}

function stripComments(css: string): string {
  return css.replace(/\/\*[\s\S]*?\*\//g, "");
}

describe("UI-19 motion micro-interactions", () => {
  it("MM1 uses only approved motion durations", () => {
    expect(MOTION_DURATIONS).toEqual({ fast: "120ms", standard: "200ms", deliberate: "320ms" });
    expect(MOTION_EASING).toBe("cubic-bezier(0.22, 1, 0.36, 1)");
    expect(TOKENS).toContain("--motion-fast: 120ms");
    expect(TOKENS).toContain("--motion-normal: 200ms");
    expect(TOKENS).toContain("--motion-slow: 320ms");
    expect(stripComments(MOTION_CSS).match(/\d+ms/g) ?? []).toEqual([]);
    expect(MOTION_CSS).toContain("var(--motion-fast)");
    expect(MOTION_CSS).toContain("var(--motion-normal)");
    expect(MOTION_CSS).toContain("var(--motion-slow)");
    expect(MOTION_CSS).toContain("var(--motion-ease-out)");
  });

  it("MM2 does not change Narrative copy on the visual dashboard", () => {
    const { container } = renderVisual();
    expect(container.querySelector('[data-overview-section="insight"]')?.textContent).toBe(
      OVERVIEW_VISUAL_FIXTURE.insight,
    );
    expect(container.querySelector("[data-int-lead='true']")?.textContent).toContain(
      INTERPRETATION_VISUAL_FIXTURE.lead,
    );
  });

  it("MM3 does not import Presentation selection into motion chrome", () => {
    const motionIndex = readFileSync(resolve(ROOT, "motion/index.ts"), "utf8");
    const selection = readFileSync(
      resolve(PORTAL, "src/resultState/narrativePresentationSelection.ts"),
      "utf8",
    );
    expect(motionIndex).not.toContain("narrativePresentationSelection");
    expect(selection).not.toContain("motionExperience");
    expect(selection).not.toContain("data-motion");
  });

  it("MM4 does not change adapters", () => {
    for (const file of ADAPTERS) {
      const src = readFileSync(resolve(ROOT, file), "utf8");
      expect(src).not.toContain("motion/");
      expect(src).not.toContain("data-motion");
      expect(src).not.toContain("MOTION_DURATIONS");
    }
  });

  it("MM5 keeps aria-expanded canonical on expand/collapse", () => {
    const { container } = renderVisual();
    const desktop = container.querySelector(".bte-int__toggle");
    expect(desktop?.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(desktop as HTMLButtonElement);
    expect(desktop?.getAttribute("aria-expanded")).toBe("true");
    const mobile = container.querySelector('[data-card="interpretation"] .bte-mobile-toggle');
    expect(mobile?.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(mobile as HTMLButtonElement);
    expect(mobile?.getAttribute("aria-expanded")).toBe("true");
    expect(container.querySelector('[data-card="interpretation"]')?.getAttribute("data-mobile-open")).toBe(
      "true",
    );
  });

  it("MM6 keeps keyboard focus visible", () => {
    expect(CSS).toContain("--focus-ring");
    expect(CSS).toContain(":focus-visible");
    expect(MOTION_CSS).toContain(":focus-visible");
    expect(MOTION_CSS).toContain("var(--focus-ring)");
    expect(MOTION_CSS).toContain("transition: box-shadow var(--motion-fast)");
  });

  it("MM7 defines reduced-motion rules", () => {
    expect(MOTION_CSS).toContain("@media (prefers-reduced-motion: reduce)");
    expect(TOKENS).toContain("@media (prefers-reduced-motion: reduce)");
    expect(TOKENS).toContain("--motion-fast: 0ms");
  });

  it("MM8 removes nonessential transitions under reduced motion", () => {
    const reduced = MOTION_CSS.slice(MOTION_CSS.indexOf("@media (prefers-reduced-motion: reduce)"));
    expect(reduced).toContain("animation: none !important");
    expect(reduced).toContain("transition: none !important");
    expect(reduced).toContain("scroll-behavior: auto");
    expect(MOTION_CSS).toContain("@media (prefers-reduced-motion: no-preference)");
    expect(MOTION_CSS).toContain("scroll-behavior: smooth");
  });

  it("MM9 keeps mobile thumb navigation functional", () => {
    const { container } = renderVisual();
    expect(container.querySelector("[data-mobile='action-bar']")).toBeTruthy();
    expect(container.querySelector('a[href="#bte-card-action-plan"]')).toBeTruthy();
    expect(container.querySelector('a[href="#bte-card-interpretation"]')).toBeTruthy();
    expect(container.querySelector("#bte-card-action-plan")).toBeTruthy();
    expect(container.querySelector("#bte-card-interpretation")).toBeTruthy();
  });

  it("MM10 does not duplicate sticky chrome", () => {
    const { container } = renderVisual();
    expect(container.querySelectorAll('[data-overview-section="top-priority"]')).toHaveLength(1);
    expect(container.querySelectorAll("[data-mobile='action-bar']")).toHaveLength(1);
    expect(container.querySelectorAll("[data-motion-reveal='priority']")).toHaveLength(1);
    expect(container.querySelectorAll("[data-motion-reveal='insight']")).toHaveLength(1);
  });

  it("MM11 does not hijack scroll", () => {
    expect(MOTION_CSS).not.toContain("scroll-snap");
    expect(MOTION_CSS).not.toContain("overscroll-behavior: none");
    expect(MOTION_CSS).not.toContain("touch-action: none");
    expect(MOTION_CSS).not.toContain("preventDefault");
    expect(readFileSync(resolve(ROOT, "CommercialDashboardPage.tsx"), "utf8")).not.toContain("onWheel");
  });

  it("MM12 does not use parallax", () => {
    expect(MOTION_CSS).not.toContain("parallax");
    expect(MOTION_CSS).not.toContain("background-attachment: fixed");
    expect(MOTION_CSS).not.toContain("translateZ");
    expect(MOTION_CSS).not.toContain("perspective");
  });

  it("MM13 does not use bounce or spring", () => {
    expect(MOTION_CSS.toLowerCase()).not.toContain("bounce");
    expect(MOTION_CSS.toLowerCase()).not.toContain("spring");
    expect(MOTION_CSS).not.toContain("cubic-bezier(0.68");
    expect(MOTION_EASING).toBe("cubic-bezier(0.22, 1, 0.36, 1)");
  });

  it("MM14 keeps print media static", () => {
    expect(MOTION_CSS).toContain("@media print");
    expect(PRINT_CSS).toContain("animation: none !important");
    expect(PRINT_CSS).toContain("transition: none !important");
  });

  it("MM15 keeps UI-14 visual hierarchy", () => {
    const { container } = renderVisual();
    const order = [...container.querySelectorAll("[data-card]")].map((node) => node.getAttribute("data-card"));
    expect(order).toEqual([...DOM_ORDER]);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    expect(VISUAL_HIERARCHY.overview).toEqual({ level: 1, type: "hero" });
    expect(CSS).toMatch(/data-card="overview"][\s\S]*order:\s*10/);
    expect(CSS).toMatch(/data-card="interpretation"][\s\S]*order:\s*20/);
    expect(CSS).toMatch(/data-card="action-plan"][\s\S]*order:\s*21/);
  });

  it("MM16 keeps UI-18 mobile hierarchy", () => {
    const { container } = renderVisual();
    expect(MOBILE_VISUAL_ORDER).toEqual({
      overview: 1,
      "action-plan": 2,
      interpretation: 3,
      luck: 4,
      "five-elements": 5,
      pattern: 6,
      bazi: 7,
      "ten-gods": 8,
      shensha: 9,
    });
    expect(MOBILE_CSS).toContain('[data-mobile-order="1"]');
    expect(container.querySelector("[data-dashboard='commercial-v1']")?.getAttribute("data-motion")).toBe("v1");
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-mobile-order")).toBe("1");
    expect(container.querySelector('[data-card="action-plan"]')?.getAttribute("data-mobile-order")).toBe("2");
  });

  it("MM17 keeps visualization semantics", () => {
    const { container } = renderVisual();
    expect(VISUALIZATIONS["five-elements"]).toBe("balance-bars");
    const labels = [...container.querySelectorAll("[data-fe-row]")].map((node) => node.getAttribute("data-fe-row"));
    expect(labels).toEqual(["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]);
    expect(container.querySelector('[data-viz-chart="timeline"] [data-luck-current="true"]')).toBeTruthy();
    expect(container.querySelector('[data-viz-chart="structure"]')).toBeTruthy();
  });

  it("MM18 keeps Narrative text byte-equivalent on the dashboard", () => {
    const { container } = renderVisual();
    expect(container.querySelector('[data-overview-section="insight"]')?.textContent).toBe(
      OVERVIEW_VISUAL_FIXTURE.insight,
    );
    expect(container.querySelector('[data-overview-section="conclusion"]')?.textContent).toBe(
      OVERVIEW_VISUAL_FIXTURE.conclusion,
    );
    expect(read("applications/api/routes/export.py")).not.toContain("motionExperience");
    expect(readFileSync(resolve(SCREEN, "reportModel.ts"), "utf8")).not.toContain("data-motion");
  });
});
