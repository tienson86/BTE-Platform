import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
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
    expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(screen.getByTestId("basis-of-assessment").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
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
    expect(entrySource()).not.toContain("runtimeMode");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("expert=true");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("URLSearchParams");
    expect(sourceOf("NumberEnergyPage.tsx")).not.toContain("searchParams");
    expect(sourceOf("ResultSection.tsx")).not.toContain("from \"./api\"");
    const bundle = bundleSource();
    expect(bundle).toContain("NUMBER_ENERGY_STATIC_UI_V1");
  });
});

describe("Number Energy RB09 explicit runtime bind P-S01/P-S02/P-S05", () => {
  const BIND_FORBIDDEN = [
    "CAT",
    "HUNG",
    "DIEN_NIEN",
    "strength_rank",
    "energy_id",
    "source_span",
    "verified_by_runtime",
  ];

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("keeps default page static and does not fetch", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("number-energy-page").getAttribute("data-runtime-mode")).toBe("off");
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-freeze")).toBe(
      NUMBER_ENERGY_STATIC_UI_V1,
    );
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("golden");
    expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("basis-of-assessment").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
  });

  it("calls runtime once in explicit runtime mode and binds only P-S01/P-S02/P-S05", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [, init] = fetchMock.mock.calls[0] as [string, { method?: string; body?: string }];
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body ?? "{}")).toEqual({
      number: "0328278786",
      purpose_context: "phone_number",
    });
    const pairDigits = Array.from(
      screen.getByTestId("pair-strip").querySelectorAll("[data-testid^='pair-digits-']"),
    ).map((node) => node.textContent);
    expect(pairDigits).toEqual(["32", "28", "82", "27", "78", "87", "78", "86"]);
    expect(pairDigits.filter((item) => item === "78")).toHaveLength(2);
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("qs-favorable-value").textContent).toBe("7 cặp");
    expect(screen.getByTestId("qs-challenging-value").textContent).toBe("1 cặp");
    expect(screen.getByTestId("qs-primary-value").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("qs-terminal-value").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    const distCounts = Array.from(
      screen.getByTestId("energy-distribution-list").querySelectorAll("[data-testid^='dist-count-']"),
    ).map((node) => node.textContent);
    expect(distCounts).toEqual(["2", "2", "3", "0", "1", "0", "0", "0"]);
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("wealth-stages").querySelectorAll("[data-testid^='wf-stage-']")).toHaveLength(4);
    expect(screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']")).toHaveLength(7);
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of BIND_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("binds P-S00 Hero from view.hero when runtime score differs", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score", summary: "Should not bind P-S08 in RB09." },
          { title: "Runtime score", summary: "Should not bind P-S08 in RB09." },
          { title: "Runtime score", summary: "Should not bind P-S08 in RB09." },
          { title: "Runtime score", summary: "Should not bind P-S08 in RB09." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
    expect(screen.getByTestId("score-grade").textContent).toBe("YẾU");
  });

  it("falls back to Golden for a missing runtime pair slot", async () => {
    const data = goldenAnalyzeData();
    delete data.pair_occurrences;
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    const pairDigits = Array.from(
      screen.getByTestId("pair-strip").querySelectorAll("[data-testid^='pair-digits-']"),
    ).map((node) => node.textContent);
    expect(pairDigits).toEqual(["32", "28", "82", "27", "78", "87", "78", "86"]);
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
  });

  it("shows a safe runtime error and does not reveal a partial result", async () => {
    stubAnalyze({ detail: "Traceback (most recent call last): energy_id" }, 500);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("input-error").textContent).toBe("Không thể hoàn tất phân tích lúc này.");
    });
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    const page = screen.getByTestId("number-energy-page").textContent || "";
    expect(page).not.toContain("Traceback");
    expect(page).not.toContain("energy_id");
    expect(page).not.toContain("HTTP_ERROR");
  });
});

describe("Number Energy RB10 explicit runtime bind P-S03", () => {
  const WEALTH_FORBIDDEN = [
    "wealth_node",
    "PRIMARY_WEALTH",
    "energy_id",
    "source_span",
    "verified_by_runtime",
    "DIEN_NIEN",
    "CAT",
    "HUNG",
  ];

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("binds P-S03 from runtime view and keeps RB09 slots bound", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("wf-label-0").textContent).toBe("Tài vận");
    expect(screen.getByTestId("wf-headline-0").textContent).toBe("Có Thiên Y");
    expect(screen.getByTestId("wf-evidence-0").textContent).toBe("27 · 86");
    expect(screen.queryByTestId("wf-interaction-0")).toBeNull();
    expect(screen.getByTestId("wf-label-1").textContent).toBe("Tài từ đâu?");
    expect(screen.getByTestId("wf-headline-1").textContent).toBe("Quý nhân & cơ hội");
    expect(screen.getByTestId("wf-evidence-1").textContent).toBe("827");
    expect(screen.getByTestId("wf-interaction-1").textContent).toBe("Sinh Khí → Thiên Y");
    expect(screen.getByTestId("wf-label-2").textContent).toBe("Tài đi đâu?");
    expect(screen.getByTestId("wf-headline-2").textContent).toBe("Sự nghiệp & lập nghiệp");
    expect(screen.getByTestId("wf-evidence-2").textContent).toBe("278");
    expect(screen.getByTestId("wf-interaction-2").textContent).toBe("Thiên Y → Diên Niên");
    expect(screen.getByTestId("wf-label-3").textContent).toBe("Hậu vận");
    expect(screen.getByTestId("wf-headline-3").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("wf-evidence-3").textContent).toBe("786");
    expect(screen.getByTestId("wf-interaction-3").textContent).toBe("Diên Niên → Thiên Y");
    expect(screen.getByTestId("wf-story-0").textContent).toBe("Quý nhân & cơ hội");
    expect(screen.getByTestId("wf-story-1").textContent).toBe("Tài");
    expect(screen.getByTestId("wf-story-2").textContent).toBe("Sự nghiệp");
    expect(screen.getByTestId("wf-story-3").textContent).toBe("Tài");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']")).toHaveLength(7);
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const section = screen.getByTestId("wealth-flow").textContent || "";
    expect(section).not.toContain("chắc chắn");
    expect(section).not.toContain("phát tài");
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of WEALTH_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("binds P-S00 Hero from view.hero when runtime score differs", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
    expect(screen.getByTestId("score-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("wf-headline-0").textContent).toBe("Có Thiên Y");
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.wealth_flow;
        delete data.wealth_story;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.wealth_flow = null;
        data.wealth_story = null;
      },
    ],
    [
      "incomplete",
      (data: Record<string, unknown>) => {
        data.wealth_flow = {
          stages: [
            {
              id: "WF-01",
              label: "Tài vận",
              headline: "Runtime incomplete wealth",
              evidence: "99",
              interaction: "",
              narrative: "Should fall back because only one stage is present.",
            },
          ],
        };
        data.wealth_story = { nodes: ["Runtime"], display: "Runtime", synthesis: "Runtime gap." };
      },
    ],
  ])("falls back to Golden P-S03 when wealth_flow is %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("wf-label-0").textContent).toBe("Tài vận");
    expect(screen.getByTestId("wf-headline-0").textContent).toBe("Có Thiên Y");
    expect(screen.getByTestId("wf-evidence-0").textContent).toBe("27 · 86");
    expect(screen.getByTestId("wealth-flow").textContent).not.toContain("Runtime incomplete wealth");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
  });
});

