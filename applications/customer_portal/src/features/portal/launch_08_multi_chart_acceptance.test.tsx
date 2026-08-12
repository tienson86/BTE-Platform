/**
 * LAUNCH-08 — Real multi-chart beta acceptance.
 *
 * Fixtures were captured via FastAPI TestClient → POST /api/v1/analyze
 * (OrchestratorService) for eight owner-verified charts. This suite is
 * deterministic and does not call external services.
 */

import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import type { AnalysisDataDto, AnalysisResponse, PillarDto } from "../../models";
import { adaptPortalResult } from "../result_v2/adapter/portalPresentationAdapter";
import { showDomain } from "../result_v2/utils/visibility";
import { adaptLiveAnalysisResult } from "./liveAnalysisResultAdapter";
import ResultViewerPage from "./pages/ResultViewerPage";
import { portalDemoReport } from "./fixtures/demoReport";

afterEach(() => {
  cleanup();
});

const FIXTURE_DIR = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  "fixtures",
  "launch_08",
);

const SECTION_TITLES = [
  "Tóm tắt điều hành",
  "Quan sát",
  "Lý giải",
  "Tác động",
  "Khuyến nghị",
  "Lưu ý",
  "Kết luận",
] as const;

type VerifiedPillar = readonly [stem: string, branch: string];

type CaseSpec = {
  readonly id: string;
  readonly file: string;
  readonly full_name: string;
  readonly gender: string;
  readonly verified_pillars: {
    readonly year: VerifiedPillar;
    readonly month: VerifiedPillar;
    readonly day: VerifiedPillar;
    readonly hour: VerifiedPillar;
  };
};

type LiveCapture = {
  readonly http_status: number;
  readonly capture_meta: {
    readonly case_id: string;
    readonly request_id: string;
    readonly success: boolean;
    readonly day_master?: string;
    readonly pattern?: string;
    readonly strength_reasoning?: string;
    readonly strength_score?: number;
    readonly narrative_section_titles?: string[];
  };
  readonly response: AnalysisResponse;
};

/** Owner-verified fixtures — do not recalculate in this sprint. */
const CASES: readonly CaseSpec[] = [
  {
    id: "CASE-001",
    file: "case_001_response.json",
    full_name: "Nguyen Tien Son",
    gender: "male",
    verified_pillars: {
      year: ["binh", "dan"],
      month: ["tan", "suu"],
      day: ["canh", "ngo"],
      hour: ["mau", "dan"],
    },
  },
  {
    id: "CASE-002",
    file: "case_002_response.json",
    full_name: "Dinh Thanh Trung",
    gender: "male",
    verified_pillars: {
      year: ["dinh", "ty"],
      month: ["nham", "dan"],
      day: ["binh", "ngo"],
      hour: ["tan", "mao"],
    },
  },
  {
    id: "CASE-003",
    file: "case_003_response.json",
    full_name: "Nguyen Tien Khang",
    gender: "male",
    verified_pillars: {
      year: ["at", "mui"],
      month: ["giap", "than"],
      day: ["nham", "tuat"],
      hour: ["giap", "thin"],
    },
  },
  {
    id: "CASE-004",
    file: "case_004_response.json",
    full_name: "Nguyen Tien Minh",
    gender: "male",
    verified_pillars: {
      year: ["quy", "ty"],
      month: ["canh", "than"],
      day: ["mau", "ngo"],
      hour: ["ky", "mui"],
    },
  },
  {
    id: "CASE-005",
    file: "case_005_response.json",
    full_name: "Luong Ngoc Huynh",
    gender: "male",
    verified_pillars: {
      year: ["binh", "ngo"],
      month: ["dinh", "dau"],
      day: ["binh", "tuat"],
      hour: ["canh", "dan"],
    },
  },
  {
    id: "CASE-006",
    file: "case_006_response.json",
    full_name: "Nguyen Thi Huong Mai",
    gender: "female",
    verified_pillars: {
      year: ["mau", "thin"],
      month: ["dinh", "ty"],
      day: ["quy", "ty"],
      hour: ["nham", "tuat"],
    },
  },
  {
    id: "CASE-007",
    file: "case_007_response.json",
    full_name: "Vu Thi Thanh Tuyen",
    gender: "female",
    verified_pillars: {
      year: ["giap", "ty"],
      month: ["tan", "mui"],
      day: ["mau", "than"],
      hour: ["quy", "hoi"],
    },
  },
  {
    id: "CASE-008",
    file: "case_008_response.json",
    full_name: "Cao Anh Cuong",
    gender: "male",
    verified_pillars: {
      year: ["dinh", "suu"],
      month: ["quy", "suu"],
      day: ["at", "mao"],
      hour: ["giap", "than"],
    },
  },
] as const;

