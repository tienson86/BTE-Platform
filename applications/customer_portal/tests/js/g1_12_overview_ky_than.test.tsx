/**
 * G1-12 — Tổng Quan keeps Kỵ Thần and restores Mệnh Cục as a compact chip.
 * Dedicated Mệnh Cục card stays.
 */

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";

import { CommercialDashboardPage, adaptOverviewCard } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

afterEach(cleanup);

const LIVE = {
  bazi: { day_master: "Bính", day_master_element: "Hỏa" },
  strength: { strength_level: "balanced" },
  pattern: { cach_cuc: "Chính Tài" },
  useful_god: {
    useful_display: "Kim · Tân · Chính Tài",
    unfavorable_display: "Canh, Tân",
  },
  temperature: { balancing_need_label: "Cần ôn ấm" },
} as AnalysisDataDto;

describe("G1-12 Overview Kỵ Thần", () => {
  it("shows Kỵ Thần from canonical unfavorable_display and Mệnh Cục as a chip", () => {
    const bound = adaptOverviewCard(LIVE);
    expect(bound.identity.map((item) => item.label)).toEqual(["Nhật Chủ", "Thân", "Mệnh Cục"]);
    expect(bound.identity.find((item) => item.key === "pattern")?.value).toBe("Chính Tài");
    expect(bound.balance.map((item) => item.label)).toEqual(["Dụng Thần", "Kỵ Thần"]);
    expect(bound.balance.find((item) => item.key === "avoid-god")?.value).toBe("Canh · Tân");
    expect(bound.conclusion).toContain("Kỵ thần Canh · Tân");
    expect(bound.insight).not.toMatch(/Mệnh cục/i);
    expect(bound.conclusion).not.toMatch(/Mệnh cục/i);

    const { container } = render(
      <CommercialDashboardPage analysis={LIVE} resultSource="current" layoutMode="live" />,
    );
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.querySelector('[data-evidence="avoid-god"]')?.textContent).toMatch(/Kỵ Thần/);
    expect(overview?.querySelector('[data-evidence="avoid-god"]')?.textContent).toMatch(/Canh · Tân/);
    expect(overview?.querySelector('[data-evidence="pattern"]')?.textContent).toMatch(/Mệnh Cục/);
    expect(overview?.querySelector('[data-evidence="pattern"]')?.textContent).toMatch(/Chính Tài/);
    expect(overview?.querySelector('[data-overview-section="conclusion"]')?.textContent).toContain(
      "Kỵ thần Canh · Tân",
    );
  });

  it("keeps the dedicated MỆNH CỤC module unchanged", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={LIVE} resultSource="current" layoutMode="live" />,
    );
    const pattern = container.querySelector('[data-card="pattern"]');
    expect(pattern?.querySelector(".bte-cdash__card-title")?.textContent).toBe("MỆNH CỤC");
    expect(pattern?.querySelector("[data-pat-primary]")?.textContent).toBe("Chính Tài");
    expect(pattern?.querySelector("[data-pat-section='primary']")?.textContent).toMatch(/Mệnh Cục chính/);
  });
});
