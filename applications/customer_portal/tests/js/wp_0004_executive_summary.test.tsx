import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  ExecutiveHero,
  ExecutiveHighlights,
  ExecutiveOverview,
  ExecutiveSummaryScreen,
  HeroActions,
  HeroBackground,
  RecommendationPanel,
  SummaryGlance,
  executiveSummaryWorkPackageId,
  type ExecutiveSummaryViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const readyFixture: Extract<ExecutiveSummaryViewModel, { status: "ready" }> = {
  status: "ready",
  hero: {
    identity: {
      dayMaster: "Jia",
      dayMasterLabel: "Jia Wood",
      chartTitle: "Jia Wood Day Master",
      subtitle: "Yang Wood · Spring birth",
    },
    verdict: {
      label: "Favorable",
      summary: "The chart shows constructive momentum with manageable risks.",
      tone: "success",
    },
  },
  recommendation: {
    title: "Protect the Useful God first",
    body: "Prioritize Water support and avoid Fire excess in near-term decisions.",
    priorityLabel: "Primary",
  },
  overview: {
    title: "Executive Summary",
    paragraphs: [
      "Overall structure is balanced with a clear Useful God pathway.",
      "Seasonal support reinforces the Day Master without overheating.",
    ],
  },
  glance: [
    { id: "strength", label: "Strength", value: "Stable", hint: "Above average" },
    { id: "useful-god", label: "Useful God", value: "Water" },
    { id: "season", label: "Season", value: "Spring" },
  ],
  highlights: [
    { id: "opportunity", label: "Opportunity", value: "Career expansion via Metal allies", tone: "success" },
    { id: "risk", label: "Risk", value: "Fire periods may overheat resources", tone: "warning" },
  ],
  transition: {
    label: "Continue to Four Pillars",
    href: "#four-pillars",
  },
};

function listBusinessSourceFiles(): string[] {
  return readdirSync(businessDir)
    .filter((name) => name.endsWith(".tsx") || name.endsWith(".ts"))
    .filter((name) => name !== "index.ts")
    .map((name) => join(businessDir, name));
}

describe("WP-0004 Executive Summary", () => {
  it("exports WP-0004 identity", () => {
    expect(executiveSummaryWorkPackageId).toBe("WP-0004");
  });

  it("business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const filePath of listBusinessSourceFiles()) {
      const source = readFileSync(filePath, "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(filePath);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("renders Executive Summary reading order when ready", () => {
    const { container } = render(<ExecutiveSummaryScreen data={readyFixture} />);

    expect(screen.getAllByLabelText("Executive Summary").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole("heading", { name: "Jia Wood Day Master" })).toBeTruthy();
    expect(screen.getByText("Protect the Useful God first")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Executive Summary" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "At a Glance" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Quick Highlights" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Continue to Four Pillars" })).toBeTruthy();

    const text = container.textContent ?? "";
    const heroIdx = text.indexOf("Jia Wood Day Master");
    const recIdx = text.indexOf("Protect the Useful God first");
    const overviewIdx = text.indexOf("Overall structure is balanced");
    const glanceIdx = text.indexOf("At a Glance");
    const highlightsIdx = text.indexOf("Quick Highlights");
    const transitionIdx = text.indexOf("Continue to Four Pillars");

    expect(heroIdx).toBeGreaterThanOrEqual(0);
    expect(recIdx).toBeGreaterThan(heroIdx);
    expect(overviewIdx).toBeGreaterThan(recIdx);
    expect(glanceIdx).toBeGreaterThan(overviewIdx);
    expect(highlightsIdx).toBeGreaterThan(glanceIdx);
    expect(transitionIdx).toBeGreaterThan(highlightsIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(<ExecutiveSummaryScreen data={{ status: "loading" }} />);
    expect(screen.getByText("Loading executive summary")).toBeTruthy();

    rerender(<ExecutiveSummaryScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No executive summary available")).toBeTruthy();

    rerender(<ExecutiveSummaryScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Executive summary unavailable")).toBeTruthy();

    rerender(
      <ExecutiveSummaryScreen
        data={{ status: "error", errorMessage: "Upstream timeout" }}
      />,
    );
    expect(screen.getByText("Unable to load executive summary")).toBeTruthy();
    expect(screen.getByText("Upstream timeout")).toBeTruthy();
  });

  it("renders Pack 06 business components in isolation", () => {
    render(
      <>
        <HeroBackground>Surface</HeroBackground>
        <HeroActions>
          <button type="button">Action</button>
        </HeroActions>
        <ExecutiveHero data={readyFixture.hero} />
        <RecommendationPanel data={readyFixture.recommendation} />
        <ExecutiveOverview
          overview={readyFixture.overview}
          verdict={readyFixture.hero.verdict}
        />
        <SummaryGlance items={readyFixture.glance} />
        <ExecutiveHighlights items={readyFixture.highlights} />
      </>,
    );

    expect(screen.getByText("Surface")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Action" })).toBeTruthy();
    expect(screen.getByText("Overall Verdict")).toBeTruthy();
    expect(screen.getByText("Primary")).toBeTruthy();
    expect(screen.getByText("Stable")).toBeTruthy();
    expect(screen.getByText("Career expansion via Metal allies")).toBeTruthy();
  });

  it("wires business styles into the foundation stylesheet entry", () => {
    const css = readFileSync(resolve(rootDir, "src/styles/index.css"), "utf8");
    expect(css).toContain('./components/business/index.css');
  });
});
