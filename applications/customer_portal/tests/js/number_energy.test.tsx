import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { NumberEnergyPage } from "../../src/features/number_energy/NumberEnergyPage";
import { APP_NAV_ITEMS } from "../../src/layouts/Navigation";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

const RESULT_SECTIONS = [
  ["P-S00", "result-hero"],
  ["P-S01", "energy-map"],
  ["P-S02", "quick-structure"],
  ["P-S03", "wealth-flow"],
  ["P-S04", "triple-story"],
  ["P-S05", "energy-distribution"],
  ["P-S06", "domain-insights"],
  ["P-S07", "strengths-cautions"],
  ["P-S08", "score-breakdown"],
  ["P-S09", "final-assessment"],
  ["P-S10", "basis-of-assessment"],
] as const;

const FORBIDDEN_SHELL_TOKENS = [
  "UNKNOWN_OR_NOT_DEFINED",
  "HIDDEN",
  "AMPLIFIED",
  "REPEATED",
  "CONTROLLED",
  "strength_rank",
  "classification",
  "source_digits",
  "occurrence_id",
  "NEUTRALIZED",
  "INVALID_INPUT",
  "parse_error",
  "normalization_failed",
];

const SOURCE_FILES = [
  "NumberEnergyPage.tsx",
  "InputSection.tsx",
  "ResultSection.tsx",
  "formModel.ts",
  "goldenHero.ts",
  "goldenPairs.ts",
  "sections/ResultHero.tsx",
  "sections/EnergyMap.tsx",
] as const;

const HERO_FORBIDDEN_TOKENS = [
  "DIEN_NIEN",
  "THIEN_Y",
  "SINH_KHI",
  "fixture_id",
  "verified_by_runtime",
  "score_verified_by_runtime",
  "knowledge_version",
  "analysis_body",
  "328278786",
  "82%",
  "NE-PHONE-GOLDEN-0001",
];

function submitGoldenPhone(): void {
  fireEvent.submit(screen.getByTestId("input-form-region"));
}

function sourceOf(fileName: (typeof SOURCE_FILES)[number]): string {
  const here = dirname(fileURLToPath(import.meta.url));
  return readFileSync(resolve(here, `../../src/features/number_energy/${fileName}`), "utf8");
}

describe("Number Energy SB01 shell", () => {
  it("renders page shell and input region without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-phase")).toBe("sb04");
    expect(screen.getByTestId("number-energy-title").textContent).toBe("Tư vấn năng lượng số");
    expect(screen.getByTestId("page-title-area")).toBeTruthy();
    expect(screen.getByTestId("input-section").getAttribute("data-section")).toBe("NE-INPUT");
    expect(screen.getByTestId("input-form-region")).toBeTruthy();
    expect(screen.getByTestId("result-section")).toBeTruthy();
    expect(APP_NAV_ITEMS).toHaveLength(4);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("keeps canonical result section order and semantic ids", () => {
    render(<NumberEnergyPage />);
    const result = screen.getByTestId("result-section");
    const ids = Array.from(result.querySelectorAll("[data-section]")).map((node) =>
      node.getAttribute("data-section"),
    );
    expect(ids).toEqual(RESULT_SECTIONS.map(([sectionId]) => sectionId));
    for (const [sectionId, testId] of RESULT_SECTIONS) {
      expect(screen.getByTestId(testId).getAttribute("data-section")).toBe(sectionId);
    }
  });

  it("does not show technical engine tokens in the shell", () => {
    render(<NumberEnergyPage />);
    const blob = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(blob).not.toContain(token);
    }
  });

  it("uses portal tokens and a consulting page width", () => {
    const here = dirname(fileURLToPath(import.meta.url));
    const css = readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
    expect(css).toContain("max-width: 75rem");
    expect(css).toContain("var(--space-6)");
    expect(css).toContain("grid-template-columns: minmax(0, 5fr) minmax(0, 7fr)");
    expect(css).toContain("overflow-x: auto");
    expect(css).not.toContain("#ff0000");
    expect(css).not.toContain("traffic");
  });
});

