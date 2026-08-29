/**
 * UI-09R — ShenSha commercial content: name + placement + approved meaning.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { CommercialDashboardPage, adaptShenShaCard } from "../../src/screens/commercial_dashboard";
import { approvedShenShaMeaning } from "../../src/adapters/shenShaApprovedKnowledge";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const CASE_0001 = {
  bazi: {
    shensha_matches: [
      {
        canonical_name: "Thiên Ất Quý Nhân",
        occurrences: [{ pillar: "month" }],
        evidence_text: "Nguyệt chi Sửu → gặp Tỵ",
      },
      {
        canonical_name: "Hồng Loan",
        occurrences: [{ pillar: "month" }],
        evidence_text: "Năm chi Mão → gặp Tỵ",
      },
      {
        canonical_name: "Thiên Đức Quý Nhân",
        occurrences: [{ pillar: "day" }],
        evidence_text: "Nguyệt chi Sửu → gặp Tân",
      },
      {
        canonical_name: "Nguyệt Đức Quý Nhân",
        occurrences: [{ pillar: "day" }],
        evidence_text: "Nguyệt chi Sửu → gặp Tân",
      },
    ],
  },
} as AnalysisDataDto;

function renderCase() {
  return render(
    <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
  );
}

function ssCard(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="shensha"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-09R ShenSha commercial content", () => {
  it("SR1 no orphan placement sequence Tháng Tháng Ngày Ngày", () => {
    const { container } = renderCase();
    const placements = [...ssCard(container).querySelectorAll("[data-ss-placement]")].map(
      (node) => node.textContent,
    );
    expect(placements.join("")).not.toBe("ThángThángNgàyNgày");
    expect(ssCard(container).textContent).not.toMatch(/Tháng\s*Tháng\s*Ngày\s*Ngày/);
  });

  it("SR2 every displayed placement belongs to a named ShenSha item", () => {
    const { container } = renderCase();
    const items = [...ssCard(container).querySelectorAll("[data-ss-name]")];
    expect(items.length).toBe(4);
    for (const item of items) {
      const placement = item.querySelector("[data-ss-placement]");
      expect(placement?.textContent).toMatch(/^Trụ /);
      expect(item.querySelector(".bte-ss__name")?.textContent).toBeTruthy();
    }
  });

  it("SR3 generic disclaimer is not the primary Card content", () => {
    const { container } = renderCase();
    const card = ssCard(container);
    const meanings = [...card.querySelectorAll("[data-ss-meaning]")];
    expect(meanings.length).toBeGreaterThan(0);
    expect(card.querySelector("[data-ss-note]")?.textContent).toMatch(/^Lưu ý:/);
    expect(meanings[0]?.textContent?.length || 0).toBeGreaterThan(10);
  });

  it("SR4 no expand button when four items already show customer content", () => {
    const { container } = renderCase();
    expect(ssCard(container).querySelector("button.bte-ss__toggle")).toBeNull();
  });

  it("SR5 approved customer meanings render when available", () => {
    const { container } = renderCase();
    expect(ssCard(container).querySelector('[data-ss-name="Thiên Ất Quý Nhân"] [data-ss-meaning]')?.textContent).toBe(
      approvedShenShaMeaning("Thiên Ất Quý Nhân"),
    );
    expect(approvedShenShaMeaning("Thiên Ất Quý Nhân")).toBeTruthy();
    expect(approvedShenShaMeaning("Hồng Loan")).toBeTruthy();
  });

  it("SR6 no local React meaning dictionary in the card", () => {
    const card = readFileSync(resolve(ROOT, "ShenShaCard.tsx"), "utf8");
    expect(card).not.toMatch(/Thiên Ất Quý Nhân.*=.*chỗ đỡ/);
    expect(card).not.toContain("approvedShenShaMeaning");
  });

  it("SR7 no local category inference", () => {
    const adapter = readFileSync(resolve(ROOT, "shenShaAdapter.ts"), "utf8");
    expect(adapter).not.toMatch(/Quý nhân & hỗ trợ|Học tập & danh tiếng|Quan hệ & tình cảm/);
    expect(adaptShenShaCard(CASE_0001).grouped).toBe(false);
  });

  it("SR8 no good/bad inference", () => {
    const { container } = renderCase();
    expect(ssCard(container).textContent).not.toMatch(/Hung|Cát|Rất tốt|Rất xấu/);
  });

  it("SR9 no fear-based copy", () => {
    const { container } = renderCase();
    expect(ssCard(container).textContent).not.toMatch(/tai họa|cô độc chắc chắn|hôn nhân xấu|đại hung|nguy hiểm/);
  });

  it("SR10 canonical placements remain unchanged", () => {
    const model = adaptShenShaCard(CASE_0001);
    expect(model.items.map((item) => [item.name, item.placement])).toEqual([
      ["Thiên Ất Quý Nhân", "Trụ Tháng"],
      ["Hồng Loan", "Trụ Tháng"],
      ["Thiên Đức Quý Nhân", "Trụ Ngày"],
      ["Nguyệt Đức Quý Nhân", "Trụ Ngày"],
    ]);
  });

  it("SR11 ShenSha absence is not rendered as Có/Không checklist", () => {
    const { container } = renderCase();
    expect(ssCard(container).textContent).not.toMatch(/Văn Xương — Không|Hoa Cái — Không/);
  });

  it("SR12 grid remains 6/12", () => {
    const { container } = renderCase();
    expect(ssCard(container).getAttribute("data-span")).toBe("6");
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("SR13 Luck remains unchanged", () => {
    const { container } = renderCase();
    expect(container.querySelector('[data-card="luck"]')?.getAttribute("data-implemented")).toBe("luck");
  });

  it("skips technical evidence_text", () => {
    const model = adaptShenShaCard(CASE_0001);
    expect(model.items.every((item) => item.evidence === "")).toBe(true);
  });
});
