/**
 * P-003B.1 High-value Ten Gods combination library.
 * Customer assets only. No Runtime / calculation / Presentation contract edits.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  TEN_GODS_VISUAL_FIXTURE,
  adaptTenGodsCard,
  listTenGodCombinationCatalog,
  tenGodCombinationAsset,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const ASSETS = readFileSync(resolve(ROOT, "tenGodsCombinationAssets.ts"), "utf8");

const CASE_0001 = {
  analysis_id: "ana-p003b1-0001",
  identity: {
    person: { full_name: "Nguyễn Tiến Sơn", gender: "male", solar_birth: "1987-01-21" },
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
  },
} as AnalysisDataDto;

const CASE_0002 = {
  analysis_id: "ana-p003b1-0002",
  identity: {
    person: { full_name: "Hoàng Thị Thu Phương", gender: "female", solar_birth: "1997-07-01" },
  },
  ten_gods: {
    visible: [
      { pillar: "year", stem: "Đinh", ten_god: "Thương Quan" },
      { pillar: "month", stem: "Bính", ten_god: "Thực Thần" },
      { pillar: "day", stem: "Giáp", ten_god: "Nhật Chủ" },
      { pillar: "hour", stem: "Tân", ten_god: "Chính Quan" },
    ],
    hidden: [
      { pillar: "year", hidden_stem: "Kỷ", ten_god: "Chính Tài" },
      { pillar: "year", hidden_stem: "Quý", ten_god: "Chính Ấn" },
    ],
  },
} as AnalysisDataDto;

const FIXTURE_L08_002 = {
  ten_gods: {
    visible: [
      { pillar: "year", ten_god: "Kiếp Tài" },
      { pillar: "month", ten_god: "Thất Sát" },
      { pillar: "day", ten_god: "Nhật Chủ" },
      { pillar: "hour", ten_god: "Chính Tài" },
    ],
  },
} as AnalysisDataDto;

const FIXTURE_L08_003 = {
  ten_gods: {
    visible: [
      { pillar: "year", ten_god: "Thương Quan" },
      { pillar: "month", ten_god: "Thực Thần" },
      { pillar: "day", ten_god: "Nhật Chủ" },
      { pillar: "hour", ten_god: "Thực Thần" },
    ],
  },
} as AnalysisDataDto;

const FIXTURE_L08_004 = {
  ten_gods: {
    visible: [
      { pillar: "year", ten_god: "Chính Tài" },
      { pillar: "month", ten_god: "Thực Thần" },
      { pillar: "day", ten_god: "Nhật Chủ" },
      { pillar: "hour", ten_god: "Kiếp Tài" },
    ],
  },
} as AnalysisDataDto;

const FIXTURE_L08_005 = {
  ten_gods: {
    visible: [
      { pillar: "year", ten_god: "Tỷ Kiên" },
      { pillar: "month", ten_god: "Kiếp Tài" },
      { pillar: "day", ten_god: "Nhật Chủ" },
      { pillar: "hour", ten_god: "Thiên Tài" },
    ],
  },
} as AnalysisDataDto;

const REQUESTED_PAIRS: readonly (readonly string[])[] = [
  ["Chính Tài", "Chính Quan"],
  ["Chính Tài", "Chính Ấn"],
  ["Chính Tài", "Thực Thần"],
  ["Thiên Tài", "Thực Thần"],
  ["Thiên Tài", "Thương Quan"],
  ["Thiên Tài", "Kiếp Tài"],
  ["Chính Quan", "Chính Ấn"],
  ["Thất Sát", "Thiên Ấn"],
  ["Thất Sát", "Kiếp Tài"],
  ["Thương Quan", "Kiếp Tài"],
  ["Tỷ Kiên", "Chính Tài"],
];

function renderedCombo(analysis: AnalysisDataDto): string {
  const { container } = render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
  return container.querySelector("[data-tg-combination]")?.textContent || "";
}

afterEach(cleanup);

describe("P-003B.1 high-value combination library", () => {
  it("ships 15–20 authored combinations with complete consulting fields", () => {
    const catalog = listTenGodCombinationCatalog();
    expect(catalog.length).toBeGreaterThanOrEqual(15);
    expect(catalog.length).toBeLessThanOrEqual(20);
    for (const entry of catalog) {
      const asset = tenGodCombinationAsset(entry.members);
      expect(asset?.title).toBeTruthy();
      expect(asset?.insight).toBeTruthy();
      expect(asset?.capability).toBeTruthy();
      expect(asset?.income).toBeTruthy();
      expect(asset?.career).toBeTruthy();
      expect(asset?.leadership).toBeTruthy();
      expect(asset?.growth).toBeTruthy();
      expect(asset?.risk).toBeTruthy();
      expect(asset?.recommendation).toBeTruthy();
      expect(asset?.title).not.toMatch(/\+|means|nghĩa là/i);
    }
  });

  it("covers the requested high-value pairs", () => {
    for (const members of REQUESTED_PAIRS) {
      expect(tenGodCombinationAsset(members)?.members.length).toBeGreaterThanOrEqual(2);
    }
  });

  it("removes internal shorthand from combination copy", () => {
    expect(ASSETS).not.toMatch(/cửa/);
    expect(ASSETS).not.toMatch(/khung/);
    expect(ASSETS).not.toMatch(/lối/);
    expect(ASSETS).not.toMatch(/món/);
    expect(ASSETS).not.toContain("Bứt cửa hiểm bằng lối không theo khuôn");
    expect(ASSETS).not.toContain("Xử lý việc khó bằng cách linh hoạt và khác biệt");
  });

  it("does not promise wealth, rank, venture, marriage, or luck", () => {
    expect(ASSETS).not.toMatch(/đảm bảo|chắc chắn giàu|sẽ giàu|giàu chắc/i);
    expect(ASSETS).not.toMatch(/lãnh đạo|quyền lực|khởi nghiệp|doanh nhân/i);
    expect(ASSETS).not.toMatch(/kết hôn|hôn nhân|vận may|\bHung\b|\bCát\b|\bTốt\b|\bXấu\b/);
    expect(ASSETS).not.toMatch(/Phù hợp làm|Giỏi tài chính|giỏi kiếm tiền|thông minh|nghiên cứu/);
  });

  it("binds CASE-0001 and CASE-0002 from published visible names", () => {
    const one = adaptTenGodsCard(CASE_0001);
    expect(one.combination?.members).toEqual(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
    expect(one.combination?.title).toBe("Gánh việc khó theo cách linh hoạt, có điểm dừng");
    expect(one.hiddenSupport).toMatch(/nền tảng/);

    const two = adaptTenGodsCard(CASE_0002);
    expect(two.combination?.members).toEqual(["Thực Thần", "Thương Quan", "Chính Quan"]);
    expect(two.combination?.title).toBe("Ra sản phẩm, phản biện, vẫn chạy được trong tổ chức");
    expect(two.combination?.members).not.toContain("Nhật Chủ");

    expect(renderedCombo(CASE_0001)).toContain(one.combination?.title ?? "");
    expect(renderedCombo(CASE_0002)).toContain(two.combination?.title ?? "");
  });

  it("binds distinct existing fixtures to different catalog entries", () => {
    expect(adaptTenGodsCard(FIXTURE_L08_002).combination?.members).toEqual(["Kiếp Tài", "Thất Sát"]);
    expect(adaptTenGodsCard(FIXTURE_L08_003).combination?.members).toEqual(["Thực Thần", "Thương Quan"]);
    expect(adaptTenGodsCard(FIXTURE_L08_004).combination?.members).toEqual(["Thực Thần", "Chính Tài"]);
    expect(adaptTenGodsCard(FIXTURE_L08_005).combination?.members).toEqual(["Kiếp Tài", "Thiên Tài"]);
    expect(TEN_GODS_VISUAL_FIXTURE.combination?.members).toEqual(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
  });

  it("does not modify Runtime, calculation, or Presentation contract", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const presentation = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    expect(adapter).not.toMatch(/engines\./);
    expect(ASSETS).not.toMatch(/engines\./);
    expect(adapter).not.toMatch(/ten_god_name\(|map_stem_to_ten_god|LABEL_TO_GOD_ID/);
    expect(adapter).not.toContain("CASE-0001");
    expect(adapter).not.toContain("CASE-0002");
    expect(ASSETS).not.toContain("Nguyễn Tiến Sơn");
    expect(ASSETS).not.toContain("Hoàng Thị Thu Phương");
    expect(presentation).not.toContain("listTenGodCombinationCatalog");
    expect(presentation).not.toContain("tenGodsCombinationAssets");
  });
});
