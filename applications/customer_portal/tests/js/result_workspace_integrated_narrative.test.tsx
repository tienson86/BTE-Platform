import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { AnalysisDataDto } from "../../src/models";
import {
  EMPTY_COPY,
  ResultWorkspace,
  adaptBaziWorkspace,
} from "../../src/features/result_workspace";
import { WORKSPACE_FIELD_OWNERS, WORKSPACE_SOURCE_MAP } from "../../src/features/result_workspace/adapter";

afterEach(() => {
  cleanup();
});

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/features/result_workspace");

function walkFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    return statSync(full).isDirectory() ? walkFiles(full) : [full];
  });
}

const INTEGRATED: AnalysisDataDto["integrated_narrative"] = {
  executive_summary: { sentences: ["Tổng quan published."], available: true, insufficient: false },
  observation: { sentences: ["Quan sát published."], available: true, insufficient: false },
  reasoning: { sentences: ["Lý do published."], available: true, insufficient: false },
  impact: { sentences: ["Tác động published."], available: true, insufficient: false },
  recommendation: { sentences: ["Khuyến nghị published."], available: true, insufficient: false },
  summary: { sentences: ["Tóm tắt published."], available: true, insufficient: false },
};

function payload(extra: Partial<AnalysisDataDto> = {}): AnalysisDataDto {
  return {
    identity: {
      interpretation: {
        observation_id: "sec-observation",
        conclusion: "Kết luận canonical.",
        action: { next_action: "Hành động canonical." },
      },
    },
    strength: { strength_level: "DO-NOT-MERGE-STRENGTH" },
    useful_god: { useful_god: "DO-NOT-MERGE-USEFUL-GOD" },
    pattern: { cach_cuc: "DO-NOT-MERGE-PATTERN" },
    luck: { evidence: "DO-NOT-MERGE-LUCK" },
    narrative_result: {
      sections: [{ id: "sec-observation", paragraphs: [{ text: "DO-NOT-USE-PACK05" }] }],
    },
    integrated_narrative: INTEGRATED,
    ...extra,
  };
}

