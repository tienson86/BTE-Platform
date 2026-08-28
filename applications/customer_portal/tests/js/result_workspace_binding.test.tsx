import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { AnalysisDataDto } from "../../src/models";
import {
  EMPTY_COPY,
  NO_RESULT_COPY,
  ResultWorkspace,
  WORKSPACE_BREAKPOINTS,
  WORKSPACE_GRID_COLUMNS,
  WORKSPACE_PANELS,
  adaptBaziWorkspace,
} from "../../src/features/result_workspace";
import { PREVIEW_FIXTURE_KIND } from "../../src/features/result_workspace/previewFixture";
import { resolveWorkspaceBoot } from "../../src/entries/workspaceBoot";
import { analysisIdOf } from "../../src/resultState/currentResult";

afterEach(() => {
  cleanup();
});

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/features/result_workspace");
const CASE_001_PATH = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../../src/features/portal/fixtures/launch_08/case_001_response.json",
);

function walkFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    return statSync(full).isDirectory() ? walkFiles(full) : [full];
  });
}

function loadCase001(): AnalysisDataDto {
  const raw = JSON.parse(readFileSync(CASE_001_PATH, "utf8")) as {
    response: { data: AnalysisDataDto };
  };
  return raw.response.data;
}

function withAnalyticalExtras(data: AnalysisDataDto): AnalysisDataDto {
  return {
    ...data,
    analysis_id: "chart-case-001",
    identity: {
      person: {
        full_name: "Nguyen Tien Son",
        gender: "male",
        solar_birth: "21/01/1987",
        lunar_birth: "22/12/Bính Dần",
        birth_time: "04:30",
        birth_place: "Ha Noi",
        timezone: "Asia/Ho_Chi_Minh",
      },
      four_pillars: {
        year: {
          stem: "Bính",
          branch: "Dần",
          can_chi: "Bính Dần",
          nayin_element: "Hỏa",
          cung_phi: "Cấn",
        },
        month: {
          stem: "Tân",
          branch: "Sửu",
          can_chi: "Tân Sửu",
          nayin_element: "Thổ",
          cung_phi: "Khôn",
        },
        day: {
          stem: "Canh",
          branch: "Ngọ",
          can_chi: "Canh Ngọ",
          nayin_element: "Thổ",
          cung_phi: "Khôn",
        },
        hour: {
          stem: "Mậu",
          branch: "Dần",
          can_chi: "Mậu Dần",
          nayin_element: "Thổ",
          cung_phi: "Cấn",
        },
      },
      bone_weight: {
        weight: "",
        classification: "",
        rating: "",
        summary: "",
      },
      luck: {
        current_cycle: "Nhâm Thân",
        current_cycle_ganzhi: "Nhâm Thân",
        current_cycle_age: "40",
        cycle_index: "1",
        reference_year: "2026",
        current_year: "2026",
        current_liunian_ganzhi: "",
        current_liunian_year: "",
      },
      interpretation: {
        observation_id: "sec-observation",
        reasoning_id: "sec-reasoning",
        recommendation_id: "sec-recommendation",
        conclusion_id: "sec-conclusion",
        conclusion:
          "Điểm tổng hợp: 51.25 — hạng D+. Họ nghề hợp bạn: ưu tiên các nhóm việc nuôi trục hỗ trợ Thực Thần trong khung Chính Ấn.",
        action: { next_action: "Giữ nhịp làm việc hiện tại." },
        section_keys: [
          "sec-observation",
          "sec-reasoning",
          "sec-impact",
          "sec-recommendation",
          "sec-conclusion",
        ],
      },
    },
    five_elements: {
      counts: { wood: 4, fire: 5, earth: 6, metal: 3, water: 1 },
      unit_total: 19,
      method_note: "Tính theo Thiên can · bản hành Địa chi · Tàng can",
    },
    score: {
      ...data.score,
      wuxing_score: 0,
      wuxing_series: [
        { label: "Mộc", value: 40 },
        { label: "Hỏa", value: 40 },
      ],
      ten_god_score: 100,
    },
    luck: {
      available: true,
      current_cycle: {
        gan_zhi: "Nhâm Thân",
        age_start: 32,
        age_end: 41,
        year_start: 2019,
        year_end: 2028,
      },
      cycles: [
        { gan_zhi: "Canh Ngọ", age_start: 22, age_end: 31 },
        { gan_zhi: "Nhâm Thân", age_start: 32, age_end: 41, year_start: 2019, year_end: 2028 },
        { gan_zhi: "Giáp Tuất", age_start: 42, age_end: 51 },
      ],
      evidence: "Chuỗi đại vận đã công bố",
    },
  };
}

