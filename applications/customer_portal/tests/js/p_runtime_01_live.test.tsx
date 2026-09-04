/**
 * P-RUNTIME-01 — production /result binding for P-001 → P-004.
 * Routing / mount / cache only. No new consulting copy.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import { resolveResultSurface } from "../../src/resultState/narrativeV2Shadow";
import { resolveNarrativeProvider } from "../../src/resultState/narrativeProvider";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  LIFE_CONSULTING_VISUAL_FIXTURE,
  OVERVIEW_VISUAL_FIXTURE,
  TEN_GODS_VISUAL_FIXTURE,
  adaptLifeConsulting,
  adaptOverviewExecutiveFacts,
  adaptTenGodsCard,
  tenGodCombinationAsset,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const HY_INCOMPLETE = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";
const LEAK = /Traceback|stack trace|rule_id|source_unit|pipeline_trace|engine_id|schema_version/i;

const PAGE = readFileSync(resolve(ROOT, "CommercialDashboardPage.tsx"), "utf8");
const GRID = readFileSync(resolve(ROOT, "DashboardGrid.tsx"), "utf8");
const ENTRY = readFileSync(resolve(PORTAL, "src/entries/resultApp.tsx"), "utf8");
const HTML = readFileSync(resolve(PORTAL, "templates/result_desktop.html"), "utf8");
const STORE = readFileSync(resolve(PORTAL, "static/js/result_store.js"), "utf8");
const ANALYZE = readFileSync(resolve(PORTAL, "static/js/analyze.js"), "utf8");
const CSS = readFileSync(resolve(ROOT, "commercial-dashboard.css"), "utf8");

const CASE_0001 = {
  analysis_id: "ana-pruntime01-0001",
  calendar: { calendar_rule_version: "G1-10C" },
  identity: {
    person: { full_name: "Nguyễn Tiến Sơn", gender: "male", solar_birth: "1987-01-21" },
  },
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
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
  pattern: { cach_cuc: "Chính Ấn" },
  strength: { strength_level: "strong" },
  useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
  useful_god: {
    useful_display: "Hỏa · Đinh · Chính Quan",
    favorable_display: HY_INCOMPLETE,
    unfavorable_display: "Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài",
  },
  can_xuong: {
    total_weight: 47,
    display_weight: "4 lượng 7 chỉ",
    classification: "Thượng cách",
    summary: "Tài lộc khá · hậu vận thuận",
    interpretation: "Luận giải chi tiết canonical.",
  },
  narrative_v2_shadow: {
    status: "ok",
    presentation: {
      metadata: { version: "bte.presentation.v2.1" },
      overview: {
        headline: "Headline live",
        summary: "Summary live",
        conclusion: "Conclusion live",
      },
      interpretation: { consulting_flow: "Consulting live" },
      action_plan: { top_priority: { title: "Priority live", description: "Do this" } },
    },
  },
} as AnalysisDataDto;

const STORE_RECORD = {
  analysis_id: "ana-pruntime01-0001",
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
  data: CASE_0001,
};

afterEach(cleanup);

describe("P-RUNTIME-01 live /result integration", () => {
  it("LIVE-01 fresh Analyze stores canonical result", () => {
    expect(ANALYZE).toContain('BtePortal.post("/api/v1/analyze"');
    expect(ANALYZE).toContain("saveLastResult");
    expect(ANALYZE).toContain('window.location.assign("/result")');
    expect(STORE).toContain('const LAST_KEY = "bte_last_result"');
    expect(STORE).toContain("function save(");
    const boot = resolveResultBoot(STORE_RECORD, "");
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.bazi?.day_master).toBe("Canh");
    expect(boot.analysis?.useful_god?.useful_display).toBe("Hỏa · Đinh · Chính Quan");
    expect(boot.analysis?.calendar).toEqual({ calendar_rule_version: "G1-10C" });
  });

  it("LIVE-02 /result loads fresh current result", () => {
    expect(ENTRY).toContain("CommercialDashboardPage");
    expect(ENTRY).toContain("resolveForDisplay");
    expect(HTML).toContain("/static/dist/result.js?v=PRUNTIME01");
    expect(HTML).toContain("/static/dist/result.css?v=PRUNTIME01");
    expect(resolveResultSurface("", "/result")).toBe("production");
    const boot = resolveResultBoot(STORE_RECORD, "");
    const { container } = render(
      <CommercialDashboardPage
        analysis={boot.analysis}
        request={boot.request}
        resultSource={boot.resultSource}
        layoutMode={boot.layoutMode}
      />,
    );
    expect(container.querySelector("[data-dashboard='commercial-v1']")).toBeTruthy();
    expect(container.querySelector("[data-narrative-surface='production']")).toBeTruthy();
  });

  it("LIVE-03 P-001 executive facts visible", () => {
    const facts = adaptOverviewExecutiveFacts(CASE_0001);
    expect(facts.identity.map((item) => item.label)).toEqual(["Nhật Chủ", "Thân", "Mệnh Cục"]);
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.querySelector('[data-evidence="day-master"]')?.textContent).toMatch(/Nhật Chủ/);
    expect(overview?.querySelector('[data-evidence="strength"]')?.textContent).toMatch(/Thân/);
    expect(overview?.querySelector('[data-evidence="pattern"]')?.textContent).toMatch(/Mệnh Cục/);
    const order = [...(overview?.querySelectorAll("[data-overview-section], [data-evidence]") ?? [])].map(
      (node) => node.getAttribute("data-overview-section") || node.getAttribute("data-evidence"),
    );
    expect(order.slice(0, 4)).toEqual(["facts", "day-master", "strength", "pattern"]);
    expect(overview?.querySelector('[data-overview-section="insight"]')?.textContent).toBe("Headline live");
  });

  it("LIVE-04 Useful God visible when published", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector('[data-evidence="useful-god"]')?.textContent).toContain("Dụng Thần");
    expect(container.querySelector('[data-evidence="useful-god"]')?.textContent).toContain(
      "Hỏa · Đinh · Chính Quan",
    );
  });

  it("LIVE-05 Unfavorable/Kỵ visible when published", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector('[data-evidence="avoid-god"]')?.textContent).toContain("Kỵ Thần");
    expect(container.querySelector('[data-evidence="avoid-god"]')?.textContent).toContain("Tỷ Kiên");
  });

  it("LIVE-06 missing Hỷ does not suppress other executive facts", () => {
    const facts = adaptOverviewExecutiveFacts(CASE_0001);
    expect(facts.balance.map((item) => item.key)).toEqual(["useful-god", "avoid-god"]);
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector('[data-evidence="favorable-god"]')).toBeNull();
    expect(container.textContent).not.toContain(HY_INCOMPLETE);
    expect(container.querySelector('[data-evidence="useful-god"]')).toBeTruthy();
    expect(container.querySelector('[data-evidence="avoid-god"]')).toBeTruthy();
    expect(container.querySelector('[data-evidence="day-master"]')).toBeTruthy();
  });

  it("LIVE-07 P-003 visible Ten Gods consulting renders", () => {
    const bound = adaptTenGodsCard(CASE_0001);
    expect(bound.commercial.map((item) => item.name)).toEqual(["Thất Sát", "Kiếp Tài", "Thiên Ấn"]);
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const card = container.querySelector('[data-card="ten-gods"]');
    expect(card?.querySelector('[data-tg-section="commercial"]')).toBeTruthy();
    expect(card?.querySelector('[data-tg-commercial="Thất Sát"]')?.textContent).toContain("Năng lực");
    expect(card?.querySelector('[data-tg-commercial="Thất Sát"]')?.textContent).toContain("Thu nhập");
    expect(card?.querySelector('[data-tg-commercial="Thất Sát"]')?.textContent).toContain("Công việc");
    expect(card?.querySelector('[data-tg-commercial="Nhật Chủ"]')).toBeNull();
  });

  it("LIVE-08 P-003B supported combination renders", () => {
    const bound = adaptTenGodsCard(CASE_0001);
    expect(bound.combination?.members).toEqual(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
    expect(bound.combination?.title).toBe(
      tenGodCombinationAsset(["Kiếp Tài", "Thất Sát", "Thiên Ấn"])?.title,
    );
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector("[data-tg-combination]")).toBeTruthy();
    expect(container.querySelector("[data-tg-combination]")?.textContent).toContain(
      bound.combination?.title ?? "",
    );
  });

  it("LIVE-09 deferred combination does not invent copy", () => {
    const deferred = {
      ten_gods: {
        visible: [
          { pillar: "year", ten_god: "Tỷ Kiên" },
          { pillar: "month", ten_god: "Thương Quan" },
          { pillar: "day", ten_god: "Nhật Chủ" },
        ],
      },
    } as AnalysisDataDto;
    expect(tenGodCombinationAsset(["Tỷ Kiên", "Thương Quan"])).toBeNull();
    const bound = adaptTenGodsCard(deferred);
    expect(bound.combination).toBeNull();
    const { container } = render(
      <CommercialDashboardPage analysis={deferred} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector("[data-tg-combination]")).toBeNull();
    expect(container.querySelector('[data-tg-section="commercial"]')).toBeTruthy();
  });

  it("LIVE-10 P-004 Life Consulting mounts", () => {
    expect(GRID).toContain("LifeConsultingSection");
    expect(PAGE).toContain("adaptLifeConsulting(analysis, { request })");
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const section = container.querySelector("[data-life-consulting]");
    expect(section).toBeTruthy();
    expect(section?.getAttribute("data-card")).toBeNull();
    expect(container.querySelector("[data-dashboard-body='canonical-grid']")?.contains(section)).toBe(
      true,
    );
  });

  it("LIVE-11 partial P-004 domains render independently", () => {
    const partial = {
      ten_gods: { visible_labels: ["Thất Sát", "Thiên Ấn"] },
    } as AnalysisDataDto;
    const bound = adaptLifeConsulting(partial);
    expect(bound.available).toBe(true);
    expect(bound.domains.map((item) => item.id)).toEqual(["career"]);
    const { container } = render(
      <CommercialDashboardPage analysis={partial} resultSource="current" layoutMode="live" />,
    );
    expect([...container.querySelectorAll("[data-life-domain]")].map((node) => node.getAttribute("data-life-domain"))).toEqual(
      ["career"],
    );
    expect(container.querySelector("[data-life-consulting]")).toBeTruthy();
  });

  it("LIVE-12 Cân Xương is not duplicated", () => {
    expect(PAGE).not.toContain("CanXuongDetail");
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelectorAll("#sec-can-xuong")).toHaveLength(1);
    expect(container.querySelectorAll('[data-can-xuong="summary"]')).toHaveLength(1);
    expect(container.querySelectorAll("[data-module='bone-weight-detail']")).toHaveLength(1);
    expect(container.querySelector(".bte-id__cx-link")).toBeNull();
    const titles = [...container.querySelectorAll(".bte-id__region-label, .bte-id__cx-detail-title")]
      .map((node) => node.textContent?.trim())
      .filter((text) => text === "Cân Xương Đoán Mệnh");
    expect(titles).toEqual(["Cân Xương Đoán Mệnh"]);
  });

  it("LIVE-13 no preview fixture dependency", () => {
    expect(PAGE).toContain("OVERVIEW_VISUAL_FIXTURE");
    expect(PAGE).toContain("selectNarrativePresentation");
    expect(PAGE).toContain("adaptLifeConsulting(analysis, { request })");
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector('[data-overview-section="insight"]')?.textContent).not.toBe(
      OVERVIEW_VISUAL_FIXTURE.insight,
    );
    expect(
      [...container.querySelectorAll("[data-tg-commercial]")].map((node) => node.getAttribute("data-tg-commercial")),
    ).not.toEqual(TEN_GODS_VISUAL_FIXTURE.commercial.map((item) => item.name));
    expect(
      [...container.querySelectorAll("[data-life-domain]")].map((node) => node.getAttribute("data-life-domain")),
    ).not.toEqual(LIFE_CONSULTING_VISUAL_FIXTURE.domains.map((item) => item.id));
  });

  it("LIVE-14 no stale Pack05 customer routing", () => {
    expect(resolveNarrativeProvider("?provider=pack05")).toBe("v2");
    expect(resolveResultSurface("?provider=pack05", "/result")).toBe("production");
    expect(HTML).not.toContain("result_legacy.html");
    expect(ENTRY).toContain('surface !== "production"');
    expect(ENTRY).toContain("CommercialDashboardPage");
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector("[data-narrative-provider='v2']")).toBeTruthy();
    expect(container.querySelector("[data-narrative-provider='pack05']")).toBeNull();
  });

  it("LIVE-15 no internal debug leakage", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    expect(container.textContent).not.toMatch(LEAK);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("LIVE-16 mobile has the same Product Ticket content", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const root = container.querySelector("[data-mobile-experience='true']");
    expect(root).toBeTruthy();
    expect(root?.querySelector("[data-overview-section='facts']")).toBeTruthy();
    expect(root?.querySelector("[data-tg-section='commercial']")).toBeTruthy();
    expect(root?.querySelector("[data-tg-combination]")).toBeTruthy();
    expect(root?.querySelector("[data-life-consulting]")).toBeTruthy();
    expect(CSS).toMatch(/data-card="overview"] \{ order: 30; \}/);
    expect(CSS).toMatch(/\.bte-cdash__grid > \.bte-life[\s\S]*order:\s*40/);
    expect(CSS).toMatch(/data-card="ten-gods"] \{ order: 50; \}/);
  });
});
