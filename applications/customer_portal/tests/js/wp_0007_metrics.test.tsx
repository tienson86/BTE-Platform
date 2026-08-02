import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  BalancePanel,
  BusinessMetricCard,
  ConfidencePanel,
  MetricExplanation,
  MetricIndicator,
  MetricSection,
  MetricsScreen,
  MetricsSummary,
  metricsWorkPackageId,
  type MetricsViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const readyFixture: Extract<MetricsViewModel, { status: "ready" }> = {
  status: "ready",
  title: "Metrics",
  hero: {
    headline: "Metrics",
    subtitle: "Supporting quantitative indicators for consultation",
  },
  summary: {
    title: "Executive Metrics Summary",
    lead: "Overall chart posture is stable with manageable imbalance pressure.",
    items: [
      { id: "s1", label: "Day Master Strength", value: "Stable", hint: "Above baseline", tone: "success" },
      { id: "s2", label: "Overall Balance", value: "Moderate", rangeLabel: "Mid range" },
    ],
  },
  explanation: {
    title: "Metric Explanation",
    paragraphs: [
      "These values are prepared presentation outputs. They reinforce insight without calculation in the UI.",
    ],
  },
  sections: [
    {
      id: "strength",
      title: "Strength Metrics",
      description: "Day Master strength indicators.",
      metrics: [
        { id: "st1", label: "Strength Index", value: "72", hint: "Presentation value" },
      ],
    },
    {
      id: "elements",
      title: "Five Elements Metrics",
      metrics: [
        { id: "el1", label: "Wood", value: "High" },
        { id: "el2", label: "Fire", value: "Low" },
      ],
    },
    {
      id: "tengods",
      title: "Ten Gods Metrics",
      metrics: [
        { id: "tg1", label: "Direct Resource", value: "Prominent" },
      ],
    },
  ],
  balance: {
    title: "Balance Indicators",
    summary: "Elemental pressure is contained with Seasonal support.",
    indicators: [
      { id: "b1", label: "Seasonal Fit", value: "Supportive", statusLabel: "Stable", tone: "success" },
    ],
  },
  confidence: {
    title: "Confidence Indicators",
    level: "high",
    summary: "Metric confidence is high for structural indicators.",
    items: [
      { id: "c1", label: "Coverage", value: "Complete", statusLabel: "Ready", tone: "info" },
    ],
  },
  transition: {
    label: "Continue to Explainable Analysis",
    href: "#explainable-analysis",
  },
};

const metricsBusinessFiles = [
  "MetricsSummary.tsx",
  "MetricSection.tsx",
  "MetricCard.tsx",
  "MetricIndicator.tsx",
  "MetricExplanation.tsx",
  "ConfidencePanel.tsx",
  "BalancePanel.tsx",
];

const calculationForbidden =
  /\b(calculate|derive|normalize|aggregate|score|sum|average|compute)\s*\(/i;

describe("WP-0007 Metrics", () => {
  it("exports WP-0007 identity", () => {
    expect(metricsWorkPackageId).toBe("WP-0007");
  });

  it("metrics business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of metricsBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("metrics business components contain no calculation logic", () => {
    const offenders: string[] = [];
    for (const name of metricsBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (calculationForbidden.test(source)) {
        offenders.push(name);
      }
    }
    const screenSource = readFileSync(
      resolve(rootDir, "src/screens/MetricsScreen.tsx"),
      "utf8",
    );
    if (calculationForbidden.test(screenSource)) {
      offenders.push("MetricsScreen.tsx");
    }
    expect(offenders).toEqual([]);
  });

  it("renders Metrics reading order when ready", () => {
    const { container } = render(<MetricsScreen data={readyFixture} />);

    expect(screen.getByLabelText("Metrics")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Metrics" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Executive Metrics Summary" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Metric Explanation" })).toBeTruthy();
    expect(screen.getByLabelText("Supporting Indicators")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Balance Indicators" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Confidence Indicators" })).toBeTruthy();
    expect(
      screen.getByRole("link", { name: "Continue to Explainable Analysis" }),
    ).toBeTruthy();

    const text = container.textContent ?? "";
    const summaryIdx = text.indexOf("Overall chart posture is stable");
    const explanationIdx = text.indexOf("prepared presentation outputs");
    const strengthIdx = text.indexOf("Strength Metrics");
    const balanceIdx = text.indexOf("Elemental pressure is contained");
    const confidenceIdx = text.indexOf("Metric confidence is high");
    const transitionIdx = text.indexOf("Continue to Explainable Analysis");

    expect(summaryIdx).toBeGreaterThanOrEqual(0);
    expect(explanationIdx).toBeGreaterThan(summaryIdx);
    expect(strengthIdx).toBeGreaterThan(explanationIdx);
    expect(balanceIdx).toBeGreaterThan(strengthIdx);
    expect(confidenceIdx).toBeGreaterThan(balanceIdx);
    expect(transitionIdx).toBeGreaterThan(confidenceIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(<MetricsScreen data={{ status: "loading" }} />);
    expect(screen.getByText("Loading metrics")).toBeTruthy();

    rerender(<MetricsScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No metrics available")).toBeTruthy();

    rerender(<MetricsScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Metrics unavailable")).toBeTruthy();

    rerender(
      <MetricsScreen data={{ status: "error", errorMessage: "Metric bind failed" }} />,
    );
    expect(screen.getByText("Unable to load metrics")).toBeTruthy();
    expect(screen.getByText("Metric bind failed")).toBeTruthy();
  });

  it("renders Pack 06 metrics business components in isolation", () => {
    render(
      <>
        <MetricsSummary data={readyFixture.summary} />
        <MetricExplanation data={readyFixture.explanation!} />
        <MetricSection data={readyFixture.sections[0]!} />
        <BusinessMetricCard data={readyFixture.summary.items[0]!} />
        <MetricIndicator data={readyFixture.balance.indicators[0]!} />
        <BalancePanel data={readyFixture.balance} />
        <ConfidencePanel data={readyFixture.confidence} />
      </>,
    );

    expect(screen.getAllByText("Day Master Strength").length).toBeGreaterThan(0);
    expect(screen.getByText("Strength Index")).toBeTruthy();
    expect(screen.getAllByText("Seasonal Fit").length).toBeGreaterThan(0);
    expect(screen.getByText("high")).toBeTruthy();
  });

  it("wires metrics styles into the business stylesheet entry", () => {
    const css = readFileSync(
      resolve(rootDir, "src/styles/components/business/index.css"),
      "utf8",
    );
    expect(css).toContain("./metrics.css");
  });
});
