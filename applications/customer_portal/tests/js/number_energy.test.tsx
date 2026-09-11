import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { NumberEnergyPage, NUMBER_ENERGY_STATIC_UI_V1 } from "../../src/features/number_energy/NumberEnergyPage";
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
  ["P-S11", "expert-details"],
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
  "goldenQuickStructure.ts",
  "goldenWealthFlow.ts",
  "goldenTriples.ts",
  "goldenDistribution.ts",
  "goldenDomains.ts",
  "goldenStrengths.ts",
  "goldenScore.ts",
  "goldenAssessment.ts",
  "goldenBasis.ts",
  "sections/ResultHero.tsx",
  "sections/EnergyMap.tsx",
  "sections/QuickStructure.tsx",
  "sections/WealthFlow.tsx",
  "sections/TripleStory.tsx",
  "sections/EnergyDistribution.tsx",
  "sections/DomainInsights.tsx",
  "sections/StrengthsCautions.tsx",
  "sections/ScoreBreakdown.tsx",
  "sections/FinalAssessment.tsx",
  "sections/BasisOfAssessment.tsx",
  "sections/ExpertDetails.tsx",
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
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-phase")).toBe("sb16");
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

describe("Number Energy SB14.1 static golden input guard", () => {
  it("does not reveal Golden result for 0868271327 and shows the static-only message", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("static-sample-note").textContent).toContain(
      "Bản dựng tĩnh đang xem trước số mẫu 0328278786.",
    );
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "0868271327" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("input-error").textContent).toBe(
      "Bản dựng tĩnh hiện chỉ hỗ trợ số mẫu 0328278786.",
    );
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("idle");
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
  });

  it("reveals Golden result for 0328278786 without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "0868271327" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("idle");
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "0328278786" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("golden");
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(false);
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
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

describe("Number Energy SB05 quick structure", () => {
  it("shows the four Golden structure cards and supporting copy without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("quick-structure").getAttribute("data-section")).toBe("P-S02");
    expect(screen.getByTestId("qs-favorable-value").textContent).toBe("7 cặp");
    expect(screen.getByTestId("qs-challenging-value").textContent).toBe("1 cặp");
    expect(screen.getByTestId("qs-primary-value").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("qs-terminal-value").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("qs-summary").textContent).toBe(
      "Dãy nghiêng rõ về Diên Niên, đi cùng Sinh Khí và Thiên Y. Họa Hại xuất hiện ở đầu thân số nhưng được đọc tiếp trong tổ hợp Họa Hại → Sinh Khí.",
    );
  });

  it("does not imply score from Cát/Hung counts or show technical fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const section = screen.getByTestId("quick-structure").textContent || "";
    expect(section).not.toContain("87.5%");
    expect(section).not.toContain("87.5");
    expect(section).not.toContain("nên rất tốt");
    expect(section).not.toContain("score = Cát");
    expect(section).toContain("chưa phải điểm số");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(section).not.toContain("DIEN_NIEN");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("HOA_HAI");
    expect(sourceOf("sections/QuickStructure.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("goldenQuickStructure.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
  });
});

describe("Number Energy SB06 wealth flow", () => {
  const EXPECTED_STAGES = [
    ["Tài vận", "Có Thiên Y", "27 · 86", ""],
    ["Tài từ đâu?", "Quý nhân & cơ hội", "827", "Sinh Khí → Thiên Y"],
    ["Tài đi đâu?", "Sự nghiệp & lập nghiệp", "278", "Thiên Y → Diên Niên"],
    ["Hậu vận", "Thiên Y", "786", "Diên Niên → Thiên Y"],
  ] as const;

  it("renders four Golden wealth stages in order without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("wealth-flow").getAttribute("data-section")).toBe("P-S03");
    const stages = screen.getByTestId("wealth-stages").querySelectorAll("[data-testid^='wf-stage-']");
    expect(stages).toHaveLength(4);
    EXPECTED_STAGES.forEach((expected, index) => {
      const [label, headline, evidence, interaction] = expected;
      expect(screen.getByTestId(`wf-label-${index}`).textContent).toBe(label);
      expect(screen.getByTestId(`wf-headline-${index}`).textContent).toBe(headline);
      expect(screen.getByTestId(`wf-evidence-${index}`).textContent).toBe(evidence);
      if (interaction) {
        expect(screen.getByTestId(`wf-interaction-${index}`).textContent).toBe(interaction);
      } else {
        expect(screen.queryByTestId(`wf-interaction-${index}`)).toBeNull();
      }
    });
    expect(screen.getByTestId("wf-story-0").textContent).toBe("Quý nhân & cơ hội");
    expect(screen.getByTestId("wf-story-1").textContent).toBe("Tài");
    expect(screen.getByTestId("wf-story-2").textContent).toBe("Sự nghiệp");
    expect(screen.getByTestId("wf-story-3").textContent).toBe("Tài");
  });

  it("does not show financial guarantees or technical wealth fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const section = screen.getByTestId("wealth-flow").textContent || "";
    expect(section).not.toContain("rất giàu");
    expect(section).not.toContain("chắc chắn");
    expect(section).not.toContain("phát tài");
    expect(section).not.toContain("primary_wealth_node");
    expect(section).not.toContain("strongest_wealth_node");
    expect(section).not.toContain("PRIMARY_WEALTH");
    expect(section).not.toContain("interaction_id");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("SINH_KHI");
    expect(section).not.toContain("DIEN_NIEN");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(sourceOf("sections/WealthFlow.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("goldenWealthFlow.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
  });
});

describe("Number Energy SB07 triple story", () => {
  const EXPECTED_TRIPLES = [
    ["328", "Khẩu tài tốt", "Họa Hại", "Sinh Khí", "standard"],
    ["282", "Quý nhân và cơ hội được tăng cường", "Sinh Khí", "Sinh Khí", "standard"],
    ["827", "Quý nhân mang đến Tài vận", "Sinh Khí", "Thiên Y", "featured"],
    ["278", "Tài đi vào sự nghiệp", "Thiên Y", "Diên Niên", "featured"],
    ["787", "Năng lực nghề nghiệp được tăng cường", "Diên Niên", "Diên Niên", "compact"],
    ["878", "Năng lực nghề nghiệp được tăng cường", "Diên Niên", "Diên Niên", "compact"],
    ["786", "Năng lực nghề nghiệp tạo Tài", "Diên Niên", "Thiên Y", "featured"],
  ] as const;

  it("renders seven Golden triples in exact chronological order without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("triple-story").getAttribute("data-section")).toBe("P-S04");
    const cards = screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']");
    expect(cards).toHaveLength(7);
    const digits = Array.from(cards).map((card) => card.getAttribute("data-triple-digits"));
    expect(digits).toEqual(EXPECTED_TRIPLES.map(([value]) => value));
    expect(digits.filter((value) => value === "787" || value === "878")).toEqual(["787", "878"]);
    EXPECTED_TRIPLES.forEach((expected, index) => {
      const [tripleDigits, title, source, target, priority] = expected;
      expect(screen.getByTestId(`triple-digits-${index}`).textContent).toBe(tripleDigits);
      expect(screen.getByTestId(`triple-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`triple-source-${index}`).textContent).toBe(source);
      expect(screen.getByTestId(`triple-target-${index}`).textContent).toBe(target);
      expect(screen.getByTestId(`triple-card-${index}`).getAttribute("data-priority")).toBe(priority);
    });
  });

  it("keeps featured triples visually marked without reordering or leaking technical fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(screen.getByTestId("triple-card-2").getAttribute("data-triple-digits")).toBe("827");
    expect(screen.getByTestId("triple-card-3").getAttribute("data-triple-digits")).toBe("278");
    expect(screen.getByTestId("triple-card-6").getAttribute("data-triple-digits")).toBe("786");
    expect(screen.getByTestId("triple-card-2").getAttribute("data-priority")).toBe("featured");
    expect(screen.getByTestId("triple-card-3").getAttribute("data-priority")).toBe("featured");
    expect(screen.getByTestId("triple-card-6").getAttribute("data-priority")).toBe("featured");
    const section = screen.getByTestId("triple-story").textContent || "";
    expect(section).not.toContain("PRIMARY_WEALTH");
    expect(section).not.toContain("TERMINAL_WEALTH");
    expect(section).not.toContain("fixture_id");
    expect(section).not.toContain("knowledge_version");
    expect(section).not.toContain("FEATURED");
    expect(section).not.toContain("COMPACT");
    expect(section).not.toContain("HOA_HAI");
    expect(section).not.toContain("DIEN_NIEN");
    expect(section).not.toContain("generic");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(sourceOf("sections/TripleStory.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("goldenTriples.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
  });
});

describe("Number Energy SB08-A energy distribution", () => {
  const EXPECTED_DISTRIBUTION = [
    ["Sinh Khí", "2", "secondary", "Phụ trợ"],
    ["Thiên Y", "2", "secondary", "Phụ trợ"],
    ["Diên Niên", "3", "primary", "Chủ đạo"],
    ["Phục Vị", "0", "none", ""],
    ["Họa Hại", "1", "none", ""],
    ["Ngũ Quỷ", "0", "none", ""],
    ["Lục Sát", "0", "none", ""],
    ["Tuyệt Mệnh", "0", "none", ""],
  ] as const;

  it("renders eight Golden energy counts in canonical order without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("energy-distribution").getAttribute("data-section")).toBe("P-S05");
    const rows = screen.getByTestId("energy-distribution-list").querySelectorAll("[data-testid^='dist-row-']");
    expect(rows).toHaveLength(8);
    EXPECTED_DISTRIBUTION.forEach((expected, index) => {
      const [label, count, role, roleLabel] = expected;
      expect(screen.getByTestId(`dist-name-${index}`).textContent).toBe(label);
      expect(screen.getByTestId(`dist-count-${index}`).textContent).toBe(count);
      expect(screen.getByTestId(`dist-row-${index}`).getAttribute("data-energy-role")).toBe(role);
      if (roleLabel) {
        expect(screen.getByTestId(`dist-role-${index}`).textContent).toBe(roleLabel);
      } else {
        expect(screen.queryByTestId(`dist-role-${index}`)).toBeNull();
      }
    });
  });

  it("treats counts as distribution, not score, and hides technical fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const section = screen.getByTestId("energy-distribution").textContent || "";
    expect(section).toContain("không phải điểm số");
    expect(section).not.toContain("87.5%");
    expect(section).not.toContain("87.5");
    expect(section).not.toContain("%");
    expect(section).not.toContain("SINH_KHI");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("DIEN_NIEN");
    expect(section).not.toContain("HOA_HAI");
    expect(section).not.toContain("rank");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(sourceOf("sections/EnergyDistribution.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("goldenDistribution.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
  });
});

describe("Number Energy SB08-B domain insights", () => {
  const EXPECTED_DOMAINS = [
    ["Tài vận", "Có đường Tài tương đối rõ"],
    ["Công việc & sự nghiệp", "Đây là một trong những điểm mạnh nhất của dãy"],
    ["Tình cảm & quan hệ", "Quan hệ xã hội có yếu tố hỗ trợ"],
    ["Tính cách & năng lực", "Trách nhiệm và năng lực làm việc khá rõ"],
    ["Cân bằng trường khí", "Cát tinh giữ vai trò chủ đạo"],
  ] as const;

  it("renders five Golden domain cards in order without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("domain-insights").getAttribute("data-section")).toBe("P-S06");
    const cards = screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']");
    expect(cards).toHaveLength(5);
    const conclusions = EXPECTED_DOMAINS.map(([, conclusion]) => conclusion);
    expect(new Set(conclusions).size).toBe(5);
    EXPECTED_DOMAINS.forEach((expected, index) => {
      const [title, conclusion] = expected;
      expect(screen.getByTestId(`domain-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`domain-conclusion-${index}`).textContent).toBe(conclusion);
      expect(screen.getByTestId(`domain-narrative-${index}`).textContent).toBeTruthy();
    });
    expect(screen.getByTestId("domain-caution-0").textContent).toContain("không nên hiểu Thiên Y như một cam kết tài chính");
    expect(screen.queryByText("Giao tiếp & nhân duyên")).toBeNull();
  });

  it("keeps domain copy distinct and avoids guarantees or technical fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const narratives = [0, 1, 2, 3, 4].map(
      (index) => screen.getByTestId(`domain-narrative-${index}`).textContent || "",
    );
    expect(new Set(narratives).size).toBe(5);
    const section = screen.getByTestId("domain-insights").textContent || "";
    expect(section).not.toContain("rất giàu");
    expect(section).not.toContain("chắc chắn");
    expect(section).not.toContain("chẩn đoán");
    expect(section).not.toContain("kết hôn");
    expect(section).not.toContain("số phận");
    expect(section).not.toContain("Có Thiên Y");
    expect(section).not.toContain("27 · 86");
    expect(section).not.toContain("SINH_KHI");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("DIEN_NIEN");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(sourceOf("sections/DomainInsights.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("goldenDomains.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
    expect(sourceOf("goldenDomains.ts")).not.toContain("GOLDEN_WEALTH_STAGES");
  });
});

