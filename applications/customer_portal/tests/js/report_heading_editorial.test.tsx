import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { ReportDocumentSection } from "../../src/screens/commercial_dashboard/ReportDocumentSection";
import type { BaziReportDocumentView } from "../../src/screens/commercial_dashboard/types";

const body = "Bạn nên giữ một kế hoạch vừa sức.";
const model: BaziReportDocumentView = {
  title: "Bản luận giải", subtitle: "", fiveElements: null, luck: null,
  chapters: [
    { id: "strength_structure_useful_god", title: "Cân bằng", paragraphs: [body], bullets: [] },
    { id: "bone_weight", title: "Cân xương", paragraphs: ["Luận Cân xương 2: " + body], bullets: [] },
    { id: "life_domains", title: "Đời sống", paragraphs: ["Góc nhìn bổ sung 1: " + body], bullets: [] },
  ],
};

describe("customer report heading editorial", () => {
  it("renders meaningful React headings without legacy placeholders", () => {
    const html = renderToStaticMarkup(<ReportDocumentSection model={model} />);
    expect(html).toContain("Cân bằng toàn cục");
    expect(html).toContain("Ý nghĩa cân lượng");
    expect(html).toContain("Ứng dụng trong đời sống");
    expect(html).toContain(body);
    expect(html).not.toMatch(/Luận trục \d|Luận Cân xương \d|Góc nhìn bổ sung \d/);
  });

  it("uses the same meaningful headings in the static bridge", () => {
    const source = readFileSync(resolve("static/js/bazi_report_document_mount.js"), "utf8");
    const expose = source.replace('  if (document.readyState === "loading") {',
      '  global.__headingTest = { renderReport }; return; if (document.readyState === "loading") {');
    const host = window as unknown as { __headingTest: { renderReport: (m: BaziReportDocumentView, id: string) => HTMLElement } };
    window.eval(expose);
    const rendered = host.__headingTest.renderReport(model, "test-heading");
    expect(rendered.textContent).toContain("Cân bằng toàn cục");
    expect(rendered.textContent).toContain("Ý nghĩa cân lượng");
    expect(rendered.textContent).toContain("Ứng dụng trong đời sống");
    expect(rendered.textContent).toContain(body);
    expect(rendered.textContent).not.toMatch(/Luận trục \d|Luận Cân xương \d|Góc nhìn bổ sung \d/);
  });
});


describe("five-elements canonical narrative", () => {
  it.each([true, false])("keeps all paragraphs after the chart on both screen paths (chart=%s)", (hasChart) => {
    const paragraphs = ["Canonical lead retained.", "Second canonical paragraph.", "Final canonical paragraph."];
    const fiveModel: BaziReportDocumentView = {
      ...model,
      fiveElements: hasChart ? {
        items: [{ key: "wood", label: "Wood", count: 2 }], maxCount: 2,
        dominantLabel: "Wood", weakLabel: "Water", methodNote: "Chart method",
      } : null,
      chapters: [{ id: "five_elements", title: "Five elements", paragraphs, bullets: [] }],
    };
    const react = document.createElement("div");
    react.innerHTML = renderToStaticMarkup(<ReportDocumentSection model={fiveModel} />);
    const source = readFileSync(resolve("static/js/bazi_report_document_mount.js"), "utf8");
    const expose = source.replace('  if (document.readyState === "loading") {',
      '  global.__headingTest = { renderReport }; return; if (document.readyState === "loading") {');
    window.eval(expose);
    const host = window as unknown as { __headingTest: { renderReport: (m: BaziReportDocumentView, id: string) => HTMLElement } };
    for (const rendered of [react, host.__headingTest.renderReport(fiveModel, "five-elements")]) {
      const chapter = rendered.querySelector('[data-report-chapter="five_elements"]')!;
      const text = chapter.textContent ?? "";
      for (const paragraph of paragraphs) expect(text.split(paragraph)).toHaveLength(2);
      expect(text.indexOf(paragraphs[0])).toBeLessThan(text.indexOf(paragraphs[1]));
      expect(text.indexOf(paragraphs[1])).toBeLessThan(text.indexOf(paragraphs[2]));
      if (hasChart) expect(text.indexOf("Wood")).toBeLessThan(text.indexOf(paragraphs[0]));
    }
  });
});