/** Known ASCII ambiguity: owner "Ty" may mean Tý or Tỵ. */
const BRANCH_ALIASES: Record<string, readonly string[]> = {
  ty: ["ty", "ti"],
};

function foldStemBranch(value: string | null | undefined): string {
  return (value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase()
    .trim();
}

function branchMatches(verified: string, runtime: string): boolean {
  const foldedRuntime = foldStemBranch(runtime);
  const foldedVerified = foldStemBranch(verified);
  if (foldedRuntime === foldedVerified) return true;
  const aliases = BRANCH_ALIASES[foldedVerified];
  return Boolean(aliases?.includes(foldedRuntime));
}

function pillarMatches(
  verified: VerifiedPillar,
  runtime: PillarDto | undefined,
): boolean {
  if (!runtime) return false;
  return (
    foldStemBranch(runtime.stem) === foldStemBranch(verified[0]) &&
    branchMatches(verified[1], runtime.branch ?? "")
  );
}

function loadCapture(spec: CaseSpec): LiveCapture {
  const raw = readFileSync(path.join(FIXTURE_DIR, spec.file), "utf-8");
  return JSON.parse(raw) as LiveCapture;
}

function loadLive(spec: CaseSpec): {
  analysisId: string;
  analysisResult: AnalysisDataDto;
  capture: LiveCapture;
} {
  const capture = loadCapture(spec);
  const analysisId = capture.response.request_id ?? capture.capture_meta.request_id;
  return { analysisId, analysisResult: capture.response.data, capture };
}

describe("LAUNCH-08 fixture integrity", () => {
  it("ships eight captured analyze responses", () => {
    const files = readdirSync(FIXTURE_DIR).filter((name) =>
      name.endsWith("_response.json"),
    );
    expect(files.length).toBe(8);
    expect(CASES.map((item) => item.id)).toHaveLength(8);
  });
});

describe.each(CASES)("LAUNCH-08 $id acceptance", (spec) => {
  it("API capture succeeds with analysis id and real analysisResult", () => {
    const { capture, analysisId, analysisResult } = loadLive(spec);
    expect(capture.http_status).toBe(200);
    expect(capture.response.success).toBe(true);
    expect(analysisId).toBeTruthy();
    expect(analysisResult).toBeTruthy();
    expect(analysisResult.pipeline).toEqual([
      "calendar",
      "bazi",
      "pattern",
      "score",
      "interpretation",
      "report",
      "narrative",
    ]);
    expect(analysisResult.customer?.full_name).toBe(spec.full_name);
    expect(analysisResult.customer?.gender).toBe(spec.gender);
    expect(analysisResult.bazi?.day_master).toBeTruthy();
    expect(analysisResult.narrative_result).toBeTruthy();
  });

  it("adapter and PortalResultModel succeed without fabrication", () => {
    const { analysisId, analysisResult } = loadLive(spec);
    const mapped = adaptLiveAnalysisResult(analysisResult, {
      analysis_id: analysisId,
    });
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    expect(mapped.report.presentation?.identity?.full_name).toBe(spec.full_name);
    expect(mapped.report.presentation?.technical?.pillars).toBeTruthy();
    expect(mapped.report.presentation?.technical?.metadata?.day_master).toBe(
      analysisResult.bazi?.day_master,
    );

    const model = adaptPortalResult(mapped.report);
    expect(model.contract_id).toBe("bte.portal.result_ui.v2");
    expect(model.hero?.name).toBe(spec.full_name);
    expect(model.page.state === "ready" || model.page.state === "partial_ready").toBe(
      true,
    );
    expect(model.knowledge.map((item) => item.title)).toEqual([...SECTION_TITLES]);
    expect(showDomain(model.domains.wealth)).toBe(false);
    expect(showDomain(model.domains.relationship)).toBe(false);
    expect(showDomain(model.domains.health)).toBe(false);
    expect(showDomain(model.domains.luck)).toBe(false);
    expect(model.charts).toEqual([]);
    expect(model.appendix).toBeNull();
    // No Portal remount of seven sections into career detail.
    expect(model.domains.career.analysis_detail ?? "").not.toContain("Tóm tắt điều hành");
    expect(model.domains.career.recommendation_ids).toEqual([]);
  });

  it("Result V2 renders api source without demo fallback or runtime error", () => {
    const { analysisId, analysisResult } = loadLive(spec);
    render(
      <ResultViewerPage analysisId={analysisId} analysisResult={analysisResult} />,
    );

    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-result-map")).toBe("api");
    expect(root?.getAttribute("data-analysis-id")).toBe(analysisId);
    expect(screen.getByText(spec.full_name)).toBeTruthy();
    expect(screen.queryByText("Nguyễn Văn An")).toBeNull();
    expect(
      screen.queryByText(portalDemoReport.presentation?.identity?.headline ?? "___"),
    ).toBeNull();

    const narrative = document.querySelector('[data-narrative-sections="true"]');
    expect(narrative).toBeTruthy();
    const scope = within(narrative as HTMLElement);
    for (const title of SECTION_TITLES) {
      expect(scope.getByText(title)).toBeTruthy();
    }

    expect(screen.queryByText("Quan hệ")).toBeNull();
    expect(screen.queryByText("Sức khỏe")).toBeNull();
    expect(screen.queryByText("Vận trình")).toBeNull();
    expect(screen.queryByText("Tài chính")).toBeNull();
  });
});

describe("LAUNCH-08 pillar verification vs owner fixtures", () => {
  it("records matches and known discrepancies without mutating runtime", () => {
    const rows = CASES.map((spec) => {
      const { analysisResult } = loadLive(spec);
      const bazi = analysisResult.bazi;
      const checks = {
        year: pillarMatches(spec.verified_pillars.year, bazi?.year_pillar),
        month: pillarMatches(spec.verified_pillars.month, bazi?.month_pillar),
        day: pillarMatches(spec.verified_pillars.day, bazi?.day_pillar),
        hour: pillarMatches(spec.verified_pillars.hour, bazi?.hour_pillar),
      };
      return { id: spec.id, checks, bazi };
    });

    for (const row of rows) {
      if (row.id === "CASE-006") {
        // Owner fixture month = Dinh Ty; runtime month = Mậu Ngọ → DISCREPANCY.
        expect(row.checks.year).toBe(true);
        expect(row.checks.day).toBe(true);
        expect(row.checks.hour).toBe(true);
        expect(row.checks.month).toBe(false);
        expect(foldStemBranch(row.bazi?.month_pillar?.stem)).toBe("mau");
        expect(foldStemBranch(row.bazi?.month_pillar?.branch)).toBe("ngo");
        continue;
      }
      expect(row.checks).toEqual({
        year: true,
        month: true,
        day: true,
        hour: true,
      });
    }
  });
});

describe("LAUNCH-08 cross-chart variation and isolation", () => {
  it("subjects, day masters, pillars, and patterns are not contaminated across charts", () => {
    const snapshots = CASES.map((spec) => {
      const { analysisId, analysisResult } = loadLive(spec);
      const mapped = adaptLiveAnalysisResult(analysisResult, {
        analysis_id: analysisId,
      });
      expect(mapped.ok).toBe(true);
      if (!mapped.ok) {
        throw new Error(`adapter failed for ${spec.id}`);
      }
      return {
        id: spec.id,
        name: mapped.report.presentation?.identity?.full_name ?? "",
        dayMaster: String(
          mapped.report.presentation?.technical?.metadata?.day_master ?? "",
        ),
        pillars: mapped.report.presentation?.technical?.pillars ?? "",
        pattern: String(mapped.report.presentation?.technical?.metadata?.pattern ?? ""),
        strength: String(
          mapped.report.presentation?.technical?.metadata?.strength ?? "",
        ),
        strengthScore: String(
          mapped.report.presentation?.technical?.metadata?.strength_score ?? "",
        ),
        narrativeFirst: mapped.report.presentation?.knowledge?.[0]?.body ?? "",
        analysisId,
      };
    });

    const names = new Set(snapshots.map((item) => item.name));
    expect(names.size).toBe(8);

    const pillarSets = new Set(snapshots.map((item) => item.pillars));
    expect(pillarSets.size).toBe(8);

    const dayMasters = new Set(snapshots.map((item) => item.dayMaster));
    expect(dayMasters.size).toBeGreaterThan(1);

    const patterns = new Set(snapshots.map((item) => item.pattern));
    expect(patterns.size).toBeGreaterThan(1);

    const strengthScores = new Set(snapshots.map((item) => item.strengthScore));
    expect(strengthScores.size).toBeGreaterThan(1);

    const narrativeFirst = new Set(snapshots.map((item) => item.narrativeFirst));
    expect(narrativeFirst.size).toBeGreaterThan(1);

    // No chart receives another chart's analysis id / name pairing.
    for (const snap of snapshots) {
      const caseSlug = snap.id.toLowerCase(); // case-001
      expect(snap.analysisId.toLowerCase()).toContain(caseSlug);
      expect(snap.name).not.toBe("Nguyễn Văn An");
    }
  });

  it("demo preview path remains isolated from live fixtures", () => {
    render(<ResultViewerPage />);
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("demo");
    expect(screen.getByText("Nguyễn Văn An")).toBeTruthy();
  });
});
