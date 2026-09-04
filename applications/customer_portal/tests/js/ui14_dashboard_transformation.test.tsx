/**
 * UI-14 Commercial Dashboard visual hierarchy. Presentation chrome only.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  ACTION_PLAN_VISUAL_FIXTURE,
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  VISUAL_HIERARCHY,
} from "../../src/screens/commercial_dashboard";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");

afterEach(cleanup);

function renderVisual() {
  return render(<CommercialDashboardPage layoutMode="visual" resultSource="preview" />);
}

describe("UI-14 dashboard transformation", () => {
  it("defines four visual levels without changing card catalog geometry", () => {
    expect(VISUAL_HIERARCHY.overview).toEqual({ level: 1, type: "hero" });
    expect(VISUAL_HIERARCHY.interpretation).toEqual({ level: 2, type: "analysis" });
    expect(VISUAL_HIERARCHY["action-plan"]).toEqual({ level: 2, type: "analysis" });
    expect(VISUAL_HIERARCHY.bazi.level).toBe(3);
    expect(VISUAL_HIERARCHY["five-elements"].level).toBe(3);
    expect(VISUAL_HIERARCHY["ten-gods"].level).toBe(3);
    expect(VISUAL_HIERARCHY.pattern.level).toBe(3);
    expect(VISUAL_HIERARCHY.luck.level).toBe(3);
    expect(VISUAL_HIERARCHY.shensha.level).toBe(3);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("marks Visual System V2 on the live dashboard root", () => {
    const { container } = renderVisual();
    const root = container.querySelector("[data-dashboard='commercial-v1']");
    expect(root?.getAttribute("data-visual")).toBe("v2");
    expect(root?.getAttribute("data-canonical-result")).toBe("ui03");
  });

  it("applies card types and visual levels on the DOM", () => {
    const { container } = renderVisual();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-visual-level")).toBe("1");
    expect(overview?.getAttribute("data-card-type")).toBe("hero");
    expect(overview?.getAttribute("data-span")).toBe("4");

    expect(container.querySelector('[data-card="interpretation"]')?.getAttribute("data-visual-level")).toBe("2");
    expect(container.querySelector('[data-card="action-plan"]')?.getAttribute("data-visual-level")).toBe("2");
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-visual-level")).toBe("3");
    expect(container.querySelector('[data-identity-header="true"]')?.getAttribute("data-visual-level")).toBe("4");
    expect(container.querySelector('[data-module="bone-weight-detail"]')?.getAttribute("data-card-type")).toBe(
      "reference",
    );
  });

  it("keeps frozen semantic DOM order", () => {
    const { container } = renderVisual();
    const order = [...container.querySelectorAll("[data-card]")].map((node) => node.getAttribute("data-card"));
    expect(order).toEqual([
      "overview",
      "bazi",
      "five-elements",
      "ten-gods",
      "pattern",
      "shensha",
      "luck",
      "interpretation",
      "action-plan",
    ]);
  });

  it("copies Top Priority into the hero without rewriting narrative", () => {
    const { container } = renderVisual();
    const heroPriority = container.querySelector('[data-overview-section="top-priority"]');
    expect(heroPriority?.textContent).toContain("Ưu tiên");
    expect(heroPriority?.textContent).toContain(ACTION_PLAN_VISUAL_FIXTURE.priority?.title ?? "");
    expect(container.querySelector('[data-overview-section="insight"]')?.textContent).toContain(
      "Bạn thuộc nhóm Thân vượng",
    );
  });

  it("uses Visual System V2 tokens and drops the legacy red palette", () => {
    expect(CSS).toContain('@import "../../styles/tokens.css"');
    expect(CSS).toContain("--accent-primary");
    expect(CSS).toContain("--font-family-display");
    expect(CSS).toContain("--font-size-section");
    expect(CSS).toContain("--space-5");
    expect(CSS).toContain("--surface-section");
    expect(CSS).toContain("--focus-ring");
    expect(CSS).toContain("--touch-target-min");
    expect(CSS).not.toContain("#9a1b1b");
    expect(CSS).not.toContain("Be Vietnam Pro");
    expect(CSS).not.toContain("rgba(154, 27, 27");
  });

  it("promotes Overview to a full-width hero via CSS order, not data-span", () => {
    expect(CSS).toContain('.bte-cdash[data-visual="v2"] .bte-cdash__card[data-card="overview"]');
    expect(CSS).toContain("grid-column: 1 / -1");
    expect(CSS).toMatch(/data-card="overview"] \{ order: 30; \}/);
    expect(CSS).toMatch(/data-card="interpretation"][\s\S]*order:\s*41/);
    expect(CSS).toMatch(/data-card="action-plan"][\s\S]*order:\s*42/);
    expect(CSS).toMatch(/data-card="bazi"][\s\S]*order:\s*10/);
  });

  it("preserves hierarchy at tablet and mobile breakpoints", () => {
    expect(CSS).toContain("@media (max-width: 1199px)");
    expect(CSS).toContain("@media (max-width: 767px)");
    expect(CSS).toContain("padding: var(--space-5) var(--space-5) var(--space-6)");
    expect(CSS).toContain("padding: var(--space-4)");
    expect(CSS).toContain('.bte-cdash[data-visual="v2"] .bte-cdash__card[data-card]');
  });

  it("unifies badges, markers, empty copy, and skeleton loading", () => {
    expect(CSS).toContain(".bte-cdash__badge--accent");
    expect(CSS).toContain(".bte-ap__marker--priority");
    expect(CSS).toContain(".bte-ap__marker--action");
    expect(CSS).toContain("animation: bte-cdash-skel");
    expect(CSS).toContain("prefers-reduced-motion");
    const { container } = render(
      <CommercialDashboardPage layoutMode="skeleton" resultSource="preview" />,
    );
    expect(container.querySelectorAll("[data-skeleton='true']")).toHaveLength(9);
    const empty = render(
      <CommercialDashboardPage resultSource="missing" analysis={null} />,
    );
    expect(empty.container.querySelector(".rp-status-gate, .cui-base-state, [data-status]")).toBeTruthy();
    empty.unmount();
  });

  it("does not edit narrative, runtime, or presentation adapters", () => {
    const adapter = readFileSync(resolve(ROOT, "overviewAdapter.ts"), "utf8");
    const interpretation = readFileSync(resolve(ROOT, "interpretationAdapter.ts"), "utf8");
    const action = readFileSync(resolve(ROOT, "actionPlanAdapter.ts"), "utf8");
    expect(adapter).not.toContain("visualHierarchy");
    expect(interpretation).not.toContain("visualHierarchy");
    expect(action).not.toContain("visualHierarchy");
    expect(adapter).not.toContain("data-visual-level");
  });
});
