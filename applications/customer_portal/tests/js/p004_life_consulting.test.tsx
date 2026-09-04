/**
 * P-004 Life Consulting Engine.
 * Customer assets only. No Runtime / calculation / Presentation contract edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  LIFE_DOMAIN_PROFILES,
  adaptLifeConsulting,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");

const ASTROLOGY_LEAK =
  /Thập Thần|Thần Sát|Dụng Thần|Nhật Chủ|Thiên Tài|Chính Tài|Thất Sát|Kiếp Tài|Thiên Ấn|Chính Ấn|Thực Thần|Thương Quan|Tỷ Kiên|Chính Quan/;
const SHORTHAND_LEAK = /cửa|khung|lối|món/;
const GUARANTEE_LEAK = /kết hôn chắc|chắc chắn sinh|phát tài|lãnh đạo|quyền lực|Phù hợp làm/;

const CASE_0001 = {
  analysis_id: "ana-p004-0001",
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
  useful_god: { useful_display: "Thủy · Nhâm · Thực Thần" },
  luck: { current_cycle: { gan_zhi: "Nhâm Ngọ", year_start: 2024, year_end: 2033 } },
} as AnalysisDataDto;

function copyBlob(item: {
  readonly insight: string;
  readonly tendency: string;
  readonly strength: string;
  readonly opportunity: string;
  readonly risk: string;
  readonly recommendation: string;
}): string {
  return [item.insight, item.tendency, item.strength, item.opportunity, item.risk, item.recommendation].join(
    " ",
  );
}

afterEach(cleanup);

describe("P-004 Life Consulting Engine", () => {
  it("binds six life domains from published CASE-0001 evidence", () => {
    const bound = adaptLifeConsulting(CASE_0001);
    expect(bound.available).toBe(true);
    expect(bound.domains.map((item) => item.id)).toEqual([
      "marriage",
      "children",
      "health",
      "career",
      "finance",
      "property",
    ]);
    expect(bound.domains.map((item) => item.title)).toEqual([
      "Hôn nhân",
      "Con cái",
      "Sức khỏe",
      "Sự nghiệp",
      "Tài chính",
      "Nhà đất",
    ]);
    for (const domain of bound.domains) {
      expect(domain.insight).toBeTruthy();
      expect(domain.tendency).toBeTruthy();
      expect(domain.strength).toBeTruthy();
      expect(domain.opportunity).toBeTruthy();
      expect(domain.risk).toBeTruthy();
      expect(domain.recommendation).toBeTruthy();
      expect(copyBlob(domain)).not.toMatch(ASTROLOGY_LEAK);
      expect(copyBlob(domain)).not.toMatch(GUARANTEE_LEAK);
    }

    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const section = container.querySelector("[data-life-consulting]");
    expect(section).toBeTruthy();
    expect(section?.getAttribute("data-card")).toBeNull();
    expect(container.querySelector(".bte-cdash__grid")?.contains(section)).toBe(true);
    expect(container.querySelector("[data-identity-header='true']")?.contains(section)).toBe(false);
    expect([...container.querySelectorAll("[data-life-domain]")].map((node) => node.getAttribute("data-life-domain"))).toEqual(
      ["marriage", "children", "health", "career", "finance", "property"],
    );
    const marriage = container.querySelector('[data-life-domain="marriage"]');
    const fields = [...(marriage?.querySelectorAll("[data-life-field]") ?? [])].map((node) =>
      node.getAttribute("data-life-field"),
    );
    expect(fields).toEqual(["insight", "tendency", "strength", "opportunity", "risk", "recommendation"]);
    expect(section?.textContent).not.toMatch(ASTROLOGY_LEAK);
    expect(DASHBOARD_CARDS.map((card) => card.span)).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
    expect([...container.querySelectorAll("[data-card]")].map((node) => Number(node.getAttribute("data-span")))).toEqual([
      4, 8, 4, 4, 4, 6, 6, 12, 12,
    ]);
  });

  it("omits a domain when published evidence is not enough", () => {
    const empty = adaptLifeConsulting({});
    expect(empty.available).toBe(false);
    expect(empty.domains).toEqual([]);
    const { container } = render(
      <CommercialDashboardPage analysis={{}} resultSource="current" layoutMode="live" />,
    );
    expect(container.querySelector("[data-life-consulting]")).toBeNull();

    const patternOnly = adaptLifeConsulting({ pattern: { cach_cuc: "Chính Ấn" } } as AnalysisDataDto);
    expect(patternOnly.domains.map((item) => item.id)).toEqual(["health", "career", "finance", "property"]);
    expect(patternOnly.domains.map((item) => item.id)).not.toContain("marriage");
    expect(patternOnly.domains.map((item) => item.id)).not.toContain("children");
  });

  it("looks up female partnership from published officer/pressure stars without listing them", () => {
    const female = adaptLifeConsulting({
      ...CASE_0001,
      identity: { person: { gender: "female" } },
    });
    const marriage = female.domains.find((item) => item.id === "marriage");
    expect(marriage?.title).toBe("Hôn nhân");
    expect(marriage?.insight).toMatch(/vai và chuẩn/);
    expect(copyBlob(marriage!)).not.toMatch(ASTROLOGY_LEAK);
  });

  it("keeps authored customer copy free of astrology labels and banned shorthand", () => {
    for (const profile of LIFE_DOMAIN_PROFILES) {
      const blob = copyBlob(profile);
      expect(blob).not.toMatch(ASTROLOGY_LEAK);
      expect(blob).not.toMatch(SHORTHAND_LEAK);
      expect(blob).not.toMatch(GUARANTEE_LEAK);
    }
  });

  it("does not modify Runtime, calculation, or Presentation contract", () => {
    const adapter = readFileSync(resolve(ROOT, "lifeConsultingAdapter.ts"), "utf8");
    const evidence = readFileSync(resolve(ROOT, "lifeConsultingEvidence.ts"), "utf8");
    const assets = readFileSync(resolve(ROOT, "lifeConsultingAssets.ts"), "utf8");
    const section = readFileSync(resolve(ROOT, "LifeConsultingSection.tsx"), "utf8");
    const presentation = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    expect(adapter).not.toMatch(/engines\./);
    expect(evidence).not.toMatch(/engines\./);
    expect(assets).not.toMatch(/engines\./);
    expect(section).not.toMatch(/engines\./);
    expect(adapter).not.toContain("CASE-0001");
    expect(evidence).not.toContain("CASE-0001");
    expect(assets).not.toContain("Nguyễn Tiến Sơn");
    expect(presentation).not.toContain("adaptLifeConsulting");
    expect(presentation).not.toContain("lifeConsultingAssets");
    expect(presentation).not.toContain("LifeConsultingSection");
  });
});
