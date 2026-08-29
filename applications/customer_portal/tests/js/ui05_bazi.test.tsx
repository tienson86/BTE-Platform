/**
 * UI-05 Card 02 BaZi Structure — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  BAZI_TITLE,
  BAZI_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptBaziCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  identity: {
    four_pillars: {
      year: { stem: "Giáp", branch: "Tý", nayin_element: "Hải Trung Kim" },
      month: { stem: "Bính", branch: "Dần", nayin_element: "Lư Trung Hỏa" },
      day: { stem: "Mậu", branch: "Ngọ", nayin_element: "Thiên Hà Thủy" },
      hour: { stem: "Canh", branch: "Thân", nayin_element: "Tuyền Trung Thủy" },
    },
  },
  bazi: {
    day_master: "Mậu",
    day_master_element: "Thổ",
    day_master_yin_yang: "Dương",
    year_pillar: {
      stem: "Giáp",
      branch: "Tý",
      nap_am: "Hải Trung Kim",
      ten_god: "Thiên Ấn",
      hidden_stems: ["Quý"],
      truong_sinh: "Mộ",
    },
    month_pillar: {
      stem: "Bính",
      branch: "Dần",
      nap_am: "Lư Trung Hỏa",
      ten_god: "Thất Sát",
      hidden_stems: ["Giáp", "Bính", "Mậu"],
      truong_sinh: "Trường Sinh",
    },
    day_pillar: {
      stem: "Mậu",
      branch: "Ngọ",
      nap_am: "Thiên Hà Thủy",
      hidden_stems: ["Đinh", "Kỷ"],
      truong_sinh: "Đế Vượng",
    },
    hour_pillar: {
      stem: "Canh",
      branch: "Thân",
      nap_am: "Tuyền Trung Thủy",
      ten_god: "Thực Thần",
      hidden_stems: ["Canh", "Nhâm", "Mậu"],
      truong_sinh: "Suy",
    },
  },
  ten_gods: {
    visible: [
      { pillar: "year", stem: "Giáp", element: "Mộc", yin_yang: "Dương", ten_god: "Thiên Ấn" },
      { pillar: "month", stem: "Bính", element: "Hỏa", yin_yang: "Dương", ten_god: "Thất Sát" },
      { pillar: "hour", stem: "Canh", element: "Kim", yin_yang: "Dương", ten_god: "Thực Thần" },
    ],
    hidden: [
      { pillar: "year", hidden_stem: "Quý", ten_god: "Chính Ấn" },
      { pillar: "month", hidden_stem: "Giáp", ten_god: "Kiếp Tài" },
      { pillar: "month", hidden_stem: "Bính", ten_god: "Thất Sát" },
      { pillar: "month", hidden_stem: "Mậu", ten_god: "Thiên Ấn" },
      { pillar: "day", hidden_stem: "Đinh", ten_god: "Thiên Tài" },
      { pillar: "day", hidden_stem: "Kỷ", ten_god: "Tỷ Kiên" },
      { pillar: "hour", hidden_stem: "Canh", ten_god: "Thực Thần" },
      { pillar: "hour", hidden_stem: "Nhâm", ten_god: "Thiên Tài" },
      { pillar: "hour", hidden_stem: "Mậu", ten_god: "Tỷ Kiên" },
    ],
  },
} as AnalysisDataDto;

function renderLive() {
  return render(
    <CommercialDashboardPage analysis={LIVE_ANALYSIS} resultSource="current" layoutMode="live" />,
  );
}

function baziCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="bazi"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-05 BaZi structure card", () => {
  it("B1 replaces the BaZi skeleton with the real BaZi component", () => {
    const { container } = renderLive();
    const card = baziCard(container);
    expect(card.getAttribute("data-implemented")).toBe("bazi");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("B2 keeps BaZi span at 8/12", () => {
    const { container } = renderLive();
    const card = baziCard(container);
    expect(card.getAttribute("data-span")).toBe("8");
    expect(card.className).toMatch(/bte-cdash__card--span-8/);
  });

  it("B3 uses the customer title BÁT TỰ", () => {
    const { container } = renderLive();
    expect(baziCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(BAZI_TITLE);
    expect(baziCard(container).textContent).not.toMatch(
      /Tứ Trụ chi tiết|BaZi Structure|Four Pillars Detail|Technical BaZi/,
    );
  });

  it("B4 renders Năm / Tháng / Ngày / Giờ column headers", () => {
    const { container } = renderLive();
    const labels = [...baziCard(container).querySelectorAll("thead [data-pillar]")].map(
      (node) => node.textContent,
    );
    expect(labels).toEqual(["Năm", "Tháng", "Ngày", "Giờ"]);
  });

  it("B5 binds canonical Thiên Can values", () => {
    const { container } = renderLive();
    const stems = [...baziCard(container).querySelectorAll('[data-bazi-field="stem"]')].map(
      (node) => node.textContent,
    );
    expect(stems[0]).toMatch(/Giáp/);
    expect(stems[1]).toMatch(/Bính/);
    expect(stems[2]).toMatch(/Mậu/);
    expect(stems[3]).toMatch(/Canh/);
    expect(adaptBaziCard(LIVE_ANALYSIS).pillars.map((pillar) => pillar.stem)).toEqual([
      "Giáp",
      "Bính",
      "Mậu",
      "Canh",
    ]);
  });

  it("B6 binds canonical Địa Chi values", () => {
    const { container } = renderLive();
    const branches = [...baziCard(container).querySelectorAll('[data-bazi-field="branch"]')].map(
      (node) => node.textContent,
    );
    expect(branches[0]).toMatch(/Tý/);
    expect(branches[1]).toMatch(/Dần/);
    expect(branches[2]).toMatch(/Ngọ/);
    expect(branches[3]).toMatch(/Thân/);
  });

  it("B7 binds all four Nạp Âm values", () => {
    const { container } = renderLive();
    const values = [...baziCard(container).querySelectorAll('[data-bazi-field="nap-am"]')].map(
      (node) => node.textContent,
    );
    expect(values).toEqual(["Hải Trung Kim", "Lư Trung Hỏa", "Thiên Hà Thủy", "Tuyền Trung Thủy"]);
  });

  it("B8 supports all canonical hidden stems under each branch", () => {
    const bound = adaptBaziCard(LIVE_ANALYSIS);
    expect(bound.pillars.find((pillar) => pillar.key === "month")?.hiddenStems.map((item) => item.stem)).toEqual([
      "Giáp",
      "Bính",
      "Mậu",
    ]);
    const { container } = renderLive();
    fireEvent.click(baziCard(container).querySelector("button.bte-bazi__toggle") as HTMLButtonElement);
    const monthHidden = baziCard(container).querySelector('[data-pillar="month"][data-bazi-field="hidden"]');
    expect(monthHidden?.textContent).toMatch(/Giáp/);
    expect(monthHidden?.textContent).toMatch(/Bính/);
    expect(monthHidden?.textContent).toMatch(/Mậu/);
  });

  it("B9 binds canonical visible Ten Gods placement", () => {
    const { container } = renderLive();
    const gods = [...baziCard(container).querySelectorAll('[data-bazi-field="ten-god"]')].map(
      (node) => node.textContent,
    );
    expect(gods).toEqual(["Thiên Ấn", "Thất Sát", "", "Thực Thần"]);
  });

  it("B10 binds canonical Trường Sinh", () => {
    const { container } = renderLive();
    fireEvent.click(baziCard(container).querySelector("button.bte-bazi__toggle") as HTMLButtonElement);
    const stages = [...baziCard(container).querySelectorAll('[data-bazi-field="stage"]')].map(
      (node) => node.textContent,
    );
    expect(stages).toEqual(["Mộ", "Trường Sinh", "Đế Vượng", "Suy"]);
  });

  it("B11 identifies the Day pillar without a second Day Master hero", () => {
    const { container } = renderLive();
    const card = baziCard(container);
    expect(card.querySelectorAll('[data-day-master="true"]').length).toBeGreaterThan(0);
    expect(card.querySelector('thead [data-pillar="day"]')?.getAttribute("data-day-master")).toBe("true");
    expect(card.textContent).not.toMatch(/NHẬT CHỦ/);
  });

  it("B12 does not calculate astrology in the UI adapter or card", () => {
    const adapter = readFileSync(resolve(ROOT, "baziAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "BaziCard.tsx"), "utf8");
    for (const source of [adapter, card]) {
      expect(source).not.toMatch(/engines\./);
      expect(source).not.toMatch(/STEM_ELEMENT|HIDDEN_STEM_MAP|TRUONG_SINH_MAP|NAP_AM_MAP/);
      expect(source).not.toMatch(/calculateHidden|inferTenGod|lookupNapAm|twelveStageFor/);
    }
    expect(adapter).not.toContain("Nguyễn Tiến Sơn");
    expect(adapter).not.toContain("CASE-0001");
    const rebound = adaptBaziCard({
      bazi: { year_pillar: { stem: "Ất", branch: "Mão", hidden_stems: ["Ất"] } },
    });
    expect(rebound.pillars[0]?.stem).toBe("Ất");
    expect(rebound.pillars[0]?.hiddenStems).toEqual([{ stem: "Ất", tenGod: "" }]);
  });

  it("B13 has no interpretation copy", () => {
    const { container } = renderLive();
    const text = baziCard(container).textContent || "";
    expect(text).not.toMatch(/Điều này cho thấy|Bạn có xu hướng|Vì vậy nên|Đây là lá số/);
    expect(text).not.toMatch(/khuyến nghị|nên làm|đại vận tốt/i);
    const adapter = readFileSync(resolve(ROOT, "baziAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "BaziCard.tsx"), "utf8");
    expect(adapter + card).not.toMatch(/Điều này cho thấy|Bạn có xu hướng/);
  });

  it("B14 expand/collapse is an accessible button", () => {
    const { container } = renderLive();
    const toggle = baziCard(container).querySelector("button.bte-bazi__toggle") as HTMLButtonElement;
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(baziCard(container).querySelector('[data-bazi-row="hidden"]')).toBeNull();
    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(toggle.textContent).toBe("Thu gọn");
    expect(baziCard(container).querySelector('[data-bazi-row="hidden"]')).toBeTruthy();
    expect(baziCard(container).querySelector('[data-bazi-row="stage"]')).toBeTruthy();
    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(toggle.textContent).toBe("Xem chi tiết");
  });

  it("B15 leaves Overview implemented and unchanged in role", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-implemented")).toBe("overview");
    expect(overview?.getAttribute("data-span")).toBe("4");
    expect(overview?.querySelector(".bte-cdash__card-title")?.textContent).toBe("TỔNG QUAN LÁ SỐ");
  });

  it("B16 leaves other Card skeletons unchanged", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual([
      "pattern",
      "shensha",
      "luck",
      "interpretation",
      "action-plan",
    ]);
  });

  it("B17 keeps the canonical grid spans frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("B18 preserves four-pillar relationships in the structural table", () => {
    const { container } = renderLive();
    const card = baziCard(container);
    expect(card.querySelector("table")).toBeTruthy();
    expect([...card.querySelectorAll("thead [data-pillar]")].map((node) => node.getAttribute("data-pillar"))).toEqual(
      ["year", "month", "day", "hour"],
    );
    expect(card.querySelector('[data-bazi-row="stem"] [data-pillar="year"]')?.textContent).toMatch(/Giáp/);
    expect(card.querySelector('[data-bazi-row="branch"] [data-pillar="year"]')?.textContent).toMatch(/Tý/);
  });

  it("B19 missing core data fails cleanly", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={{}} resultSource="current" layoutMode="live" />,
    );
    const card = baziCard(container);
    expect(card.querySelector("[data-bazi-empty]")?.textContent).toBe("Chưa đủ dữ liệu Bát Tự.");
    expect(card.querySelector("table")).toBeNull();
    expect(card.textContent).not.toMatch(/undefined|null|NaN|—/);
    expect(adaptBaziCard({}).available).toBe(false);
  });

  it("B20 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Hỏa" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.bazi?.day_master).toBe("Mậu");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(container.querySelector('[data-layout="visual"]')).toBeTruthy();
    expect(baziCard(container).textContent).toMatch(/Giáp/);
    expect(adaptBaziCard(LIVE_ANALYSIS).pillars[0]?.stem).toBe("Giáp");
    const fixture = readFileSync(resolve(ROOT, "baziFixture.ts"), "utf8");
    const adapter = readFileSync(resolve(ROOT, "baziAdapter.ts"), "utf8");
    expect(fixture).not.toContain("CASE-0001");
    expect(adapter).not.toContain("Hải Trung Kim");
    expect(BAZI_VISUAL_FIXTURE.pillars[0]?.stem).toBe("Giáp");
    expect(BAZI_VISUAL_FIXTURE.pillars[0]?.branch).toBe("Tý");
  });
});
