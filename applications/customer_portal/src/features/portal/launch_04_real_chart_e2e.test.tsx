/**
 * LAUNCH-04 — Real chart end-to-end validation.
 *
 * Live API capture was produced by FastAPI TestClient against
 * applications.api.app:create_app() → POST /api/v1/analyze
 * for Nguyen Tien Son (1987-01-21 04:30).
 *
 * This suite validates the captured LIVE payload through:
 * adaptLiveAnalysisResult → adaptPortalResult → ResultViewerPage
 * and asserts source=api (never portalDemoReport).
 */

import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { adaptPortalResult } from "../result_v2/adapter/portalPresentationAdapter";
import type { AnalysisDataDto, AnalysisResponse } from "../../models";
import { adaptLiveAnalysisResult } from "./liveAnalysisResultAdapter";
import ResultViewerPage from "./pages/ResultViewerPage";

afterEach(() => {
  cleanup();
});

const FIXTURE_DIR = path.dirname(fileURLToPath(import.meta.url));
const CAPTURE_PATH = path.join(
  FIXTURE_DIR,
  "fixtures",
  "launch_04_real_chart_response.json",
);

type LiveCapture = {
  readonly http_status: number;
  readonly capture_meta: {
    readonly http_status: number;
    readonly success: boolean;
    readonly request_id: string;
    readonly pipeline: readonly string[];
    readonly pillars: Record<string, { stem?: string; branch?: string }>;
    readonly day_master?: string;
    readonly narrative_contract?: string;
    readonly narrative_status?: string;
    readonly customer?: Record<string, unknown>;
  };
  readonly response: AnalysisResponse;
};

/** User-verified Four Pillars (ASCII romanization). */
const VERIFIED_PILLARS = {
  year: { stem: "binh", branch: "dan" },
  month: { stem: "tan", branch: "suu" },
  day: { stem: "canh", branch: "ngo" },
  hour: { stem: "mau", branch: "dan" },
} as const;

const BIRTH_REQUEST = {
  year: 1987,
  month: 1,
  day: 21,
  hour: 4,
  minute: 30,
  gender: "male",
  timezone: "Asia/Ho_Chi_Minh",
  full_name: "Nguyen Tien Son",
  birth_place: "Ha Noi, Vietnam",
} as const;

function loadCapture(): LiveCapture {
  const raw = readFileSync(CAPTURE_PATH, "utf-8");
  return JSON.parse(raw) as LiveCapture;
}

/** Strip Vietnamese diacritics for pillar comparison against ASCII fixture labels. */
function foldStemBranch(value: string | null | undefined): string {
  return (value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase()
    .trim();
}

function loadLiveAnalysis(): {
  analysisId: string;
  analysisResult: AnalysisDataDto;
  capture: LiveCapture;
} {
  const capture = loadCapture();
  const analysisId = capture.response.request_id ?? capture.capture_meta.request_id;
  const analysisResult = capture.response.data;
  return { analysisId, analysisResult, capture };
}

describe("LAUNCH-04 real chart — API capture integrity", () => {
  it("Test 1 — live POST /api/v1/analyze capture succeeded with analysis id and payload", () => {
    const capture = loadCapture();
    expect(capture.http_status).toBe(200);
    expect(capture.response.success).toBe(true);
    expect(capture.response.request_id).toBe("launch04-nguyen-tien-son");
    expect(capture.response.data.pipeline).toEqual([
      "calendar",
      "bazi",
      "pattern",
      "score",
      "interpretation",
      "report",
      "narrative",
    ]);
    expect(capture.response.data.customer?.full_name).toBe(BIRTH_REQUEST.full_name);
    expect(capture.response.data.customer?.gender).toBe(BIRTH_REQUEST.gender);
    expect(capture.response.data.narrative_result).toBeTruthy();
    expect(
      (capture.response.data.narrative_result as { contract?: string })?.contract,
    ).toBe("pack05_narrative_result_v1");
  });

  it("Four Pillars match the verified fixture (Binh Dan / Tan Suu / Canh Ngo / Mau Dan)", () => {
    const { analysisResult } = loadLiveAnalysis();
    const bazi = analysisResult.bazi;
    expect(bazi).toBeTruthy();

    const observed = {
      year: {
        stem: foldStemBranch(bazi?.year_pillar?.stem),
        branch: foldStemBranch(bazi?.year_pillar?.branch),
      },
      month: {
        stem: foldStemBranch(bazi?.month_pillar?.stem),
        branch: foldStemBranch(bazi?.month_pillar?.branch),
      },
      day: {
        stem: foldStemBranch(bazi?.day_pillar?.stem),
        branch: foldStemBranch(bazi?.day_pillar?.branch),
      },
      hour: {
        stem: foldStemBranch(bazi?.hour_pillar?.stem),
        branch: foldStemBranch(bazi?.hour_pillar?.branch),
      },
    };

    expect(observed).toEqual(VERIFIED_PILLARS);
    expect(foldStemBranch(bazi?.day_master)).toBe("canh");
  });
});

describe("LAUNCH-04 real chart — adapter + PortalResultModel", () => {
  it("Test 2 — adaptLiveAnalysisResult succeeds for live payload", () => {
    const { analysisId, analysisResult } = loadLiveAnalysis();
    const mapped = adaptLiveAnalysisResult(analysisResult, {
      analysis_id: analysisId,
    });
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    expect(mapped.report.success).toBe(true);
    expect(mapped.report.presentation?.identity?.full_name).toBe("Nguyen Tien Son");
    expect(mapped.report.presentation?.identity?.headline).toBeTruthy();
    expect(mapped.report.presentation?.identity?.one_line_summary).toBeTruthy();
    expect((mapped.report.presentation?.summary?.bullets ?? []).length).toBeGreaterThan(0);
    expect(mapped.report.presentation?.technical?.ids).toBe(analysisId);
    expect(mapped.report.presentation?.technical?.pillars).toMatch(/Bính|Dần/);
  });

  it("Test 3 — adaptPortalResult produces PortalResultModel", () => {
    const { analysisId, analysisResult } = loadLiveAnalysis();
    const mapped = adaptLiveAnalysisResult(analysisResult, {
      analysis_id: analysisId,
    });
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const model = adaptPortalResult(mapped.report);
    expect(model.contract_id).toBe("bte.portal.result_ui.v2");
    expect(model.hero?.name).toBe("Nguyen Tien Son");
    expect(model.summary?.bullets.length).toBeGreaterThan(0);
    expect(["ready", "partial_ready"]).toContain(model.page.state);
    expect(model.page.state).not.toBe("error");
    expect(model.technical.ids).toBe(analysisId);
  });
});

describe("LAUNCH-04 real chart — Result Viewer", () => {
  it("Test 4 + 5 — ResultViewer renders live subject with source=api (not demo)", () => {
    const { analysisId, analysisResult } = loadLiveAnalysis();

    render(
      <ResultViewerPage analysisId={analysisId} analysisResult={analysisResult} />,
    );

    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-analysis-source")).not.toBe("demo");
    expect(root?.getAttribute("data-result-map")).toBe("api");
    expect(root?.getAttribute("data-analysis-id")).toBe(analysisId);
    expect(root?.getAttribute("data-has-analysis-result")).toBe("true");

    expect(screen.queryByRole("alert")).toBeNull();
    expect(screen.getByText("Nguyen Tien Son")).toBeTruthy();
    // Demo fixture identity must not appear as the live subject source.
    expect(screen.queryByText("Nguyễn Văn An")).toBeNull();
  });
});
