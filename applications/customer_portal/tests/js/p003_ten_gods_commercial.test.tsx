/**
 * P-003 Ten Gods commercial interpretation.
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
  tenGodCommercialAsset,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");

const CASE_0001 = {
  analysis_id: "ana-p003-0001",
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

afterEach(cleanup);

describe("P-003 Ten Gods commercial interpretation", () => {
  it("binds consulting cards from published visible Ten Gods on CASE-0001", () => {
    const bound = adaptTenGodsCard(CASE_0001);
    expect(bound.commercial.map((item) => item.name)).toEqual(["Thất Sát", "Kiếp Tài", "Thiên Ấn"]);
    expect(bound.commercial.find((item) => item.name === "Nhật Chủ")).toBeUndefined();
    expect(bound.commercial.find((item) => item.name === "Thiên Tài")).toBeUndefined();
    for (const card of bound.commercial) {
      expect(card.insight).toBeTruthy();
      expect(card.capability).toBeTruthy();
      expect(card.income).toBeTruthy();
      expect(card.career).toBeTruthy();
      expect(card.risk).toBeTruthy();
      expect(card.recommendation).toBeTruthy();
      expect(card.insight).not.toMatch(/là quan hệ nhật chủ|represents/i);
    }

    const { container } = render(
      <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
    );
    const card = container.querySelector('[data-card="ten-gods"]');
    const names = [...(card?.querySelectorAll("[data-tg-commercial]") ?? [])].map((node) =>
      node.getAttribute("data-tg-commercial"),
    );
    expect(names).toEqual(["Thất Sát", "Kiếp Tài", "Thiên Ấn"]);
    expect(card?.querySelector('[data-tg-commercial="Thất Sát"] [data-tg-field="insight"]')?.textContent).toBe(
      tenGodCommercialAsset("Thất Sát")?.insight,
    );
    expect(card?.querySelector('[data-tg-section="hidden-summary"]')?.textContent).toMatch(/Thiên Tài/);
    expect(card?.querySelector('[data-tg-commercial="Thiên Tài"]')).toBeNull();
  });

  it("omits missing gods and does not invent a Useful God or hidden-equal card", () => {
    const sparse = adaptTenGodsCard({
      ten_gods: { visible: [{ pillar: "day", ten_god: "Nhật Chủ" }] },
    } as AnalysisDataDto);
    expect(sparse.commercial).toEqual([]);
    const unknown = tenGodCommercialAsset("Không Có");
    expect(unknown).toBeNull();
  });

  it("does not modify Runtime, calculation, or Presentation contract", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const assets = readFileSync(resolve(ROOT, "tenGodsCommercialAssets.ts"), "utf8");
    const presentation = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    expect(adapter).not.toMatch(/engines\./);
    expect(assets).not.toMatch(/engines\./);
    expect(adapter).not.toMatch(/ten_god_name\(|map_stem_to_ten_god|LABEL_TO_GOD_ID/);
    expect(adapter).not.toContain("CASE-0001");
    expect(assets).not.toContain("Nguyễn Tiến Sơn");
    expect(presentation).not.toContain("tenGodCommercialAsset");
  });
});
