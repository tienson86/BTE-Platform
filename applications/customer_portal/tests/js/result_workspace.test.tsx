import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  ResultWorkspace,
  WORKSPACE_BREAKPOINTS,
  WORKSPACE_GRID_COLUMNS,
  WORKSPACE_PANELS,
} from "../../src/features/result_workspace";

afterEach(() => {
  cleanup();
});

const PANEL_TITLES = [
  "Tứ Trụ",
  "Tổng quan lá số",
  "Ngũ Hành",
  "Thập Thần",
  "Mệnh Cục",
  "Thần Sát",
  "Cân Xương Đoán Mệnh",
  "Đại Vận / Lưu Niên",
  "Luận Giải Tổng Thể",
  "Kết Luận & Hành Động",
];

describe("BZ-UI-01 Result Workspace V2", () => {
  it("renders top navigation, sidebar, header, and workspace grid", () => {
    const { container } = render(<ResultWorkspace />);
    const root = container.querySelector("[data-workspace='bazi-result-v2']");
    expect(root).toBeTruthy();
    expect(root?.getAttribute("data-sprint")).toBe("BZ-UI-01");
    expect(root?.getAttribute("data-grid")).toBe(String(WORKSPACE_GRID_COLUMNS));
    expect(root?.getAttribute("data-architecture")).toBe("zones-rows-grid-cards");
    expect(container.querySelector("[data-chrome='top-nav']")).toBeTruthy();
    expect(container.querySelector("[data-chrome='sidebar']")).toBeTruthy();
    expect(container.querySelector("[data-chrome='header']")).toBeTruthy();
    expect(container.querySelector("[data-workspace-region='result']")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Kết quả Bát Tự" })).toBeTruthy();
    expect(screen.getByLabelText("Điều hướng chính").textContent).toContain("Kết quả");
  });

  it("places the ten approved panels on the 10-column grid", () => {
    const { container } = render(<ResultWorkspace />);
    const cells = Array.from(container.querySelectorAll("[data-panel]"));
    expect(cells).toHaveLength(10);
    expect(cells.map((el) => el.getAttribute("data-panel"))).toEqual(
      WORKSPACE_PANELS.map((panel) => panel.id),
    );
    expect(cells.map((el) => el.getAttribute("data-span"))).toEqual(
      WORKSPACE_PANELS.map((panel) => String(panel.span)),
    );
    expect(cells.map((el) => Number(el.getAttribute("data-row")))).toEqual([1, 1, 2, 2, 2, 3, 3, 3, 4, 4]);
    PANEL_TITLES.forEach((title) => {
      expect(container.textContent).toContain(title);
    });
    expect(container.querySelector("[data-grid='10']")).toBeTruthy();
    expect(WORKSPACE_GRID_COLUMNS).toBe(10);
    expect(container.querySelectorAll("[data-canonical-card='true']")).toHaveLength(10);
  });

  it("reuses TuTruPanel in panel 1 and keeps production empty-state copy", () => {
    const { container } = render(<ResultWorkspace />);
    const tuTru = container.querySelector("[data-panel='tu-tru'] [data-canonical='tu-tru-panel']");
    expect(tuTru).toBeTruthy();
    expect(tuTru?.textContent).toContain("Can Chi");
    expect(tuTru?.textContent).toContain("Nạp âm");
    expect(tuTru?.textContent).toContain("Cung Phi");
    expect(container.querySelector("[data-empty='true']")).toBeTruthy();
    expect(container.textContent).toContain("Chưa có dữ liệu");
    expect(container.textContent).not.toContain("4 lượng 8 chỉ");
  });

  it("defines desktop / tablet / mobile span behavior without inventing breakpoints", () => {
    expect(WORKSPACE_BREAKPOINTS.mobile).toBe(640);
    expect(WORKSPACE_BREAKPOINTS.tablet).toBe(1024);
    const css = readFileSync(
      resolve(dirname(fileURLToPath(import.meta.url)), "../../static/css/result_workspace.css"),
      "utf8",
    );
    expect(css).toContain("repeat(var(--rw-columns), minmax(0, 1fr))");
    expect(css).toContain("--rw-columns: 10");
    expect(css).toContain("@media (max-width: 1023px)");
    expect(css).toContain("@media (max-width: 639px)");
    expect(css).toContain("grid-column: span 5");
    expect(css).toContain("grid-column: span 10");
  });

  it("does not bind engine, API, or calculation data", () => {
    const { container } = render(<ResultWorkspace />);
    const root = container.querySelector("[data-workspace='bazi-result-v2']");
    expect(root?.getAttribute("data-binding")).toBe("none");
    expect(container.querySelector("[data-bound]")).toBeNull();
    expect(container.textContent).not.toContain("Bính Ngọ");
    const sourceFiles = [
      "ResultWorkspace.tsx",
      "layout.ts",
      "cards/CanonicalWorkspaceCard.tsx",
      "chrome/WorkspaceChrome.tsx",
      "panels/OverviewPanel.tsx",
      "catalog.ts",
    ].map((file) =>
      readFileSync(
        resolve(
          dirname(fileURLToPath(import.meta.url)),
          "../../src/features/result_workspace",
          file,
        ),
        "utf8",
      ),
    );
    const joined = sourceFiles.join("\n");
    expect(joined).not.toMatch(/engines\//);
    expect(joined).not.toMatch(/fetch\(/);
    expect(joined).not.toMatch(/AnalyzeService/);
    expect(joined).not.toMatch(/useCanonicalDesktopResult/);
  });
});