describe("BZ-CONSUME-01 Workspace IntegratedNarrative consumer", () => {
  it("Workspace consumes IntegratedNarrative only", () => {
    const viewModel = adaptBaziWorkspace(payload());
    expect(viewModel?.interpretation.executive.value).toBe("Tổng quan published.");
    expect(viewModel?.interpretation.observe.value).toBe("Quan sát published.");
    expect(viewModel?.interpretation.reason.value).toBe("Lý do published.");
    expect(viewModel?.interpretation.impact.value).toBe("Tác động published.");
    expect(viewModel?.interpretation.advice.value).toBe("Khuyến nghị published.");
    expect(viewModel?.interpretation.summary.value).toBe("Tóm tắt published.");
    expect(viewModel?.conclusion.summary.value).toBe("Tóm tắt published.");
    expect(viewModel?.conclusion.overall.value).toBe("Kết luận canonical.");
    expect(viewModel?.conclusion.action.value).toBe("Hành động canonical.");
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-block='executive']")?.textContent).toContain(
      "Tổng quan published.",
    );
    expect(container.querySelector("[data-block='observe']")?.textContent).toContain(
      "Quan sát published.",
    );
    expect(container.querySelector("[data-block='reason']")?.textContent).toContain("Lý do published.");
    expect(container.querySelector("[data-block='impact']")?.textContent).toContain(
      "Tác động published.",
    );
    expect(container.querySelector("[data-block='advice']")?.textContent).toContain(
      "Khuyến nghị published.",
    );
    expect(container.querySelector("[data-block='summary']")?.textContent).toContain(
      "Tóm tắt published.",
    );
    const panel9 = container.querySelector("[data-panel='interpretation']");
    const panel10 = container.querySelector("[data-panel='conclusion']");
    expect(panel9?.textContent).toContain("Tổng quan published.");
    expect(panel9?.textContent).toContain("Quan sát published.");
    expect(panel9?.textContent).toContain("Lý do published.");
    expect(panel9?.textContent).toContain("Tác động published.");
    expect(panel9?.textContent).toContain("Khuyến nghị published.");
    expect(panel9?.textContent).toContain("Tóm tắt published.");
    expect(panel9?.textContent).not.toContain("DO-NOT-MERGE-STRENGTH");
    expect(panel9?.textContent).not.toContain("DO-NOT-MERGE-USEFUL-GOD");
    expect(panel9?.textContent).not.toContain("DO-NOT-MERGE-PATTERN");
    expect(panel9?.textContent).not.toContain("DO-NOT-MERGE-LUCK");
    expect(panel9?.textContent).not.toContain("DO-NOT-USE-PACK05");
    expect(panel10?.textContent).not.toContain("DO-NOT-USE-PACK05");
    expect(panel10?.textContent).toContain("Tóm tắt published.");
    expect(panel10?.textContent).toContain("Kết luận canonical.");
  });

  it("does not merge topic narratives or generate executive summary", () => {
    const adapter = readFileSync(join(ROOT, "adapter/baziWorkspaceAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/compose_integrated_narrative|compose_strength_narrative/);
    expect(adapter).not.toMatch(/compose_useful_god_narrative|compose_pattern_narrative|compose_luck_narrative/);
    expect(adapter).not.toMatch(/asNarrativeResult|sectionParagraphTexts|sectionBodyById/);
    expect(adapter).not.toMatch(/deduplicate|executive summary generation|recommendation merge/i);
    expect(adapter).not.toMatch(/strength\.observation|useful_god\.observation/);
    expect(WORKSPACE_SOURCE_MAP.interpretation).toContain("integrated_narrative");
    expect(WORKSPACE_FIELD_OWNERS["interpretation.body"]).toBe("integrated_narrative");
    expect(WORKSPACE_FIELD_OWNERS["conclusion.summary"]).toBe("integrated_narrative.summary");
  });

  it("does not import topic narrative packages in Workspace", () => {
    const joined = walkFiles(ROOT)
      .filter((file) => file.endsWith(".ts") || file.endsWith(".tsx"))
      .map((file) => readFileSync(file, "utf8"))
      .join("\n");
    expect(joined).not.toMatch(/from ["'].*engines\//);
    expect(joined).not.toMatch(/narrative_framework/);
    expect(joined).not.toMatch(/compose_integrated_narrative/);
    expect(joined).not.toMatch(/from ["'].*narrativeResultAdapter/);
  });

  it("shows Chưa có dữ liệu when IntegratedNarrative is absent", () => {
    const viewModel = adaptBaziWorkspace(
      payload({
        integrated_narrative: undefined,
      }),
    );
    expect(viewModel?.interpretation.executive.available).toBe(false);
    expect(viewModel?.interpretation.observe.available).toBe(false);
    expect(viewModel?.interpretation.reason.available).toBe(false);
    expect(viewModel?.interpretation.impact.available).toBe(false);
    expect(viewModel?.interpretation.advice.available).toBe(false);
    expect(viewModel?.interpretation.summary.available).toBe(false);
    expect(viewModel?.conclusion.summary.available).toBe(false);
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const panel = container.querySelector("[data-panel='interpretation']");
    expect(panel?.textContent).toContain(EMPTY_COPY);
    expect(panel?.textContent).not.toContain("DO-NOT-MERGE-STRENGTH");
    expect(panel?.textContent).not.toContain("DO-NOT-USE-PACK05");
  });

  it("Panel 10 binds summary plus canonical conclusion without concatenating", () => {
    const viewModel = adaptBaziWorkspace(payload());
    expect(viewModel?.conclusion.summary.value).toBe("Tóm tắt published.");
    expect(viewModel?.conclusion.overall.value).toBe("Kết luận canonical.");
    expect(`${viewModel?.conclusion.summary.value} ${viewModel?.conclusion.overall.value}`).not.toBe(
      viewModel?.conclusion.overall.value,
    );
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='conclusion-summary']")?.textContent).toContain(
      "Tóm tắt published.",
    );
    expect(container.querySelector("[data-slot='conclusion-overall']")?.textContent).toContain(
      "Kết luận canonical.",
    );
    expect(container.querySelector("[data-slot='conclusion-action']")?.textContent).toContain(
      "Hành động canonical.",
    );
  });
});
