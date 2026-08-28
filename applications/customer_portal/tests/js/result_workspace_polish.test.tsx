import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  EMPTY_COPY,
  INTERPRETATION_BLOCKS,
  PREVIEW_FIXTURE_KIND,
  ResultWorkspace,
  WORKSPACE_GRID_COLUMNS,
  WORKSPACE_PANELS,
  adaptBaziWorkspace,
} from "../../src/features/result_workspace";
import { resolveWorkspaceBoot } from "../../src/entries/workspaceBoot";
import type { AnalysisDataDto } from "../../src/models";

afterEach(() => {
  cleanup();
});

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/features/result_workspace");
const CSS = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../../static/css/result_workspace.css",
);

function walkFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    return statSync(full).isDirectory() ? walkFiles(full) : [full];
  });
}

const SAMPLE: AnalysisDataDto = {
  identity: {
    person: {
      full_name: "Nguyễn Tiến Sơn",
      gender: "male",
      solar_birth: "21/01/1987",
      birth_time: "04:30",
    },
    four_pillars: {
      year: { can_chi: "Bính Dần", nayin_element: "Hỏa", cung_phi: "Cấn" },
      month: { can_chi: "Tân Sửu", nayin_element: "Thổ", cung_phi: "Khôn" },
      day: { can_chi: "Canh Ngọ", nayin_element: "Thổ", cung_phi: "Khảm" },
      hour: { can_chi: "Mậu Dần", nayin_element: "Thổ", cung_phi: "Khôn" },
    },
    luck: {
      current_cycle: "Ất Tỵ",
      current_cycle_ganzhi: "Ất Tỵ",
      current_cycle_age: "40",
      current_year: "2026",
      current_liunian_ganzhi: "Bính Ngọ",
    },
    interpretation: {
      observation_id: "sec-observation",
      conclusion: "Kết luận đã công bố.",
      action: { next_action: "Giữ nhịp." },
    },
  },
  narrative_result: {
    sections: [{ id: "sec-observation", paragraphs: [{ text: "Quan sát canonical." }] }],
  },
    luck: {
      cycles: [
        { gan_zhi: "Canh Ngọ", age_start: 22, age_end: 31 },
        { gan_zhi: "Ất Tỵ", age_start: 32, age_end: 41 },
        { gan_zhi: "Giáp Tuất", age_start: 42, age_end: 51 },
      ],
    },
};

