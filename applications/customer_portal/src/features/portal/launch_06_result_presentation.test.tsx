/**
 * LAUNCH-06 — Real chart Result V2 presentation fixes.
 */

import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { adaptPortalResult } from "../result_v2/adapter/portalPresentationAdapter";
import type { AnalysisResponse } from "../../models";
import {
  adaptLiveAnalysisResult,
  formatLabeledPillars,
} from "./liveAnalysisResultAdapter";
import ResultViewerPage from "./pages/ResultViewerPage";
import { portalDemoReport } from "./fixtures/demoReport";
import { showDomain } from "../result_v2/utils/visibility";

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
  readonly response: AnalysisResponse;
};

function loadLive() {
  const capture = JSON.parse(readFileSync(CAPTURE_PATH, "utf-8")) as LiveCapture;
  const analysisId = capture.response.request_id ?? "launch04-nguyen-tien-son";
  const analysisResult = capture.response.data;
  const mapped = adaptLiveAnalysisResult(analysisResult, {
    analysis_id: analysisId,
  });
  return { analysisId, analysisResult, mapped };
}

describe("LAUNCH-06 chart fundamentals mapping", () => {
  it("surfaces Four Pillars, Day Master, pattern, strength, and score from live data", () => {
    const { mapped, analysisResult } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const presentation = mapped.report.presentation;
    const pillars = presentation?.technical?.pillars ?? "";
    expect(pillars).toContain("Năm Bính Dần");
    expect(pillars).toContain("Tháng Tân Sửu");
    expect(pillars).toContain("Ngày Canh Ngọ");
    expect(pillars).toContain("Giờ Mậu Dần");
    expect(formatLabeledPillars(analysisResult.bazi)).toBe(pillars);

    const meta = presentation?.technical?.metadata ?? {};
    expect(meta.day_master).toBe("Canh");
    expect(meta.year_pillar).toBe("Bính Dần");
    expect(meta.month_pillar).toBe("Tân Sửu");
    expect(meta.day_pillar).toBe("Canh Ngọ");
    expect(meta.hour_pillar).toBe("Mậu Dần");
    expect(meta.pattern).toBe("Chính Ấn");
    expect(meta.strength).toBeTruthy();
    expect(meta.strength_score).toBeTruthy();
    expect(meta.score_grade).toBe("D+");

    expect(presentation?.identity?.headline).toContain("Canh");
    expect(presentation?.identity?.headline).toContain("Chính Ấn");
    expect(presentation?.summary?.bullets?.[0]).toMatch(/Năm Bính Dần/);
  });

  it("maps seven narrative sections when present", () => {
    const { mapped, analysisResult } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const sections = (
      analysisResult.narrative_result as { sections?: unknown[] } | undefined
    )?.sections;
    expect(Array.isArray(sections)).toBe(true);
    expect(sections?.length).toBe(7);

    const knowledge = mapped.report.presentation?.knowledge ?? [];
    expect(knowledge.length).toBe(7);
    expect(knowledge[0]?.title).toBeTruthy();
    expect(knowledge[0]?.teaser).toBeTruthy();
    expect(knowledge[0]?.body).toBeTruthy();
  });

  it("hides empty domains in PortalResultModel navigation/content rules", () => {
    const { mapped } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const model = adaptPortalResult(mapped.report);
    expect(showDomain(model.domains.career)).toBe(true);
    expect(showDomain(model.domains.wealth)).toBe(false);
    expect(showDomain(model.domains.relationship)).toBe(false);
    expect(showDomain(model.domains.health)).toBe(false);
    expect(showDomain(model.domains.luck)).toBe(false);

    const visibleDomainNav = model.nav.items.filter((item) =>
      item.target_ui_id.startsWith("Domain"),
    );
    expect(visibleDomainNav.every((item) => item.visible)).toBe(true);
    expect(visibleDomainNav.map((item) => item.target_ui_id)).toEqual([
      "DomainCareer",
    ]);
  });
});

describe("LAUNCH-06 ResultViewer live vs demo", () => {
  it("renders fundamentals for live Nguyen Tien Son without demo fallback", async () => {
    const { analysisId, analysisResult } = loadLive();
    render(
      <ResultViewerPage analysisId={analysisId} analysisResult={analysisResult} />,
    );

    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-result-map")).toBe("api");

    expect(screen.getByText("Nguyen Tien Son")).toBeTruthy();
    expect((await screen.findAllByText(/Năm Bính Dần/)).length).toBeGreaterThan(0);
    expect(document.querySelector('[data-chart-fundamentals="true"]')).toBeTruthy();
    expect(screen.getByText(/Nhật chủ:\s*Canh/)).toBeTruthy();
    expect(screen.getByText(/Canh\s*·\s*Chính Ấn/)).toBeTruthy();
    expect(screen.getByText(/Cách cục:\s*Chính Ấn/)).toBeTruthy();
    expect(screen.queryByText("Nguyễn Văn An")).toBeNull();
    expect(screen.queryByText("Quan hệ")).toBeNull();
    expect(screen.queryByText("Sức khỏe")).toBeNull();
    expect(screen.queryByText("Vận trình")).toBeNull();
    expect(screen.queryByText("Tài chính")).toBeNull();

    // Narrative sections visible under knowledge slot (lazy + expanded by default).
    expect(await screen.findByText("Tóm tắt điều hành")).toBeTruthy();
    expect(screen.getByText("Quan sát")).toBeTruthy();
  });

  it("preserves demo preview path", () => {
    render(<ResultViewerPage />);
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("demo");
    expect(screen.getByText("Nguyễn Văn An")).toBeTruthy();
    expect(
      screen.getByText(portalDemoReport.presentation?.identity?.headline ?? "___"),
    ).toBeTruthy();
  });
});