describe("Number Energy SB02 input form", () => {
  it("defaults to Golden phone preview values and contextual CTA", () => {
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("analysis-type-phone_number").getAttribute("data-selected")).toBe("true");
    expect((screen.getByTestId("number-input") as HTMLInputElement).value).toBe("0328278786");
    expect(screen.getByTestId("analysis-submit").textContent).toBe("PHÂN TÍCH SỐ ĐIỆN THOẠI");
    expect((screen.getByTestId("analysis-submit") as HTMLButtonElement).disabled).toBe(false);
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("idle");
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
  });

  it("offers three analysis types and updates CTA plus field when the type changes", () => {
    render(<NumberEnergyPage />);
    fireEvent.click(screen.getByTestId("analysis-type-car_plate"));
    expect(screen.getByTestId("analysis-type-car_plate").getAttribute("data-selected")).toBe("true");
    expect((screen.getByTestId("number-input") as HTMLInputElement).value).toBe("");
    expect(screen.getByTestId("analysis-submit").textContent).toBe("PHÂN TÍCH BIỂN SỐ Ô TÔ");
    expect(screen.getByPlaceholderText("Ví dụ: 30A-123.45")).toBeTruthy();
    expect((screen.getByTestId("analysis-submit") as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByTestId("analysis-type-motorcycle_plate"));
    expect(screen.getByTestId("analysis-submit").textContent).toBe("PHÂN TÍCH BIỂN SỐ XE MÁY");
    expect(screen.getByPlaceholderText("Ví dụ: 29X1-123.45")).toBeTruthy();
  });

  it("disables the CTA when the number field is empty", () => {
    render(<NumberEnergyPage />);
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "" } });
    expect((screen.getByTestId("analysis-submit") as HTMLButtonElement).disabled).toBe(true);
  });

  it("reveals Golden preview state on submit without calling fetch", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("golden");
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(false);
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
  });

  it("shows a customer-friendly phone format error and does not reveal the result", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "abcd" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(screen.getByTestId("input-error").textContent).toContain("Số điện thoại chưa đúng định dạng");
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("idle");
    expect(fetchMock).not.toHaveBeenCalled();
    const blob = screen.getByTestId("number-energy-page").textContent || "";
    expect(blob).not.toContain("INVALID_INPUT");
    expect(blob).not.toContain("parse_error");
  });

  it("does not import live API or the previous runtime result view", () => {
    for (const fileName of SOURCE_FILES) {
      const source = sourceOf(fileName);
      expect(source).not.toContain("analyzeNumberEnergy");
      expect(source).not.toContain("from \"./api\"");
      expect(source).not.toContain("from './api'");
      expect(source).not.toContain("ResultView");
    }
  });
});

describe("Number Energy SB03 result hero", () => {
  it("shows Golden identity, score, grade, energies, and summary after submit without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("result-hero").getAttribute("data-section")).toBe("P-S00");
    expect(screen.getByTestId("hero-analysis-type").textContent).toBe("Số điện thoại");
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("hero-primary-energy").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("hero-terminal-energy").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("hero-summary").textContent).toBe(
      "Công việc và năng lực nghề nghiệp là trục nổi bật; phần cuối dãy quy về Thiên Y.",
    );
  });

  it("does not expose technical fixture or runtime fields in the hero", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const hero = screen.getByTestId("result-hero").textContent || "";
    for (const token of HERO_FORBIDDEN_TOKENS) {
      expect(hero).not.toContain(token);
    }
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(hero).not.toContain(token);
    }
  });
});

describe("Number Energy SB04 pair energy map", () => {
  const EXPECTED_PAIRS = [
    ["32", "Họa Hại", "Hung", "Nhẹ"],
    ["28", "Sinh Khí", "Cát", "Nhẹ"],
    ["82", "Sinh Khí", "Cát", "Nhẹ"],
    ["27", "Thiên Y", "Cát", "Nhẹ"],
    ["78", "Diên Niên", "Cát", "Mạnh"],
    ["87", "Diên Niên", "Cát", "Mạnh"],
    ["78", "Diên Niên", "Cát", "Mạnh"],
    ["86", "Thiên Y", "Cát", "Mạnh"],
  ] as const;

  const PAIR_FORBIDDEN_TOKENS = [
    "HOA_HAI",
    "DIEN_NIEN",
    "THIEN_Y",
    "SINH_KHI",
    "strength_rank",
    "classification",
    "T4",
    "T2",
    "T1",
  ];

  it("renders eight Golden pairs in exact order without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    const cards = screen.getByTestId("pair-strip").querySelectorAll("[data-testid^='pair-card-']");
    expect(cards).toHaveLength(8);
    const digits = Array.from(cards).map((card) => card.getAttribute("data-pair-digits"));
    expect(digits).toEqual(EXPECTED_PAIRS.map(([pairDigits]) => pairDigits));
    expect(digits.filter((value) => value === "78")).toHaveLength(2);
    EXPECTED_PAIRS.forEach((expected, index) => {
      const [pairDigits, energy, category, strength] = expected;
      expect(screen.getByTestId(`pair-digits-${index}`).textContent).toBe(pairDigits);
      expect(screen.getByTestId(`pair-energy-${index}`).textContent).toBe(energy);
      expect(screen.getByTestId(`pair-category-${index}`).textContent).toBe(category);
      expect(screen.getByTestId(`pair-strength-${index}`).textContent).toBe(strength);
    });
  });

  it("keeps the first Hung pair light and the last Thiên Y pair strong", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(screen.getByTestId("pair-card-0").getAttribute("data-pair-digits")).toBe("32");
    expect(screen.getByTestId("pair-energy-0").textContent).toBe("Họa Hại");
    expect(screen.getByTestId("pair-category-0").textContent).toBe("Hung");
    expect(screen.getByTestId("pair-strength-0").textContent).toBe("Nhẹ");
    expect(screen.getByTestId("pair-card-7").getAttribute("data-pair-digits")).toBe("86");
    expect(screen.getByTestId("pair-energy-7").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("pair-category-7").textContent).toBe("Cát");
    expect(screen.getByTestId("pair-strength-7").textContent).toBe("Mạnh");
  });

  it("does not expose technical pair metadata", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const map = screen.getByTestId("energy-map").textContent || "";
    for (const token of PAIR_FORBIDDEN_TOKENS) {
      expect(map).not.toContain(token);
    }
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(map).not.toContain(token);
    }
  });
});