describe("Number Energy SB09 strengths and cautions", () => {
  const EXPECTED_STRENGTHS = [
    [
      "Quý nhân có thể mở đường cho Tài",
      "Quan hệ, người hỗ trợ hoặc những cơ hội thuận lợi có thể trở thành một trong những con đường hình thành Tài.",
    ],
    [
      "Năng lực nghề nghiệp nổi bật",
      "Diên Niên được lặp lại liên tiếp, làm công việc, trách nhiệm và năng lực nghề nghiệp trở thành chủ đề mạnh của dãy.",
    ],
    [
      "Công việc có khả năng tạo thành quả",
      "Phần cuối dãy tiếp tục đưa năng lực nghề nghiệp về Thiên Y, làm rõ hơn con đường tạo Tài bằng chuyên môn và công việc.",
    ],
    [
      "Khẩu tài có thể phát huy tích cực",
      "Khả năng nói và diễn đạt có giá trị khi được sử dụng đúng cách, đặc biệt trong giao tiếp và công việc với con người.",
    ],
  ] as const;

  const EXPECTED_CAUTIONS = [
    [
      "Cần chú ý cách sử dụng lời nói",
      "Họa Hại xuất hiện ở đầu thân số, vì vậy lời nói và cách phản ứng vẫn là một điểm cần tiết chế. Khi dùng tốt, bộ 328 lại phát huy thành khẩu tài.",
    ],
    [
      "Không nên chỉ nhìn số lượng Cát tinh",
      "Dãy có nhiều Cát tinh, nhưng giá trị thực tế vẫn nằm ở cách các trường khí nối tiếp và vận động với nhau.",
    ],
  ] as const;

  function cssSource(): string {
    const here = dirname(fileURLToPath(import.meta.url));
    return readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
  }

  it("renders four Golden strengths and fixture cautions without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-section")).toBe("P-S07");
    expect(screen.getByTestId("strengths-column").textContent).toContain("Điểm mạnh");
    expect(screen.getByTestId("cautions-column").textContent).toContain("Điểm cần lưu ý");
    expect(screen.getByTestId("strength-list").querySelectorAll("[data-testid^='strength-card-']")).toHaveLength(4);
    expect(screen.getByTestId("caution-list").querySelectorAll("[data-testid^='caution-card-']")).toHaveLength(2);
    EXPECTED_STRENGTHS.forEach(([title, copy], index) => {
      expect(screen.getByTestId(`strength-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`strength-copy-${index}`).textContent).toBe(copy);
    });
    EXPECTED_CAUTIONS.forEach(([title, copy], index) => {
      expect(screen.getByTestId(`caution-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`caution-copy-${index}`).textContent).toBe(copy);
    });
  });

  it("keeps cautions practical and avoids guarantees or technical fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const section = screen.getByTestId("strengths-cautions").textContent || "";
    expect(section).not.toContain("rất giàu");
    expect(section).not.toContain("chắc chắn");
    expect(section).not.toContain("chẩn đoán");
    expect(section).not.toContain("số phận");
    expect(section).not.toContain("định mệnh");
    expect(section).not.toContain("cảnh báo");
    expect(section).not.toContain("SINH_KHI");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("DIEN_NIEN");
    expect(section).not.toContain("HOA_HAI");
    expect(section).not.toContain("fixture_id");
    expect(section).not.toContain("knowledge_version");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    const css = cssSource();
    expect(css).toContain(".ne-findings-grid");
    expect(css).toMatch(/\.ne-findings-grid\s*\{[^}]*grid-template-columns:\s*minmax\(0,\s*1fr\)\s+minmax\(0,\s*1fr\)/s);
    expect(css).toMatch(/@media \(max-width: 1024px\)[\s\S]*\.ne-findings-grid/);
    expect(sourceOf("sections/StrengthsCautions.tsx")).not.toContain("--danger");
    expect(sourceOf("sections/StrengthsCautions.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("sections/StrengthsCautions.tsx")).not.toContain("goldenTriples");
    expect(sourceOf("sections/StrengthsCautions.tsx")).not.toContain("goldenDistribution");
    expect(sourceOf("sections/StrengthsCautions.tsx")).not.toContain("goldenDomains");
    expect(sourceOf("goldenStrengths.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
    expect(sourceOf("goldenStrengths.ts")).not.toContain("GOLDEN_WEALTH_STAGES");
    expect(sourceOf("goldenStrengths.ts")).not.toContain("GOLDEN_DOMAIN_INSIGHTS");
  });
});

describe("Number Energy SB10 score breakdown", () => {
  const EXPECTED_DIMENSIONS = [
    ["Cấu trúc năng lượng", "21 / 25"],
    ["Dòng tài vận", "22 / 25"],
    ["Công việc & trợ lực", "17 / 20"],
    ["Ổn định & rủi ro", "10 / 15"],
    ["Năng lượng kết", "12 / 15"],
  ] as const;

  const EXPECTED_REASONS = [
    [
      "Cấu trúc Cát giữ vai trò chủ đạo",
      "Sinh Khí, Thiên Y và Diên Niên chiếm phần lớn thân số.",
    ],
    [
      "Dòng Tài có nguồn rõ",
      "Sinh Khí → Thiên Y cho thấy quý nhân và cơ hội có khả năng dẫn tới Tài.",
    ],
    [
      "Công việc là trục mạnh",
      "Diên Niên xuất hiện liên tiếp và tiếp tục dẫn tới Thiên Y ở phần cuối dãy.",
    ],
    [
      "Họa Hại cần được sử dụng đúng cách",
      "Họa Hại xuất hiện ở đầu thân số, nhưng tổ hợp tiếp theo là Họa Hại → Sinh Khí, giúp khả năng giao tiếp có hướng phát huy tích cực.",
    ],
  ] as const;

  it("renders Golden illustrative score, breakdown, and reasons without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("score-breakdown").getAttribute("data-section")).toBe("P-S08");
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("score-static-note").textContent).toContain("điểm minh họa của bản dựng tĩnh");
    expect(screen.getByTestId("score-static-note").textContent).toContain("chưa phải điểm đã được đối chiếu");
    const rows = screen.getByTestId("score-dimension-list").querySelectorAll("[data-testid^='score-row-']");
    expect(rows).toHaveLength(5);
    EXPECTED_DIMENSIONS.forEach(([label, points], index) => {
      expect(screen.getByTestId(`score-dim-label-${index}`).textContent).toBe(label);
      expect(screen.getByTestId(`score-dim-points-${index}`).textContent).toBe(points);
    });
    expect(screen.getByTestId("score-reason-list").querySelectorAll("[data-testid^='score-reason-card-']")).toHaveLength(4);
    EXPECTED_REASONS.forEach(([title, copy], index) => {
      expect(screen.getByTestId(`score-reason-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`score-reason-copy-${index}`).textContent).toBe(copy);
    });
  });

  it("does not convert score to percent or expose runtime/technical fields", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const section = screen.getByTestId("score-breakdown").textContent || "";
    expect(section).not.toContain("%");
    expect(section).not.toContain("82%");
    expect(section).not.toContain("87.5");
    expect(section).not.toContain("87,5");
    expect(section).not.toContain("thuật toán");
    expect(section).not.toContain("coefficient");
    expect(section).not.toContain("verified_by_runtime");
    expect(section).not.toContain("presentation_fixture");
    expect(section).not.toContain("fixture_id");
    expect(section).not.toContain("knowledge_version");
    expect(section).not.toContain("SINH_KHI");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("DIEN_NIEN");
    expect(section).not.toContain("HOA_HAI");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(sourceOf("sections/ScoreBreakdown.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("sections/ScoreBreakdown.tsx")).not.toContain("goldenTriples");
    expect(sourceOf("sections/ScoreBreakdown.tsx")).not.toContain("goldenDistribution");
    expect(sourceOf("sections/ScoreBreakdown.tsx")).not.toContain("goldenHero");
    expect(sourceOf("goldenScore.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
    expect(sourceOf("goldenScore.ts")).not.toContain("GOLDEN_ENERGY_DISTRIBUTION");
    expect(sourceOf("goldenScore.ts")).not.toContain("reduce(");
    expect(sourceOf("goldenScore.ts")).not.toContain("earned / max");
  });
});

describe("Number Energy SB11 final assessment", () => {
  const EXPECTED_FLOW = ["QUÝ NHÂN", "TÀI", "SỰ NGHIỆP", "TÀI"] as const;

  it("renders Golden assessment, story flow, and recommendation without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("final-assessment").getAttribute("data-section")).toBe("P-S09");
    expect(screen.getByTestId("assessment-title").textContent).toBe("Đánh giá tổng thể");
    expect(screen.getByTestId("assessment-story").textContent).toContain(
      "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y.",
    );
    expect(screen.getByTestId("assessment-story").textContent).toContain(
      "Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy.",
    );
    EXPECTED_FLOW.forEach((node, index) => {
      expect(screen.getByTestId(`assessment-flow-${index}`).textContent).toBe(node);
    });
    expect(screen.getByTestId("recommendation-title").textContent).toBe("Khuyến nghị");
    expect(screen.getByTestId("recommendation-state").textContent).toBe("PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG");
    expect(screen.getByTestId("recommendation-supporting").textContent).toBe(
      "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài.",
    );
  });

  it("avoids sales, guarantees, and technical leakage", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const section = screen.getByTestId("final-assessment").textContent || "";
    expect(section).not.toContain("đổi sim ngay");
    expect(section).not.toContain("mua số mới");
    expect(section).not.toContain("không dùng được");
    expect(section).not.toContain("chắc chắn");
    expect(section).not.toContain("rất giàu");
    expect(section).not.toContain("số phận");
    expect(section).not.toContain("định mệnh");
    expect(section).not.toContain("chẩn đoán");
    expect(section).not.toContain("verified_by_runtime");
    expect(section).not.toContain("presentation_fixture");
    expect(section).not.toContain("fixture_id");
    expect(section).not.toContain("knowledge_version");
    expect(section).not.toContain("SINH_KHI");
    expect(section).not.toContain("THIEN_Y");
    expect(section).not.toContain("DIEN_NIEN");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(section).not.toContain(token);
    }
    expect(sourceOf("sections/FinalAssessment.tsx")).not.toContain("goldenScore");
    expect(sourceOf("sections/FinalAssessment.tsx")).not.toContain("goldenWealthFlow");
    expect(sourceOf("sections/FinalAssessment.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("goldenAssessment.ts")).not.toContain("GOLDEN_SCORE_TOTAL");
    expect(sourceOf("goldenAssessment.ts")).not.toContain("GOLDEN_WEALTH_STORY");
    expect(sourceOf("goldenAssessment.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
  });
});

describe("Number Energy SB12 basis and expert seam", () => {
  const EXPECTED_PRINCIPLES = [
    "Dựa trên 8 cặp năng lượng chính.",
    "Dựa trên các bộ ba nổi bật.",
    "Dựa trên dòng Tài vận.",
    "Dựa trên năng lượng kết.",
    "Dựa trên điểm minh họa tĩnh.",
  ] as const;

  const EXPECTED_EVIDENCE = [
    ["32 · Họa Hại", "28 / 82 · Sinh Khí", "27 / 86 · Thiên Y", "78 / 87 / 78 · Diên Niên"],
    ["827 · Sinh Khí → Thiên Y", "278 · Thiên Y → Diên Niên", "786 · Diên Niên → Thiên Y"],
    ["82 / 100 · TỐT"],
  ] as const;

  it("renders Golden customer basis evidence without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("basis-of-assessment").getAttribute("data-section")).toBe("P-S10");
    expect(screen.getByTestId("basis-helper").textContent).toContain("không chỉ dựa trên số lượng Cát và Hung");
    EXPECTED_PRINCIPLES.forEach((principle, index) => {
      expect(screen.getByTestId(`basis-principle-${index}`).textContent).toBe(principle);
    });
    expect(screen.getByTestId("basis-highlight-label-0").textContent).toBe("Trường nổi bật");
    expect(screen.getByTestId("basis-highlight-value-0").textContent).toBe("Diên Niên · Thiên Y · Sinh Khí");
    expect(screen.getByTestId("basis-highlight-value-1").textContent).toBe("86 · Thiên Y");
    expect(screen.getByTestId("basis-highlight-value-2").textContent).toBe("8 cặp · 7 Cát · 1 Hung");
    EXPECTED_EVIDENCE.forEach((items, groupIndex) => {
      items.forEach((item, itemIndex) => {
        expect(screen.getByTestId(`basis-item-${groupIndex}-${itemIndex}`).textContent).toBe(item);
      });
    });
  });

  it("keeps the expert seam present but hidden and free of runtime binding", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    const expert = screen.getByTestId("expert-details");
    expect(expert.getAttribute("data-section")).toBe("P-S11");
    expect(expert.hasAttribute("hidden")).toBe(true);
    expect(expert.getAttribute("aria-hidden")).toBe("true");
    expect(screen.getByTestId("expert-seam-note").textContent).toContain("Khe kiểm tra cho bước sau");
    expect(screen.getByTestId("expert-seam-note").textContent).toContain("chưa phải liên kết với kết quả vận hành thực");
    const basis = screen.getByTestId("basis-of-assessment").textContent || "";
    expect(basis).not.toContain("fixture_id");
    expect(basis).not.toContain("presentation_fixture");
    expect(basis).not.toContain("score_verified_by_runtime");
    expect(basis).not.toContain("verified_by_runtime");
    expect(basis).not.toContain("knowledge_version");
    expect(basis).not.toContain("SINH_KHI");
    expect(basis).not.toContain("THIEN_Y");
    expect(basis).not.toContain("DIEN_NIEN");
    expect(basis).not.toContain("82%");
    expect(basis).not.toContain("87.5");
    for (const token of FORBIDDEN_SHELL_TOKENS) {
      expect(basis).not.toContain(token);
    }
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("expert=true");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("URLSearchParams");
    expect(sourceOf("ResultSection.tsx")).not.toContain("expert=true");
    expect(sourceOf("sections/ExpertDetails.tsx")).not.toContain("fixture_id");
    expect(sourceOf("sections/ExpertDetails.tsx")).not.toContain("analyzeNumberEnergy");
    expect(sourceOf("sections/BasisOfAssessment.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("sections/BasisOfAssessment.tsx")).not.toContain("goldenScore");
    expect(sourceOf("goldenBasis.ts")).not.toContain("GOLDEN_PHONE_PAIRS");
    expect(sourceOf("goldenBasis.ts")).not.toContain("GOLDEN_SCORE_TOTAL");
  });
});

describe("Number Energy SB13 responsive polish", () => {
  function cssSource(): string {
    const here = dirname(fileURLToPath(import.meta.url));
    return readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
  }

  it("keeps Golden sections readable and expert hidden without fetching", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-phase")).toBe("sb16");
    expect(screen.getByTestId("analysis-submit").textContent).toBe("PHÂN TÍCH SỐ ĐIỆN THOẠI");
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("pair-strip").querySelectorAll("[data-testid^='pair-card-']")).toHaveLength(8);
    expect(screen.getByTestId("wealth-stages").querySelectorAll("[data-testid^='wf-stage-']")).toHaveLength(4);
    expect(screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']")).toHaveLength(5);
    expect(screen.getByTestId("recommendation-state").textContent).toBe("PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
  });

  it("locks page overflow except the approved Pair Map scroll and stacks mobile sections", () => {
    const css = cssSource();
    expect(css).toMatch(/\.ne-page\s*\{[^}]*overflow-x:\s*hidden/s);
    expect(css).toMatch(/\.ne-pair-strip-scroller\s*\{[^}]*overflow-x:\s*auto/s);
    expect(css).not.toMatch(/\.ne-pair-strip\s*\{[^}]*overflow-x:\s*auto/s);
    expect(css).toMatch(/\.ne-pair-card\s*\{[^}]*min-width:\s*8\.25rem/s);
    expect(css).toMatch(
      /@media \(max-width: 1024px\)[\s\S]*\.ne-wealth-stages\s*\{[\s\S]*flex-direction:\s*column/,
    );
    expect(css).toMatch(
      /@media \(max-width: 1024px\)[\s\S]*\.ne-findings-grid[\s\S]*grid-template-columns:\s*minmax\(0,\s*1fr\)/,
    );
    expect(css).toMatch(
      /@media \(max-width: 768px\)[\s\S]*\.ne-triple-list\s*\{[\s\S]*grid-template-columns:\s*minmax\(0,\s*1fr\)/,
    );
    expect(css).toContain(".ne-expert[hidden]");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("expert=true");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("analyzeNumberEnergy");
    expect(sourceOf("sections/EnergyMap.tsx")).not.toContain("from \"./api\"");
    expect(sourceOf("sections/WealthFlow.tsx")).not.toContain("from \"./api\"");
    expect(sourceOf("sections/ScoreBreakdown.tsx")).not.toContain("from \"./api\"");
  });
});

describe("Number Energy SB14 accessibility", () => {
  it("exposes form labels, required state, CTA name, and invalid errors", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByRole("heading", { level: 1, name: "Tư vấn năng lượng số" })).toBeTruthy();
    expect(screen.getByRole("heading", { level: 2, name: "Nhập số cần phân tích" })).toBeTruthy();
    expect(screen.getByRole("radio", { name: "Số điện thoại" })).toBeTruthy();
    expect(screen.getByRole("radio", { name: "Biển số ô tô" })).toBeTruthy();
    expect(screen.getByRole("radio", { name: "Biển số xe máy" })).toBeTruthy();
    const numberInput = screen.getByRole("textbox", { name: /Số điện thoại/ });
    expect(numberInput.getAttribute("aria-required")).toBe("true");
    expect(numberInput.getAttribute("aria-invalid")).toBe("false");
    expect((numberInput as HTMLInputElement).labels?.[0]?.textContent).toContain("Bắt buộc");
    expect(screen.getByRole("button", { name: "PHÂN TÍCH SỐ ĐIỆN THOẠI" })).toBeTruthy();
    fireEvent.change(numberInput, { target: { value: "abcd" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(screen.getByRole("alert").textContent).toContain("Số điện thoại chưa đúng định dạng");
    expect(numberInput.getAttribute("aria-invalid")).toBe("true");
    expect(numberInput.getAttribute("aria-describedby")).toContain(screen.getByTestId("input-error").id);
  });

  it("keeps result headings, textual Cát/Hung, score text, and a hidden expert seam", () => {
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(screen.getByTestId("form-status").textContent).toBe("Đã hiện kết quả minh họa.");
    const headings = Array.from(screen.getByTestId("number-energy-page").querySelectorAll("h1, h2")).map(
      (node) => node.tagName,
    );
    expect(headings[0]).toBe("H1");
    expect(headings.slice(1).every((tag) => tag === "H2")).toBe(true);
    expect(screen.getByTestId("pair-category-0").textContent).toBe("Hung");
    expect(screen.getByTestId("pair-category-1").textContent).toBe("Cát");
    expect(screen.getByTestId("pair-strip-scroller").getAttribute("role")).toBe("region");
    expect(screen.getByTestId("pair-strip-scroller").getAttribute("tabindex")).toBe("0");
    expect(screen.getByTestId("score-dim-points-0").textContent).toBe("21 / 25");
    expect(screen.getByTestId("score-row-0").querySelector("[role='meter']")?.getAttribute("aria-valuetext")).toBe(
      "21 / 25",
    );
    const expert = screen.getByTestId("expert-details");
    expect(expert.hasAttribute("hidden")).toBe(true);
    expect(expert.getAttribute("aria-hidden")).toBe("true");
    expect(expert.hasAttribute("inert")).toBe(true);
    const page = screen.getByTestId("number-energy-page").textContent || "";
    expect(page).not.toContain("fixture_id");
    expect(page).not.toContain("strength_rank");
    expect(page).not.toContain("verified_by_runtime");
  });

  it("keeps visible focus styles and does not wire a keyboard trap into Expert Mode", () => {
    const here = dirname(fileURLToPath(import.meta.url));
    const css = readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
    expect(css).toContain(".ne-page :focus-visible");
    expect(css).toContain(".ne-sr-only");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("expert=true");
    expect(sourceOf("sections/ExpertDetails.tsx")).not.toContain("tabIndex={0}");
    expect(sourceOf("InputSection.tsx")).not.toContain("analyzeNumberEnergy");
  });
});

describe("Number Energy SB15 golden visual review", () => {
  const GOLDEN_PAIR_ORDER = ["32", "28", "82", "27", "78", "87", "78", "86"];
  const GOLDEN_TRIPLE_ORDER = ["328", "282", "827", "278", "787", "878", "786"];
  const GOLDEN_ENERGY_COUNTS = [
    ["Sinh Khí", "2"],
    ["Thiên Y", "2"],
    ["Diên Niên", "3"],
    ["Phục Vị", "0"],
    ["Họa Hại", "1"],
    ["Ngũ Quỷ", "0"],
    ["Lục Sát", "0"],
    ["Tuyệt Mệnh", "0"],
  ] as const;
  const REQUIRED_DOMAINS = [
    "Tài vận",
    "Công việc & sự nghiệp",
    "Tình cảm & quan hệ",
    "Tính cách & năng lực",
    "Cân bằng trường khí",
  ];
  const REVIEW_FORBIDDEN = [
    "fixture_id",
    "presentation_fixture",
    "verified_by_runtime",
    "knowledge_version",
    "knowledge version",
    "DIEN_NIEN",
    "THIEN_Y",
    "HOA_HAI",
    "82%",
    "TODO",
    "N/A",
    "loading...",
    "bảo hành",
    "đảm bảo giàu",
    "cam kết thành công",
  ];

  function cssSource(): string {
    const here = dirname(fileURLToPath(import.meta.url));
    return readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
  }

  it("keeps the input as a static Golden sample preview and blocks other numbers", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-phase")).toBe("sb16");
    expect(screen.getByTestId("static-sample-note").textContent).toBe(
      "Bản dựng tĩnh đang xem trước số mẫu 0328278786.",
    );
    expect(screen.getByTestId("analysis-submit").textContent).toBe("PHÂN TÍCH SỐ ĐIỆN THOẠI");
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "0868271327" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("input-error").textContent).toBe(
      "Bản dựng tĩnh hiện chỉ hỗ trợ số mẫu 0328278786.",
    );
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
  });

  it("reviews Golden Result P-S00…P-S10 after 0328278786 and keeps P-S11 hidden", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(false);

    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("hero-primary-energy").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("hero-terminal-energy").textContent).toBe("Thiên Y");

    const pairDigits = Array.from(screen.getByTestId("pair-strip").querySelectorAll("[data-testid^='pair-digits-']")).map(
      (node) => node.textContent,
    );
    expect(pairDigits).toEqual(GOLDEN_PAIR_ORDER);
    expect(pairDigits.filter((digits) => digits === "78")).toHaveLength(2);

    expect(screen.getByTestId("qs-favorable-value").textContent).toBe("7 cặp");
    expect(screen.getByTestId("qs-challenging-value").textContent).toBe("1 cặp");
    expect(screen.getByTestId("qs-primary-value").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("qs-terminal-value").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("quick-structure").textContent).toContain("chưa phải điểm số");

    expect(screen.getByTestId("wealth-flow").textContent).toContain("Có Tài không");
    expect(screen.getByTestId("wf-headline-0").textContent).toBe("Có Thiên Y");
    expect(screen.getByTestId("wf-headline-1").textContent).toBe("Quý nhân & cơ hội");
    expect(screen.getByTestId("wf-headline-2").textContent).toBe("Sự nghiệp & lập nghiệp");
    expect(screen.getByTestId("wf-headline-3").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("wealth-stages").querySelectorAll("[data-testid^='wf-stage-']")).toHaveLength(4);

    const tripleDigits = Array.from(
      screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-digits-']"),
    ).map((node) => node.textContent);
    expect(tripleDigits).toEqual(GOLDEN_TRIPLE_ORDER);

    GOLDEN_ENERGY_COUNTS.forEach(([label, count], index) => {
      expect(screen.getByTestId(`dist-name-${index}`).textContent).toBe(label);
      expect(screen.getByTestId(`dist-count-${index}`).textContent).toBe(count);
    });

    REQUIRED_DOMAINS.forEach((title, index) => {
      expect(screen.getByTestId(`domain-title-${index}`).textContent).toBe(title);
    });
    expect(screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']")).toHaveLength(5);
    expect(screen.getByTestId("domain-list").textContent).not.toContain("Giao tiếp");

    expect(screen.getByTestId("strength-list").querySelectorAll("[data-testid^='strength-card-']")).toHaveLength(4);
    expect(screen.getByTestId("caution-list").querySelectorAll("[data-testid^='caution-card-']")).toHaveLength(2);
    expect(screen.getByTestId("caution-title-0").textContent).toBe("Cần chú ý cách sử dụng lời nói");
    expect(screen.getByTestId("caution-title-1").textContent).toBe("Không nên chỉ nhìn số lượng Cát tinh");

    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-dimension-list").querySelectorAll("[data-testid^='score-row-']")).toHaveLength(5);
    expect(screen.getByTestId("score-reason-list").querySelectorAll("[data-testid^='score-reason-card-']")).toHaveLength(4);
    expect(screen.getByTestId("score-breakdown").textContent).not.toContain("%");

    expect(screen.getByTestId("recommendation-state").textContent).toBe("PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG");
    expect(screen.getByTestId("final-assessment").textContent).not.toMatch(/bảo hành|đảm bảo|guarantee/i);
    expect(screen.getByTestId("basis-helper").textContent).toContain("không chỉ dựa trên số lượng Cát và Hung");

    const expert = screen.getByTestId("expert-details");
    expect(expert.getAttribute("data-section")).toBe("P-S11");
    expect(expert.hasAttribute("hidden")).toBe(true);
    expect(expert.getAttribute("aria-hidden")).toBe("true");

    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of REVIEW_FORBIDDEN) {
      expect(page.toLowerCase()).not.toContain(token.toLowerCase());
    }
  });

  it("locks visual polish: one Pair Map scroller, readable identity, no stuck CTA, no heavy red caution", () => {
    const css = cssSource();
    expect(css).toMatch(/\.ne-pair-strip-scroller\s*\{[^}]*overflow-x:\s*auto/s);
    expect(css).toMatch(/\.ne-pair-strip-scroller\s*\{[^}]*width:\s*0/s);
    expect(css).toMatch(/\.ne-result\[hidden\]\s*\{[^}]*display:\s*none/s);
    expect(css).toMatch(/\.ne-pair-strip\s*\{[^}]*overflow-x:\s*visible/s);
    expect(css).toMatch(/\.ne-pair-strip\s*\{[^}]*width:\s*max-content/s);
    expect(css).toMatch(/\.ne-hero__identity\s*\{[^}]*overflow-x:\s*auto/s);
    expect(css).toMatch(/\.ne-hero__identity\s*\{[^}]*max-width:\s*100%/s);
    expect(css).toMatch(/\.ne-form-actions\s*\{[^}]*position:\s*static/s);
    expect(css).not.toMatch(/\.ne-form-actions\s*\{[^}]*position:\s*(sticky|fixed)/s);
    expect(css).toMatch(/\.ne-findings-column--caution\s*\{[^}]*border-left:\s*1px solid var\(--line\)/s);
    expect(css).not.toMatch(/\.ne-findings-column--caution\s*\{[^}]*--danger/s);
    expect(css).not.toMatch(/\.ne-pair-card\[data-pair-tone="caution"\]\s*\{[^}]*--danger/s);
    expect(css).toMatch(/@media \(max-width: 768px\)[\s\S]*\.ne-form-actions button\s*\{[\s\S]*width:\s*100%/);
    expect(css).toContain('html:has([data-screen="number-energy"])');
    expect(css).toContain("contain: paint");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("analyzeNumberEnergy");
    expect(sourceOf("InputSection.tsx")).not.toContain("from \"./api\"");
    expect(sourceOf("ResultSection.tsx")).not.toContain("from \"./api\"");
    expect(sourceOf("sections/ExpertDetails.tsx")).not.toContain("expert=true");
  });
});

describe("Number Energy SB16 static freeze", () => {
  const FREEZE_FORBIDDEN = [
    "fixture_id",
    "presentation_fixture",
    "verified_by_runtime",
    "knowledge_version",
    "DIEN_NIEN",
    "THIEN_Y",
    "82%",
  ];

  function bundleSource(): string {
    const here = dirname(fileURLToPath(import.meta.url));
    return readFileSync(resolve(here, "../../static/dist/numberEnergy.js"), "utf8");
  }

  function entrySource(): string {
    const here = dirname(fileURLToPath(import.meta.url));
    return readFileSync(resolve(here, "../../src/entries/numberEnergyApp.tsx"), "utf8");
  }

  it("marks the page as NUMBER_ENERGY_STATIC_UI_V1 at sb16", () => {
    render(<NumberEnergyPage />);
    const page = screen.getByTestId("number-energy-page");
    expect(page.getAttribute("data-static-phase")).toBe("sb16");
    expect(page.getAttribute("data-static-freeze")).toBe(NUMBER_ENERGY_STATIC_UI_V1);
    expect(NUMBER_ENERGY_STATIC_UI_V1).toBe("NUMBER_ENERGY_STATIC_UI_V1");
  });

  it("keeps Golden Result hidden until the sample number is submitted", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("idle");
    fireEvent.change(screen.getByTestId("number-input"), { target: { value: "0868271327" } });
    fireEvent.submit(screen.getByTestId("input-form-region"));
    expect(fetchMock).not.toHaveBeenCalled();
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    expect(screen.getByTestId("input-error").textContent).toBe(
      "Bản dựng tĩnh hiện chỉ hỗ trợ số mẫu 0328278786.",
    );
  });

  it("reveals frozen P-S00…P-S10 for 0328278786 and keeps P-S11 hidden", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(false);
    for (const [sectionId, testId] of RESULT_SECTIONS) {
      expect(screen.getByTestId(testId).getAttribute("data-section")).toBe(sectionId);
    }
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("pair-strip").querySelectorAll("[data-testid^='pair-card-']")).toHaveLength(8);
    expect(screen.getByTestId("wealth-stages").querySelectorAll("[data-testid^='wf-stage-']")).toHaveLength(4);
    expect(screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']")).toHaveLength(7);
    expect(screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']")).toHaveLength(5);
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    const expert = screen.getByTestId("expert-details");
    expect(expert.hasAttribute("hidden")).toBe(true);
    expect(expert.getAttribute("aria-hidden")).toBe("true");
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of FREEZE_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("does not wire runtime/API/analyze or an Expert Mode adapter", () => {
    const cssHere = dirname(fileURLToPath(import.meta.url));
    const css = readFileSync(resolve(cssHere, "../../static/css/number_energy.css"), "utf8");
    expect(css).toMatch(/\.ne-result\[hidden\]\s*\{[^}]*display:\s*none/s);
    expect(entrySource()).not.toContain("analyzeNumberEnergy");
    expect(entrySource()).not.toContain("from \"../features/number_energy/api\"");
    expect(entrySource()).not.toContain("ResultView");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("expert=true");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("URLSearchParams");
    expect(sourceOf("ResultSection.tsx")).not.toContain("from \"./api\"");
    const bundle = bundleSource();
    expect(bundle).toContain("NUMBER_ENERGY_STATIC_UI_V1");
    expect(bundle).not.toContain("fetch(");
    expect(bundle).not.toContain("/number-energy/analyze");
    expect(bundle).not.toContain("analyzeNumberEnergy");
  });
});
