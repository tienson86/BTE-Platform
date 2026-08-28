import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  FIVE_ELEMENTS,
  INTERPRETATION_BLOCKS,
  OVERVIEW_SLOTS,
  ResultWorkspace,
  SHEN_SHA_NAMES,
  TEN_GODS,
  WORKSPACE_BREAKPOINTS,
  WORKSPACE_GRID_COLUMNS,
  WORKSPACE_PANELS,
} from "../../src/features/result_workspace";

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

describe("BZ-UI-02 Canonical Panels", () => {
  it("keeps all ten frozen panels in order with desktop spans", () => {
    const { container } = render(<ResultWorkspace />);
    const cells = Array.from(container.querySelectorAll("[data-panel]"));
    expect(cells).toHaveLength(10);
    expect(cells.map((el) => el.getAttribute("data-panel"))).toEqual([
      "tu-tru",
      "overview",
      "five-elements",
      "ten-gods",
      "destiny",
      "shen-sha",
      "bone-weight",
      "luck-cycles",
      "interpretation",
      "conclusion",
    ]);
    expect(cells.map((el) => el.getAttribute("data-span"))).toEqual(["6", "4", "4", "3", "3", "4", "3", "3", "6", "4"]);
    expect(WORKSPACE_PANELS.map((panel) => panel.row)).toEqual([1, 1, 2, 2, 2, 3, 3, 3, 4, 4]);
    expect(WORKSPACE_GRID_COLUMNS).toBe(10);
  });

  it("reuses TuTruPanel without recreating four-pillar markup", () => {
    const { container } = render(<ResultWorkspace />);
    expect(container.querySelector("[data-panel='tu-tru'] [data-canonical='tu-tru-panel']")).toBeTruthy();
    expect(container.querySelectorAll("[data-canonical='tu-tru-panel']")).toHaveLength(1);
  });

  it("builds Tổng quan slots for Strength / Useful God / Hỷ / Kỵ", () => {
    const { container } = render(<ResultWorkspace />);
    const overview = container.querySelector("[data-panel='overview']");
    expect(overview?.querySelector("[data-slot='strength']")?.textContent).toContain("Thân vượng");
    expect(overview?.querySelector("[data-slot='useful-god']")?.textContent).toContain("Dụng thần");
    expect(overview?.querySelector("[data-slot='favorable-god']")?.textContent).toContain("Hỷ thần");
    expect(overview?.querySelector("[data-slot='avoid-god']")?.textContent).toContain("Kỵ thần");
    expect(overview?.querySelector("[data-slot='overview-score']")?.textContent).toContain("Điểm tổng quan");
    expect(overview?.querySelector("[data-slot='overview-confidence']")).toBeTruthy();
    expect(OVERVIEW_SLOTS).toHaveLength(4);
  });

  it("reserves five Ngũ Hành entries and a chart area", () => {
    const { container } = render(<ResultWorkspace />);
    const panel = container.querySelector("[data-panel='five-elements']");
    expect(panel?.querySelector("[data-slot='five-elements-chart']")).toBeTruthy();
    const rows = panel?.querySelectorAll("[data-slot='five-element']") ?? [];
    expect(rows).toHaveLength(5);
    expect(Array.from(rows).map((row) => row.getAttribute("data-element"))).toEqual(
      FIVE_ELEMENTS.map((el) => el.id),
    );
    expect(panel?.textContent).toContain("Mộc");
    expect(panel?.textContent).toContain("Hỏa");
    expect(panel?.textContent).toContain("Thổ");
    expect(panel?.textContent).toContain("Kim");
    expect(panel?.textContent).toContain("Thủy");
  });

  it("reserves ten canonical Thập Thần rows", () => {
    const { container } = render(<ResultWorkspace />);
    const rows = container.querySelectorAll("[data-panel='ten-gods'] [data-slot='ten-god']");
    expect(rows).toHaveLength(10);
    expect(Array.from(rows).map((row) => row.getAttribute("data-god"))).toEqual([...TEN_GODS]);
  });

  it("reserves Mệnh Cục structure", () => {
    const { container } = render(<ResultWorkspace />);
    const panel = container.querySelector("[data-panel='destiny']");
    expect(panel?.querySelector("[data-slot='destiny-pattern']")?.textContent).toContain("Cách cục");
    expect(panel?.querySelector("[data-slot='destiny-climate']")?.textContent).toContain("Điều hậu");
    expect(panel?.querySelector("[data-slot='destiny-summary']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='destiny-quality']")).toBeTruthy();
  });

  it("reserves Thần Sát list structure", () => {
    const { container } = render(<ResultWorkspace />);
    const rows = container.querySelectorAll("[data-panel='shen-sha'] [data-slot='shen-sha-row']");
    expect(rows).toHaveLength(SHEN_SHA_NAMES.length);
    expect(Array.from(rows).map((row) => row.getAttribute("data-name"))).toEqual([...SHEN_SHA_NAMES]);
  });

  it("reserves Cân Xương structure", () => {
    const { container } = render(<ResultWorkspace />);
    const panel = container.querySelector("[data-panel='bone-weight']");
    expect(panel?.querySelector("[data-slot='bone-amount']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='bone-rating']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='bone-class']")?.textContent).toContain("Phân loại");
    expect(panel?.querySelector("[data-slot='bone-preview']")).toBeTruthy();
  });

  it("reserves Đại Vận / Lưu Niên timeline structure", () => {
    const { container } = render(<ResultWorkspace />);
    const panel = container.querySelector("[data-panel='luck-cycles']");
    expect(panel?.querySelector("[data-slot='luck-current']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='luck-age']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='luck-ganzhi']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='luck-year']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='luck-timeline']")).toBeTruthy();
    expect(panel?.querySelector("[data-slot='luck-note']")).toBeTruthy();
  });

  it("reserves four interpretation reasoning blocks", () => {
    const { container } = render(<ResultWorkspace />);
    const blocks = container.querySelectorAll("[data-panel='interpretation'] [data-slot='reason-block']");
    expect(blocks).toHaveLength(4);
    expect(Array.from(blocks).map((el) => el.getAttribute("data-block"))).toEqual(
      INTERPRETATION_BLOCKS.map((block) => block.id),
    );
    expect(container.querySelector("[data-panel='interpretation']")?.textContent).toContain("Quan sát");
    expect(container.querySelector("[data-panel='interpretation']")?.textContent).toContain("Lý do");
    expect(container.querySelector("[data-panel='interpretation']")?.textContent).toContain("Tác động");
    expect(container.querySelector("[data-panel='interpretation']")?.textContent).toContain("Khuyến nghị");
  });

  it("reserves conclusion and action-chip structure", () => {
    const { container } = render(<ResultWorkspace />);
    const panel = container.querySelector("[data-panel='conclusion']");
    expect(panel?.querySelector("[data-slot='conclusion-overall']")?.textContent).toContain("Kết luận");
    expect(panel?.querySelectorAll("[data-slot='action-chip']")).toHaveLength(4);
    expect(panel?.textContent).toContain("Công việc");
    expect(panel?.textContent).toContain("Tài chính");
    expect(panel?.textContent).toContain("Quan hệ");
    expect(panel?.textContent).toContain("Sức khỏe");
  });

  it("does not import engines, call APIs, or bind ResultStore", () => {
    const joined = walkFiles(ROOT)
      .filter((file) => file.endsWith(".ts") || file.endsWith(".tsx"))
      .map((file) => readFileSync(file, "utf8"))
      .join("\n");
    expect(joined).not.toMatch(/from ["'].*engines\//);
    expect(joined).not.toMatch(/\bfetch\s*\(/);
    expect(joined).not.toMatch(/\bResultStore\b/);
    expect(joined).not.toMatch(/AnalyzeService/);
    expect(joined).not.toMatch(/useCanonicalDesktopResult/);
    const { container } = render(<ResultWorkspace />);
    expect(container.querySelector("[data-workspace]")?.getAttribute("data-binding")).toBe("none");
  });

  it("keeps production empty-state semantics and isolates preview fixture", () => {
    const empty = render(<ResultWorkspace />);
    expect(empty.container.getAttribute).toBeDefined();
    expect(empty.container.querySelector("[data-preview='off']")).toBeTruthy();
    expect(empty.container.textContent).toContain("Chờ dữ liệu");
    expect(empty.container.textContent).not.toContain("78 / 100");
    expect(empty.container.textContent).not.toContain("4 lượng 8 chỉ");
    expect(empty.container.textContent).not.toContain("Bính Ngọ");
    expect(empty.container.querySelector("[data-preview='fixture']")).toBeNull();
    empty.unmount();

    const preview = render(<ResultWorkspace preview />);
    expect(preview.container.querySelector("[data-preview='fixture']")).toBeTruthy();
    expect(preview.container.textContent).toContain("78 / 100");
    expect(preview.container.textContent).toContain("4 lượng 8 chỉ");
    expect(preview.container.textContent).toContain("Bính Ngọ");
  });

  it("keeps BZ-UI-01 responsive breakpoints", () => {
    expect(WORKSPACE_BREAKPOINTS.mobile).toBe(640);
    expect(WORKSPACE_BREAKPOINTS.tablet).toBe(1024);
    const css = readFileSync(
      resolve(dirname(fileURLToPath(import.meta.url)), "../../static/css/result_workspace.css"),
      "utf8",
    );
    expect(css).toContain("--rw-columns: 10");
    expect(css).toContain("overflow-x: hidden");
    expect(css).toContain("@media (max-width: 1023px)");
    expect(css).toContain("@media (max-width: 639px)");
  });
});
