/**
 * P-003B.2 Ten Gods combination knowledge base V1.0.
 * Knowledge lookup only. No Runtime / adapter / calculation / Presentation edits.
 */

import { readdirSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup } from "@testing-library/react";
import {
  adaptTenGodsCard,
  classifyTenGodCombination,
  listTenGodCombinationCatalog,
  tenGodCombinationAsset,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";
import matrix from "../../../../knowledge/consulting/ten_gods/combinations/matrix.json";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORTAL = resolve(HERE, "../..");
const ROOT = resolve(PORTAL, "src/screens/commercial_dashboard");
const REPO = resolve(PORTAL, "../..");
const KNOWLEDGE = resolve(REPO, "knowledge/consulting/ten_gods/combinations");

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

const CASE_0001 = analysisWithVisible(["Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"]);
const CASE_0002 = analysisWithVisible(["Thương Quan", "Thực Thần", "Nhật Chủ", "Chính Quan"]);
const L08 = {
  case_001: analysisWithVisible(["Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"]),
  case_002: analysisWithVisible(["Kiếp Tài", "Thất Sát", "Nhật Chủ", "Chính Tài"]),
  case_003: analysisWithVisible(["Thương Quan", "Thực Thần", "Nhật Chủ", "Thực Thần"]),
  case_004: analysisWithVisible(["Chính Tài", "Thực Thần", "Nhật Chủ", "Kiếp Tài"]),
  case_005: analysisWithVisible(["Tỷ Kiên", "Kiếp Tài", "Nhật Chủ", "Thiên Tài"]),
  case_006: analysisWithVisible(["Chính Quan", "Chính Quan", "Nhật Chủ", "Kiếp Tài"]),
  case_007: analysisWithVisible(["Thất Sát", "Thương Quan", "Nhật Chủ", "Chính Tài"]),
  case_008: analysisWithVisible(["Thực Thần", "Thiên Ấn", "Nhật Chủ", "Kiếp Tài"]),
};

afterEach(cleanup);

describe("P-003B.2 combination knowledge base", () => {
  it("classifies all 45 visible pairs without inventing copy", () => {
    expect(matrix.pair_count).toBe(45);
    expect(matrix.pairs).toHaveLength(45);
    const counts: Record<string, number> = {};
    for (const row of matrix.pairs) {
      counts[row.status] = (counts[row.status] ?? 0) + 1;
      const classified = classifyTenGodCombination(row.members);
      expect(classified.status).toBe(row.status);
      if (row.status !== "SUPPORTED") {
        expect(tenGodCombinationAsset(row.members)).toBeNull();
      } else {
        expect(tenGodCombinationAsset(row.members)?.title).toBeTruthy();
      }
    }
    expect(counts).toEqual({
      SUPPORTED: 16,
      DEFERRED: 13,
      CONFLICTING: 12,
      LOW_VALUE: 2,
      NOT_CUSTOMER_SAFE: 2,
    });
  });

  it("looks up authored knowledge units only", () => {
    expect(listTenGodCombinationCatalog()).toHaveLength(18);
    const files = readdirSync(resolve(KNOWLEDGE, "supported")).filter((name) => name.endsWith(".json"));
    expect(files).toHaveLength(18);
    for (const file of files) {
      const unit = JSON.parse(readFileSync(resolve(KNOWLEDGE, "supported", file), "utf8")) as {
        members: string[];
        status: string;
        title: string;
        executive_insight: string;
        commercial_value: string;
        capability: string;
        income_model: string;
        career_model: string;
        management_style: string;
        growth_model: string;
        risk_model: string;
        recommendation: string;
        metadata: { version: string };
      };
      expect(unit.status).toBe("SUPPORTED");
      expect(unit.metadata.version).toBe("1.0.0");
      expect(tenGodCombinationAsset(unit.members)?.title).toBe(unit.title);
      expect(unit.executive_insight).toBeTruthy();
      expect(unit.commercial_value).toBeTruthy();
    }
  });

  it("omits unknown, conflicting, and deferred combinations", () => {
    expect(tenGodCombinationAsset(["Không Có", "Thiên Tài"])).toBeNull();
    expect(classifyTenGodCombination(["Không Có", "Thiên Tài"]).status).toBe("UNKNOWN");
    expect(adaptTenGodsCard(analysisWithVisible(["Tỷ Kiên", "Thiên Ấn"])).combination).toBeNull();
    expect(classifyTenGodCombination(["Tỷ Kiên", "Thiên Ấn"]).status).toBe("DEFERRED");
    expect(adaptTenGodsCard(L08.case_006).combination).toBeNull();
    expect(classifyTenGodCombination(["Chính Quan", "Kiếp Tài"]).status).toBe("CONFLICTING");
    expect(adaptTenGodsCard(L08.case_007).combination).toBeNull();
  });

  it("covers CASE-0001, CASE-0002, and launch_08 published visible sets", () => {
    expect(adaptTenGodsCard(CASE_0001).combination?.members).toEqual(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
    expect(adaptTenGodsCard(CASE_0002).combination?.members).toEqual([
      "Thực Thần",
      "Thương Quan",
      "Chính Quan",
    ]);
    expect(adaptTenGodsCard(L08.case_001).combination?.members).toEqual(["Kiếp Tài", "Thất Sát", "Thiên Ấn"]);
    expect(adaptTenGodsCard(L08.case_002).combination?.members).toEqual(["Kiếp Tài", "Thất Sát"]);
    expect(adaptTenGodsCard(L08.case_003).combination?.members).toEqual(["Thực Thần", "Thương Quan"]);
    expect(adaptTenGodsCard(L08.case_004).combination?.members).toEqual(["Thực Thần", "Chính Tài"]);
    expect(adaptTenGodsCard(L08.case_005).combination?.members).toEqual(["Kiếp Tài", "Thiên Tài"]);
    expect(adaptTenGodsCard(L08.case_006).combination).toBeNull();
    expect(adaptTenGodsCard(L08.case_007).combination).toBeNull();
    expect(adaptTenGodsCard(L08.case_008).combination?.members).toEqual(["Thực Thần", "Thiên Ấn"]);
  });

  it("does not change Runtime, Presentation, adapters, or calculation", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const presentation = readFileSync(
      resolve(PORTAL, "src/adapters/narrativeV2PresentationAdapter.ts"),
      "utf8",
    );
    const assets = readFileSync(resolve(ROOT, "tenGodsCombinationAssets.ts"), "utf8");
    expect(adapter).not.toMatch(/engines\./);
    expect(adapter).not.toContain("knowledge/consulting");
    expect(adapter).not.toContain("CASE-0001");
    expect(presentation).not.toContain("tenGodsCombinationAssets");
    expect(assets).toContain("knowledge/consulting/ten_gods/combinations");
    expect(assets).not.toMatch(/engines\./);
    expect(assets).not.toMatch(/ten_god_name\(|map_stem_to_ten_god|LABEL_TO_GOD_ID/);
  });
});
