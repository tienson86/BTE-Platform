/**
 * UI-20 Commercial Finish freeze. QA only. No Narrative / Presentation / Runtime edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  INTERPRETATION_VISUAL_FIXTURE,
  MOBILE_VISUAL_ORDER,
  MOTION_DURATIONS,
  OVERVIEW_VISUAL_FIXTURE,
  VISUAL_HIERARCHY,
  VISUALIZATIONS,
} from "../../src/screens/commercial_dashboard";
import { ExecutiveReportPage, formatPublishedDate } from "../../src/screens/executive_report";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const SCREEN = resolve(PORTAL, "src/screens/executive_report");
const REPO = resolve(PORTAL, "../..");

const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
const MOBILE_CSS = readFileSync(resolve(ROOT, "mobile/mobileExperience.css"), "utf8");
const MOTION_CSS = readFileSync(resolve(ROOT, "motion/motionExperience.css"), "utf8");
const FINISH_CSS = readFileSync(resolve(ROOT, "finish.css"), "utf8");
const TOKENS = readFileSync(resolve(PORTAL, "src/styles/tokens.css"), "utf8");
const PRINT_CSS = readFileSync(resolve(SCREEN, "print/print.css"), "utf8");
const PAGE_SRC = readFileSync(resolve(SCREEN, "ExecutiveReportPage.tsx"), "utf8");
const IDENTITY_SRC = readFileSync(resolve(ROOT, "IdentityRegions.tsx"), "utf8");

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

const PRESENTATION = JSON.parse(
  readFileSync(resolve(REPO, "implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json"), "utf8"),
) as { overview: { headline: string }; interpretation: { consulting_flow: string } };

const LIVE: AnalysisDataDto = {
  analysis_id: "ana-ui20",
  identity: {
    person: {
      full_name: "Nguyễn Tiến Sơn",
      gender: "male",
      solar_birth: "1987-01-21",
      birth_time: "04:30",
      birth_place: "Hà Tây, Việt Nam",
    },
  },
  result_meta: { created_at: "2026-08-30T09:15:00Z", release_label: "BTE V1.0" },
  narrative_v2_shadow: { status: "ok", presentation: PRESENTATION, error: null },
};

afterEach(cleanup);

function renderVisual() {
  return render(<CommercialDashboardPage layoutMode="visual" resultSource="preview" />);
}

function read(rel: string): string {
  return readFileSync(resolve(REPO, rel), "utf8");
}

describe("UI-20 commercial finish", () => {
  it("F1 respects UI-13 tokens in finish and motion overlays", () => {
    expect(TOKENS).toContain("--space-5: 24px");
    expect(TOKENS).toContain("--touch-target-min: 44px");
    expect(TOKENS).toContain("--motion-fast: 120ms");
    expect(FINISH_CSS).toContain("var(--bte-radius-12)");
    expect(MOBILE_CSS).toContain("var(--touch-target-min)");
    expect(MOBILE_CSS).not.toContain("56px");
    expect(CSS).toContain('@import "../../styles/tokens.css"');
  });

  it("F2 preserves UI-14 hierarchy", () => {
    const { container } = renderVisual();
    expect(VISUAL_HIERARCHY.overview).toEqual({ level: 1, type: "hero" });
    expect(CSS).toMatch(/data-card="overview"][\s\S]*order:\s*10/);
    expect(CSS).toMatch(/data-card="interpretation"][\s\S]*order:\s*20/);
    expect(CSS).toMatch(/data-card="action-plan"][\s\S]*order:\s*21/);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    expect(container.querySelector("[data-visual]")).toHaveProperty("className");
    expect(container.querySelector("[data-dashboard='commercial-v1']")?.getAttribute("data-visual")).toBe("v2");
  });

  it("F3 preserves UI-15 visualization semantics", () => {
    const { container } = renderVisual();
    expect(VISUALIZATIONS["five-elements"]).toBe("balance-bars");
    const labels = [...container.querySelectorAll("[data-fe-row]")].map((node) => node.getAttribute("data-fe-row"));
    expect(labels).toEqual(["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]);
    expect(container.querySelector('[data-viz-chart="timeline"] [data-luck-current="true"]')).toBeTruthy();
  });

  it("F4 preserves UI-16 report architecture", () => {
    expect(PAGE_SRC).toContain("ExecutiveSummarySection");
    expect(PAGE_SRC).toContain("InterpretationSection");
    expect(PAGE_SRC).toContain("ActionPlanSection");
    expect(PAGE_SRC).toContain("data-pdf-export=\"false\"");
    const { container } = render(<ExecutiveReportPage analysis={LIVE} />);
    expect(container.querySelector('[data-ui="executive-report"]')).toBeTruthy();
    expect(container.querySelectorAll("[data-consulting-flow='true']")).toHaveLength(1);
  });

  it("F5 preserves UI-17 print rules", () => {
    expect(PRINT_CSS).toContain("size: A4 portrait");
    expect(PRINT_CSS).toContain("animation: none !important");
    expect(PRINT_CSS).toContain("page-break");
  });

  it("F6 preserves UI-18 mobile hierarchy", () => {
    expect(MOBILE_VISUAL_ORDER.overview).toBe(1);
    expect(MOBILE_VISUAL_ORDER["action-plan"]).toBe(2);
    expect(MOBILE_VISUAL_ORDER.interpretation).toBe(3);
    expect(MOBILE_CSS).toContain('[data-mobile-order="1"]');
  });

  it("F7 preserves UI-19 motion rules", () => {
    expect(MOTION_DURATIONS.fast).toBe("120ms");
    expect(MOTION_CSS).toContain("@media (prefers-reduced-motion: reduce)");
    expect(MOTION_CSS.toLowerCase()).not.toContain("bounce");
  });

  it("F8 keeps Narrative text unchanged", () => {
    const { container } = renderVisual();
    expect(container.querySelector('[data-overview-section="insight"]')?.textContent).toBe(
      OVERVIEW_VISUAL_FIXTURE.insight,
    );
    expect(container.querySelector("[data-int-lead='true']")?.textContent).toContain(
      INTERPRETATION_VISUAL_FIXTURE.lead,
    );
  });

  it("F9 does not change Presentation selection", () => {
    const selection = readFileSync(resolve(PORTAL, "src/resultState/narrativePresentationSelection.ts"), "utf8");
    expect(selection).not.toContain("data-finish");
    expect(selection).not.toContain("finish.css");
  });

  it("F10 does not change adapter semantics", () => {
    for (const file of ADAPTERS) {
      const src = readFileSync(resolve(ROOT, file), "utf8");
      expect(src).not.toContain("data-finish");
      expect(src).not.toContain("finish.css");
    }
  });

  it("F11 does not leak debug internals on customer surfaces", () => {
    const { container } = renderVisual();
    const text = container.textContent ?? "";
    expect(text).not.toContain("undefined");
    expect(text).not.toContain("[object Object]");
    expect(text).not.toContain("source_unit");
    expect(text).not.toContain("rule_id");
    expect(text).not.toContain("schema_version");
    expect(text).not.toMatch(/\bnull\b/);
  });

  it("F12 maintains DD/MM/YYYY customer dates", () => {
    expect(formatPublishedDate("1987-01-21")).toBe("21/01/1987");
    expect(IDENTITY_SRC).toContain("formatCustomerDate");
    const { container } = render(
      <CommercialDashboardPage analysis={LIVE} resultSource="current" />,
    );
    expect(container.textContent).toContain("21/01/1987");
    expect(container.textContent).not.toContain("1987-01-21");
  });

  it("F13 maintains 24-hour time", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={LIVE} resultSource="current" />,
    );
    expect(container.textContent).toContain("04:30");
    expect(container.textContent).not.toMatch(/\bAM\b|\bPM\b/);
    expect(formatPublishedDate("2026-08-30T09:15:00Z")).toContain("09:15");
  });

  it("F14 prevents horizontal mobile overflow", () => {
    expect(FINISH_CSS).toContain("overflow-x: clip");
    expect(FINISH_CSS).toContain("@media (max-width: 767px)");
  });

  it("F15 keeps reduced motion", () => {
    expect(MOTION_CSS).toContain("@media (prefers-reduced-motion: reduce)");
    expect(MOTION_CSS).toContain("animation: none !important");
    expect(TOKENS).toContain("--motion-fast: 0ms");
  });

  it("F16 keeps focus visible", () => {
    expect(CSS).toContain(":focus-visible");
    expect(CSS).toContain("--focus-ring");
    expect(MOTION_CSS).toContain(":focus-visible");
  });

  it("F17 keeps empty optional content safe", () => {
    const { container } = render(
      <CommercialDashboardPage resultSource="missing" analysis={null} />,
    );
    expect(container.querySelector(".rp-status-gate, .cui-base-state, [data-status]")).toBeTruthy();
    expect(container.textContent).not.toContain("[object Object]");
  });

  it("F18 passes desktop / tablet / mobile baseline flags", () => {
    const { container } = renderVisual();
    const root = container.querySelector("[data-dashboard='commercial-v1']");
    expect(root?.getAttribute("data-visual")).toBe("v2");
    expect(root?.getAttribute("data-mobile-experience")).toBe("true");
    expect(root?.getAttribute("data-motion")).toBe("v1");
    expect(root?.getAttribute("data-finish")).toBe("v2");
    expect(MOBILE_CSS).toContain("@media (max-width: 1199px) and (min-width: 768px)");
    expect(CSS).toContain("max-width: 1440px");
  });

  it("F19 passes report baseline", () => {
    const { container } = render(<ExecutiveReportPage analysis={LIVE} />);
    const root = container.querySelector('[data-ui="executive-report"]');
    expect(root?.getAttribute("data-finish")).toBe("v2");
    expect(root?.getAttribute("data-print-ready")).toBe("true");
    expect(container.querySelector('[data-report-section="executive-summary"]')).toBeTruthy();
    expect(container.querySelector('[data-report-section="action-plan"]')).toBeTruthy();
  });

  it("F20 passes print baseline", () => {
    expect(PRINT_CSS).toContain("@page");
    expect(PRINT_CSS).toContain("size: A4 portrait");
    expect(FINISH_CSS).toContain("@media print");
    expect(read("applications/api/routes/export.py")).not.toContain("data-finish");
  });
});
