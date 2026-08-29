/**
 * UI-07 Card 04 Ten Gods — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  TEN_GODS_TITLE,
  TEN_GODS_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptTenGodsCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  bazi: {
    day_master: "Canh",
    year_pillar: { stem: "Bính", ten_god: "Thất Sát" },
    month_pillar: { stem: "Tân", ten_god: "Kiếp Tài" },
    day_pillar: { stem: "Canh", ten_god: "Nhật Chủ" },
    hour_pillar: { stem: "Mậu", ten_god: "Thiên Ấn" },
  },
  ten_gods: {
    visible: [
      { pillar: "year", stem: "Bính", ten_god: "Thất Sát" },
      { pillar: "month", stem: "Tân", ten_god: "Kiếp Tài" },
      { pillar: "day", stem: "Canh", ten_god: "Nhật Chủ" },
      { pillar: "hour", stem: "Mậu", ten_god: "Thiên Ấn" },
    ],
    hidden: [
      { pillar: "year", hidden_stem: "Giáp", ten_god: "Thiên Tài" },
      { pillar: "year", hidden_stem: "Bính", ten_god: "Thất Sát" },
      { pillar: "month", hidden_stem: "Kỷ", ten_god: "Chính Ấn" },
      { pillar: "day", hidden_stem: "Đinh", ten_god: "Chính Quan" },
      { pillar: "hour", hidden_stem: "Giáp", ten_god: "Thiên Tài" },
    ],
    visible_labels: ["Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"],
  },
  score: { ten_god_score: 100 },
} as AnalysisDataDto;

function renderLive() {
  return render(
    <CommercialDashboardPage analysis={LIVE_ANALYSIS} resultSource="current" layoutMode="live" />,
  );
}

function tgCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="ten-gods"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

function toggle(container: HTMLElement): HTMLButtonElement {
  const button = tgCard(container).querySelector("button.bte-tg__toggle");
  expect(button).toBeTruthy();
  return button as HTMLButtonElement;
}

afterEach(cleanup);

describe("UI-07 Ten Gods card", () => {
  it("T1 replaces the Ten Gods skeleton with the real component", () => {
    const { container } = renderLive();
    const card = tgCard(container);
    expect(card.getAttribute("data-implemented")).toBe("ten-gods");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("T2 keeps Ten Gods span at 4/12", () => {
    const { container } = renderLive();
    expect(tgCard(container).getAttribute("data-span")).toBe("4");
    expect(tgCard(container).className).toMatch(/bte-cdash__card--span-4/);
  });

  it("T3 uses the customer title THẬP THẦN", () => {
    const { container } = renderLive();
    expect(tgCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(TEN_GODS_TITLE);
    expect(tgCard(container).textContent).not.toMatch(/Ten Gods|Shishen Engine|Ten God Score/);
  });

  it("T4 binds canonical visible pillar Ten Gods", () => {
    const { container } = renderLive();
    const card = tgCard(container);
    expect(card.querySelector('[data-pillar="year"]')?.getAttribute("data-ten-god")).toBe("Thất Sát");
    expect(card.querySelector('[data-pillar="month"]')?.getAttribute("data-ten-god")).toBe("Kiếp Tài");
    expect(card.querySelector('[data-pillar="day"]')?.getAttribute("data-ten-god")).toBe("Nhật Chủ");
    expect(card.querySelector('[data-pillar="hour"]')?.getAttribute("data-ten-god")).toBe("Thiên Ấn");
  });

  it("T5 binds canonical hidden Ten Gods", () => {
    const bound = adaptTenGodsCard(LIVE_ANALYSIS);
    expect(bound.hidden.map((item) => item.tenGod)).toEqual([
      "Thiên Tài",
      "Thất Sát",
      "Chính Ấn",
      "Chính Quan",
      "Thiên Tài",
    ]);
    const { container } = renderLive();
    fireEvent.click(toggle(container));
    expect(tgCard(container).querySelector('[data-tg-section="hidden"]')?.textContent).toMatch(/Thiên Tài/);
    expect(tgCard(container).querySelector('[data-tg-section="hidden"]')?.textContent).toMatch(/Chính Ấn/);
  });

  it("T6 keeps the Day pillar as Nhật Chủ, not Tỷ Kiên", () => {
    const bound = adaptTenGodsCard(LIVE_ANALYSIS);
    expect(bound.visible.find((item) => item.pillar === "day")?.tenGod).toBe("Nhật Chủ");
    expect(bound.distribution.map((item) => item.name)).not.toContain("Nhật Chủ");
    const { container } = renderLive();
    const day = tgCard(container).querySelector('[data-pillar="day"]');
    expect(day?.getAttribute("data-day-master")).toBe("true");
    expect(day?.textContent).toMatch(/Nhật Chủ/);
    expect(day?.textContent).not.toMatch(/Tỷ Kiên/);
  });

  it("T7 preserves traditional order in the full distribution", () => {
    const { container } = renderLive();
    fireEvent.click(toggle(container));
    const names = [...tgCard(container).querySelectorAll("[data-tg-dist]")].map((node) =>
      node.getAttribute("data-tg-dist"),
    );
    expect(names).toEqual(["Kiếp Tài", "Thiên Tài", "Thất Sát", "Chính Quan", "Thiên Ấn", "Chính Ấn"]);
  });

  it("T8 does not calculate Ten Gods relationships in the UI", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "TenGodsCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/engines\./);
    expect(card).not.toMatch(/engines\./);
    expect(adapter).not.toMatch(/ten_god_name\(|map_stem_to_ten_god|LABEL_TO_GOD_ID/);
    expect(adapter).not.toContain("CASE-0001");
  });

  it("T9 has no local personality dictionary", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "TenGodsCard.tsx"), "utf8");
    expect(adapter + card).not.toMatch(/Tư duy nghiên cứu|Quyết đoán|Cạnh tranh|thông minh/);
  });

  it("T10 has no capability-group mapping", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "TenGodsCard.tsx"), "utf8");
    expect(adapter + card).not.toMatch(/Lãnh đạo|Học tập|Sáng tạo|Tài chính/);
  });

  it("T11 has no career recommendations", () => {
    const { container } = renderLive();
    expect(tgCard(container).textContent).not.toMatch(/Phù hợp làm|Phù hợp kinh doanh|Giỏi tài chính/);
  });

  it("T12 has no good/bad labels", () => {
    const { container } = renderLive();
    expect(tgCard(container).textContent).not.toMatch(/\bTốt\b|\bXấu\b|\bHung\b|\bCát\b/);
  });

  it("T13 missing data fails cleanly", () => {
    const { container } = render(
      <CommercialDashboardPage analysis={{}} resultSource="current" layoutMode="live" />,
    );
    expect(tgCard(container).querySelector("[data-tg-empty]")?.textContent).toBe(
      "Chưa đủ dữ liệu Thập Thần.",
    );
    expect(tgCard(container).querySelector("[data-tg-section]")).toBeNull();
    expect(adaptTenGodsCard({}).available).toBe(false);
  });

  it("T14 does not call engines", () => {
    const adapter = readFileSync(resolve(ROOT, "tenGodsAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/engines\./);
    expect(adapter).not.toContain("ten_god_score");
  });

  it("T15 keeps the canonical grid spans frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("T16 leaves Identity, Overview, BaZi, and Five Elements in role", () => {
    const { container } = renderLive();
    expect(container.querySelector("[data-identity-header='true']")).toBeTruthy();
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-implemented")).toBe(
      "overview",
    );
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-implemented")).toBe("bazi");
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-implemented")).toBe(
      "five-elements",
    );
  });

  it("T17 leaves ShenSha and later Cards as skeletons", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual(["interpretation", "action-plan"]);
  });

  it("T18 expand/collapse is an accessible button", () => {
    const { container } = renderLive();
    const button = toggle(container);
    expect(button.getAttribute("aria-expanded")).toBe("false");
    expect(tgCard(container).querySelector('[data-tg-section="hidden"]')).toBeNull();
    fireEvent.click(button);
    expect(toggle(container).getAttribute("aria-expanded")).toBe("true");
    expect(toggle(container).textContent).toBe("Thu gọn");
    expect(tgCard(container).querySelector('[data-tg-section="hidden"]')).toBeTruthy();
    expect(tgCard(container).querySelector('[data-tg-section="distribution"]')).toBeTruthy();
  });

  it("T19 mobile structure stays a vertical stacked card", () => {
    const { container } = renderLive();
    expect(tgCard(container).querySelector('[data-tg-section="visible"]')).toBeTruthy();
    expect(tgCard(container).textContent).toMatch(/Lộ rõ/);
  });

  it("T20 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Hỏa" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.ten_gods?.visible_labels).toContain("Thất Sát");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("semantic safety: raw Ten God names do not become personality or capability copy", () => {
    const { container } = renderLive();
    const text = tgCard(container).textContent || "";
    expect(text).toMatch(/Thất Sát/);
    expect(text).toMatch(/Thiên Ấn/);
    expect(text).toMatch(/Thiên Tài/);
    expect(text).not.toMatch(/lãnh đạo|quyết đoán|quyền lực/i);
    expect(text).not.toMatch(/nghiên cứu|học tập tốt|thông minh/i);
    expect(text).not.toMatch(/giỏi kiếm tiền/i);
    const rebound = adaptTenGodsCard({
      ten_gods: { visible: [{ pillar: "day", ten_god: "Nhật Chủ" }] },
    });
    expect(rebound.visible[0]?.tenGod).toBe("Nhật Chủ");
    expect(rebound.visible[0]?.tenGod).not.toBe("Tỷ Kiên");
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(tgCard(container).textContent).toMatch(/Nổi bật/);
    expect(TEN_GODS_VISUAL_FIXTURE.featured).toEqual(["Thiên Ấn", "Thất Sát", "Kiếp Tài"]);
    expect(adaptTenGodsCard(LIVE_ANALYSIS).featured).toEqual([]);
    const fixture = readFileSync(resolve(ROOT, "tenGodsFixture.ts"), "utf8");
    expect(fixture).not.toContain("Bính");
  });
});