describe("BZ-UI-03 Canonical Data Binding", () => {
  const data = withAnalyticalExtras(loadCase001());
  const viewModel = adaptBaziWorkspace(data, {
    analysisId: "chart-case-001",
    input: {
      full_name: "Nguyễn Tiến Sơn",
      year: 1987,
      month: 1,
      day: 21,
      hour: 4,
      minute: 30,
      timezone: "Asia/Ho_Chi_Minh",
    },
  });

  it("1. normal workspace loads current canonical result", () => {
    const boot = resolveWorkspaceBoot(
      { input: { full_name: "Nguyễn Tiến Sơn" }, data, analysis_id: "chart-case-001" },
      "",
    );
    expect(boot.preview).toBe(false);
    expect(boot.noResult).toBe(false);
    expect(boot.viewModel?.overview.usefulGod.value).toBe("Thực Thần");
    expect(boot.viewModel?.fourPillars.year.canChi).toBe("Bính Dần");
    const { container } = render(
      <ResultWorkspace viewModel={boot.viewModel} noResult={boot.noResult} />,
    );
    expect(container.querySelector("[data-binding='canonical']")).toBeTruthy();
    expect(container.textContent).toContain("Thực Thần");
    expect(container.textContent).toContain("Bính Dần");
  });

  it("2. preview fixture is not used in normal mode", () => {
    const boot = resolveWorkspaceBoot({ data, analysis_id: "chart-case-001" }, "");
    const { container } = render(<ResultWorkspace viewModel={boot.viewModel} />);
    expect(container.textContent).not.toContain("Bính Ngọ");
    expect(container.textContent).not.toContain("4 lượng 8 chỉ");
    expect(container.textContent).not.toContain("78 / 100");
    expect(container.querySelector("[data-preview='fixture']")).toBeNull();
    expect(PREVIEW_FIXTURE_KIND).toBe("bz-ui-02-preview-only");
  });

  it("3. no-result empty state", () => {
    const boot = resolveWorkspaceBoot(null, "");
    expect(boot.noResult).toBe(true);
    expect(boot.preview).toBe(false);
    const { container } = render(<ResultWorkspace noResult />);
    expect(container.querySelector("[data-empty-page='true']")?.textContent).toBe(NO_RESULT_COPY);
    expect(container.querySelector("[data-binding='none']")).toBeTruthy();
    expect(container.textContent).not.toContain("Bính Dần");
    expect(container.textContent).not.toContain("Nguyen Tien Son");
  });

  it("4. header identity binding", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='profile']")?.textContent).toContain("Nguyen Tien Son");
    expect(container.querySelector("[data-slot='gender']")?.textContent).toContain("male");
    expect(container.querySelector("[data-slot='solar-date']")?.textContent).toContain("21/01/1987");
    expect(container.querySelector("[data-slot='lunar-date']")?.textContent).toContain("22/12/Bính Dần");
    expect(container.querySelector("[data-slot='birth-time']")?.textContent).toContain("04:30");
    expect(container.querySelector("[data-slot='location']")?.textContent).toContain("Ha Noi");
    expect(container.querySelector("[data-slot='timezone']")?.textContent).toContain("Asia/Ho_Chi_Minh");
    expect(container.querySelector("[data-slot='chart-id']")?.textContent).toContain("chart-case-001");
  });

  it("5. TuTruPanel four pillars binding", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const tuTru = container.querySelector("[data-panel='tu-tru']");
    expect(tuTru?.textContent).toContain("Bính Dần");
    expect(tuTru?.textContent).toContain("Tân Sửu");
    expect(tuTru?.textContent).toContain("Canh Ngọ");
    expect(tuTru?.textContent).toContain("Mậu Dần");
    expect(viewModel?.fourPillars.year.napAm).toBe("Hỏa");
    expect(viewModel?.fourPillars.year.stem).toBe("Bính");
    expect(viewModel?.fourPillars.year.branch).toBe("Dần");
    expect(viewModel?.fourPillars.day.cungPhi).toBe("Khôn");
  });

  it("6. Strength binding", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='strength']")?.textContent).toContain("Thân vượng");
    expect(viewModel?.overview.strengthScore.value).toBe("0.87");
  });

  it("7. Useful God / Hỷ / Kỵ binding", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='useful-god']")?.textContent).toContain("Thực Thần");
    expect(container.querySelector("[data-slot='favorable-god']")?.textContent).toContain("Thương Quan");
    expect(container.querySelector("[data-slot='avoid-god']")?.textContent).toContain("Tỷ Kiên");
    expect(viewModel?.overview.usefulGod.value).not.toMatch(/Kim|Mộc|Hỏa|Thổ|Thủy/);
  });

  it("8. Five Elements binding uses analytical counts, not wuxing_score", () => {
    expect(viewModel?.fiveElements.rows.map((row) => row.count.value)).toEqual([4, 5, 6, 3, 1]);
    expect(viewModel?.fiveElements.rows.map((row) => row.percent.value)).toEqual([21, 26, 32, 16, 5]);
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const panel = container.querySelector("[data-panel='five-elements']");
    expect(panel?.textContent).toContain("21%");
    expect(panel?.textContent).not.toContain("40%");
  });

  it("9. Ten Gods binding from analytical labels", () => {
    const sat = viewModel?.tenGods.rows.find((row) => row.name === "Thất Sát / Thiên Quan");
    const jie = viewModel?.tenGods.rows.find((row) => row.name === "Kiếp Tài");
    const an = viewModel?.tenGods.rows.find((row) => row.name === "Thiên Ấn");
    expect(sat?.count.value).toBe(1);
    expect(jie?.count.value).toBe(1);
    expect(an?.count.value).toBe(1);
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-god='Thất Sát / Thiên Quan']")?.textContent).toContain("1");
  });

  it("10. Pattern binding", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='destiny-pattern']")?.textContent).toContain("Chính Ấn");
    expect(container.querySelector("[data-slot='destiny-climate']")?.textContent).toContain("Nhiệt");
  });

  it("11. ShenSha binding does not fabricate absent catalog stars", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const duc = container.querySelector("[data-name='Thiên Đức']");
    const van = container.querySelector("[data-name='Văn Xương']");
    expect(duc?.textContent).toContain("Có");
    expect(van?.textContent).toContain(EMPTY_COPY);
    expect(van?.textContent).not.toContain("Không");
  });

  it("12. Bone Weight stays unavailable without canonical field", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const panel = container.querySelector("[data-panel='bone-weight']");
    expect(panel?.textContent).toContain(EMPTY_COPY);
    expect(panel?.textContent).not.toContain("4 lượng 8 chỉ");
    expect(viewModel?.boneWeight.amount.available).toBe(false);
  });

  it("13. Luck cycles binding preserves order", () => {
    expect(viewModel?.luck.cycles.map((cycle) => cycle.ganZhi)).toEqual([
      "Canh Ngọ",
      "Nhâm Thân",
      "Giáp Tuất",
    ]);
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='luck-ganzhi']")?.textContent).toContain("Nhâm Thân");
    expect(container.querySelector("[data-slot='luck-age']")?.textContent).toContain("40");
    expect(container.querySelector("[data-slot='luck-year']")?.textContent).toContain("2026");
    const nodes = container.querySelectorAll("[data-slot='luck-timeline'] .bte-rw-timeline__node");
    expect(Array.from(nodes).map((node) => node.textContent?.trim())).toEqual([
      "Canh Ngọ",
      "Nhâm Thân",
      "Giáp Tuất",
    ]);
  });

  it("14. Interpretation binding maps narrative sections", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-block='observe']")?.textContent).toContain("Thất Sát");
    expect(container.querySelector("[data-block='reason']")?.textContent).toContain("Thực Thần");
    expect(container.querySelector("[data-block='impact']")?.textContent).toBeTruthy();
    expect(container.querySelector("[data-block='advice']")?.textContent).toBeTruthy();
    expect(viewModel?.interpretation.observe.available).toBe(true);
    expect(viewModel?.interpretation.observationId.value).toBe("sec-observation");
  });

  it("15. Conclusion binding without invented advice", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    expect(container.querySelector("[data-slot='conclusion-overall']")?.textContent).toMatch(/Điểm tổng hợp|51/);
    expect(container.querySelector("[data-slot='conclusion-action']")?.textContent).toContain("Giữ nhịp");
    const chips = container.querySelectorAll("[data-slot='action-chip']");
    expect(chips).toHaveLength(4);
    chips.forEach((chip) => expect(chip.getAttribute("data-unavailable")).toBe("true"));
  });

  it("16. same analysis ID as /result current resolver", () => {
    const stored = { data, analysis_id: "chart-case-001" };
    const boot = resolveWorkspaceBoot(stored, "");
    expect(boot.analysisId).toBe("chart-case-001");
    expect(analysisIdOf(stored)).toBe("chart-case-001");
    expect(boot.viewModel?.analysisId).toBe("chart-case-001");
    const { container } = render(<ResultWorkspace viewModel={boot.viewModel} />);
    expect(container.querySelector("[data-analysis-id]")?.getAttribute("data-analysis-id")).toBe(
      "chart-case-001",
    );
  });

  it("17. no engine imports in UI panels", () => {
    const joined = walkFiles(join(ROOT, "panels"))
      .concat(walkFiles(join(ROOT, "cards")))
      .concat(walkFiles(join(ROOT, "chrome")))
      .map((file) => readFileSync(file, "utf8"))
      .join("\n");
    expect(joined).not.toMatch(/from ["'].*engines\//);
    expect(joined).not.toMatch(/engines\.(calendar|bazi|score|pattern)/);
  });

  it("18. no Date Selection imports", () => {
    const joined = walkFiles(ROOT)
      .filter((file) => file.endsWith(".ts") || file.endsWith(".tsx"))
      .map((file) => readFileSync(file, "utf8"))
      .join("\n");
    expect(joined).not.toMatch(/date_selection/);
    expect(joined).not.toMatch(/good-date/);
  });

  it("19. no analytical calculations in frontend adapter", () => {
    const adapter = readFileSync(join(ROOT, "adapter/baziWorkspaceAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/nayin_lookup|hoa_giap|cung_phi_lookup/);
    expect(adapter).not.toMatch(/strength_score\s*\+|wuxing_score/);
    expect(adapter).toContain("presentation: count / canonical total");
    expect(adapter).not.toMatch(/from ["'].*engines\//);
  });

  it("20. fixture remains preview-only", () => {
    const withResult = resolveWorkspaceBoot({ data, analysis_id: "chart-case-001" }, "?preview=1");
    expect(withResult.preview).toBe(true);
    expect(withResult.viewModel).toBeNull();
    const { container } = render(<ResultWorkspace preview />);
    expect(container.querySelector("[data-preview='fixture']")).toBeTruthy();
    expect(container.textContent).toContain("Bính Ngọ");
    expect(container.textContent).toContain("78 / 100");
    const normal = render(<ResultWorkspace viewModel={viewModel} />);
    expect(normal.container.textContent).not.toContain("Bính Ngọ");
    expect(normal.container.textContent).toContain("Bính Dần");
  });

  it("21. desktop layout unchanged", () => {
    const { container } = render(<ResultWorkspace viewModel={viewModel} />);
    const cells = Array.from(container.querySelectorAll("[data-panel]"));
    expect(cells.map((el) => el.getAttribute("data-span"))).toEqual(["6", "4", "4", "3", "3", "4", "3", "3", "6", "4"]);
    expect(cells.map((el) => Number(el.getAttribute("data-row")))).toEqual([1, 1, 2, 2, 2, 3, 3, 3, 4, 4]);
    expect(WORKSPACE_GRID_COLUMNS).toBe(10);
    expect(WORKSPACE_PANELS).toHaveLength(10);
  });

  it("22. responsive layout unchanged", () => {
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
    expect(css).toContain("grid-column: span 5");
    expect(css).toContain("grid-column: span 10");
  });
});
