/**
 * UI-04 Card 01 Overview — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  CommercialDashboardPage,
  OVERVIEW_VISUAL_FIXTURE,
  adaptOverviewCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  bazi: { day_master: "Canh", day_master_element: "Kim" },
  strength: { strength_level: "strong", strength_score: 0.87 },
  pattern: { cach_cuc: "Chính Ấn" },
  useful_god: {
    useful_display: "Hỏa · Đinh · Chính Quan",
    unfavorable_display: "Canh, Tân",
    short_reason: "Lá số cần Hỏa để điều tiết khí hậu.",
  },
  temperature: { balancing_need: "warming", balancing_need_label: "Cần ôn ấm" },
} as AnalysisDataDto;

function renderLive() {
  return render(
    <CommercialDashboardPage
      analysis={LIVE_ANALYSIS}
      resultSource="current"
      layoutMode="live"
    />,
  );
}

afterEach(cleanup);

describe("UI-04 Overview card", () => {
  it("O1 replaces the Overview skeleton with the real Overview component", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-implemented")).toBe("overview");
    expect(overview?.getAttribute("data-skeleton")).toBeNull();
    expect(overview?.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("O2 keeps Overview span at 4/12", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-span")).toBe("4");
    expect(overview?.className).toMatch(/bte-cdash__card--span-4/);
  });

  it("O3 uses the customer title TỔNG QUAN LÁ SỐ", () => {
    renderLive();
    expect(screen.getByText("TỔNG QUAN LÁ SỐ")).toBeTruthy();
    expect(document.body.textContent).not.toMatch(/Executive Overview|Technical Summary/);
  });

  it("O4 has an Insight area", () => {
    const { container } = renderLive();
    const insight = container.querySelector('[data-overview-section="insight"]');
    expect(insight?.textContent).toMatch(/Thân vượng/);
    expect(insight?.textContent).toMatch(/Canh Kim/);
  });

  it("O5 supports exactly five canonical evidence concepts", () => {
    const { container } = renderLive();
    expect(container.querySelector('[data-evidence="day-master"]')?.textContent).toMatch(/Nhật Chủ/);
    expect(container.querySelector('[data-evidence="strength"]')?.textContent).toMatch(/Thân vượng/);
    expect(container.querySelector('[data-evidence="avoid-god"]')?.textContent).toMatch(/Kỵ Thần/);
    expect(container.querySelector('[data-evidence="useful-god"]')?.textContent).toMatch(/Dụng Thần/);
    expect(container.querySelector('[data-evidence="temperature"]')?.textContent).toMatch(/Cần ôn ấm/);
    expect(container.querySelectorAll("[data-evidence]")).toHaveLength(5);
    const overview = container.querySelector('[data-card="overview"]')?.textContent || "";
    expect(overview).not.toMatch(/Mệnh Cục/);
    expect(container.querySelector('[data-card="pattern"]')?.textContent).toMatch(/MỆNH CỤC/);
  });

  it("O6 has a Quick Conclusion area", () => {
    const { container } = renderLive();
    expect(container.querySelector('[data-overview-section="conclusion"]')?.textContent).toMatch(
      /Hỏa/,
    );
  });

  it("O7 has no chart in Overview", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.querySelector("svg")).toBeNull();
    expect(overview?.querySelector("canvas")).toBeNull();
    expect(overview?.querySelector("[data-chart]")).toBeNull();
  });

  it("O8 does not expose rule IDs, engine IDs, or raw enums", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]')?.textContent || "";
    expect(overview).not.toMatch(/strength_class|useful_god_code|pattern_id|temperature_state/);
    expect(overview).not.toMatch(/\bstrong\b|\bwarming\b|0\.87|87%/);
    expect(overview).not.toMatch(/str_|pat_|tmp_/);
  });

  it("O9 live values come from the canonical result payload", () => {
    const bound = adaptOverviewCard(LIVE_ANALYSIS);
    expect(bound.identity.find((item) => item.key === "day-master")?.value).toBe("Canh Kim");
    expect(bound.identity.find((item) => item.key === "strength")?.value).toBe("Thân vượng");
    expect(bound.identity.find((item) => item.key === "avoid-god")?.value).toBe("Canh · Tân");
    expect(bound.balance.find((item) => item.key === "useful-god")?.value).toBe(
      "Hỏa · Đinh · Chính Quan",
    );
    expect(bound.balance.find((item) => item.key === "temperature")?.value).toBe("Cần ôn ấm");
    const rebound = adaptOverviewCard({
      bazi: { day_master: "Ất", day_master_element: "Mộc" },
      strength: { strength_level: "weak" },
      pattern: { cach_cuc: "Thương Quan" },
    });
    expect(rebound.identity.find((item) => item.key === "day-master")?.value).toBe("Ất Mộc");
    expect(rebound.identity.find((item) => item.key === "strength")?.value).toBe("Thân nhược");
  });

  it("O10 does not call engines from Overview", () => {
    const adapter = readFileSync(resolve(ROOT, "overviewAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "OverviewCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/engines\./);
    expect(card).not.toMatch(/engines\./);
    expect(adapter).not.toContain("Nguyễn Tiến Sơn");
    expect(adapter).not.toContain("CASE-0001");
  });

  it("O11 missing values fail cleanly", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={{}} resultSource="current" layoutMode="live" />,
    );
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.textContent).not.toMatch(/undefined|null|NaN/);
    expect(overview?.querySelector("[data-overview-empty]")?.textContent).toBe("Chưa đủ dữ liệu");
    expect(overview?.querySelectorAll("[data-evidence]")).toHaveLength(0);
  });

  it("O12 leaves other Card skeletons unchanged", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual([]);
  });

  it("O13 keeps the canonical grid spans", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("O14 preserves mobile semantic order", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    const order = [...(overview?.querySelectorAll("[data-overview-section], [data-evidence]") ?? [])]
      .map((node) => node.getAttribute("data-overview-section") || node.getAttribute("data-evidence"));
    expect(order).toEqual([
      "insight",
      "identity",
      "day-master",
      "strength",
      "avoid-god",
      "balance",
      "useful-god",
      "temperature",
      "conclusion",
    ]);
  });

  it("O15 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: {
          useful_display: "Hỏa · Đinh · Chính Quan",
          short_reason: "Lá số cần Hỏa để điều tiết khí hậu.",
        },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.bazi?.day_master).toBe("Canh");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(container.querySelector('[data-layout="visual"]')).toBeTruthy();
    expect(screen.getByText(OVERVIEW_VISUAL_FIXTURE.insight)).toBeTruthy();
    expect(adaptOverviewCard(LIVE_ANALYSIS).insight).not.toBe(OVERVIEW_VISUAL_FIXTURE.insight);
    const fixture = readFileSync(resolve(ROOT, "overviewFixture.ts"), "utf8");
    const adapter = readFileSync(resolve(ROOT, "overviewAdapter.ts"), "utf8");
    expect(fixture).toContain("visual-fixture");
    expect(adapter).not.toContain("có nội lực tốt");
  });
});
