/**
 * P-004R Life Consulting live runtime integration.
 * Mounting / ResultStore bind only. No new copy, Narrative, or Presentation edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  LIFE_CONSULTING_VISUAL_FIXTURE,
  adaptLifeConsulting,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");
const MOBILE_CSS = readFileSync(resolve(ROOT, "mobile/mobileExperience.css"), "utf8");
const PAGE = readFileSync(resolve(ROOT, "CommercialDashboardPage.tsx"), "utf8");

const LIVE_STORE = {
  analysis_id: "ana-p004r-0001",
  source: "current",
  input: {
    year: 1987,
    month: 1,
    day: 21,
    hour: 4,
    minute: 30,
    gender: "male",
    full_name: "Nguyễn Tiến Sơn",
  },
  data: {
    analysis_id: "ana-p004r-0001",
    calendar: { calendar_rule_version: "G1-10C" },
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
        { pillar: "year", ten_god: "Thất Sát" },
        { pillar: "month", ten_god: "Kiếp Tài" },
        { pillar: "day", ten_god: "Nhật Chủ" },
        { pillar: "hour", ten_god: "Thiên Ấn" },
      ],
      hidden: [
        { pillar: "year", ten_god: "Thiên Tài" },
        { pillar: "month", ten_god: "Chính Ấn" },
      ],
      visible_labels: ["Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"],
    },
    pattern: { cach_cuc: "Chính Ấn" },
    strength: { strength_level: "strong" },
    useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
    useful_god: { useful_display: "Thủy · Nhâm · Thực Thần" },
    luck: { current_cycle: { gan_zhi: "Nhâm Ngọ", year_start: 2024, year_end: 2033 } },
  } as AnalysisDataDto,
};

afterEach(cleanup);

describe("P-004R Life Consulting live runtime integration", () => {
  it("R1 mounts LifeConsultingSection on the production result grid", () => {
    const boot = resolveResultBoot(LIVE_STORE, "");
    const { container } = render(
      <CommercialDashboardPage
        analysis={boot.analysis}
        request={boot.request}
        resultSource={boot.resultSource}
        layoutMode={boot.layoutMode}
      />,
    );
    const section = container.querySelector("[data-life-consulting]");
    const grid = container.querySelector("[data-dashboard-body='canonical-grid']");
    expect(boot.resultSource).toBe("current");
    expect(section).toBeTruthy();
    expect(grid?.contains(section)).toBe(true);
    expect(section?.getAttribute("data-card")).toBeNull();
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("R2 live /result does not depend on the visual fixture", () => {
    expect(PAGE).toMatch(/layoutMode === "visual"[\s\S]*LIFE_CONSULTING_VISUAL_FIXTURE/);
    expect(PAGE).toMatch(/adaptLifeConsulting\(analysis, \{ request \}\)/);
    const { container } = render(
      <CommercialDashboardPage
        analysis={{ pattern: { cach_cuc: "Chính Ấn" } } as AnalysisDataDto}
        resultSource="current"
        layoutMode="live"
      />,
    );
    const ids = [...container.querySelectorAll("[data-life-domain]")].map((node) =>
      node.getAttribute("data-life-domain"),
    );
    expect(ids).not.toEqual(LIFE_CONSULTING_VISUAL_FIXTURE.domains.map((item) => item.id));
    expect(ids).not.toContain("marriage");
    expect(ids).not.toContain("children");
    expect(ids.length).toBeGreaterThan(0);
  });

  it("R3 ResultStore payload reaches the adapter", () => {
    const boot = resolveResultBoot(LIVE_STORE, "");
    expect(boot.analysis?.ten_gods?.visible_labels).toContain("Thất Sát");
    expect(boot.analysis?.pattern).toEqual({ cach_cuc: "Chính Ấn" });
    const bound = adaptLifeConsulting(boot.analysis, { request: boot.request });
    expect(bound.domains.map((item) => item.id)).toEqual([
      "marriage",
      "children",
      "health",
      "career",
      "finance",
      "property",
    ]);
  });

  it("R4 and R5 render only domains with published evidence", () => {
    const partial = adaptLifeConsulting({
      ten_gods: { visible_labels: ["Thất Sát", "Thiên Ấn"] },
    } as AnalysisDataDto);
    expect(partial.available).toBe(true);
    expect(partial.domains.map((item) => item.id)).toEqual(["career"]);
    expect(partial.domains.map((item) => item.id)).not.toContain("children");
    const { container } = render(
      <CommercialDashboardPage
        analysis={{ ten_gods: { visible_labels: ["Thất Sát", "Thiên Ấn"] } } as AnalysisDataDto}
        resultSource="current"
        layoutMode="live"
      />,
    );
    expect([...container.querySelectorAll("[data-life-domain]")].map((node) => node.getAttribute("data-life-domain"))).toEqual(
      ["career"],
    );
    expect(container.querySelector("[data-life-consulting]")).toBeTruthy();
  });

  it("R6 R7 R8 do not change Narrative, Presentation, or astrology calculation", () => {
    const presentation = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    const selection = readFileSync(
      resolve(PORTAL, "src/resultState/narrativePresentationSelection.ts"),
      "utf8",
    );
    const adapter = readFileSync(resolve(ROOT, "lifeConsultingAdapter.ts"), "utf8");
    expect(presentation).not.toContain("adaptLifeConsulting");
    expect(presentation).not.toContain("LifeConsultingSection");
    expect(selection).not.toContain("adaptLifeConsulting");
    expect(adapter).not.toMatch(/engines\./);
    expect(adapter).not.toContain("CASE-0001");
  });

  it("R9 desktop visual order places Life Consulting after Overview", () => {
    expect(CSS).toMatch(/data-card="overview"][\s\S]*order:\s*10/);
    expect(CSS).toMatch(/\.bte-cdash__grid > \.bte-life[\s\S]*order:\s*15/);
    expect(CSS).toMatch(/data-card="interpretation"][\s\S]*order:\s*20/);
    const { container } = render(
      <CommercialDashboardPage
        analysis={LIVE_STORE.data}
        resultSource="current"
        layoutMode="live"
      />,
    );
    const grid = container.querySelector(".bte-cdash__grid");
    const overview = grid?.querySelector('[data-card="overview"]');
    const life = grid?.querySelector("[data-life-consulting]");
    expect(overview).toBeTruthy();
    expect(life).toBeTruthy();
    expect(window.getComputedStyle(life as Element).order === "15" || CSS.includes("order: 15")).toBe(
      true,
    );
  });

  it("R10 mobile visual order keeps Life Consulting reachable after Overview", () => {
    expect(MOBILE_CSS).toMatch(/\[data-mobile-experience="true"\] \.bte-cdash__grid > \.bte-life/);
    expect(MOBILE_CSS).toMatch(/\.bte-cdash__grid > \.bte-life[\s\S]*order:\s*1/);
    const { container } = render(
      <CommercialDashboardPage
        analysis={LIVE_STORE.data}
        resultSource="current"
        layoutMode="live"
      />,
    );
    expect(container.querySelector("[data-life-consulting]")).toBeTruthy();
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-mobile-order")).toBe("1");
  });
});
