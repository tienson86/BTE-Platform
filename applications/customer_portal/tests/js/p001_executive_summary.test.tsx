/**
 * P-001 Executive Summary completion on Overview Hero.
 * Presentation of published fields only. No Runtime / Narrative / contract edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { CommercialDashboardPage } from "../../src/screens/commercial_dashboard";
import { adaptNarrativeV2Presentation } from "../../src/adapters/narrativeV2PresentationAdapter";
import { selectNarrativePresentation } from "../../src/resultState/narrativePresentationSelection";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const REPO = resolve(PORTAL, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");

const PRESENTATION = JSON.parse(
  readFileSync(resolve(REPO, "implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json"), "utf8"),
) as {
  overview: { headline: string; summary: string; identity: null; balance: null; conclusion: null };
  interpretation: { consulting_flow: string };
};

const HEADLINE = PRESENTATION.overview.headline;
const SUMMARY = PRESENTATION.overview.summary;
const CONSULTING = PRESENTATION.interpretation.consulting_flow;
const HY_INCOMPLETE = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng";

const CASE_0001 = {
  analysis_id: "ana-p001-0001",
  identity: {
    person: { full_name: "Nguyễn Tiến Sơn", gender: "male", solar_birth: "1987-01-21" },
  },
  bazi: { day_master: "Canh", day_master_element: "Kim" },
  strength: { strength_level: "strong" },
  pattern: { cach_cuc: "Chính Ấn" },
  useful_god: {
    useful_display: "Thủy · Nhâm · Thực Thần",
    favorable_display: HY_INCOMPLETE,
    unfavorable_display: "Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài",
  },
  narrative_v2_shadow: {
    status: "ok",
    presentation: PRESENTATION,
    error: null,
  },
} as AnalysisDataDto;

afterEach(cleanup);

describe("P-001 Executive Summary completion", () => {
  it("renders executive facts before Narrative on CASE-0001", () => {
    const selected = selectNarrativePresentation(CASE_0001, "v2");
    expect(selected.overview.identity.map((item) => item.label)).toEqual(["Nhật Chủ", "Thân", "Mệnh Cục"]);
    expect(selected.overview.identity.find((item) => item.key === "day-master")?.value).toBe("Canh Kim");
    expect(selected.overview.identity.find((item) => item.key === "strength")?.value).toBe("Thân vượng");
    expect(selected.overview.identity.find((item) => item.key === "pattern")?.value).toBe("Chính Ấn");
    expect(selected.overview.balance.map((item) => item.label)).toEqual(["Dụng Thần", "Kỵ Thần"]);
    expect(selected.overview.balance.find((item) => item.key === "useful-god")?.value).toBe(
      "Thủy · Nhâm · Thực Thần",
    );
    expect(selected.overview.balance.find((item) => item.key === "avoid-god")?.value).toBe(
      "Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài",
    );
    expect(selected.overview.insight).toBe(HEADLINE);
    expect(selected.overview.summary).toBe(SUMMARY);
    expect(selected.overview.insight).not.toContain(SUMMARY);
    expect(selected.interpretation.lead).toBe(CONSULTING);

    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const overview = container.querySelector('[data-card="overview"]');
    const order = [...(overview?.querySelectorAll("[data-overview-section], [data-evidence]") ?? [])].map(
      (node) => node.getAttribute("data-overview-section") || node.getAttribute("data-evidence"),
    );
    expect(order.slice(0, 8)).toEqual([
      "facts",
      "day-master",
      "strength",
      "pattern",
      "useful-god",
      "avoid-god",
      "insight",
      "summary",
    ]);
    expect(overview?.querySelector('[data-overview-section="insight"]')?.textContent).toBe(HEADLINE);
    expect(overview?.querySelector('[data-overview-section="summary"]')?.textContent).toBe(SUMMARY);
    expect(overview?.textContent).not.toContain(HY_INCOMPLETE);
    expect(container.querySelector("[data-int-lead='true']")?.textContent).toContain(CONSULTING);
  });

  it("omits unavailable executive fields and does not invent Useful God or Kỵ Thần", () => {
    const sparse = {
      ...CASE_0001,
      pattern: undefined,
      useful_god: { useful_display: "Chưa đủ căn cứ xác định Dụng thần tổng thể" },
    } as AnalysisDataDto;
    const selected = selectNarrativePresentation(sparse, "v2");
    expect(selected.overview.identity.map((item) => item.key)).toEqual(["day-master", "strength"]);
    expect(selected.overview.balance).toEqual([]);
    expect(selected.overview.insight).toBe(HEADLINE);
  });

  it("does not modify Runtime, Narrative, or Presentation contract", () => {
    const presentationAdapter = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    const selection = readFileSync(
      resolve(PORTAL, "src/resultState/narrativePresentationSelection.ts"),
      "utf8",
    );
    const overviewCard = readFileSync(resolve(ROOT, "OverviewCard.tsx"), "utf8");
    const overviewAdapter = readFileSync(resolve(ROOT, "overviewAdapter.ts"), "utf8");
    expect(presentationAdapter).not.toContain("adaptOverviewExecutiveFacts");
    expect(presentationAdapter).not.toContain("Mệnh Cục");
    expect(selection).not.toContain("engines.");
    expect(overviewCard).not.toContain("engines.");
    expect(overviewAdapter).not.toContain("engines.");
    expect(overviewAdapter).not.toMatch(/hy_than\s*\|\||pattern\.hy_than|dung_than\s*\|\|/);
    const view = adaptNarrativeV2Presentation(CASE_0001.narrative_v2_shadow);
    expect(view.overview?.headline).toBe(HEADLINE);
    expect(view.overview?.summary).toBe(SUMMARY);
    expect(view.interpretation?.consulting_flow).toBe(CONSULTING);
  });
});
