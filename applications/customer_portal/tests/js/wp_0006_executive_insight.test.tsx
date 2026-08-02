import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  ExecutiveConclusion,
  ExecutiveInsightHero,
  ExecutiveInsightScreen,
  InsightSection,
  InsightSummary,
  OpportunityPanel,
  RecommendationPanel,
  RiskPanel,
  executiveInsightWorkPackageId,
  type ExecutiveInsightViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const readyFixture: Extract<ExecutiveInsightViewModel, { status: "ready" }> = {
  status: "ready",
  title: "Executive Insight",
  hero: {
    headline: "Executive Insight",
    subtitle: "High-level consulting conclusions from prepared analysis",
  },
  conclusion: {
    title: "Overall Strategy",
    body: "Protect Useful God pathways and prioritize Water support this decade.",
    confidence: "high",
  },
  summary: {
    title: "Insight Summary",
    paragraphs: ["Prepared narrative summarizing chart posture without calculation."],
  },
  insights: [
    {
      id: "strength",
      title: "Strength Insight",
      summary: "Stable Day Master with constructive Resource support.",
      body: "Supporting explanation rendered from presentation data only.",
      confidence: "high",
      priorityLabel: "Primary",
      tone: "success",
      evidence: [
        { id: "e1", label: "Resource stem present", detail: "Display only", meta: "E-01" },
      ],
    },
    {
      id: "weakness",
      title: "Weakness Insight",
      summary: "Fire excess can overheat productive cycles.",
      confidence: "medium",
      priorityLabel: "Watch",
      tone: "warning",
    },
    {
      id: "career",
      title: "Career Insight",
      summary: "Authority stars favor structured leadership roles.",
      confidence: "medium",
    },
  ],
  opportunities: [
    {
      id: "o1",
      title: "Career expansion",
      body: "Metal allies open collaborative channels.",
      priorityLabel: "Focus",
    },
  ],
  risks: [
    {
      id: "r1",
      title: "Overheating periods",
      body: "Fire luck cycles may deplete resources.",
      priorityLabel: "Attention",
    },
  ],
  recommendation: {
    title: "Recommended Focus",
    body: "Keep Water support active and avoid Fire-heavy decisions near-term.",
    priorityLabel: "Primary",
  },
  transition: {
    label: "Continue to Metrics",
    href: "#metrics",
  },
};

const insightBusinessFiles = [
  "ExecutiveInsightHero.tsx",
  "InsightSection.tsx",
  "OpportunityPanel.tsx",
  "RiskPanel.tsx",
  "InsightSummary.tsx",
  "ExecutiveConclusion.tsx",
];

const analysisForbidden = /\b(calculate|evaluate|score|derive|analyze|infer)\s*\(/i;

describe("WP-0006 Executive Insight", () => {
  it("exports WP-0006 identity", () => {
    expect(executiveInsightWorkPackageId).toBe("WP-0006");
  });

  it("insight business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of insightBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("insight business components contain no analysis logic", () => {
    const offenders: string[] = [];
    for (const name of [...insightBusinessFiles, "RecommendationPanel.tsx"]) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (analysisForbidden.test(source)) {
        offenders.push(name);
      }
    }
    const screenSource = readFileSync(
      resolve(rootDir, "src/screens/ExecutiveInsightScreen.tsx"),
      "utf8",
    );
    if (analysisForbidden.test(screenSource)) {
      offenders.push("ExecutiveInsightScreen.tsx");
    }
    expect(offenders).toEqual([]);
  });

  it("renders Executive Insight reading order when ready", () => {
    const { container } = render(<ExecutiveInsightScreen data={readyFixture} />);

    expect(screen.getAllByLabelText("Executive Insight").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Overall Strategy")).toBeTruthy();
    expect(screen.getByLabelText("Key Insights")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Opportunities" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Risks" })).toBeTruthy();
    expect(screen.getByText("Recommended Focus")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Continue to Metrics" })).toBeTruthy();

    const text = container.textContent ?? "";
    const heroIdx = text.indexOf("High-level consulting conclusions");
    const conclusionIdx = text.indexOf("Protect Useful God pathways");
    const strengthIdx = text.indexOf("Strength Insight");
    const opportunityIdx = text.indexOf("Career expansion");
    const riskIdx = text.indexOf("Overheating periods");
    const recommendationIdx = text.indexOf("Recommended Focus");
    const transitionIdx = text.indexOf("Continue to Metrics");

    expect(heroIdx).toBeGreaterThanOrEqual(0);
    expect(conclusionIdx).toBeGreaterThan(heroIdx);
    expect(strengthIdx).toBeGreaterThan(conclusionIdx);
    expect(opportunityIdx).toBeGreaterThan(strengthIdx);
    expect(riskIdx).toBeGreaterThan(opportunityIdx);
    expect(recommendationIdx).toBeGreaterThan(riskIdx);
    expect(transitionIdx).toBeGreaterThan(recommendationIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(<ExecutiveInsightScreen data={{ status: "loading" }} />);
    expect(screen.getByText("Loading executive insight")).toBeTruthy();

    rerender(<ExecutiveInsightScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No executive insight available")).toBeTruthy();

    rerender(<ExecutiveInsightScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Executive insight unavailable")).toBeTruthy();

    rerender(
      <ExecutiveInsightScreen
        data={{ status: "error", errorMessage: "Insight mapping failed" }}
      />,
    );
    expect(screen.getByText("Unable to load executive insight")).toBeTruthy();
    expect(screen.getByText("Insight mapping failed")).toBeTruthy();
  });

  it("renders Pack 06 insight business components in isolation", () => {
    render(
      <>
        <ExecutiveInsightHero data={readyFixture.hero} />
        <ExecutiveConclusion data={readyFixture.conclusion} />
        <InsightSummary data={readyFixture.summary!} />
        <InsightSection data={readyFixture.insights[0]!} />
        <OpportunityPanel items={readyFixture.opportunities} />
        <RiskPanel items={readyFixture.risks} />
        <RecommendationPanel data={readyFixture.recommendation} />
      </>,
    );

    expect(screen.getByText("Executive Conclusion")).toBeTruthy();
    expect(screen.getByText("Resource stem present")).toBeTruthy();
    expect(screen.getByText("Career expansion")).toBeTruthy();
    expect(screen.getByText("Overheating periods")).toBeTruthy();
    expect(screen.getAllByText("Primary").length).toBeGreaterThan(0);
  });

  it("wires executive insight styles into the business stylesheet entry", () => {
    const css = readFileSync(
      resolve(rootDir, "src/styles/components/business/index.css"),
      "utf8",
    );
    expect(css).toContain("./executive-insight.css");
  });
});
