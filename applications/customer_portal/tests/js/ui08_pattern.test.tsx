/**
 * UI-08 Card 05 Pattern — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  PATTERN_TITLE,
  PATTERN_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptPatternCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  pattern: {
    pattern: "chinh_an",
    cach_cuc: "Chính Ấn",
    winning_rule_id: "pat_ca_01",
    evidence_compact:
      "Nguyệt lệnh Sửu · khí chính Kỷ · Kỷ đối với Canh là Chính Ấn · rule pat_ca_01",
    dung_than: "Hỏa",
    hy_than: "Mộc",
    ky_than: "Thủy",
  },
  bazi: { day_master: "Canh" },
} as AnalysisDataDto;

function renderLive(analysis: AnalysisDataDto = LIVE_ANALYSIS) {
  return render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
}

function patCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="pattern"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

function toggle(container: HTMLElement): HTMLButtonElement {
  const button = patCard(container).querySelector("button.bte-pat__toggle");
  expect(button).toBeTruthy();
  return button as HTMLButtonElement;
}

afterEach(cleanup);

describe("UI-08 Pattern card", () => {
  it("P1 replaces the Pattern skeleton with the real component", () => {
    const { container } = renderLive();
    const card = patCard(container);
    expect(card.getAttribute("data-implemented")).toBe("pattern");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("P2 keeps Pattern span at 4/12", () => {
    const { container } = renderLive();
    expect(patCard(container).getAttribute("data-span")).toBe("4");
    expect(patCard(container).className).toMatch(/bte-cdash__card--span-4/);
  });

  it("P3 shows the customer title MỆNH CỤC", () => {
    const { container } = renderLive();
    expect(patCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(PATTERN_TITLE);
    expect(patCard(container).textContent).not.toMatch(/Pattern Engine|Cách Cục Engine|Pattern Classification/i);
  });

  it("P4 binds the canonical customer-facing Pattern label", () => {
    const { container } = renderLive();
    expect(patCard(container).querySelector("[data-pat-primary]")?.textContent).toBe("Chính Ấn");
    expect(adaptPatternCard(LIVE_ANALYSIS).primary).toBe("Chính Ấn");
  });

  it("P5 shows secondary Pattern only from a canonical source", () => {
    const { container } = renderLive();
    expect(patCard(container).querySelector("[data-pat-section='secondary']")).toBeNull();
    const withSecondary = adaptPatternCard({
      pattern: { cach_cuc: "Chính Ấn", secondary_pattern: "Thiên Ấn" },
    });
    expect(withSecondary.secondary).toBe("Thiên Ấn");
    expect(adaptPatternCard(LIVE_ANALYSIS).secondary).toBe("");
  });

  it("P6 shows Pattern Status only from a canonical trusted status", () => {
    const { container } = renderLive();
    expect(patCard(container).querySelector("[data-pat-section='status']")).toBeNull();
    expect(adaptPatternCard({ pattern: { cach_cuc: "Chính Ấn", pattern_quality: "Đắc cách" } }).status).toBe(
      "Đắc cách",
    );
    expect(adaptPatternCard({ pattern: { cach_cuc: "Chính Ấn", qualification_level: 2 } }).status).toBe("");
    expect(adaptPatternCard({ pattern: { cach_cuc: "Chính Ấn", score: 0.9 } }).status).toBe("");
  });

  it("P7 shows Formation only from canonical evidence", () => {
    const { container } = renderLive();
    const flow = patCard(container).querySelector("[data-pat-section='formation']")?.textContent || "";
    expect(flow).toMatch(/Nguyệt lệnh Sửu/);
    expect(adaptPatternCard({ pattern: { cach_cuc: "Chính Ấn" } }).formation).toEqual([]);
  });

  it("P8 does not classify Pattern in the frontend", () => {
    const adapter = readFileSync(resolve(ROOT, "patternAdapter.ts"), "utf8");
    expect(adapter).toMatch(/canonicalPatternLabel/);
    expect(adapter).toMatch(/TRUSTED_STATUS/);
    expect(adapter).not.toMatch(/qualification_level|strength_level|month_branch|month_main_qi/);
    expect(adapter).not.toMatch(/Chính Cách|Phụ Cách/);
  });

  it("P9 does not infer Formation from raw chart fields", () => {
    const rebound = adaptPatternCard({
      pattern: {
        month_branch: "Sửu",
        month_main_qi: "Kỷ",
        month_hidden_stems: ["Mậu"],
        penetration_exact: true,
      },
      bazi: { month_pillar: { branch: "Sửu", stem: "Kỷ" } },
    });
    expect(rebound.available).toBe(false);
    expect(rebound.primary).toBe("");
    expect(rebound.formation).toEqual([]);
  });

  it("P10 does not display Useful God", () => {
    const { container } = renderLive();
    const text = patCard(container).textContent || "";
    expect(text).not.toMatch(/Dụng Thần|Hỷ Thần|Kỵ Thần/);
    expect(text).not.toMatch(/Hỏa|Mộc|Thủy/);
  });

  it("P11 does not display Luck", () => {
    const { container } = renderLive();
    expect(patCard(container).textContent).not.toMatch(/Đại Vận|Lưu Niên/);
  });

  it("P12 does not display career advice", () => {
    const { container } = renderLive();
    expect(patCard(container).textContent).not.toMatch(/Phù hợp lãnh đạo|Phù hợp kinh doanh|Phù hợp nghiên cứu/);
  });

  it("P13 does not expose raw Pattern or Rule IDs", () => {
    const { container } = renderLive();
    const text = patCard(container).textContent || "";
    expect(text).not.toMatch(/chinh_an|pat_ca_01|winning_rule_id|rule /);
  });

  it("P14 missing data fails cleanly", () => {
    const { container } = renderLive({ pattern: { pattern: "chinh_an" } });
    expect(patCard(container).querySelector("[data-pat-empty]")?.textContent).toBe(
      "Chưa đủ dữ liệu Mệnh Cục.",
    );
    expect(patCard(container).querySelector("[data-pat-primary]")).toBeNull();
  });

  it("P15 does not call astrology engines", () => {
    const adapter = readFileSync(resolve(ROOT, "patternAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "PatternCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/engines\/|PatternEngine|pattern_engine/);
    expect(card).not.toMatch(/engines\/|PatternEngine|pattern_engine/);
  });

  it("P16 keeps the canonical grid spans frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("P17 leaves Identity, Overview, BaZi, Five Elements, and Ten Gods in role", () => {
    const { container } = renderLive();
    expect(container.querySelector("[data-identity-header='true']")).toBeTruthy();
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-implemented")).toBe(
      "overview",
    );
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-implemented")).toBe("bazi");
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-implemented")).toBe(
      "five-elements",
    );
    expect(container.querySelector('[data-card="ten-gods"]')?.getAttribute("data-implemented")).toBe(
      "ten-gods",
    );
  });

  it("P18 leaves Luck and later Cards as skeletons", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual(["action-plan"]);
  });

  it("P19 expand/collapse is an accessible button", () => {
    const { container } = renderLive();
    const button = toggle(container);
    expect(button.getAttribute("aria-expanded")).toBe("false");
    expect(button.textContent).toBe("Xem quá trình hình thành");
    const collapsed = patCard(container).querySelector("[data-pat-section='formation']")?.textContent || "";
    expect(collapsed).toMatch(/Nguyệt lệnh Sửu/);
    expect(collapsed).not.toMatch(/khí chính Kỷ/);
    fireEvent.click(button);
    expect(toggle(container).getAttribute("aria-expanded")).toBe("true");
    expect(toggle(container).textContent).toBe("Thu gọn");
    expect(patCard(container).querySelector("[data-pat-section='formation']")?.textContent).toMatch(
      /khí chính Kỷ/,
    );
  });

  it("P20 mobile structure stays a vertical stacked card", () => {
    const { container } = renderLive();
    expect(patCard(container).querySelector("[data-pat-section='primary']")).toBeTruthy();
    expect(patCard(container).querySelector("[data-pat-section='formation']")).toBeTruthy();
  });

  it("P21 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Hỏa" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.pattern).toMatchObject({ cach_cuc: "Chính Ấn" });
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("semantic safety: raw month branch, stems, strength, and Ten Gods do not become Pattern", () => {
    expect(
      adaptPatternCard({
        pattern: { month_branch: "Sửu", month_main_qi_ten_god: "Chính Ấn" },
      }).primary,
    ).toBe("");
    expect(
      adaptPatternCard({
        bazi: { hour_pillar: { stem: "Mậu" } },
        pattern: { cach_cuc: "Chính Ấn", penetration_exact: true },
      }).status,
    ).toBe("");
    expect(
      adaptPatternCard({
        strength: { strength_level: "weak", strength_score: 0.2 },
        pattern: { cach_cuc: "Chính Ấn" },
      }).status,
    ).toBe("");
    expect(
      adaptPatternCard({
        ten_gods: { visible_labels: ["Chính Ấn", "Thiên Ấn"] },
      }).available,
    ).toBe(false);
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(patCard(container).querySelector("[data-pat-primary]")?.textContent).toBe("CHÍNH ẤN CÁCH");
    expect(PATTERN_VISUAL_FIXTURE.status).toBe("Đắc cách");
    expect(adaptPatternCard(LIVE_ANALYSIS).primary).toBe("Chính Ấn");
    expect(adaptPatternCard(LIVE_ANALYSIS).status).toBe("");
    const fixture = readFileSync(resolve(ROOT, "patternFixture.ts"), "utf8");
    expect(fixture).not.toContain("Bính");
    expect(fixture).not.toContain("CASE-0001");
  });
});
