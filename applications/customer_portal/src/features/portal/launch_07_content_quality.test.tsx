/**
 * LAUNCH-07 — Real chart content quality & readability (presentation only).
 */

import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import type { AnalysisResponse } from "../../models";
import { adaptPortalResult } from "../result_v2/adapter/portalPresentationAdapter";
import { splitProseParagraphs } from "../result_v2/components/Knowledge";
import { adaptLiveAnalysisResult } from "./liveAnalysisResultAdapter";
import ResultViewerPage from "./pages/ResultViewerPage";
import { portalDemoReport } from "./fixtures/demoReport";

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

const SECTION_TITLES = [
  "Tóm tắt điều hành",
  "Quan sát",
  "Lý giải",
  "Tác động",
  "Khuyến nghị",
  "Lưu ý",
  "Kết luận",
] as const;

function loadLive() {
  const capture = JSON.parse(readFileSync(CAPTURE_PATH, "utf-8")) as LiveCapture;
  const analysisId = capture.response.request_id ?? "launch04-nguyen-tien-son";
  const analysisResult = capture.response.data;
  const mapped = adaptLiveAnalysisResult(analysisResult, {
    analysis_id: analysisId,
  });
  return { analysisId, analysisResult, mapped };
}

describe("LAUNCH-07 content quality mapping", () => {
  it("keeps summary concise and preserves full narrative section text", () => {
    const { mapped, analysisResult } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const presentation = mapped.report.presentation;
    expect((presentation?.summary?.bullets ?? []).length).toBeLessThanOrEqual(5);
    expect(presentation?.summary?.bullets?.[0]).toMatch(/Năm Bính Dần/);

    const knowledge = presentation?.knowledge ?? [];
    expect(knowledge.map((item) => item.title)).toEqual([...SECTION_TITLES]);

    const sourceSections =
      (
        analysisResult.narrative_result as {
          sections?: Array<{ title?: string; paragraphs?: Array<{ text?: string }> }>;
        }
      ).sections ?? [];

    for (let index = 0; index < SECTION_TITLES.length; index += 1) {
      const sourceText = sourceSections[index]?.paragraphs?.[0]?.text ?? "";
      expect(knowledge[index]?.body).toBe(sourceText);
      expect(knowledge[index]?.body?.includes("…")).toBe(false);
    }
  });

  it("does not duplicate narrative into career domain or duplicate recommendation cards", () => {
    const { mapped } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const presentation = mapped.report.presentation;
    const career = presentation?.domains?.career;
    expect(career?.available).toBe(true);
    expect(career?.recommendation_ids ?? []).toEqual([]);
    expect(career?.analysis_preview).toBeTruthy();
    expect(career?.analysis_detail).toBeTruthy();
    expect(career?.analysis_detail).not.toContain("Tóm tắt điều hành");
    expect(career?.analysis_detail).not.toContain("Quan sát");

    const model = adaptPortalResult(mapped.report);
    const careerRecCards = model.recommendations.filter((item) => item.domain === "career");
    expect(careerRecCards.length).toBe(1);
    expect(model.domains.career.recommendation_ids).toEqual([]);
  });

  it("preserves upstream truncated commercial strings without rewriting", () => {
    const { mapped, analysisResult } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    const upstreamWhat = (
      analysisResult.narrative_result as {
        primary_recommendation?: { what?: string };
      }
    ).primary_recommendation?.what;
    expect(upstreamWhat).toContain("…");
    expect(mapped.report.presentation?.recommendations?.[0]?.title).toBe(upstreamWhat);
  });

  it("splitProseParagraphs separates blank-line blocks only", () => {
    expect(splitProseParagraphs("Một.\n\nHai.")).toEqual(["Một.", "Hai."]);
    expect(splitProseParagraphs("Một câu duy nhất.")).toEqual(["Một câu duy nhất."]);
  });
});

describe("LAUNCH-07 ResultViewer readability", () => {
  it("renders seven full sections without Portal truncation and keeps career secondary", () => {
    const { analysisId, analysisResult, mapped } = loadLive();
    expect(mapped.ok).toBe(true);
    if (!mapped.ok) return;

    render(
      <ResultViewerPage analysisId={analysisId} analysisResult={analysisResult} />,
    );

    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("api");
    expect(root?.getAttribute("data-result-map")).toBe("api");

    const narrative = document.querySelector('[data-narrative-sections="true"]');
    expect(narrative).toBeTruthy();
    const knowledgeScope = within(narrative as HTMLElement);

    for (const title of SECTION_TITLES) {
      expect(knowledgeScope.getByText(title)).toBeTruthy();
    }

    const firstBody = mapped.report.presentation?.knowledge?.[0]?.body ?? "";
    expect(knowledgeScope.getByText(firstBody)).toBeTruthy();
    expect(firstBody.includes("…")).toBe(false);

    // Career exists after narrative in DOM order.
    const main = document.querySelector("#rv2-main");
    const html = main?.innerHTML ?? "";
    const knowledgePos = html.indexOf('id="rv2-Knowledge"');
    const careerPos = html.indexOf('id="rv2-DomainCareer"');
    const technicalPos = html.indexOf('id="rv2-Technical"');
    expect(knowledgePos).toBeGreaterThan(-1);
    expect(careerPos).toBeGreaterThan(knowledgePos);
    expect(technicalPos).toBeGreaterThan(careerPos);

    // Technical collapsed until expanded.
    expect(screen.queryByText("Nhật chủ")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Xem chi tiết kỹ thuật" }));
    expect(screen.getByText("Nhật chủ")).toBeTruthy();
    expect(screen.getByText("Canh")).toBeTruthy();

    expect(screen.queryByText("Nguyễn Văn An")).toBeNull();
  });

  it("preserves demo preview path separately", () => {
    render(<ResultViewerPage />);
    const root = document.querySelector(".pv-result-viewer");
    expect(root?.getAttribute("data-analysis-source")).toBe("demo");
    expect(screen.getByText("Nguyễn Văn An")).toBeTruthy();
    expect(
      screen.getByText(portalDemoReport.presentation?.identity?.headline ?? "___"),
    ).toBeTruthy();
  });
});