describe("BZ-UI-04 Commercial Polish", () => {
  it("keeps frozen panel order and spans", () => {
    const { container } = render(<ResultWorkspace />);
    const cells = Array.from(container.querySelectorAll("[data-panel]"));
    expect(cells.map((el) => el.getAttribute("data-panel"))).toEqual(
      WORKSPACE_PANELS.map((panel) => panel.id),
    );
    expect(cells.map((el) => el.getAttribute("data-span"))).toEqual([
      "6", "4", "4", "3", "3", "4", "3", "3", "6", "4",
    ]);
    expect(WORKSPACE_GRID_COLUMNS).toBe(10);
  });

  it("uses the canonical card system on all ten panels", () => {
    const { container } = render(<ResultWorkspace />);
    expect(container.querySelectorAll("[data-canonical-card='true']")).toHaveLength(10);
    expect(container.querySelectorAll("[data-card-system='canonical']")).toHaveLength(10);
    expect(container.querySelector("[data-polish='BZ-UI-04']")).toBeTruthy();
  });

  it("reuses CP-01 TuTruPanel without a second visualization", () => {
    const { container } = render(<ResultWorkspace />);
    expect(container.querySelectorAll("[data-canonical='tu-tru-panel']")).toHaveLength(1);
    const source = readFileSync(join(ROOT, "cards/CanonicalWorkspaceCard.tsx"), "utf8");
    expect(source).toContain("TuTruPanel");
    expect(source).not.toMatch(/FourPillarsChart|PillarColumn/);
  });

  it("does not add engine or API computation", () => {
    const joined = walkFiles(ROOT)
      .filter((file) => file.endsWith(".ts") || file.endsWith(".tsx"))
      .map((file) => readFileSync(file, "utf8"))
      .join("\n");
    expect(joined).not.toMatch(/from ["'].*engines\//);
    expect(joined).not.toMatch(/\bfetch\s*\(/);
    expect(joined).not.toMatch(/AnalyzeService/);
  });

  it("standardizes empty copy and avoids production N/A", () => {
    const { container } = render(<ResultWorkspace />);
    expect(container.textContent).toContain(EMPTY_COPY);
    expect(container.textContent).not.toContain("N/A");
    expect(container.textContent).not.toContain("Chờ dữ liệu");
    expect(container.textContent).not.toContain("4 lượng 8 chỉ");
    const css = readFileSync(CSS, "utf8");
    expect(css).toContain(".bte-rw-empty");
  });

  it("keeps a single five-element token set", () => {
    const css = readFileSync(CSS, "utf8");
    expect(css).toContain("--rw-elem-wood");
    expect(css).toContain("--rw-elem-fire");
    expect(css).toContain("--rw-elem-earth");
    expect(css).toContain("--rw-elem-metal");
    expect(css).toContain("--rw-elem-water");
  });

  it("keeps six IntegratedNarrative interpretation blocks", () => {
    const { container } = render(<ResultWorkspace />);
    const blocks = container.querySelectorAll("[data-panel='interpretation'] [data-block]");
    expect(Array.from(blocks).map((el) => el.getAttribute("data-block"))).toEqual(
      INTERPRETATION_BLOCKS.map((block) => block.id),
    );
  });

  it("highlights the current luck cycle from identity", () => {
    const viewModel = adaptBaziWorkspace(SAMPLE);
    expect(viewModel?.luck.currentLiunian.value).toBe("Bính Ngọ");
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='luck-liunian']")?.textContent).toContain("Bính Ngọ");
    expect(container.querySelector(".bte-rw-timeline__node--now")?.textContent).toContain("Ất Tỵ");
  });

  it("prevents mobile horizontal overflow in CSS", () => {
    const css = readFileSync(CSS, "utf8");
    expect(css).toContain("overflow-x: hidden");
    expect(css).not.toMatch(/\.bte-rw__nav \{[^}]*overflow-x: auto/);
  });

  it("isolates preview fixture from production binding", () => {
    const viewModel = adaptBaziWorkspace(SAMPLE);
    const production = render(<ResultWorkspace viewModel={viewModel} />);
    expect(production.container.querySelector("[data-binding='canonical']")).toBeTruthy();
    expect(production.container.textContent).toContain("Bính Dần");
    expect(production.container.textContent).not.toContain("4 lượng 8 chỉ");
    production.unmount();
    const preview = render(<ResultWorkspace preview />);
    expect(preview.container.querySelector("[data-preview='fixture']")).toBeTruthy();
    expect(PREVIEW_FIXTURE_KIND).toBe("bz-ui-02-preview-only");
  });

  it("keeps ResultStore current-result boot unchanged", () => {
    const boot = resolveWorkspaceBoot({ data: SAMPLE, analysis_id: "chart-1" }, "");
    expect(boot.preview).toBe(false);
    expect(boot.viewModel?.person.name.value).toBe("Nguyễn Tiến Sơn");
    expect(boot.viewModel?.fourPillars.hour.canChi).toBe("Mậu Dần");
  });

  it("does not regress /result or /analyze entry points", () => {
    const resultApp = readFileSync(
      resolve(dirname(fileURLToPath(import.meta.url)), "../../src/entries/resultApp.tsx"),
      "utf8",
    );
    const analyze = readFileSync(
      resolve(dirname(fileURLToPath(import.meta.url)), "../../templates/analyze.html"),
      "utf8",
    );
    expect(resultApp).toContain("PortalPage");
    expect(resultApp).toContain("resolveResultBoot");
    expect(analyze).toContain('id="btnAnalyze"');
    const joined = walkFiles(ROOT)
      .filter((file) => file.endsWith(".ts") || file.endsWith(".tsx"))
      .map((file) => readFileSync(file, "utf8"))
      .join("\n");
    expect(joined).not.toContain("useCanonicalDesktopResult");
  });
});
