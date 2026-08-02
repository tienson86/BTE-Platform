import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  ConsultationReport,
  ConsultationReportScreen,
  PrintFooter,
  PrintHeader,
  ReportContainer,
  ReportFooter,
  ReportHeader,
  ReportProgress,
  ReportSection,
  SectionTransition,
  TableOfContents,
  consultationReportWorkPackageId,
  type ConsultationReportViewModel,
} from "../../src";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const businessDir = resolve(rootDir, "src/components/business");

afterEach(() => {
  cleanup();
});

const readyFixture: Extract<ConsultationReportViewModel, { status: "ready" }> = {
  status: "ready",
  header: {
    title: "BaZi Consultation Report",
    subtitle: "Commercial advisory document",
    clientLabel: "Client A",
    generatedLabel: "2026-08-02",
  },
  toc: [
    { id: "toc-es", label: "Executive Summary", href: "#executive-summary" },
    { id: "toc-fp", label: "Four Pillars", href: "#four-pillars" },
    { id: "toc-ei", label: "Executive Insight", href: "#executive-insight" },
    { id: "toc-m", label: "Metrics", href: "#metrics" },
    { id: "toc-ea", label: "Explainable Analysis", href: "#explainable-analysis" },
  ],
  sections: [
    {
      id: "executive-summary",
      title: "Executive Summary",
      href: "#executive-summary",
      transitionLabel: "Continue to Four Pillars",
    },
    {
      id: "four-pillars",
      title: "Four Pillars",
      href: "#four-pillars",
      transitionLabel: "Continue to Executive Insight",
    },
    {
      id: "executive-insight",
      title: "Executive Insight",
      href: "#executive-insight",
      transitionLabel: "Continue to Metrics",
    },
    {
      id: "metrics",
      title: "Metrics",
      href: "#metrics",
      transitionLabel: "Continue to Explainable Analysis",
    },
    {
      id: "explainable-analysis",
      title: "Explainable Analysis",
      href: "#explainable-analysis",
    },
  ],
  progress: 42,
  footer: {
    note: "Prepared for consultation use only.",
    copyright: "BTE Platform",
  },
  print: {
    headerTitle: "BaZi Consultation Report — Print",
    footerNote: "Confidential consultation print copy",
  },
  closing: {
    title: "Report Closing",
    body: "Thank you for reviewing this consultation report.",
  },
  executiveSummary: { status: "loading" },
  fourPillars: { status: "loading" },
  executiveInsight: { status: "loading" },
  metrics: { status: "loading" },
  explainableAnalysis: { status: "loading" },
};

const reportBusinessFiles = [
  "ConsultationReport.tsx",
  "ReportContainer.tsx",
  "ReportHeader.tsx",
  "ReportSection.tsx",
  "ReportFooter.tsx",
  "ReportProgress.tsx",
  "SectionTransition.tsx",
  "TableOfContents.tsx",
  "PrintHeader.tsx",
  "PrintFooter.tsx",
];

