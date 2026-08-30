/**
 * UI-16 Executive Report Experience. Layout only. Presentation copy unchanged.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { ExecutiveReportPage } from "../../src/screens/executive_report";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const REPO = resolve(PORTAL, "../..");
const SCREEN = resolve(PORTAL, "src/screens/executive_report");

const PRESENTATION = JSON.parse(
  readFileSync(resolve(REPO, "implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json"), "utf8"),
) as Record<string, unknown>;

const CONSULTING = (PRESENTATION.interpretation as { consulting_flow: string }).consulting_flow;
const HEADLINE = (PRESENTATION.overview as { headline: string }).headline;
const SUMMARY = (PRESENTATION.overview as { summary: string }).summary;
const PRIORITY = (PRESENTATION.action_plan as { top_priority: { title: string; description: string } })
  .top_priority;
const PACK05_IDENTITY = "Pack05 identity stays independent";

const REQUEST: AnalyzeChartRequest = {
  year: 1987,
  month: 1,
  day: 21,
  hour: 4,
  minute: 30,
  gender: "male",
  full_name: "Nguyễn Tiến Sơn",
  birth_place: "Hà Tây, Việt Nam",
};

const ANALYSIS = {
  analysis_id: "ana-secret-debug-id",
  identity: {
    person: {
      full_name: "Nguyễn Tiến Sơn",
      gender: "male",
      solar_birth: "1987-01-21",
      birth_time: "04:30",
      birth_place: "Hà Tây, Việt Nam",
    },
  },
  result_meta: {
    created_at: "2026-08-30T09:15:00Z",
    release_label: "BTE V1.0",
  },
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
    day_master_yin_yang: "Dương",
    year_pillar: { stem: "Bính", branch: "Dần", ten_god: "Thiên Ấn" },
    month_pillar: { stem: "Canh", branch: "Dần", ten_god: "Tỷ Kiên" },
    day_pillar: { stem: "Canh", branch: "Thân", ten_god: "Nhật Chủ" },
    hour_pillar: { stem: "Canh", branch: "Dần", ten_god: "Tỷ Kiên" },
    shensha: ["Thiên Ất Quý Nhân", "Văn Xương"],
  },
  five_elements: { counts: { wood: 3, fire: 1, earth: 2, metal: 4, water: 2 } },
  strength: { strength_level: "strong" },
  pattern: {
    cach_cuc: "Chính Ấn cách",
    status: "Đắc cách",
    formation: ["Ấn tinh tọa tháng", "Nhật Chủ được ấn sinh"],
  },
  luck: {
    direction_label: "Thuận",
    start_age: 5,
    current_cycle: {
      index: 3,
      gan_zhi: "Quý Mão",
      year_start: 2021,
      year_end: 2030,
    },
    cycles: [
      { index: 0, gan_zhi: "Canh Tý", year_start: 1991, year_end: 2000 },
      { index: 1, gan_zhi: "Tân Sửu", year_start: 2001, year_end: 2010 },
      { index: 2, gan_zhi: "Nhâm Dần", year_start: 2011, year_end: 2020 },
      { index: 3, gan_zhi: "Quý Mão", year_start: 2021, year_end: 2030 },
      { index: 4, gan_zhi: "Giáp Thìn", year_start: 2031, year_end: 2040 },
    ],
  },
  narrative_result: {
    contract: "pack05_narrative_result_v1",
    status: "ok",
    summary: { identity: PACK05_IDENTITY, priority_recommendation: "Pack05 priority" },
  },
  narrative_v2_shadow: {
    status: "ok",
    presentation: PRESENTATION,
    error: null,
    pipeline_trace: "must-not-render",
    source_unit_ids: ["NR-REL-001"],
  },
} as AnalysisDataDto;

const CSS = readFileSync(resolve(SCREEN, "executive-report.css"), "utf8");
const PAGE_SRC = readFileSync(resolve(SCREEN, "ExecutiveReportPage.tsx"), "utf8");
const MODEL_SRC = readFileSync(resolve(SCREEN, "reportModel.ts"), "utf8");
const APP_PY = readFileSync(resolve(PORTAL, "app.py"), "utf8");
const RESULT_APP = readFileSync(resolve(PORTAL, "src/entries/resultApp.tsx"), "utf8");

const FORBIDDEN = [
  "pipeline_trace",
  "source_unit_ids",
  "NR-REL-001",
  "ana-secret-debug-id",
  "rule_id",
  "engines.narrative_v2",
  "must-not-render",
  PACK05_IDENTITY,
  "Không có trong Presentation",
];

afterEach(cleanup);

function renderReport(analysis: AnalysisDataDto | null = ANALYSIS) {
  return render(<ExecutiveReportPage analysis={analysis} request={REQUEST} />);
}

describe("UI-16 executive report", () => {
  it("R1 Narrative source is Presentation only", () => {
    const { container } = renderReport();
    expect(container.querySelector("[data-narrative-source]")?.getAttribute("data-narrative-source")).toBe(
      "presentation-v2",
    );
    expect(MODEL_SRC).toContain("adaptNarrativeV2Presentation");
    expect(MODEL_SRC).not.toContain("selectNarrativePresentation");
    expect(container.textContent).toContain(HEADLINE);
    expect(container.textContent).not.toContain(PACK05_IDENTITY);
  });

  it("R2 consulting_flow rendered unchanged", () => {
    const { container } = renderReport();
    const flow = container.querySelector("[data-consulting-flow]");
    expect(flow?.textContent).toBe(CONSULTING);
    expect(container.querySelectorAll("[data-consulting-flow]")).toHaveLength(1);
  });

  it("R3 Action wording rendered unchanged", () => {
    const { container } = renderReport();
    expect(container.querySelector("[data-action-priority-title]")?.textContent).toBe(PRIORITY.title);
    expect(container.querySelector("[data-action-priority-description]")?.textContent).toBe(
      PRIORITY.description,
    );
  });

  it("R4 No report-side Narrative composition", () => {
    expect(MODEL_SRC).not.toMatch(/consulting_flow\s*\+/);
    expect(MODEL_SRC).not.toContain("composeOverview");
    expect(PAGE_SRC).not.toContain("selectNarrativePresentation");
    const { container } = renderReport();
    const interpretation = container.querySelector('[data-report-section="interpretation"]');
    expect(interpretation?.querySelector("[data-report-overview]")).toBeNull();
    expect(container.querySelectorAll("[data-report-overview='summary']")).toHaveLength(1);
  });

  it("R5 Missing optional sections omitted", () => {
    const { container } = render(<ExecutiveReportPage analysis={{ analysis_id: "empty-case" }} />);
    expect(container.querySelector('[data-report-section="cover"]')).toBeTruthy();
    expect(container.querySelector('[data-report-section="executive-summary"]')).toBeNull();
    expect(container.querySelector('[data-report-section="interpretation"]')).toBeNull();
    expect(container.querySelector('[data-report-section="action-plan"]')).toBeNull();
    expect(container.querySelector('[data-report-section="luck"]')).toBeNull();
    expect(container.querySelector('[data-report-section="key-findings"]')).toBeNull();
    expect(container.textContent).not.toContain("Không có trong Presentation");
  });

  it("R6 No internal ids/debug exposed", () => {
    const html = renderReport().container.textContent || "";
    for (const leak of FORBIDDEN) {
      expect(html).not.toContain(leak);
    }
  });

  it("R7 Report order follows approved architecture", () => {
    const { container } = renderReport();
    const order = [...container.querySelectorAll("[data-report-section]")].map((node) =>
      node.getAttribute("data-report-section"),
    );
    expect(order).toEqual([
      "cover",
      "identity",
      "executive-summary",
      "chart-snapshot",
      "key-findings",
      "interpretation",
      "action-plan",
      "luck",
      "supporting",
      "appendix",
    ]);
  });

  it("R8 Executive and detailed levels are distinct", () => {
    const { container } = renderReport();
    expect(container.querySelector('[data-report-section="cover"]')?.getAttribute("data-report-level")).toBe(
      "executive",
    );
    expect(
      container.querySelector('[data-report-section="executive-summary"]')?.getAttribute("data-report-level"),
    ).toBe("executive");
    expect(container.querySelector("[data-consulting-flow]")?.getAttribute("data-report-level")).toBe(
      "executive",
    );
    expect(container.querySelector("[data-action-priority-title]")?.getAttribute("data-report-level")).toBe(
      "executive",
    );
    expect(container.querySelector(".bte-er__detail")?.getAttribute("data-report-level")).toBe("detailed");
    expect(
      container.querySelector('[data-report-section="supporting"]')?.getAttribute("data-report-level"),
    ).toBe("detailed");
    expect(container.querySelector('[data-report-section="appendix"]')?.getAttribute("data-report-level")).toBe(
      "reference",
    );
  });

  it("R9 UI-15 visualizations reused", () => {
    const { container } = renderReport();
    expect(container.querySelector('[data-viz="balance-bars"]')).toBeTruthy();
    expect(container.querySelector('[data-viz="timeline"]')).toBeTruthy();
    expect(container.querySelector('[data-viz="formation-flow"]')).toBeTruthy();
    expect(container.querySelector('[data-viz="structure"]')).toBeTruthy();
    expect(container.querySelector('[data-viz="relationship"]')).toBeTruthy();
    expect(container.querySelector('[data-viz="grouped-chips"]')).toBeTruthy();
  });

  it("R10 No Dashboard DOM/layout dependency", () => {
    expect(PAGE_SRC).not.toMatch(/bte-cdash|DashboardGrid|CommercialDashboardPage|commercial-dashboard\.css/);
    const { container } = renderReport();
    expect(container.querySelector(".bte-cdash")).toBeNull();
    expect(container.querySelector("[data-dashboard]")).toBeNull();
    expect(container.querySelector(".bte-er")).toBeTruthy();
  });

  it("R11 Print page-break rules exist", () => {
    expect(CSS).toMatch(/@page\s*\{[^}]*size:\s*A4 portrait/);
    expect(CSS).toContain("page-break-after: always");
    expect(CSS).toContain("page-break-inside: avoid");
    expect(CSS).toContain("break-inside: avoid");
    expect(CSS).toMatch(/margin:\s*18mm/);
  });

  it("R12 No production PDF switch", () => {
    expect(APP_PY).toMatch(/@app\.get\("\/reports"[\s\S]*return page\("reports", "reports\.html"\)/);
    expect(APP_PY).toContain("/report-preview");
    expect(PAGE_SRC).not.toContain("fullReportViewModel");
    expect(PAGE_SRC).not.toContain("customerExport");
    expect(RESULT_APP).toContain("ExecutiveReportPage");
    expect(renderReport().container.querySelector("[data-pdf-export]")?.getAttribute("data-pdf-export")).toBe(
      "false",
    );
  });

  it("R13 No Runtime changes", () => {
    expect(MODEL_SRC).not.toMatch(/engines\.|narrative_v2\.runtime|run_narrative/);
    expect(PAGE_SRC).not.toMatch(/engines\./);
  });

  it("R14 No Narrative changes", () => {
    expect(MODEL_SRC).toContain("adaptNarrativeV2Presentation");
    expect(containerText(renderReport().container, "interpretation")).toContain(CONSULTING);
  });

  it("R15 No Presentation changes", () => {
    const { container } = renderReport();
    expect(container.querySelector("[data-report-overview='headline']")?.textContent).toBe(HEADLINE);
    expect(container.querySelector("[data-report-overview='summary']")?.textContent).toBe(SUMMARY);
    expect(container.querySelector("[data-presentation-version]")?.textContent).toBe("bte.presentation.v2.1");
  });

  it("formats published dates as DD/MM/YYYY without AM/PM", () => {
    const { container } = renderReport();
    expect(container.querySelector("[data-report-cover='birth']")?.textContent).toContain("21/01/1987");
    expect(container.querySelector("[data-report-cover='birth']")?.textContent).toContain("04:30");
    expect(container.textContent).not.toMatch(/\bAM\b|\bPM\b/);
  });
});

function containerText(container: HTMLElement, section: string): string {
  return container.querySelector(`[data-report-section="${section}"]`)?.textContent || "";
}
