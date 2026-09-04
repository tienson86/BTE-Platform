/**
 * P-003B Ten Gods combination consulting model.
 * Customer assets only. No Runtime / calculation / Presentation contract edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  adaptTenGodsCard,
  tenGodCombinationAsset,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");

const CASE_0001 = {
  analysis_id: "ana-p003b-0001",
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
} as AnalysisDataDto;

function analysisWithVisible(names: readonly string[]): AnalysisDataDto {
  const pillars = ["year", "month", "day", "hour"] as const;
  return {
    ten_gods: {
      visible: names.map((ten_god, index) => ({
        pillar: pillars[index] ?? "hour",
        ten_god,
      })),
    },
  } as AnalysisDataDto;
}

afterEach(cleanup);

describe("P-003B Ten Gods combination consulting", () => {
  it("binds a business-model card from published visible Ten Gods on CASE-0001", () => {
    const bound = adaptTenGodsCard(CASE_0001);
    expect(bound.combination).not.toBeNull();
    expect(bound.combination?.members).toEqual(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
    expect(bound.combination?.members).not.toContain("Nhật Chủ");
    expect(bound.combination?.title).toBe(
      tenGodCombinationAsset(["Kiếp Tài", "Thất Sát", "Thiên Ấn"])?.title,
    );
    expect(bound.combination?.title).not.toMatch(/\+|means|nghĩa là/i);
    expect(bound.combination?.insight).toBeTruthy();
    expect(bound.combination?.capability).toBeTruthy();
    expect(bound.combination?.income).toBeTruthy();
    expect(bound.combination?.career).toBeTruthy();
    expect(bound.combination?.leadership).toBeTruthy();
    expect(bound.combination?.growth).toBeTruthy();
    expect(bound.combination?.risk).toBeTruthy();
    expect(bound.combination?.recommendation).toBeTruthy();
    expect(bound.hiddenSupport).toBeTruthy();
    expect(bound.commercial.map((item) => item.name)).toEqual(["Thất Sát", "Kiếp Tài", "Thiên Ấn"]);

    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const card = container.querySelector('[data-card="ten-gods"]');
    const combo = card?.querySelector("[data-tg-combination]");
    expect(combo).toBeTruthy();
    expect(combo?.querySelector("[data-tg-field='insight']")?.textContent).toBe(bound.combination?.insight);
    expect(combo?.textContent).not.toMatch(/means|nghĩa là/i);
    const sections = [...(card?.querySelectorAll("[data-tg-section]") ?? [])].map((node) =>
      node.getAttribute("data-tg-section"),
    );
    expect(sections.indexOf("combination")).toBeGreaterThanOrEqual(0);
    expect(sections.indexOf("combination")).toBeLessThan(sections.indexOf("commercial"));
    expect(card?.querySelector("[data-tg-combo-hidden]")?.textContent).toBe(bound.hiddenSupport);
  });

  it("looks up published pair patterns without calculating new gods", () => {
    const output = tenGodCombinationAsset(["Thiên Tài", "Thực Thần"]);
    expect(output?.title).toBe("Biến cơ hội không cố định thành sản phẩm có hạn");
    expect(output?.members).toEqual(["Thực Thần", "Thiên Tài"]);
    expect(tenGodCombinationAsset(["Thiên Tài", "Thương Quan"])?.title).toBe(
      "Sửa quy trình kém và mở kênh phụ",
    );
    expect(tenGodCombinationAsset(["Chính Quan", "Chính Ấn"])?.title).toBe(
      "Làm việc có chuẩn, có chỗ tích lũy trước khi bung",
    );
    expect(tenGodCombinationAsset(["Kiếp Tài", "Thất Sát"])?.title).toBe(
      "Chớp việc khó đúng lúc nguồn đang kẹt",
    );

    const pair = adaptTenGodsCard(analysisWithVisible(["Thiên Tài", "Thực Thần"]));
    expect(pair.combination?.title).toBe(output?.title);
    expect(pair.combination?.members).toEqual(["Thực Thần", "Thiên Tài"]);
  });

  it("omits combination when the published set has no asset", () => {
    const one = adaptTenGodsCard(analysisWithVisible(["Nhật Chủ"]));
    expect(one.combination).toBeNull();
    expect(one.hiddenSupport).toBe("");
    const unknown = adaptTenGodsCard(analysisWithVisible(["Tỷ Kiên", "Thiên Ấn"]));
    expect(unknown.combination).toBeNull();
    expect(tenGodCombinationAsset(["Không Có", "Thiên Tài"])).toBeNull();
  });

  it("does not modify Runtime, calculation, or Presentation contract", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const assets = readFileSync(resolve(ROOT, "tenGodsCombinationAssets.ts"), "utf8");
    const presentation = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    expect(adapter).not.toMatch(/engines\./);
    expect(assets).not.toMatch(/engines\./);
    expect(adapter).not.toMatch(/ten_god_name\(|map_stem_to_ten_god|LABEL_TO_GOD_ID/);
    expect(adapter).not.toContain("CASE-0001");
    expect(assets).not.toContain("Nguyễn Tiến Sơn");
    expect(presentation).not.toContain("tenGodCombinationAsset");
    expect(presentation).not.toContain("tenGodsCombinationAssets");
  });
});