const purityForbidden =
  /\b(calculate|derive|evaluate|analyze|infer|transform|query)\s*\(/i;

describe("WP-0009 Consultation Report", () => {
  it("exports WP-0009 identity", () => {
    expect(consultationReportWorkPackageId).toBe("WP-0009");
  });

  it("report business components do not import Base Components directly", () => {
    const offenders: string[] = [];
    for (const name of reportBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/base["']/.test(source) || /from\s+["']\.\.\/base\//.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("report business components do not import Screens (orchestration stays in Screen)", () => {
    const offenders: string[] = [];
    for (const name of reportBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (/from\s+["']\.\.\/\.\.\/screens/.test(source) || /from\s+["']\.\.\/screens/.test(source)) {
        offenders.push(name);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("report business components contain no analysis logic", () => {
    const offenders: string[] = [];
    for (const name of reportBusinessFiles) {
      const source = readFileSync(join(businessDir, name), "utf8");
      if (purityForbidden.test(source)) {
        offenders.push(name);
      }
    }
    const screenSource = readFileSync(
      resolve(rootDir, "src/screens/ConsultationReportScreen.tsx"),
      "utf8",
    );
    if (purityForbidden.test(screenSource)) {
      offenders.push("ConsultationReportScreen.tsx");
    }
    expect(offenders).toEqual([]);
  });

  it("renders Consultation Report section order when ready", () => {
    const { container } = render(<ConsultationReportScreen data={readyFixture} />);

    expect(screen.getByLabelText("Consultation Report")).toBeTruthy();
    expect(screen.getByText("BaZi Consultation Report")).toBeTruthy();
    expect(screen.getAllByLabelText("Executive Summary").length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText("Four Pillars").length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText("Executive Insight").length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText("Metrics").length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText("Explainable Analysis").length).toBeGreaterThan(0);
    expect(screen.getByText("Report Closing")).toBeTruthy();
    expect(screen.getByText("Prepared for consultation use only.")).toBeTruthy();

    const sectionIds = Array.from(
      container.querySelectorAll<HTMLElement>("[data-report-section]"),
    ).map((node) => node.dataset.reportSection);
    expect(sectionIds).toEqual([
      "executive-summary",
      "four-pillars",
      "executive-insight",
      "metrics",
      "explainable-analysis",
    ]);

    const text = container.textContent ?? "";
    const headerIdx = text.indexOf("BaZi Consultation Report");
    const esIdx = text.indexOf("Loading executive summary");
    const fpIdx = text.indexOf("Loading four pillars");
    const eiIdx = text.indexOf("Loading executive insight");
    const metricsIdx = text.indexOf("Loading metrics");
    const eaIdx = text.indexOf("Loading explainable analysis");
    const closingIdx = text.indexOf("Thank you for reviewing");

    expect(headerIdx).toBeGreaterThanOrEqual(0);
    expect(esIdx).toBeGreaterThan(headerIdx);
    expect(fpIdx).toBeGreaterThan(esIdx);
    expect(eiIdx).toBeGreaterThan(fpIdx);
    expect(metricsIdx).toBeGreaterThan(eiIdx);
    expect(eaIdx).toBeGreaterThan(metricsIdx);
    expect(closingIdx).toBeGreaterThan(eaIdx);
  });

  it("renders loading, empty, unavailable, and error screen states", () => {
    const { rerender } = render(
      <ConsultationReportScreen data={{ status: "loading" }} />,
    );
    expect(screen.getByText("Loading consultation report")).toBeTruthy();

    rerender(<ConsultationReportScreen data={{ status: "empty" }} />);
    expect(screen.getByText("No consultation report available")).toBeTruthy();

    rerender(<ConsultationReportScreen data={{ status: "unavailable" }} />);
    expect(screen.getByText("Consultation report unavailable")).toBeTruthy();

    rerender(
      <ConsultationReportScreen
        data={{ status: "error", errorMessage: "Report assemble failed" }}
      />,
    );
    expect(screen.getByText("Unable to load consultation report")).toBeTruthy();
    expect(screen.getByText("Report assemble failed")).toBeTruthy();
  });

  it("renders Pack 06 report business components in isolation", () => {
    render(
      <>
        <ReportContainer>
          <PrintHeader title="Print Title" />
          <ReportHeader data={readyFixture.header} />
          <ReportProgress value={10} />
          <TableOfContents items={readyFixture.toc} />
          <ReportSection id="demo" title="Demo Section">
            <p>Section body</p>
          </ReportSection>
          <SectionTransition label="Next section" href="#next" />
          <ReportFooter data={readyFixture.footer} />
          <PrintFooter note="Print footer" />
        </ReportContainer>
        <ConsultationReport data={readyFixture}>
          <ReportSection id="slot" title="Slot Section">
            <span>Child slot</span>
          </ReportSection>
        </ConsultationReport>
      </>,
    );

    expect(screen.getAllByText("BaZi Consultation Report").length).toBeGreaterThan(0);
    expect(screen.getByText("Section body")).toBeTruthy();
    expect(screen.getByText("Child slot")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Next section" })).toBeTruthy();
  });

  it("wires consultation report styles including print rules", () => {
    const indexCss = readFileSync(
      resolve(rootDir, "src/styles/components/business/index.css"),
      "utf8",
    );
    const reportCss = readFileSync(
      resolve(rootDir, "src/styles/components/business/consultation-report.css"),
      "utf8",
    );
    expect(indexCss).toContain("./consultation-report.css");
    expect(reportCss).toContain("@media print");
  });
});
