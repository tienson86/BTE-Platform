/**
 * CP-01 commercial consulting bind on Desktop V2 Knowledge zone.
 */

import { describe, expect, it } from "vitest";

import { adaptAnalysisToCanonicalDesktop } from "../../src/adapters/canonicalDesktopAdapter";
import { adaptResultPageViewModel } from "../../src/screens/result/adapters/resultPresentationAdapter";
import type { AnalysisDataDto } from "../../src/models";

const BASE: AnalysisDataDto = {
  pipeline: ["calendar", "bazi"],
  customer: { full_name: "Nguyễn Tiến Sơn" },
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
  },
};

const COMPLETE = {
  status: "complete" as const,
  sections: [
    {
      domain: "career",
      title: "Sự nghiệp",
      summary: "Tóm tắt sự nghiệp.",
      meaning: ["Ý nghĩa sự nghiệp."],
      recommendations: ["Hành động sự nghiệp."],
      source_unit_ids: ["ck-career-001"],
    },
    {
      domain: "finance",
      title: "Tài chính",
      summary: "Tóm tắt tài chính.",
      meaning: ["Ý nghĩa tài chính."],
      recommendations: ["Hành động tài chính."],
      source_unit_ids: ["ck-finance-001"],
    },
  ],
};

function knowledgeTitles(data: AnalysisDataDto): string[] {
  const desktop = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
  const page = adaptResultPageViewModel(desktop);
  return page.knowledge.sections.map((section) => section.title);
}

function consultingCopy(data: AnalysisDataDto): string {
  const desktop = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
  const page = adaptResultPageViewModel(desktop);
  return page.knowledge.sections
    .filter((section) => section.kind === "consulting")
    .map((section) =>
      [section.title, section.definition.text, section.reference.text, section.detail.text].join(
        " ",
      ),
    )
    .join(" ");
}

describe("CP-01 commercial presentation on Desktop V2", () => {
  it("P1 displays composed consulting in the Knowledge zone", () => {
    const data: AnalysisDataDto = { ...BASE, commercial_consulting: COMPLETE };
    const desktop = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
    expect(desktop.commercialConsulting?.visible).toBe(true);
    expect(desktop.commercialConsulting?.sections[0]?.sourceUnitIds).toEqual(["ck-career-001"]);
    const page = adaptResultPageViewModel(desktop);
    const consulting = page.knowledge.sections.filter((section) => section.kind === "consulting");
    expect(consulting).toHaveLength(2);
    expect(consulting[0]?.title).toBe("Sự nghiệp");
    expect(consulting[0]?.definition.text).toContain("Tóm tắt sự nghiệp.");
    expect(consulting[0]?.detail.text).toContain("Ý nghĩa sự nghiệp.");
    expect(consulting[0]?.detail.text).toContain("Hành động sự nghiệp.");
    expect(consultingCopy(data)).not.toContain("ck-career-001");
    expect(consultingCopy(data)).not.toContain("source_unit_ids");
  });

  it("P2 keeps domain order before existing knowledge sections", () => {
    const titles = knowledgeTitles({ ...BASE, commercial_consulting: COMPLETE });
    expect(titles.slice(0, 2)).toEqual(["Sự nghiệp", "Tài chính"]);
    expect(titles).toContain("Thuật ngữ");
  });

  it("P3 omits commercial advice when consulting is insufficient", () => {
    const data: AnalysisDataDto = {
      ...BASE,
      commercial_consulting: { status: "insufficient", sections: [] },
    };
    const desktop = adaptAnalysisToCanonicalDesktop(data, { source: "api" });
    expect(desktop.commercialConsulting?.visible).toBe(false);
    const page = adaptResultPageViewModel(desktop);
    const consulting = page.knowledge.sections.filter((section) => section.kind === "consulting");
    expect(consulting).toHaveLength(0);
    expect(consultingCopy(data)).not.toContain("Hành động sự nghiệp.");
    const absent = adaptResultPageViewModel(
      adaptAnalysisToCanonicalDesktop(BASE, { source: "api" }),
    );
    expect(absent.knowledge.sections.some((section) => section.kind === "consulting")).toBe(
      false,
    );
  });
});