describe("Number Energy RB11 explicit runtime bind P-S04", () => {
  const TRIPLE_FORBIDDEN = [
    "HH_TO_SK",
    "FEATURED",
    "STANDARD",
    "COMPACT",
    "energy_id",
    "source_span",
    "interpretation_status",
    "DIEN_NIEN",
    "CAT",
    "HUNG",
    "verified_by_runtime",
  ];

  const EXPECTED_TRIPLES = [
    ["328", "Khẩu tài tốt", "Họa Hại", "Sinh Khí", "standard"],
    ["282", "Quý nhân và cơ hội được tăng cường", "Sinh Khí", "Sinh Khí", "standard"],
    ["827", "Quý nhân mang đến Tài vận", "Sinh Khí", "Thiên Y", "featured"],
    ["278", "Tài đi vào sự nghiệp", "Thiên Y", "Diên Niên", "featured"],
    ["787", "Năng lực nghề nghiệp được tăng cường", "Diên Niên", "Diên Niên", "compact"],
    ["878", "Năng lực nghề nghiệp được tăng cường", "Diên Niên", "Diên Niên", "compact"],
    ["786", "Năng lực nghề nghiệp tạo Tài", "Diên Niên", "Thiên Y", "featured"],
  ] as const;

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("binds P-S04 from runtime view and keeps RB09/RB10 slots bound", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const cards = screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']");
    expect(cards).toHaveLength(7);
    const digits = Array.from(cards).map((card) => card.getAttribute("data-triple-digits"));
    expect(digits).toEqual(["328", "282", "827", "278", "787", "878", "786"]);
    expect(digits.filter((value) => value === "787" || value === "878")).toEqual(["787", "878"]);
    EXPECTED_TRIPLES.forEach((expected, index) => {
      const [tripleDigits, title, source, target, priority] = expected;
      expect(screen.getByTestId(`triple-digits-${index}`).textContent).toBe(tripleDigits);
      expect(screen.getByTestId(`triple-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`triple-source-${index}`).textContent).toBe(source);
      expect(screen.getByTestId(`triple-target-${index}`).textContent).toBe(target);
      expect(screen.getByTestId(`triple-card-${index}`).getAttribute("data-priority")).toBe(priority);
    });
    expect(screen.getByTestId("triple-card-2").getAttribute("data-priority")).toBe("featured");
    expect(screen.getByTestId("triple-card-3").getAttribute("data-priority")).toBe("featured");
    expect(screen.getByTestId("triple-card-6").getAttribute("data-priority")).toBe("featured");
    expect(screen.getByTestId("triple-card-0").getAttribute("data-priority")).toBe("standard");
    expect(screen.getByTestId("triple-card-1").getAttribute("data-priority")).toBe("standard");
    expect(screen.getByTestId("triple-card-4").getAttribute("data-priority")).toBe("compact");
    expect(screen.getByTestId("triple-card-5").getAttribute("data-priority")).toBe("compact");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of TRIPLE_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("preserves runtime triple order and does not merge 787 with 878", async () => {
    const data = goldenAnalyzeData();
    const rows = data.triple_occurrences as Record<string, unknown>[];
    data.triple_occurrences = [rows[6], rows[5], rows[4], rows[3], rows[2], rows[1], rows[0]];
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    const digits = Array.from(
      screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']"),
    ).map((card) => card.getAttribute("data-triple-digits"));
    expect(digits).toEqual(["786", "878", "787", "278", "827", "282", "328"]);
    expect(screen.getByTestId("triple-card-1").getAttribute("data-triple-digits")).toBe("878");
    expect(screen.getByTestId("triple-card-2").getAttribute("data-triple-digits")).toBe("787");
    expect(screen.getByTestId("triple-title-1").textContent).toBe("Năng lực nghề nghiệp được tăng cường");
    expect(screen.getByTestId("triple-title-2").textContent).toBe("Năng lực nghề nghiệp được tăng cường");
  });

  it("binds P-S00 Hero from view.hero when runtime triples and score differ", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      triple_occurrences: [
        tripleRow(
          "999",
          "Họa Hại",
          "Sinh Khí",
          "Runtime triple binds P-S04",
          "Runtime triple copy should bind Triple Story.",
          ["Tài vận"],
          "FEATURED",
        ),
      ],
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("triple-digits-0").textContent).toBe("999");
    expect(screen.getByTestId("triple-title-0").textContent).toBe("Runtime triple binds P-S04");
    expect(screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']")).toHaveLength(1);
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.triple_occurrences;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.triple_occurrences = null;
      },
    ],
    [
      "empty",
      (data: Record<string, unknown>) => {
        data.triple_occurrences = [];
      },
    ],
    [
      "incomplete",
      (data: Record<string, unknown>) => {
        data.triple_occurrences = [
          {
            digits: "999",
            left_energy_label: "Họa Hại",
            right_energy_label: "Sinh Khí",
            customer_title: "",
            customer_summary: "",
            domains: ["Tài vận"],
            priority: "FEATURED",
            interpretation_status: "DEFINED",
          },
        ];
      },
    ],
  ])("falls back to Golden P-S04 when triples are %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("triple-digits-0").textContent).toBe("328");
    expect(screen.getByTestId("triple-title-0").textContent).toBe("Khẩu tài tốt");
    expect(screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-card-']")).toHaveLength(7);
    expect(screen.getByTestId("triple-list").textContent).not.toContain("Runtime triple binds P-S04");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
  });

  it("omits UNDEFINED triple narrative instead of composing from left/right", async () => {
    const data = goldenAnalyzeData();
    data.triple_occurrences = [
      {
        digits: "999",
        left_energy_label: "Họa Hại",
        right_energy_label: "Họa Hại",
        interpretation_status: "UNDEFINED",
        priority: "STANDARD",
        domains: [],
      },
    ];
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("triple-digits-0").textContent).toBe("999");
    expect(screen.getByTestId("triple-source-0").textContent).toBe("Họa Hại");
    expect(screen.getByTestId("triple-target-0").textContent).toBe("Họa Hại");
    expect(screen.queryByTestId("triple-title-0")).toBeNull();
    const section = screen.getByTestId("triple-story").textContent || "";
    expect(section).not.toContain("interpretation_status");
    expect(section).not.toContain("UNDEFINED");
    expect(section).not.toContain("HH_TO_SK");
  });
});

describe("Number Energy RB12 explicit runtime bind P-S06/P-S07", () => {
  const DOMAIN_FINDING_FORBIDDEN = [
    "domain_key",
    "copy_key",
    "finding_key",
    "evidence_id",
    "energy_id",
    "source_span",
    "verified_by_runtime",
    "DIEN_NIEN",
    "CAT",
    "HUNG",
  ];

  const EXPECTED_DOMAINS = [
    ["Tài vận", "Có đường Tài tương đối rõ"],
    ["Công việc & sự nghiệp", "Đây là một trong những điểm mạnh nhất của dãy"],
    ["Tình cảm & quan hệ", "Quan hệ xã hội có yếu tố hỗ trợ"],
    ["Tính cách & năng lực", "Trách nhiệm và năng lực làm việc khá rõ"],
    ["Cân bằng trường khí", "Cát tinh giữ vai trò chủ đạo"],
  ] as const;

  const EXPECTED_STRENGTHS = [
    "Quý nhân có thể mở đường cho Tài",
    "Năng lực nghề nghiệp nổi bật",
    "Công việc có khả năng tạo thành quả",
    "Khẩu tài có thể phát huy tích cực",
  ] as const;

  const EXPECTED_CAUTIONS = [
    "Cần chú ý cách sử dụng lời nói",
    "Không nên chỉ nhìn số lượng Cát tinh",
  ] as const;

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("binds P-S06/P-S07 from runtime view and keeps RB09-RB11 slots bound", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']")).toHaveLength(5);
    EXPECTED_DOMAINS.forEach(([title, conclusion], index) => {
      expect(screen.getByTestId(`domain-title-${index}`).textContent).toBe(title);
      expect(screen.getByTestId(`domain-conclusion-${index}`).textContent).toBe(conclusion);
    });
    expect(screen.queryByText("Giao tiếp & nhân duyên")).toBeNull();
    expect(screen.queryByTestId("domain-card-5")).toBeNull();
    EXPECTED_STRENGTHS.forEach((title, index) => {
      expect(screen.getByTestId(`strength-title-${index}`).textContent).toBe(title);
    });
    EXPECTED_CAUTIONS.forEach((title, index) => {
      expect(screen.getByTestId(`caution-title-${index}`).textContent).toBe(title);
    });
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const domains = screen.getByTestId("domain-insights").textContent || "";
    const findings = screen.getByTestId("strengths-cautions").textContent || "";
    expect(domains).not.toContain("chắc chắn");
    expect(domains).not.toContain("rất giàu");
    expect(domains).not.toContain("chẩn đoán");
    expect(findings).not.toContain("chắc chắn");
    expect(findings).not.toContain("chẩn đoán");
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of DOMAIN_FINDING_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("binds P-S00 Hero from view.hero when runtime domains and findings differ", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      domain_insights: [0, 1, 2, 3, 4].map((index) => ({
        domain: `Runtime domain ${index} binds P-S06`,
        conclusion: "Runtime domain conclusion",
        narrative: "Runtime domain narrative",
      })),
      strengths: [{ title: "Runtime strength binds P-S07", summary: "Runtime strength copy." }],
      cautions: [{ title: "Runtime caution binds P-S07", summary: "Runtime caution copy." }],
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
          { title: "Runtime score", summary: "Should not bind P-S08." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("domain-title-0").textContent).toBe("Runtime domain 0 binds P-S06");
    expect(screen.getByTestId("strength-title-0").textContent).toBe("Runtime strength binds P-S07");
    expect(screen.getByTestId("caution-title-0").textContent).toBe("Runtime caution binds P-S07");
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.domain_insights;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.domain_insights = null;
      },
    ],
    [
      "empty",
      (data: Record<string, unknown>) => {
        data.domain_insights = [];
      },
    ],
    [
      "incomplete",
      (data: Record<string, unknown>) => {
        data.domain_insights = [
          {
            domain: "Runtime incomplete domain",
            conclusion: "Should fall back because only one domain is present.",
            narrative: "Incomplete domain payload.",
          },
        ];
      },
    ],
  ])("falls back to Golden P-S06 when domains are %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("domain-title-0").textContent).toBe("Tài vận");
    expect(screen.getByTestId("domain-conclusion-0").textContent).toBe("Có đường Tài tương đối rõ");
    expect(screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']")).toHaveLength(5);
    expect(screen.getByTestId("domain-insights").textContent).not.toContain("Runtime incomplete domain");
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.strengths;
        delete data.cautions;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.strengths = null;
        data.cautions = null;
      },
    ],
    [
      "empty",
      (data: Record<string, unknown>) => {
        data.strengths = [];
        data.cautions = [];
      },
    ],
    [
      "incomplete",
      (data: Record<string, unknown>) => {
        data.strengths = [{ title: "", summary: "Runtime incomplete strength." }];
        data.cautions = [{ title: "Runtime incomplete caution", summary: "Should fall back." }];
      },
    ],
  ])("falls back to Golden P-S07 when strengths/cautions are %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("strength-title-0").textContent).toBe("Quý nhân có thể mở đường cho Tài");
    expect(screen.getByTestId("caution-title-0").textContent).toBe("Cần chú ý cách sử dụng lời nói");
    expect(screen.getByTestId("strengths-cautions").textContent).not.toContain("Runtime incomplete caution");
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
  });

  it("does not add an optional sixth communication domain", async () => {
    const data = goldenAnalyzeData();
    const rows = [...((data.domain_insights as Record<string, unknown>[]) ?? [])];
    rows.push({
      domain: "Giao tiếp & nhân duyên",
      conclusion: "Optional domain must not appear.",
      narrative: "Runtime must not bind a sixth communication domain.",
    });
    data.domain_insights = rows;
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("domain-list").querySelectorAll("[data-testid^='domain-card-']")).toHaveLength(5);
    expect(screen.queryByText("Giao tiếp & nhân duyên")).toBeNull();
    expect(screen.getByTestId("domain-title-0").textContent).toBe("Tài vận");
  });
});

describe("Number Energy RB13 explicit runtime bind P-S08", () => {
  const SCORE_FORBIDDEN = [
    "verified_by_runtime",
    "score_axis",
    "axis_key",
    "energy_id",
    "source_span",
    "DIEN_NIEN",
    "CAT",
    "HUNG",
  ];

  const EXPECTED_DIMENSIONS = [
    ["Cấu trúc năng lượng", "21 / 25"],
    ["Dòng tài vận", "22 / 25"],
    ["Công việc & trợ lực", "17 / 20"],
    ["Ổn định & rủi ro", "10 / 15"],
    ["Năng lượng kết", "12 / 15"],
  ] as const;

  const EXPECTED_REASONS = [
    "Cấu trúc Cát giữ vai trò chủ đạo",
    "Dòng Tài có nguồn rõ",
    "Công việc là trục mạnh",
    "Họa Hại cần được sử dụng đúng cách",
  ] as const;

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("binds P-S08 from runtime view and keeps RB09-RB12 slots bound", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-grade").textContent).toBe("TỐT");
    expect(screen.queryByTestId("score-static-note")).toBeNull();
    EXPECTED_DIMENSIONS.forEach(([label, points], index) => {
      expect(screen.getByTestId(`score-dim-label-${index}`).textContent).toBe(label);
      expect(screen.getByTestId(`score-dim-points-${index}`).textContent).toBe(points);
    });
    EXPECTED_REASONS.forEach((title, index) => {
      expect(screen.getByTestId(`score-reason-title-${index}`).textContent).toBe(title);
    });
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const section = screen.getByTestId("score-breakdown").textContent || "";
    expect(section).not.toContain("82%");
    expect(section).not.toContain("%");
    expect(section).not.toContain("chắc chắn");
    expect(section).not.toContain("chẩn đoán");
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of SCORE_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("binds P-S00 Hero from view.hero when runtime score differs", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score binds P-S08", summary: "Runtime score copy." },
          { title: "Runtime score binds P-S08", summary: "Runtime score copy." },
          { title: "Runtime score binds P-S08", summary: "Runtime score copy." },
          { title: "Runtime score binds P-S08", summary: "Runtime score copy." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
    expect(screen.getByTestId("score-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("score-reason-title-0").textContent).toBe("Runtime score binds P-S08");
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("YẾU");
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.score;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.score = null;
      },
    ],
    [
      "incomplete",
      (data: Record<string, unknown>) => {
        data.score = {
          total: 11,
          max: 100,
          display: "11 / 100",
          grade: "YẾU",
          verified_by_runtime: true,
          breakdown: [{ label: "Cấu trúc năng lượng", earned: 1, max: 25 }],
          reasons: [{ title: "Runtime incomplete score", summary: "Should fall back." }],
        };
      },
    ],
    [
      "unverified",
      (data: Record<string, unknown>) => {
        data.verified_by_runtime = false;
        data.score = {
          ...(data.score as Record<string, unknown>),
          display: "11 / 100",
          grade: "YẾU",
          verified_by_runtime: false,
        };
      },
    ],
  ])("falls back to Golden P-S08 when score is %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("score-total").textContent).toBe("82 / 100");
    expect(screen.getByTestId("score-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("score-static-note").textContent).toContain("điểm minh họa của bản dựng tĩnh");
    expect(screen.getByTestId("score-breakdown").textContent).not.toContain("Runtime incomplete score");
    expect(screen.getByTestId("score-breakdown").textContent).not.toContain("11 / 100");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
  });
});

describe("Number Energy RB14 explicit runtime bind P-S09/P-S10", () => {
  const ASSESS_BASIS_FORBIDDEN = [
    "verified_by_runtime",
    "fixture_id",
    "presentation_fixture",
    "evidence_id",
    "copy_key",
    "energy_id",
    "source_span",
    "DIEN_NIEN",
    "CAT",
    "HUNG",
  ];

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("binds P-S09 and P-S10 from runtime view and keeps RB09-RB13 slots bound", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("basis-of-assessment").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("assessment-title").textContent).toBe("Đánh giá tổng thể");
    expect(screen.getByTestId("assessment-story").textContent).toContain(
      "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y.",
    );
    expect(screen.getByTestId("assessment-story").textContent).toContain(
      "Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy.",
    );
    expect(screen.getByTestId("assessment-flow-0").textContent).toBe("QUÝ NHÂN");
    expect(screen.getByTestId("assessment-flow-1").textContent).toBe("TÀI");
    expect(screen.getByTestId("assessment-flow-2").textContent).toBe("SỰ NGHIỆP");
    expect(screen.getByTestId("assessment-flow-3").textContent).toBe("TÀI");
    expect(screen.getByTestId("recommendation-state").textContent).toBe("PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG");
    expect(screen.getByTestId("recommendation-supporting").textContent).toBe(
      "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài.",
    );
    expect(screen.getByTestId("basis-helper").textContent).toContain("không chỉ dựa trên số lượng Cát và Hung");
    expect(screen.getByTestId("basis-principle-0").textContent).toContain("8 cặp");
    expect(screen.getByTestId("basis-principle-1").textContent).toContain("bộ ba nổi bật");
    expect(screen.getByTestId("basis-principle-2").textContent).toContain("dòng Tài vận");
    expect(screen.getByTestId("basis-principle-3").textContent).toContain("năng lượng kết");
    expect(screen.queryByTestId("basis-principle-4")).toBeNull();
    expect(screen.getByTestId("basis-item-0-0").textContent).toBe("32 · Họa Hại");
    expect(screen.getByTestId("basis-item-0-1").textContent).toBe("28 / 82 · Sinh Khí");
    expect(screen.getByTestId("basis-item-0-2").textContent).toBe("27 / 86 · Thiên Y");
    expect(screen.getByTestId("basis-item-0-3").textContent).toBe("78 / 87 / 78 · Diên Niên");
    expect(screen.getByTestId("basis-item-1-0").textContent).toBe("827 · Sinh Khí → Thiên Y");
    expect(screen.getByTestId("basis-item-1-1").textContent).toBe("278 · Thiên Y → Diên Niên");
    expect(screen.getByTestId("basis-item-1-2").textContent).toBe("786 · Diên Niên → Thiên Y");
    expect(screen.getByTestId("basis-item-2-0").textContent).toBe("82 / 100 · TỐT");
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const assess = screen.getByTestId("final-assessment").textContent || "";
    const basis = screen.getByTestId("basis-of-assessment").textContent || "";
    expect(assess).not.toContain("chắc chắn");
    expect(assess).not.toContain("chẩn đoán");
    expect(assess).not.toContain("đổi số ngay");
    expect(assess).not.toContain("mua sim");
    expect(basis).not.toContain("chẩn đoán");
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of ASSESS_BASIS_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
    expect(sourceOf("sections/FinalAssessment.tsx")).not.toContain("goldenScore");
    expect(sourceOf("sections/FinalAssessment.tsx")).not.toContain("view.score");
    expect(sourceOf("sections/BasisOfAssessment.tsx")).not.toContain("goldenPairs");
    expect(sourceOf("sections/BasisOfAssessment.tsx")).not.toContain("goldenTriples");
  });

  it("binds P-S00 Hero from view.hero when runtime assessment and basis differ", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      assessment: {
        title: "Runtime assessment binds P-S09",
        summary: "Runtime assessment copy.",
        story_nodes: ["A", "B"],
      },
      recommendation: { label: "RUNTIME STATE", summary: "Runtime recommendation copy." },
      evidence: [{ group: "Runtime evidence binds P-S10", items: ["runtime evidence item"] }],
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score", summary: "Runtime score copy." },
          { title: "Runtime score", summary: "Runtime score copy." },
          { title: "Runtime score", summary: "Runtime score copy." },
          { title: "Runtime score", summary: "Runtime score copy." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("assessment-title").textContent).toBe("Runtime assessment binds P-S09");
    expect(screen.getByTestId("recommendation-state").textContent).toBe("RUNTIME STATE");
    expect(screen.getByTestId("basis-group-0").textContent).toBe("Runtime evidence binds P-S10");
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.assessment;
        delete data.recommendation;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.assessment = null;
        data.recommendation = null;
      },
    ],
    [
      "incomplete assessment",
      (data: Record<string, unknown>) => {
        data.assessment = { title: "Runtime incomplete assessment" };
      },
    ],
    [
      "incomplete recommendation",
      (data: Record<string, unknown>) => {
        data.recommendation = { label: "" };
      },
    ],
  ])("falls back to Golden P-S09 when assessment/recommendation is %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("assessment-title").textContent).toBe("Đánh giá tổng thể");
    expect(screen.getByTestId("recommendation-state").textContent).toBe("PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG");
    expect(screen.getByTestId("final-assessment").textContent).not.toContain("Runtime incomplete assessment");
    expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
  });

  it.each([
    [
      "missing",
      (data: Record<string, unknown>) => {
        delete data.evidence;
      },
    ],
    [
      "null",
      (data: Record<string, unknown>) => {
        data.evidence = null;
      },
    ],
    [
      "empty",
      (data: Record<string, unknown>) => {
        data.evidence = [];
      },
    ],
    [
      "incomplete",
      (data: Record<string, unknown>) => {
        data.evidence = [{ group: "Runtime incomplete evidence", items: [{ evidence_id: "E-01" }] }];
      },
    ],
  ])("falls back to Golden P-S10 when basis/evidence is %s", async (_label, mutate) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("basis-of-assessment").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("basis-item-0-0").textContent).toBe("32 · Họa Hại");
    expect(screen.getByTestId("basis-of-assessment").textContent).not.toContain("Runtime incomplete evidence");
    expect(screen.getByTestId("basis-of-assessment").textContent).not.toContain("evidence_id");
    expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
  });
});

describe("Number Energy RB15 explicit runtime bind P-S00", () => {
  const RUNTIME_SLOTS = RESULT_SECTIONS.filter(([sectionId]) => sectionId !== "P-S11");
  const HERO_RUNTIME_FORBIDDEN = [
    "verified_by_runtime",
    "fixture_id",
    "presentation_fixture",
    "energy_id",
    "source_span",
    "DIEN_NIEN",
    "THIEN_Y",
    "CAT",
    "HUNG",
  ];
  const HERO_SALES_HEALTH = [
    "bảo hành",
    "đảm bảo giàu",
    "cam kết thành công",
    "guarantee",
    "chẩn đoán",
    "chữa bệnh",
    "phát tài",
    "đổi số ngay",
    "mua sim",
  ];

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("keeps default page static and does not fetch", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("number-energy-page").getAttribute("data-runtime-mode")).toBe("off");
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-freeze")).toBe(
      NUMBER_ENERGY_STATIC_UI_V1,
    );
    expect(NUMBER_ENERGY_STATIC_UI_V1).toBe("NUMBER_ENERGY_STATIC_UI_V1");
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("golden");
    expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
  });

  it("binds P-S00 Hero from runtime view.hero", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("hero-primary-energy").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("hero-terminal-energy").textContent).toBe("Thiên Y");
    expect(screen.getByTestId("hero-summary").textContent).toBe(
      "Công việc và năng lực nghề nghiệp là trục nổi bật; phần cuối dãy quy về Thiên Y.",
    );
    expect(screen.getByTestId("hero-primary-keywords").textContent).toBe(
      "Công việc · năng lực · trách nhiệm",
    );
    expect(screen.getByTestId("hero-terminal-keywords").textContent).toBe(
      "Tài vận · tài nguyên · thành quả",
    );
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const hero = screen.getByTestId("result-hero").textContent || "";
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of HERO_RUNTIME_FORBIDDEN) {
      expect(hero).not.toContain(token);
      expect(page).not.toContain(token);
    }
    for (const token of HERO_SALES_HEALTH) {
      expect(page.toLowerCase()).not.toContain(token.toLowerCase());
    }
  });

  it("binds complete Golden runtime payload to P-S00…P-S10 and keeps P-S11 hidden", async () => {
    stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    for (const [, testId] of RUNTIME_SLOTS) {
      expect(screen.getByTestId(testId).getAttribute("data-slot-source")).toBe("RUNTIME");
    }
    const expert = screen.getByTestId("expert-details");
    expect(expert.hasAttribute("hidden")).toBe(true);
    expect(expert.getAttribute("aria-hidden")).toBe("true");
    expect(expert.getAttribute("data-slot-source")).not.toBe("RUNTIME");
  });

  it.each([
    [
      "missing original input",
      (data: Record<string, unknown>) => {
        delete data.metadata;
        delete data.input_raw;
        delete data.identity;
      },
    ],
    [
      "incomplete hero summary",
      (data: Record<string, unknown>) => {
        const chain = data.chain;
        if (chain && typeof chain === "object") {
          (chain as { dominant_flow_summary: string }).dominant_flow_summary = "";
        }
      },
    ],
  ])("falls back to Golden P-S00 when hero is %s and keeps other complete slots runtime", async (
    _label,
    mutate,
  ) => {
    const data = goldenAnalyzeData();
    mutate(data);
    stubAnalyze(data);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("hero-summary").textContent).toBe(
      "Công việc và năng lực nghề nghiệp là trục nổi bật; phần cuối dãy quy về Thiên Y.",
    );
    expect(screen.getByTestId("energy-map").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("quick-structure").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("wealth-flow").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("triple-story").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("energy-distribution").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("domain-insights").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("strengths-cautions").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("score-breakdown").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("final-assessment").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("basis-of-assessment").getAttribute("data-slot-source")).toBe("RUNTIME");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
  });

  it("shows a safe runtime error and does not reveal a partial result", async () => {
    stubAnalyze({ detail: "Traceback (most recent call last): energy_id" }, 500);
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("input-error").textContent).toBe("Không thể hoàn tất phân tích lúc này.");
    });
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    const page = screen.getByTestId("number-energy-page").textContent || "";
    expect(page).not.toContain("Traceback");
    expect(page).not.toContain("energy_id");
    expect(page).not.toContain("HTTP_ERROR");
    expect(page).not.toContain("verified_by_runtime");
  });

  it("uses view.hero for a mismatched runtime score and does not recalculate in React", async () => {
    stubAnalyze({
      ...goldenAnalyzeData(),
      score: {
        total: 11,
        max: 100,
        display: "11 / 100",
        grade: "YẾU",
        verified_by_runtime: true,
        breakdown: [
          { label: "Cấu trúc năng lượng", earned: 1, max: 25 },
          { label: "Dòng tài vận", earned: 2, max: 25 },
          { label: "Công việc & trợ lực", earned: 3, max: 20 },
          { label: "Ổn định & rủi ro", earned: 2, max: 15 },
          { label: "Năng lượng kết", earned: 3, max: 15 },
        ],
        reasons: [
          { title: "Runtime score binds hero via view", summary: "Adapter maps verified score into view.hero." },
          { title: "Runtime score binds hero via view", summary: "Adapter maps verified score into view.hero." },
          { title: "Runtime score binds hero via view", summary: "Adapter maps verified score into view.hero." },
          { title: "Runtime score binds hero via view", summary: "Adapter maps verified score into view.hero." },
        ],
      },
      grade: "YẾU",
      verified_by_runtime: true,
    });
    render(<NumberEnergyPage runtimeMode />);
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-hero").getAttribute("data-slot-source")).toBe("RUNTIME");
    });
    expect(screen.getByTestId("hero-score").textContent).toBe("11 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("YẾU");
    expect(screen.getByTestId("score-total").textContent).toBe("11 / 100");
    const heroSource = sourceOf("sections/ResultHero.tsx");
    expect(heroSource).not.toContain("goldenScore");
    expect(heroSource).not.toContain("view.score");
    expect(heroSource).not.toContain("totalDisplay");
    expect(heroSource).toContain("hero.scoreDisplay");
    const resultSource = sourceOf("ResultSection.tsx");
    expect(resultSource).toContain("runtimeView?.hero");
    expect(resultSource).not.toContain("runtimeView?.score.totalDisplay");
    expect(resultSource).not.toMatch(/hero\.scoreDisplay\s*=/);
  });
});

describe("Number Energy RB16 runtime visual review", () => {
  const REVIEW_DIR = resolve(
    dirname(fileURLToPath(import.meta.url)),
    "../../screenshots/number_energy/rb16",
  );
  const REQUIRED_SHOTS = [
    "01_static_input_desktop.png",
    "02_static_result_desktop.png",
    "03_runtime_input_desktop.png",
    "04_runtime_result_top_desktop.png",
    "05_runtime_result_full_desktop.png",
    "06_runtime_error_desktop.png",
    "07_static_input_mobile.png",
    "08_static_result_mobile.png",
    "09_runtime_input_mobile.png",
    "10_runtime_result_top_mobile.png",
    "11_runtime_result_full_mobile.png",
    "12_runtime_error_mobile.png",
  ] as const;
  const RUNTIME_SLOT_TESTIDS = RESULT_SECTIONS.filter(([sectionId]) => sectionId !== "P-S11");
  const VISUAL_FORBIDDEN = [
    "verified_by_runtime",
    "fixture_id",
    "presentation_fixture",
    "energy_id",
    "source_span",
    "DIEN_NIEN",
    "THIEN_Y",
    "CAT",
    "HUNG",
    "score_axis",
    "copy_key",
    "evidence_id",
  ];

  function stubAnalyze(data: Record<string, unknown>, status = 200): ReturnType<typeof vi.fn> {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      text: async () => JSON.stringify({ success: status < 300, data }),
    });
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  function reviewReport(): Record<string, unknown> {
    return JSON.parse(readFileSync(resolve(REVIEW_DIR, "review.json"), "utf8")) as Record<string, unknown>;
  }

  it("keeps public default page static, frozen, and fetch-free", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    render(<NumberEnergyPage />);
    expect(screen.getByTestId("number-energy-page").getAttribute("data-runtime-mode")).toBe("off");
    expect(screen.getByTestId("number-energy-page").getAttribute("data-static-freeze")).toBe(
      NUMBER_ENERGY_STATIC_UI_V1,
    );
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    submitGoldenPhone();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("golden");
    for (const [, testId] of RUNTIME_SLOT_TESTIDS) {
      expect(screen.getByTestId(testId).getAttribute("data-slot-source")).toBe("GOLDEN_FIXTURE");
    }
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
  });

  it("keeps result hidden until runtime success and binds P-S00…P-S10 as RUNTIME", async () => {
    const fetchMock = stubAnalyze(goldenAnalyzeData());
    render(<NumberEnergyPage runtimeMode />);
    expect(screen.getByTestId("number-energy-page").getAttribute("data-runtime-mode")).toBe("on");
    expect((screen.getByTestId("result-section") as HTMLElement).hidden).toBe(true);
    expect(fetchMock).not.toHaveBeenCalled();
    submitGoldenPhone();
    await waitFor(() => {
      expect(screen.getByTestId("result-section").getAttribute("data-preview-state")).toBe("runtime");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    for (const [, testId] of RUNTIME_SLOT_TESTIDS) {
      expect(screen.getByTestId(testId).getAttribute("data-slot-source")).toBe("RUNTIME");
    }
    expect(screen.getByTestId("hero-identity").textContent).toBe("0328 278 786");
    expect(screen.getByTestId("hero-score").textContent).toBe("82 / 100");
    expect(screen.getByTestId("hero-grade").textContent).toBe("TỐT");
    expect(screen.getByTestId("hero-primary-energy").textContent).toBe("Diên Niên");
    expect(screen.getByTestId("hero-terminal-energy").textContent).toBe("Thiên Y");
    const tripleDigits = Array.from(
      screen.getByTestId("triple-list").querySelectorAll("[data-testid^='triple-digits-']"),
    ).map((node) => node.textContent);
    expect(tripleDigits).toEqual(["328", "282", "827", "278", "787", "878", "786"]);
    expect(screen.getByTestId("score-breakdown").textContent).not.toContain("%");
    expect(screen.getByTestId("expert-details").hasAttribute("hidden")).toBe(true);
    const page = screen.getByTestId("number-energy-page").textContent || "";
    for (const token of VISUAL_FORBIDDEN) {
      expect(page).not.toContain(token);
    }
  });

  it("keeps the public entry, nav, and template off runtime and Expert Mode", () => {
    const here = dirname(fileURLToPath(import.meta.url));
    const entry = readFileSync(resolve(here, "../../src/entries/numberEnergyApp.tsx"), "utf8");
    const template = readFileSync(resolve(here, "../../templates/number_energy.html"), "utf8");
    const nav = readFileSync(resolve(here, "../../src/layouts/Navigation/navItems.ts"), "utf8");
    const harness = readFileSync(
      resolve(here, "../../src/entries/numberEnergyRuntimeScreenshotApp.tsx"),
      "utf8",
    );
    expect(entry).not.toContain("runtimeMode");
    expect(template).not.toContain("runtimeMode");
    expect(nav).not.toContain("/number-energy");
    expect(APP_NAV_ITEMS).toHaveLength(4);
    expect(APP_NAV_ITEMS.map((item) => item.id)).toEqual([
      "home",
      "choose-date",
      "analyze",
      "marriage-consulting",
    ]);
    expect(harness).toContain("runtimeMode");
    expect(sourceOf("sections/ExpertDetails.tsx")).toContain("hidden");
    const css = readFileSync(resolve(here, "../../static/css/number_energy.css"), "utf8");
    expect(css).toMatch(/\.ne-result\[hidden\]\s*\{[^}]*display:\s*none/s);
    expect(css).toMatch(/\.ne-pair-strip-scroller\s*\{[^}]*overflow-x:\s*auto/s);
    expect(css).toMatch(/\.ne-form-actions\s*\{[^}]*position:\s*static/s);
    expect(css).toMatch(/\.ne-wealth-connector--mobile\s*\{[^}]*display:\s*none/s);
    expect(css).toMatch(/@media \(max-width: 768px\)[\s\S]*\.ne-wealth-connector--desktop\s*\{[\s\S]*display:\s*none/);
  });

  it("stores RB16 screenshots and Playwright review gates", () => {
    for (const name of REQUIRED_SHOTS) {
      expect(readFileSync(resolve(REVIEW_DIR, name)).byteLength).toBeGreaterThan(1000);
    }
    const review = reviewReport();
    expect(review.stage).toBe("RB16");
    expect(review.staticAnalyzeCalls).toEqual([]);
    expect((review.runtimeAnalyzeBeforeSubmit as unknown[]).length).toBe(0);
    expect((review.runtimeAnalyzeCalls as unknown[]).length).toBeGreaterThanOrEqual(1);
    expect(review.leaks).toEqual([]);
    const staticDesktop = review.staticDesktop as Record<string, unknown>;
    const runtimeDesktop = review.runtimeDesktop as Record<string, unknown>;
    const runtimeError = review.runtimeError as Record<string, unknown>;
    const runtimeFallback = review.runtimeFallback as Record<string, unknown>;
    expect(staticDesktop.runtimeMode).toBe("off");
    expect(staticDesktop.freeze).toBe(NUMBER_ENERGY_STATIC_UI_V1);
    expect(staticDesktop.resultHiddenBeforeSubmit).toBe(true);
    expect(runtimeDesktop.runtimeMode).toBe("on");
    expect(runtimeDesktop.resultHiddenBeforeSubmit).toBe(true);
    const staticSlots = staticDesktop.slotSources as Record<string, string>;
    const runtimeSlots = runtimeDesktop.slotSources as Record<string, unknown>;
    for (const [sectionId] of RUNTIME_SLOT_TESTIDS) {
      expect(staticSlots[sectionId]).toBe("GOLDEN_FIXTURE");
      expect(runtimeSlots[sectionId]).toBe("RUNTIME");
    }
    expect((runtimeSlots["P-S11"] as { hidden: boolean }).hidden).toBe(true);
    expect((staticDesktop.overflow as { documentOverflowPx: number }).documentOverflowPx).toBeLessThanOrEqual(0);
    expect((runtimeDesktop.overflow as { documentOverflowPx: number }).documentOverflowPx).toBeLessThanOrEqual(0);
    expect((runtimeDesktop.overflow as { pageScrollLeft: number }).pageScrollLeft).toBe(0);
    expect(runtimeDesktop.triples).toBe(7);
    expect(runtimeDesktop.triple787).toBe("787");
    expect(runtimeDesktop.triple878).toBe("878");
    expect(runtimeDesktop.scoreHasPercent).toBe(false);
    expect(runtimeError.resultHidden).toBe(true);
    expect(runtimeError.message).toBe("Không thể hoàn tất phân tích lúc này.");
    const fallbackSlots = runtimeFallback.slotSources as Record<string, string>;
    expect(fallbackSlots["P-S00"]).toBe("GOLDEN_FIXTURE");
    expect(fallbackSlots["P-S01"]).toBe("RUNTIME");
  });
});

function goldenAnalyzeData(): Record<string, unknown> {
  return {
    purpose_context: "phone_number",
    metadata: { input_raw: "0328278786", purpose_context: "phone_number" },
    pair_occurrences: [
      pairRow("32", "Họa Hại", "HUNG", "Hung", "Nhẹ", [true, false, false, false]),
      pairRow("28", "Sinh Khí", "CAT", "Cát", "Nhẹ", [true, false, false, false]),
      pairRow("82", "Sinh Khí", "CAT", "Cát", "Nhẹ", [true, false, false, false]),
      pairRow("27", "Thiên Y", "CAT", "Cát", "Nhẹ", [true, false, false, false]),
      pairRow("78", "Diên Niên", "CAT", "Cát", "Mạnh", [true, true, true, false]),
      pairRow("87", "Diên Niên", "CAT", "Cát", "Mạnh", [true, true, true, false]),
      pairRow("78", "Diên Niên", "CAT", "Cát", "Mạnh", [true, true, true, false]),
      pairRow("86", "Thiên Y", "CAT", "Cát", "Mạnh", [true, true, true, false]),
    ],
    pair_summary: {
      pair_count: 8,
      supportive_pair_count: 7,
      challenging_pair_count: 1,
    },
    energy_distribution: [
      { energy_label: "Sinh Khí", count: 2 },
      { energy_label: "Thiên Y", count: 2 },
      { energy_label: "Diên Niên", count: 3 },
      { energy_label: "Phục Vị", count: 0 },
      { energy_label: "Họa Hại", count: 1 },
      { energy_label: "Ngũ Quỷ", count: 0 },
      { energy_label: "Lục Sát", count: 0 },
      { energy_label: "Tuyệt Mệnh", count: 0 },
    ],
    chain: {
      primary_energy_label: "Diên Niên",
      secondary_energy_labels: ["Sinh Khí", "Thiên Y"],
      terminal_energy_label: "Thiên Y",
      terminal_pair_digits: "86",
      dominant_flow_summary:
        "Công việc và năng lực nghề nghiệp là trục nổi bật; phần cuối dãy quy về Thiên Y.",
    },
    wealth_flow: {
      stages: [
        {
          id: "WF-01",
          label: "Tài vận",
          headline: "Có Thiên Y",
          evidence: "27 · 86",
          interaction: "",
          narrative: "Dãy xuất hiện hai điểm Thiên Y, vì vậy trục tài vận được hình thành rõ.",
        },
        {
          id: "WF-02",
          label: "Tài từ đâu?",
          headline: "Quý nhân & cơ hội",
          evidence: "827",
          interaction: "Sinh Khí → Thiên Y",
          narrative: "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.",
        },
        {
          id: "WF-03",
          label: "Tài đi đâu?",
          headline: "Sự nghiệp & lập nghiệp",
          evidence: "278",
          interaction: "Thiên Y → Diên Niên",
          narrative: "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh hoặc phát triển sự nghiệp.",
        },
        {
          id: "WF-04",
          label: "Hậu vận",
          headline: "Thiên Y",
          evidence: "786",
          interaction: "Diên Niên → Thiên Y",
          narrative:
            "Phần cuối dãy quy về Thiên Y. Diên Niên đứng trước cho thấy năng lực và công việc tiếp tục là nguồn dẫn tới tài vận.",
        },
      ],
    },
    wealth_story: {
      nodes: ["Quý nhân & cơ hội", "Tài", "Sự nghiệp", "Tài"],
      display: "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài",
      synthesis:
        "Dòng tài vận của dãy đi theo hướng: quý nhân và cơ hội mở đường, nguồn lực được đưa vào sự nghiệp, và phần cuối lại quy về khả năng tạo Tài từ chính năng lực nghề nghiệp.",
    },
    triple_occurrences: [
      tripleRow(
        "328",
        "Họa Hại",
        "Sinh Khí",
        "Khẩu tài tốt",
        "Khả năng giao tiếp và diễn đạt là điểm mạnh của tổ hợp này. Lời nói có giá trị và dễ được người khác lắng nghe, tiếp nhận.",
        ["Giao tiếp", "Công việc"],
        "STANDARD",
      ),
      tripleRow(
        "282",
        "Sinh Khí",
        "Sinh Khí",
        "Quý nhân và cơ hội được tăng cường",
        "Sinh Khí được tiếp nối, làm nổi bật khả năng gặp người hỗ trợ, cơ hội và những mối quan hệ thuận lợi.",
        ["Quý nhân", "Cơ hội"],
        "STANDARD",
      ),
      tripleRow(
        "827",
        "Sinh Khí",
        "Thiên Y",
        "Quý nhân mang đến Tài vận",
        "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.",
        ["Tài vận", "Quý nhân"],
        "FEATURED",
      ),
      tripleRow(
        "278",
        "Thiên Y",
        "Diên Niên",
        "Tài đi vào sự nghiệp",
        "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh hoặc phát triển sự nghiệp.",
        ["Tài vận", "Công việc"],
        "FEATURED",
      ),
      tripleRow(
        "787",
        "Diên Niên",
        "Diên Niên",
        "Năng lực nghề nghiệp được tăng cường",
        "Diên Niên được tiếp nối, làm nổi bật năng lực làm việc, trách nhiệm và khả năng tổ chức.",
        ["Công việc", "Năng lực"],
        "COMPACT",
      ),
      tripleRow(
        "878",
        "Diên Niên",
        "Diên Niên",
        "Năng lực nghề nghiệp được tăng cường",
        "Diên Niên tiếp tục xuất hiện, cho thấy công việc và năng lực nghề nghiệp là chủ đề được duy trì rõ trong dãy.",
        ["Công việc", "Năng lực"],
        "COMPACT",
      ),
      tripleRow(
        "786",
        "Diên Niên",
        "Thiên Y",
        "Năng lực nghề nghiệp tạo Tài",
        "Tài vận chủ yếu đến từ năng lực làm việc, chuyên môn và sự nghiệp.",
        ["Tài vận", "Công việc"],
        "FEATURED",
      ),
    ],
    domain_insights: [
      domainRow(
        "Tài vận",
        "Có đường Tài tương đối rõ",
        "Dãy có hai trường Thiên Y. Điểm Thiên Y đầu được Sinh Khí dẫn vào, cho thấy quý nhân, quan hệ và cơ hội có thể hỗ trợ việc hình thành tài vận. Phần cuối Diên Niên → Thiên Y nhấn mạnh khả năng tạo Tài thông qua chuyên môn, năng lực làm việc và sự nghiệp.",
        "Tài vận vẫn cần được nhìn trong toàn bộ cách sử dụng dãy số, không nên hiểu Thiên Y như một cam kết tài chính.",
      ),
      domainRow(
        "Công việc & sự nghiệp",
        "Đây là một trong những điểm mạnh nhất của dãy",
        "Diên Niên xuất hiện ba lần liên tiếp ở phần sau của thân số, cho thấy công việc, trách nhiệm và năng lực nghề nghiệp là chủ đề nổi bật. Tổ hợp Thiên Y → Diên Niên cho thấy nguồn lực có xu hướng được đưa vào công việc hoặc lập nghiệp.",
        "",
      ),
      domainRow(
        "Tình cảm & quan hệ",
        "Quan hệ xã hội có yếu tố hỗ trợ",
        "Sinh Khí xuất hiện hai lần và được tiếp nối ở đoạn đầu, làm nổi bật yếu tố nhân duyên, quý nhân và khả năng nhận được hỗ trợ. Tuy nhiên, dãy này không lấy trường tình cảm làm trục nổi bật nhất; trọng tâm vẫn nghiêng nhiều hơn về công việc và tài vận.",
        "",
      ),
      domainRow(
        "Tính cách & năng lực",
        "Trách nhiệm và năng lực làm việc khá rõ",
        "Diên Niên giữ vai trò chủ đạo, vì vậy dãy thiên về tính trách nhiệm, khả năng làm việc, tổ chức và xu hướng muốn tạo kết quả rõ ràng. Sinh Khí phía trước giúp cấu trúc bớt khô cứng, tăng yếu tố kết nối và hỗ trợ.",
        "",
      ),
      domainRow(
        "Cân bằng trường khí",
        "Cát tinh giữ vai trò chủ đạo",
        "Toàn thân số có Sinh Khí, Thiên Y và Diên Niên chiếm ưu thế. Họa Hại chỉ xuất hiện ở đầu thân số và ngay sau đó đi vào tổ hợp Họa Hại → Sinh Khí. Cấu trúc tổng thể không nên được đọc theo cách đơn giản là “có một Hung tinh”.",
        "",
      ),
    ],
    strengths: [
      findingRow(
        "Quý nhân có thể mở đường cho Tài",
        "Quan hệ, người hỗ trợ hoặc những cơ hội thuận lợi có thể trở thành một trong những con đường hình thành Tài.",
      ),
      findingRow(
        "Năng lực nghề nghiệp nổi bật",
        "Diên Niên được lặp lại liên tiếp, làm công việc, trách nhiệm và năng lực nghề nghiệp trở thành chủ đề mạnh của dãy.",
      ),
      findingRow(
        "Công việc có khả năng tạo thành quả",
        "Phần cuối dãy tiếp tục đưa năng lực nghề nghiệp về Thiên Y, làm rõ hơn con đường tạo Tài bằng chuyên môn và công việc.",
      ),
      findingRow(
        "Khẩu tài có thể phát huy tích cực",
        "Khả năng nói và diễn đạt có giá trị khi được sử dụng đúng cách, đặc biệt trong giao tiếp và công việc với con người.",
      ),
    ],
    cautions: [
      findingRow(
        "Cần chú ý cách sử dụng lời nói",
        "Họa Hại xuất hiện ở đầu thân số, vì vậy lời nói và cách phản ứng vẫn là một điểm cần tiết chế. Khi dùng tốt, bộ 328 lại phát huy thành khẩu tài.",
      ),
      findingRow(
        "Không nên chỉ nhìn số lượng Cát tinh",
        "Dãy có nhiều Cát tinh, nhưng giá trị thực tế vẫn nằm ở cách các trường khí nối tiếp và vận động với nhau.",
      ),
    ],
    evidence: [
      {
        title: "Cặp năng lượng",
        items: [
          { ref: "32", label: "Họa Hại" },
          { ref: "28 / 82", label: "Sinh Khí" },
          { ref: "27 / 86", label: "Thiên Y" },
          { ref: "78 / 87 / 78", label: "Diên Niên" },
        ],
      },
      {
        title: "Bộ ba nổi bật",
        items: [
          { ref: "827", label: "Sinh Khí → Thiên Y" },
          { ref: "278", label: "Thiên Y → Diên Niên" },
          { ref: "786", label: "Diên Niên → Thiên Y" },
        ],
      },
      {
        title: "Điểm đánh giá",
        items: [{ ref: "82 / 100", label: "TỐT" }],
      },
    ],
    assessment: {
      title: "Đánh giá tổng thể",
      summary:
        "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y. Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy.",
      story_line: "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI",
      story_nodes: ["QUÝ NHÂN", "TÀI", "SỰ NGHIỆP", "TÀI"],
    },
    recommendation: {
      state: "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG",
      label: "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG",
      summary: "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài.",
      copy_key: "CONTINUE",
    },
    score: {
      total: 82,
      max: 100,
      display: "82 / 100",
      grade: "TỐT",
      verified_by_runtime: true,
      breakdown: [
        { label: "Cấu trúc năng lượng", earned: 21, max: 25 },
        { label: "Dòng tài vận", earned: 22, max: 25 },
        { label: "Công việc & trợ lực", earned: 17, max: 20 },
        { label: "Ổn định & rủi ro", earned: 10, max: 15 },
        { label: "Năng lượng kết", earned: 12, max: 15 },
      ],
      reasons: [
        {
          title: "Cấu trúc Cát giữ vai trò chủ đạo",
          summary: "Sinh Khí, Thiên Y và Diên Niên chiếm phần lớn thân số.",
        },
        {
          title: "Dòng Tài có nguồn rõ",
          summary: "Sinh Khí → Thiên Y cho thấy quý nhân và cơ hội có khả năng dẫn tới Tài.",
        },
        {
          title: "Công việc là trục mạnh",
          summary: "Diên Niên xuất hiện liên tiếp và tiếp tục dẫn tới Thiên Y ở phần cuối dãy.",
        },
        {
          title: "Họa Hại cần được sử dụng đúng cách",
          summary:
            "Họa Hại xuất hiện ở đầu thân số, nhưng tổ hợp tiếp theo là Họa Hại → Sinh Khí, giúp khả năng giao tiếp có hướng phát huy tích cực.",
        },
      ],
    },
    grade: "TỐT",
    verified_by_runtime: true,
  };
}

function pairRow(
  pair_digits: string,
  display_name: string,
  category: string,
  category_label: string,
  strength_label: string,
  strength_visual: boolean[],
): Record<string, unknown> {
  return { pair_digits, display_name, category, category_label, strength_label, strength_visual };
}

function tripleRow(
  digits: string,
  left_energy_label: string,
  right_energy_label: string,
  customer_title: string,
  customer_summary: string,
  domains: string[],
  priority: string,
): Record<string, unknown> {
  return {
    digits,
    left_energy_label,
    right_energy_label,
    customer_title,
    customer_summary,
    domains,
    priority,
    interpretation_status: "DEFINED",
  };
}

function domainRow(
  domain: string,
  conclusion: string,
  narrative: string,
  caution: string,
): Record<string, unknown> {
  return { domain, conclusion, narrative, caution };
}

function findingRow(title: string, summary: string): Record<string, unknown> {
  return { title, summary };
}
