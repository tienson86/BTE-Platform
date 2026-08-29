/**
 * UI-03R1 — Tứ Trụ summary vs Bát Tự detail presentation.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import {
  CommercialDashboardPage,
  adaptIdentityHeader,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");

const LIVE_ANALYSIS = {
  identity: {
    four_pillars: {
      year: { stem: "Bính", branch: "Dần", can_chi: "Bính Dần", nayin_element: "Hỏa", cung_phi: "Cấn" },
      month: { stem: "Tân", branch: "Sửu", can_chi: "Tân Sửu", nayin_element: "Thổ", cung_phi: "Khôn" },
      day: { stem: "Canh", branch: "Ngọ", can_chi: "Canh Ngọ", nayin_element: "Thổ", cung_phi: "Khảm" },
      hour: { stem: "Mậu", branch: "Dần", can_chi: "Mậu Dần", nayin_element: "Thổ", cung_phi: "Cấn" },
    },
  },
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
    year_pillar: {
      stem: "Bính",
      branch: "Dần",
      nap_am: "Lư Trung Hỏa",
      ten_god: "Thất Sát",
      hidden_stems: ["Giáp", "Bính", "Mậu"],
      truong_sinh: "Dục",
    },
    month_pillar: {
      stem: "Tân",
      branch: "Sửu",
      nap_am: "Bích Thượng Thổ",
      ten_god: "Kiếp Tài",
      hidden_stems: ["Kỷ", "Quý", "Tân"],
      truong_sinh: "Mộ",
    },
    day_pillar: {
      stem: "Canh",
      branch: "Ngọ",
      nap_am: "Lộ Bàng Thổ",
      hidden_stems: ["Đinh", "Kỷ"],
      truong_sinh: "Bệnh",
    },
    hour_pillar: {
      stem: "Mậu",
      branch: "Dần",
      nap_am: "Thành Đầu Thổ",
      ten_god: "Thiên Ấn",
      hidden_stems: ["Giáp", "Bính", "Mậu"],
      truong_sinh: "Quan Đới",
    },
  },
} as AnalysisDataDto;

function renderLive() {
  return render(
    <CommercialDashboardPage analysis={LIVE_ANALYSIS} resultSource="current" layoutMode="live" />,
  );
}

function tuTru(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-region="pillars"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

function bazi(container: HTMLElement): HTMLElement {
  const node = container.querySelector('[data-card="bazi"]');
  expect(node).toBeTruthy();
  return node as HTMLElement;
}

afterEach(cleanup);

describe("UI-03R1 Tứ Trụ summary and Bát Tự detail", () => {
  it("R1 Tứ Trụ summary has Trụ / Can Chi / Nạp âm / Cung Phi headers", () => {
    const { container } = renderLive();
    const headers = [...tuTru(container).querySelectorAll("thead th")].map((node) => node.textContent?.trim());
    expect(headers).toEqual(["Trụ", "Can Chi", "Nạp âm", "Cung Phi"]);
  });

  it("R2 Tứ Trụ summary has Năm / Tháng / Ngày / Giờ rows", () => {
    const { container } = renderLive();
    const rows = [...tuTru(container).querySelectorAll("tbody th[scope='row']")].map(
      (node) => node.textContent?.trim(),
    );
    expect(rows).toEqual(["Năm", "Tháng", "Ngày", "Giờ"]);
  });

  it("R3 Can Chi is a combined value per row", () => {
    const { container } = renderLive();
    const values = [...tuTru(container).querySelectorAll(".bte-tu-tru__can-chi")].map(
      (node) => node.textContent,
    );
    expect(values).toEqual(["Bính Dần", "Tân Sửu", "Canh Ngọ", "Mậu Dần"]);
    expect(adaptIdentityHeader(LIVE_ANALYSIS).pillars.year.canChi).toBe("Bính Dần");
  });

  it("R4 Tứ Trụ summary does not use Thiên Can / Địa Chi as its row model", () => {
    const { container } = renderLive();
    const region = tuTru(container).textContent || "";
    expect(region).not.toContain("Thiên Can");
    expect(region).not.toContain("Địa Chi");
    expect(region).not.toContain("Tàng Can");
    expect(region).not.toContain("Thập Thần");
    expect(region).not.toContain("Trường Sinh");
  });

  it("R5 Bát Tự uses four pillar columns", () => {
    const { container } = renderLive();
    expect([...bazi(container).querySelectorAll("thead [data-pillar]")].map((node) => node.getAttribute("data-pillar"))).toEqual(
      ["year", "month", "day", "hour"],
    );
  });

  it("R6 Bát Tự contains Thiên Can", () => {
    const { container } = renderLive();
    expect(bazi(container).querySelector('[data-bazi-row="stem"]')?.textContent).toContain("Thiên Can");
  });

  it("R7 Bát Tự contains Địa Chi", () => {
    const { container } = renderLive();
    expect(bazi(container).querySelector('[data-bazi-row="branch"]')?.textContent).toContain("Địa Chi");
  });

  it("R8 Bát Tự contains Tàng Can", () => {
    const { container } = renderLive();
    expect(bazi(container).querySelector('[data-bazi-row="hidden"]')?.textContent).toContain("Tàng Can");
  });

  it("R9 Bát Tự contains Thập Thần", () => {
    const { container } = renderLive();
    expect(bazi(container).querySelector('[data-bazi-row="ten-god"]')?.textContent).toContain("Thập Thần");
  });

  it("R10 Bát Tự contains Trường Sinh", () => {
    const { container } = renderLive();
    expect(bazi(container).querySelector('[data-bazi-row="stage"]')?.textContent).toContain("Trường Sinh");
  });

  it("R11 Day pillar is marked Nhật Chủ", () => {
    const { container } = renderLive();
    expect(bazi(container).querySelector('thead [data-pillar="day"] .bte-bazi__day-master')?.textContent).toBe(
      "Nhật Chủ",
    );
  });

  it("R12 Tứ Trụ and Bát Tự do not share the same presentation model", () => {
    const { container } = renderLive();
    expect(tuTru(container).querySelector("[data-canonical='tu-tru-panel']")).toBeTruthy();
    expect(bazi(container).querySelector("[data-canonical='tu-tru-panel']")).toBeNull();
    expect(bazi(container).getAttribute("data-bazi-model")).toBe("detail");
    expect(tuTru(container).querySelector("[data-bazi-row]")).toBeNull();
  });

  it("R13 does not add astrology computation to the frontend", () => {
    const files = ["adapter.ts", "FourPillars.tsx", "BaziCard.tsx", "baziAdapter.ts"].map((name) =>
      readFileSync(resolve(ROOT, name), "utf8"),
    );
    for (const source of files) {
      expect(source).not.toMatch(/engines\./);
      expect(source).not.toMatch(/pillar_contract|cung_for_ganzhi|nayin_lookup|hoa_giap/);
      expect(source).not.toMatch(/calculateHidden|inferTenGod|lookupNapAm|twelveStageFor/);
    }
  });

  it("R14 outer grid spans remain frozen", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("R15 Overview remains unchanged", () => {
    const { container } = renderLive();
    const overview = container.querySelector('[data-card="overview"]');
    expect(overview?.getAttribute("data-implemented")).toBe("overview");
    expect(overview?.getAttribute("data-span")).toBe("4");
    expect(overview?.querySelector(".bte-cdash__card-title")?.textContent).toBe("TỔNG QUAN LÁ SỐ");
  });
});
