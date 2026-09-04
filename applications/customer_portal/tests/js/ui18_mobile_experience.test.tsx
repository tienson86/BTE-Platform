/**
 * UI-18 Mobile Experience. Visual priority only. No Narrative / Presentation / Runtime edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import {
  ACTION_PLAN_VISUAL_FIXTURE,
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  INTERPRETATION_VISUAL_FIXTURE,
  MOBILE_EVIDENCE_CARDS,
  MOBILE_VISUAL_ORDER,
  OVERVIEW_VISUAL_FIXTURE,
  VISUAL_HIERARCHY,
} from "../../src/screens/commercial_dashboard";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const SCREEN = resolve(PORTAL, "src/screens/executive_report");
const REPO = resolve(PORTAL, "../..");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
const MOBILE_CSS = readFileSync(resolve(ROOT, "mobile/mobileExperience.css"), "utf8");

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

describe("UI-18 mobile experience", () => {
  it("M1 keeps narrative copy on the visual dashboard", () => {
    const { container } = renderVisual();
    expect(container.querySelector('[data-overview-section="insight"]')?.textContent).toBe(
      OVERVIEW_VISUAL_FIXTURE.insight,
    );
    expect(container.querySelector("[data-int-lead='true']")?.textContent).toContain(
      INTERPRETATION_VISUAL_FIXTURE.lead,
    );
    expect(container.querySelector("[data-ap-section='priority']")?.textContent).toContain(
      ACTION_PLAN_VISUAL_FIXTURE.priority?.title ?? "",
    );
  });

  it("M2 does not import Presentation selection into mobile chrome", () => {
    const mobileIndex = readFileSync(resolve(ROOT, "mobile/index.ts"), "utf8");
    const selection = readFileSync(
      resolve(PORTAL, "src/resultState/narrativePresentationSelection.ts"),
      "utf8",
    );
    expect(mobileIndex).not.toContain("narrativePresentationSelection");
    expect(selection).not.toContain("mobileExperience");
    expect(selection).not.toContain("data-mobile");
  });

  it("M3 keeps desktop visual hierarchy and frozen DOM order", () => {
    const { container } = renderVisual();
    const order = [...container.querySelectorAll("[data-card]")].map((node) => node.getAttribute("data-card"));
    expect(order).toEqual([...DOM_ORDER]);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    expect(VISUAL_HIERARCHY.overview).toEqual({ level: 1, type: "hero" });
    expect(CSS).toMatch(/data-card="overview"] \{ order: 30; \}/);
    expect(CSS).toMatch(/data-card="interpretation"][\s\S]*order:\s*41/);
    expect(CSS).toMatch(/data-card="action-plan"][\s\S]*order:\s*42/);
  });

  it("M4 assigns the mobile visual order without rewriting source order", () => {
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
    const { container } = renderVisual();
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-mobile-order")).toBe("1");
    expect(container.querySelector('[data-card="action-plan"]')?.getAttribute("data-mobile-order")).toBe("2");
    expect(container.querySelector('[data-card="interpretation"]')?.getAttribute("data-mobile-order")).toBe("3");
    expect(container.querySelector('[data-card="luck"]')?.getAttribute("data-mobile-order")).toBe("4");
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-mobile-order")).toBe("5");
    expect(container.querySelector('[data-card="pattern"]')?.getAttribute("data-mobile-order")).toBe("6");
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-mobile-order")).toBe("7");
    expect(container.querySelector('[data-card="ten-gods"]')?.getAttribute("data-mobile-order")).toBe("8");
    expect(container.querySelector('[data-card="shensha"]')?.getAttribute("data-mobile-order")).toBe("9");
    expect(MOBILE_CSS).toContain('[data-mobile-order="1"]');
    expect(MOBILE_CSS).toContain("order: 1");
    expect(MOBILE_CSS).toContain("order: 2");
  });

  it("M5 marks the Overview hero for the first mobile viewport", () => {
    const { container } = renderVisual();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-mobile-hero")).toBe("true");
    expect(container.querySelector("[data-dashboard='commercial-v1']")?.getAttribute("data-mobile-experience")).toBe(
      "true",
    );
    expect(MOBILE_CSS).toContain("min-height: 70dvh");
  });

  it("M6 keeps Top Priority visible in the hero", () => {
    const { container } = renderVisual();
    const priority = container.querySelector('[data-overview-section="top-priority"]');
    expect(priority?.textContent).toContain("Ưu tiên");
    expect(priority?.textContent).toContain(ACTION_PLAN_VISUAL_FIXTURE.priority?.title ?? "");
    expect(MOBILE_CSS).toContain(".bte-ov__priority");
    expect(MOBILE_CSS).toContain("position: sticky");
  });

  it("M7 collapses evidence bodies by default", () => {
    const { container } = renderVisual();
    for (const id of MOBILE_EVIDENCE_CARDS) {
      const card = container.querySelector(`[data-card="${id}"]`);
      expect(card?.getAttribute("data-mobile-evidence")).toBe("true");
      expect(card?.getAttribute("data-mobile-open")).toBe("false");
      expect(card?.querySelector("[data-mobile-body]")).toBeTruthy();
    }
    expect(MOBILE_CSS).toContain('[data-mobile-evidence="true"]:not([data-mobile-open="true"]) [data-mobile-body]');
    expect(container.querySelector('[data-viz-chart="balance-bars"]')).toBeTruthy();
    expect(container.querySelector('[data-viz-chart="structure"]')).toBeTruthy();
  });

  it("M8 keeps consulting_flow visible and structured interpretation collapsed", () => {
    const { container } = renderVisual();
    const interpretation = container.querySelector('[data-card="interpretation"]');
    expect(interpretation?.querySelector("[data-int-lead='true']")?.textContent).toContain(
      INTERPRETATION_VISUAL_FIXTURE.lead,
    );
    expect(interpretation?.getAttribute("data-mobile-open")).toBe("false");
    expect(interpretation?.querySelector("[data-mobile-body]")?.classList.contains("bte-int__zones")).toBe(true);
    expect(MOBILE_CSS).toContain('[data-card="interpretation"]:not([data-mobile-open="true"]) [data-mobile-body]');
  });

  it("M9 keeps the Action card expanded", () => {
    const { container } = renderVisual();
    const action = container.querySelector('[data-card="action-plan"]');
    expect(action?.getAttribute("data-mobile-expanded")).toBe("true");
    expect(action?.querySelector("[data-ap-section='priority']")).toBeTruthy();
    expect(action?.querySelector("[data-ap-section='actions']")).toBeTruthy();
    expect(action?.querySelector("[data-mobile-body]")).toBeNull();
  });

  it("M10 places expand, collapse, and next controls in the thumb zone", () => {
    const { container } = renderVisual();
    const thumbs = container.querySelectorAll("[data-thumb-zone='true']");
    expect(thumbs.length).toBeGreaterThanOrEqual(3);
    expect(container.querySelector("[data-mobile='action-bar']")).toBeTruthy();
    expect(container.querySelector('a[href="#bte-card-action-plan"]')).toBeTruthy();
    expect(container.querySelector('a[href="#bte-card-interpretation"]')).toBeTruthy();
    expect(MOBILE_CSS).toContain("min-height: var(--touch-target-min)");
    expect(MOBILE_CSS).toContain(".bte-mobile-bar");
    const toggle = container.querySelector('[data-card="five-elements"] .bte-mobile-toggle');
    expect(toggle).toBeTruthy();
    fireEvent.click(toggle as HTMLButtonElement);
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-mobile-open")).toBe("true");
  });

  it("M11 reorganizes mobile and intermediates tablet without changing desktop CSS", () => {
    expect(MOBILE_CSS).toContain("@media (max-width: 1199px) and (min-width: 768px)");
    expect(MOBILE_CSS).toContain("@media (max-width: 767px)");
    expect(MOBILE_CSS).toContain("gap: var(--space-7) 0");
    expect(CSS).toContain('.bte-cdash[data-visual="v2"] .bte-cdash__card[data-card="overview"]');
    expect(CSS).toContain("grid-column: 1 / -1");
  });

  it("M12 does not touch Runtime modules", () => {
    const page = readFileSync(resolve(ROOT, "CommercialDashboardPage.tsx"), "utf8");
    expect(page).not.toContain("applications.engine");
    expect(page).not.toContain("from \"../../../../engine");
    expect(read("applications/api/app.py")).not.toContain("mobileExperience");
    expect(read("applications/api/app.py")).not.toContain("data-mobile");
  });

  it("M13 does not rewrite Presentation adapters or copy", () => {
    for (const file of ADAPTERS) {
      const src = readFileSync(resolve(ROOT, file), "utf8");
      expect(src).not.toContain("mobile/");
      expect(src).not.toContain("data-mobile");
      expect(src).not.toContain("MOBILE_VISUAL_ORDER");
    }
  });

  it("M14 does not change Export", () => {
    const exportSrc = read("applications/api/routes/export.py");
    const model = readFileSync(resolve(SCREEN, "reportModel.ts"), "utf8");
    expect(exportSrc).not.toContain("mobileExperience");
    expect(exportSrc).not.toContain("data-mobile");
    expect(model).not.toContain("mobileExperience");
    expect(model).not.toContain("data-mobile-order");
  });

  it("M15 does not change adapters", () => {
    for (const file of ADAPTERS) {
      const src = readFileSync(resolve(ROOT, file), "utf8");
      expect(src).not.toMatch(/mobileCardDom|useMobileOpen|MobileToggle/);
    }
    expect(readFileSync(resolve(PORTAL, "src/resultState/narrativePresentationSelection.ts"), "utf8")).not.toContain(
      "MobileActionBar",
    );
  });
});
