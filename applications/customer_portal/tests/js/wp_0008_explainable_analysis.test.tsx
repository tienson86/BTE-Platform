import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  AnalysisSection,
  AnalysisSummary,
  ConclusionPanel,
  EvidencePanel,
  ExplainableAnalysis,
  ExplainableAnalysisScreen,
  ExplanationPanel,
  KnowledgeReferencePanel,
  RecommendationPanel,
  RuleReferencePanel,
  explainableAnalysisWorkPackageId,
  type AnalysisBlockViewModel,
  type ExplainableAnalysisViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const strengthBlock: AnalysisBlockViewModel = {
  id: "strength",
  title: "Day Master Strength",
  conclusion: {
    title: "Strength Conclusion",
    body: "Day Master is structurally stable with Resource support.",
  },
  explanation: {
    title: "Strength Explanation",
    paragraphs: [
      "Prepared reasoning explains why strength is assessed as stable.",
    ],
  },
  evidence: [
    {
      id: "ev1",
      label: "Resource stem present",
      detail: "Display-only evidence row",
      meta: "E-101",
    },
  ],
  rules: [
    {
      id: "r1",
      label: "Strength Rule A",
      citation: "Rule STR-01",
      source: "Prepared reference",
    },
  ],
  confidence: {
    title: "Strength Confidence",
    level: "high",
    summary: "Confidence is high for structural strength indicators.",
  },
  knowledge: [
    {
      id: "k1",
      citation: "Day Master fundamentals",
      source: "Knowledge catalog",
    },
  ],
  recommendation: {
    title: "Strength Recommendation",
    body: "Maintain Water support pathways.",
    priorityLabel: "Primary",
  },
};

const readyFixture: Extract<ExplainableAnalysisViewModel, { status: "ready" }> = {
  status: "ready",
  title: "Explainable Analysis",
  subtitle: "Traceable conclusions with prepared evidence",
  summary: {
    title: "Analysis Summary",
    paragraphs: [
      "This screen displays prepared explanations without performing analysis.",
    ],
  },
  blocks: [strengthBlock],
  transition: {
    label: "Continue to Consultation Report",
    href: "#consultation-report",
  },
};

const explainableBusinessFiles = [
  "ExplainableAnalysis.tsx",
  "AnalysisSection.tsx",
  "ConclusionPanel.tsx",
  "ExplanationPanel.tsx",
  "EvidencePanel.tsx",
  "RuleReferencePanel.tsx",
  "KnowledgeReferencePanel.tsx",
  "AnalysisSummary.tsx",
];

const explanationForbidden =
  /\b(derive|generate|evaluate|calculate|infer|summarize|reason)\s*\(/i;

describe("WP-0008 Explainable Analysis", () => {
  it("exports WP-0008 identity", () => {
    expect(explainableAnalysisWorkPackageId).toBe("WP-0008");
  });

  it("explainable business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of explainableBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("explainable business components contain no analysis or reasoning logic", () => {
    const offenders: string[] = [];
    for (const name of explainableBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (explanationForbidden.test(source)) {
        offenders.push(name);
      }
    }
    const screenSource = readFileSync(
      resolve(rootDir, "src/screens/ExplainableAnalysisScreen.tsx"),
      "utf8",
    );
    if (explanationForbidden.test(screenSource)) {
      offenders.push("ExplainableAnalysisScreen.tsx");
    }
    expect(offenders).toEqual([]);
  });

  it("preserves explainability contract order inside an analysis block", () => {
    const { container } = render(<AnalysisSection data={strengthBlock} />);
    const text = container.textContent ?? "";

    const conclusionIdx = text.indexOf("Day Master is structurally stable");
    const explanationIdx = text.indexOf("Prepared reasoning explains");
    const evidenceIdx = text.indexOf("Resource stem present");
    const ruleIdx = text.indexOf("Rule STR-01");
    const confidenceIdx = text.indexOf("Confidence is high for structural");
    const knowledgeIdx = text.indexOf("Day Master fundamentals");
    const recommendationIdx = text.indexOf("Maintain Water support pathways");

    expect(conclusionIdx).toBeGreaterThanOrEqual(0);
    expect(explanationIdx).toBeGreaterThan(conclusionIdx);
    expect(evidenceIdx).toBeGreaterThan(explanationIdx);
    expect(ruleIdx).toBeGreaterThan(evidenceIdx);
    expect(confidenceIdx).toBeGreaterThan(ruleIdx);
    expect(knowledgeIdx).toBeGreaterThan(confidenceIdx);
    expect(recommendationIdx).toBeGreaterThan(knowledgeIdx);
  });

  it("renders Explainable Analysis screen reading order when ready", () => {
    const { container } = render(<ExplainableAnalysisScreen data={readyFixture} />);

    expect(screen.getAllByLabelText("Explainable Analysis").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole("heading", { name: "Explainable Analysis" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Analysis Summary" })).toBeTruthy();
    expect(screen.getByLabelText("Day Master Strength")).toBeTruthy();
    expect(
      screen.getByRole("link", { name: "Continue to Consultation Report" }),
    ).toBeTruthy();

    const text = container.textContent ?? "";
    const summaryIdx = text.indexOf("prepared explanations without performing");
    const blockIdx = text.indexOf("Day Master Strength");
    const transitionIdx = text.indexOf("Continue to Consultation Report");

    expect(summaryIdx).toBeGreaterThanOrEqual(0);
    expect(blockIdx).toBeGreaterThan(summaryIdx);
    expect(transitionIdx).toBeGreaterThan(blockIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(
      <ExplainableAnalysisScreen data={{ status: "loading" }} />,
    );
    expect(screen.getByText("Loading explainable analysis")).toBeTruthy();

    rerender(<ExplainableAnalysisScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No explainable analysis available")).toBeTruthy();

    rerender(<ExplainableAnalysisScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Explainable analysis unavailable")).toBeTruthy();

    rerender(
      <ExplainableAnalysisScreen
        data={{ status: "error", errorMessage: "Explanation bind failed" }}
      />,
    );
    expect(screen.getByText("Unable to load explainable analysis")).toBeTruthy();
    expect(screen.getByText("Explanation bind failed")).toBeTruthy();
  });

  it("renders Pack 06 explainable business components in isolation", () => {
    render(
      <>
        <AnalysisSummary data={readyFixture.summary!} />
        <ConclusionPanel data={strengthBlock.conclusion} />
        <ExplanationPanel data={strengthBlock.explanation} />
        <EvidencePanel items={strengthBlock.evidence} />
        <RuleReferencePanel items={strengthBlock.rules} />
        <KnowledgeReferencePanel items={strengthBlock.knowledge} />
        <RecommendationPanel data={strengthBlock.recommendation!} />
        <ExplainableAnalysis blocks={readyFixture.blocks} />
      </>,
    );

    expect(screen.getAllByText("Conclusion").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Resource stem present").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Rule STR-01").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Day Master fundamentals").length).toBeGreaterThan(0);
  });

  it("wires explainable analysis styles into the business stylesheet entry", () => {
    const css = readFileSync(
      resolve(rootDir, "src/styles/components/business/index.css"),
      "utf8",
    );
    expect(css).toContain("./explainable-analysis.css");
  });
});
