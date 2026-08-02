import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  AppendixContainer,
  AppendixScreen,
  AppendixSummary,
  CitationSection,
  CreditsSection,
  GlossarySection,
  KnowledgeReferenceSection,
  RuleReferenceSection,
  TerminologySection,
  VersionInformation,
  appendixWorkPackageId,
  type AppendixViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const readyFixture: Extract<AppendixViewModel, { status: "ready" }> = {
  status: "ready",
  header: {
    title: "Appendix",
    subtitle: "Supporting reference material",
  },
  summary: {
    title: "Appendix Summary",
    paragraphs: [
      "Prepared reference content for verification. No knowledge lookup in the UI.",
    ],
  },
  glossary: [
    { id: "g1", term: "Day Master", definition: "The Day Stem representing the native." },
  ],
  terminology: [
    {
      id: "t1",
      term: "Useful God",
      definition: "The elemental remedy preferred by the chart.",
      abbreviation: "UG",
    },
  ],
  knowledgeReferences: [
    { id: "k1", citation: "Five Elements fundamentals", source: "Knowledge catalog" },
  ],
  ruleReferences: [
    { id: "r1", citation: "Rule STR-01", source: "Strength ruleset" },
  ],
  citations: [
    { id: "c1", citation: "Classical source excerpt", source: "Prepared citation" },
  ],
  credits: {
    title: "Credits",
    paragraphs: ["Commercial UI V3 consultation packaging."],
    items: [{ id: "cr1", label: "Product", value: "BTE Platform" }],
  },
  version: {
    title: "Version Information",
    items: [
      { id: "v1", label: "UI Version", value: "3.0.0" },
      { id: "v2", label: "Work Package", value: "WP-0010" },
    ],
  },
  transition: {
    label: "Return to Consultation Report",
    href: "#consultation-report",
  },
};

const appendixBusinessFiles = [
  "AppendixContainer.tsx",
  "AppendixSummary.tsx",
  "GlossarySection.tsx",
  "TerminologySection.tsx",
  "KnowledgeReferenceSection.tsx",
  "RuleReferenceSection.tsx",
  "CitationSection.tsx",
  "CreditsSection.tsx",
  "VersionInformation.tsx",
];

const purityForbidden =
  /\b(query|lookup|fetch|generate|calculate|derive|evaluate|analyze)\s*\(/i;

describe("WP-0010 Appendix", () => {
  it("exports WP-0010 identity", () => {
    expect(appendixWorkPackageId).toBe("WP-0010");
  });

  it("appendix business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of appendixBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("appendix business components contain no knowledge lookup or analysis logic", () => {
    const offenders: string[] = [];
    for (const name of appendixBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (purityForbidden.test(source)) {
        offenders.push(name);
      }
    }
    const screenSource = readFileSync(
      resolve(rootDir, "src/screens/AppendixScreen.tsx"),
      "utf8",
    );
    if (purityForbidden.test(screenSource)) {
      offenders.push("AppendixScreen.tsx");
    }
    expect(offenders).toEqual([]);
  });

  it("renders Appendix reading order when ready", () => {
    const { container } = render(<AppendixScreen data={readyFixture} />);

    expect(screen.getByLabelText("Appendix")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Appendix" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Glossary" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Terminology" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Knowledge References" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Rule References" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Citations" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Credits" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Version Information" })).toBeTruthy();
    expect(
      screen.getByRole("link", { name: "Return to Consultation Report" }),
    ).toBeTruthy();

    const text = container.textContent ?? "";
    const glossaryIdx = text.indexOf("Day Master");
    const terminologyIdx = text.indexOf("Useful God");
    const knowledgeIdx = text.indexOf("Five Elements fundamentals");
    const ruleIdx = text.indexOf("Rule STR-01");
    const citationIdx = text.indexOf("Classical source excerpt");
    const creditsIdx = text.indexOf("Commercial UI V3 consultation packaging");
    const versionIdx = text.indexOf("WP-0010");

    expect(glossaryIdx).toBeGreaterThanOrEqual(0);
    expect(terminologyIdx).toBeGreaterThan(glossaryIdx);
    expect(knowledgeIdx).toBeGreaterThan(terminologyIdx);
    expect(ruleIdx).toBeGreaterThan(knowledgeIdx);
    expect(citationIdx).toBeGreaterThan(ruleIdx);
    expect(creditsIdx).toBeGreaterThan(citationIdx);
    expect(versionIdx).toBeGreaterThan(creditsIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(<AppendixScreen data={{ status: "loading" }} />);
    expect(screen.getByText("Loading appendix")).toBeTruthy();

    rerender(<AppendixScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No appendix available")).toBeTruthy();

    rerender(<AppendixScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Appendix unavailable")).toBeTruthy();

    rerender(
      <AppendixScreen data={{ status: "error", errorMessage: "Appendix bind failed" }} />,
    );
    expect(screen.getByText("Unable to load appendix")).toBeTruthy();
    expect(screen.getByText("Appendix bind failed")).toBeTruthy();
  });

  it("renders Pack 06 appendix business components in isolation", () => {
    render(
      <>
        <AppendixContainer>
          <AppendixSummary data={readyFixture.summary!} />
          <GlossarySection items={readyFixture.glossary} />
          <TerminologySection items={readyFixture.terminology} />
          <KnowledgeReferenceSection items={readyFixture.knowledgeReferences} />
          <RuleReferenceSection items={readyFixture.ruleReferences} />
          <CitationSection items={readyFixture.citations} />
          <CreditsSection data={readyFixture.credits} />
          <VersionInformation data={readyFixture.version} />
        </AppendixContainer>
      </>,
    );

    expect(screen.getByText("Day Master")).toBeTruthy();
    expect(screen.getByText("UG")).toBeTruthy();
    expect(screen.getByText("Five Elements fundamentals")).toBeTruthy();
    expect(screen.getByText("Rule STR-01")).toBeTruthy();
    expect(screen.getByText("BTE Platform")).toBeTruthy();
  });

  it("wires appendix styles including print rules", () => {
    const indexCss = readFileSync(
      resolve(rootDir, "src/styles/components/business/index.css"),
      "utf8",
    );
    const appendixCss = readFileSync(
      resolve(rootDir, "src/styles/components/business/appendix.css"),
      "utf8",
    );
    expect(indexCss).toContain("./appendix.css");
    expect(appendixCss).toContain("@media print");
  });
});
