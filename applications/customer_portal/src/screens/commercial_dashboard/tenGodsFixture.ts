/**
 * Phase A visual fixture for Ten Gods. Not production content.
 */

import { TEN_GODS_TITLE } from "./cards";
import { tenGodCommercialAsset } from "./tenGodsCommercialAssets";
import {
  tenGodCombinationAsset,
  tenGodHiddenCombinationSupport,
} from "./tenGodsCombinationAssets";
import type { TenGodCombinationView, TenGodCommercialView, TenGodsView } from "./types";

function fixtureCombination(): TenGodCombinationView | null {
  const asset = tenGodCombinationAsset(["Thiên Ấn", "Thất Sát", "Kiếp Tài"]);
  if (!asset) return null;
  return {
    title: asset.title,
    members: asset.members,
    insight: asset.insight,
    capability: asset.capability,
    income: asset.income,
    career: asset.career,
    leadership: asset.leadership,
    growth: asset.growth,
    risk: asset.risk,
    recommendation: asset.recommendation,
  };
}

function fixtureCommercial(): readonly TenGodCommercialView[] {
  const names = [
    { name: "Thiên Ấn", pillarLabel: "Năm" },
    { name: "Thất Sát", pillarLabel: "Tháng" },
    { name: "Kiếp Tài", pillarLabel: "Giờ" },
  ] as const;
  return names.flatMap((row) => {
    const asset = tenGodCommercialAsset(row.name);
    if (!asset) return [];
    return [{ name: row.name, pillarLabel: row.pillarLabel, ...asset }];
  });
}

/** Deterministic sample structure. Not the production validation case. */
export const TEN_GODS_VISUAL_FIXTURE: TenGodsView = {
  title: TEN_GODS_TITLE,
  available: true,
  featured: ["Thiên Ấn", "Thất Sát", "Kiếp Tài"],
  visible: [
    { pillar: "year", pillarLabel: "Năm", stem: "Giáp", tenGod: "Thiên Ấn", isDayMaster: false },
    { pillar: "month", pillarLabel: "Tháng", stem: "Ất", tenGod: "Thất Sát", isDayMaster: false },
    { pillar: "day", pillarLabel: "Ngày", stem: "Mậu", tenGod: "Nhật Chủ", isDayMaster: true },
    { pillar: "hour", pillarLabel: "Giờ", stem: "Canh", tenGod: "Kiếp Tài", isDayMaster: false },
  ],
  hidden: [
    { pillar: "year", pillarLabel: "Năm", stem: "Quý", tenGod: "Chính Ấn", isDayMaster: false },
    { pillar: "month", pillarLabel: "Tháng", stem: "Giáp", tenGod: "Thiên Ấn", isDayMaster: false },
    { pillar: "hour", pillarLabel: "Giờ", stem: "Nhâm", tenGod: "Thiên Tài", isDayMaster: false },
  ],
  hiddenNames: ["Thiên Tài", "Thiên Ấn", "Chính Ấn"],
  distribution: [
    { name: "Kiếp Tài", visible: true, hidden: false },
    { name: "Thiên Tài", visible: false, hidden: true },
    { name: "Thất Sát", visible: true, hidden: false },
    { name: "Thiên Ấn", visible: true, hidden: true },
    { name: "Chính Ấn", visible: false, hidden: true },
  ],
  combination: fixtureCombination(),
  hiddenSupport: tenGodHiddenCombinationSupport(["Thiên Tài", "Chính Ấn"]),
  commercial: fixtureCommercial(),
  detailed: [],
  relations: [],
  ecosystem: null,
  summary: "",
};
