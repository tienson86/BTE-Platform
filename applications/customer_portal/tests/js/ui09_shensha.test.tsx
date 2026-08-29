/**
 * UI-09 Card 06 ShenSha — visual structure + canonical binding.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  SHENSHA_TITLE,
  SHENSHA_VISUAL_FIXTURE,
  CommercialDashboardPage,
  adaptShenShaCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  bazi: {
    day_master: "Canh",
    shensha: ["Thiên Ất Quý Nhân", "Hoa Cái"],
    shensha_matches: [
      {
        canonical_name: "Thiên Ất Quý Nhân",
        occurrences: [{ pillar: "year" }, { pillar: "day" }],
      },
      {
        canonical_name: "Hoa Cái",
        occurrences: [{ pillar: "hour" }],
      },
      {
        canonical_name: "Đào Hoa",
        occurrences: [{ pillar: "month" }],
      },
      {
        canonical_name: "Dịch Mã",
        occurrences: [{ pillar: "day" }],
      },
      {
        canonical_name: "Cô Thần",
        occurrences: [{ pillar: "year" }],
      },
    ],
  },
} as AnalysisDataDto;

function renderLive(analysis: AnalysisDataDto = LIVE_ANALYSIS) {
  return render(
    <CommercialDashboardPage analysis={analysis} resultSource="current" layoutMode="live" />,
  );
}

function ssCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="shensha"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

function toggle(container: HTMLElement): HTMLButtonElement {
  const button = ssCard(container).querySelector("button.bte-ss__toggle");
  expect(button).toBeTruthy();
  return button as HTMLButtonElement;
}

afterEach(cleanup);

describe("UI-09 ShenSha card", () => {
  it("S1 replaces the ShenSha skeleton with the real component", () => {
    const { container } = renderLive();
    const card = ssCard(container);
    expect(card.getAttribute("data-implemented")).toBe("shensha");
    expect(card.getAttribute("data-skeleton")).toBeNull();
    expect(card.querySelector(".bte-cdash__skel")).toBeNull();
  });

  it("S2 keeps ShenSha span at 6/12", () => {
    const { container } = renderLive();
    expect(ssCard(container).getAttribute("data-span")).toBe("6");
    expect(ssCard(container).className).toMatch(/bte-cdash__card--span-6/);
  });

  it("S3 shows the customer title THẦN SÁT", () => {
    const { container } = renderLive();
    expect(ssCard(container).querySelector(".bte-cdash__card-title")?.textContent).toBe(SHENSHA_TITLE);
    expect(ssCard(container).textContent).not.toMatch(/ShenSha Engine|Auxiliary Stars|Stars/);
  });

  it("S4 renders canonical ShenSha names", () => {
    const { container } = renderLive();
    const text = ssCard(container).textContent || "";
    expect(text).toMatch(/Thiên Ất Quý Nhân/);
    expect(text).toMatch(/Hoa Cái/);
    expect(adaptShenShaCard(LIVE_ANALYSIS).items.map((item) => item.name)).toEqual([
      "Thiên Ất Quý Nhân",
      "Hoa Cái",
      "Đào Hoa",
      "Dịch Mã",
      "Cô Thần",
    ]);
  });

  it("S5 renders canonical placements attached to named items", () => {
    const { container } = renderLive();
    expect(
      ssCard(container).querySelector('[data-ss-name="Thiên Ất Quý Nhân"] [data-ss-placement]')?.textContent,
    ).toBe("Trụ Năm · Trụ Ngày");
  });

  it("S6 does not build an absent Có/Không checklist", () => {
    const { container } = renderLive();
    const text = ssCard(container).textContent || "";
    expect(text).not.toMatch(/Không$/m);
    expect(text).not.toMatch(/Thiên Đức — Không|Văn Xương — Không/);
    expect(adaptShenShaCard(LIVE_ANALYSIS).items.some((item) => item.name === "Văn Xương")).toBe(false);
  });

  it("S7 does not invent category membership in the adapter", () => {
    const adapter = readFileSync(resolve(ROOT, "shenShaAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/Quý Nhân & Hỗ trợ|Học tập & Danh tiếng|Quan hệ & Tình cảm/);
    expect(adaptShenShaCard(LIVE_ANALYSIS).grouped).toBe(false);
    expect(adaptShenShaCard(LIVE_ANALYSIS).groups).toEqual([]);
  });

  it("S8 does not contain a local meaning dictionary", () => {
    const adapter = readFileSync(resolve(ROOT, "shenShaAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "ShenShaCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/nghệ thuật|tâm linh|tình duyên|đi xa|xuất ngoại|cô độc/);
    expect(card).not.toMatch(/nghệ thuật|tâm linh|tình duyên/);
    expect(adapter).toContain("approvedShenShaMeaning");
    const rebound = adaptShenShaCard({
      bazi: {
        shensha_matches: [{ canonical_name: "Đào Hoa" }, { canonical_name: "Dịch Mã" }, { canonical_name: "Cô Thần" }],
      },
    });
    expect(rebound.items.every((item) => item.meaning === "")).toBe(true);
  });

  it("S9 does not infer Hung/Cát labels", () => {
    const { container } = renderLive();
    expect(ssCard(container).textContent).not.toMatch(/Hung|Cát|Rất tốt|Rất xấu/);
  });

  it("S10 does not show fake ranking stars", () => {
    const { container } = renderLive();
    expect(ssCard(container).textContent).not.toMatch(/★/);
  });

  it("S11 does not use fear-based copy", () => {
    const { container } = renderLive();
    expect(ssCard(container).textContent).not.toMatch(/Đại hung|Rất nguy hiểm|Tai họa|Khắc chồng|ly hôn/);
  });

  it("S12 does not predict life outcomes", () => {
    const { container } = renderLive();
    expect(ssCard(container).textContent).not.toMatch(/kết hôn|giàu có|bệnh tật|tai nạn|kiện tụng/);
  });

  it("S13 missing data fails cleanly", () => {
    const { container } = renderLive({ bazi: { day_master: "Canh" } });
    expect(ssCard(container).querySelector("[data-ss-empty]")?.textContent).toBe("Chưa có dữ liệu Thần Sát.");
    expect(ssCard(container).querySelector("[data-ss-section]")).toBeNull();
  });

  it("S14 does not call astrology engines", () => {
    const adapter = readFileSync(resolve(ROOT, "shenShaAdapter.ts"), "utf8");
    const card = readFileSync(resolve(ROOT, "ShenShaCard.tsx"), "utf8");
    expect(adapter).not.toMatch(/engines\/|ShenShaEngine|shensha_engine/);
    expect(card).not.toMatch(/engines\/|ShenShaEngine|shensha_engine/);
  });

  it("S15 keeps the canonical grid spans frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("S16 leaves Identity through Pattern in role", () => {
    const { container } = renderLive();
    expect(container.querySelector("[data-identity-header='true']")).toBeTruthy();
    expect(container.querySelector('[data-card="overview"]')?.getAttribute("data-implemented")).toBe("overview");
    expect(container.querySelector('[data-card="bazi"]')?.getAttribute("data-implemented")).toBe("bazi");
    expect(container.querySelector('[data-card="five-elements"]')?.getAttribute("data-implemented")).toBe(
      "five-elements",
    );
    expect(container.querySelector('[data-card="ten-gods"]')?.getAttribute("data-implemented")).toBe("ten-gods");
    expect(container.querySelector('[data-card="pattern"]')?.getAttribute("data-implemented")).toBe("pattern");
  });

  it("S17 leaves Interpretation and Action Plan as skeletons", () => {
    const { container } = renderLive();
    const skeletons = [...container.querySelectorAll("[data-card][data-skeleton='true']")].map(
      (node) => node.getAttribute("data-card"),
    );
    expect(skeletons).toEqual(["interpretation", "action-plan"]);
  });

  it("S18 expand/collapse is an accessible button", () => {
    const { container } = renderLive();
    const button = toggle(container);
    expect(button.getAttribute("aria-expanded")).toBe("false");
    expect(button.textContent).toBe("Xem chi tiết");
    expect(ssCard(container).querySelector('[data-ss-name="Cô Thần"]')).toBeNull();
    fireEvent.click(button);
    expect(toggle(container).getAttribute("aria-expanded")).toBe("true");
    expect(ssCard(container).querySelector('[data-ss-name="Cô Thần"]')).toBeTruthy();
    expect(ssCard(container).querySelector("[data-ss-placement]")).toBeTruthy();
  });

  it("S19 mobile structure stays a vertical stacked card", () => {
    const { container } = renderLive();
    expect(ssCard(container).querySelector("[data-ss-section='featured']")).toBeTruthy();
    expect(ssCard(container).textContent).toMatch(/Thần Sát nổi bật/);
  });

  it("S20 ResultStore / routing boot remains intact", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Hỏa" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.bazi?.shensha_matches?.[0]?.canonical_name).toBe("Thiên Ất Quý Nhân");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
    expect(resolveResultBoot(null, "?layout=visual").layoutMode).toBe("visual");
  });

  it("semantic safety: raw star names do not become meanings or Hung/Cát", () => {
    const rebound = adaptShenShaCard({
      bazi: {
        shensha_matches: [
          { canonical_name: "Hoa Cái" },
          { canonical_name: "Đào Hoa" },
          { canonical_name: "Dịch Mã" },
          { canonical_name: "Cô Thần" },
        ],
      },
    });
    const blob = JSON.stringify(rebound);
    expect(rebound.items.map((item) => item.name)).toEqual(["Hoa Cái", "Đào Hoa", "Dịch Mã", "Cô Thần"]);
    expect(rebound.items.filter((item) => item.name !== "Hoa Cái").every((item) => item.meaning === "")).toBe(true);
    expect(rebound.items.find((item) => item.name === "Hoa Cái")?.meaning).not.toMatch(/cô độc|artist|hôn nhân/);
    expect(blob).not.toMatch(/nghệ thuật|tâm linh|cô độc/);
    expect(blob).not.toMatch(/tình duyên tốt|nhiều người yêu/);
    expect(blob).not.toMatch(/đi xa|xuất ngoại/);
    expect(blob).not.toMatch(/hôn nhân xấu/);
    expect(blob).not.toMatch(/Hung|Cát/);
  });

  it("Phase A visual fixture is isolated from live binding", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="visual" resultSource="preview" />,
    );
    expect(ssCard(container).getAttribute("data-grouped")).toBe("true");
    expect(ssCard(container).textContent).toMatch(/Quý Nhân & Hỗ trợ/);
    expect(adaptShenShaCard(LIVE_ANALYSIS).grouped).toBe(false);
    const fixture = readFileSync(resolve(ROOT, "shenShaFixture.ts"), "utf8");
    expect(fixture).not.toContain("Bính");
    expect(fixture).not.toContain("CASE-0001");
  });
});
