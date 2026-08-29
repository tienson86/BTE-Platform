/**
 * UI-03 Identity Header + canonical Commercial Dashboard grid.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { resolveResultBoot } from "../../src/entries/resultBoot";
import {
  CommercialDashboardPage,
  DASHBOARD_CARDS,
  adaptIdentityHeader,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const LIVE_ANALYSIS = {
  analysis_id: "ana-ui03-0001",
  identity: {
    person: {
      full_name: "Nguyễn Tiến Sơn",
      gender: "male",
      solar_birth: "1987-01-21",
      lunar_birth: "1986-12-22",
      birth_time: "04:30",
      birth_place: "Hà Tây, Việt Nam",
    },
    calendar: { solar_term: "Đại Hàn" },
    four_pillars: {
      year: { stem: "Bính", branch: "Dần", can_chi: "Bính Dần", nayin_element: "Hỏa" },
      month: { stem: "Tân", branch: "Sửu", can_chi: "Tân Sửu", nayin_element: "Thổ" },
      day: { stem: "Canh", branch: "Ngọ", can_chi: "Canh Ngọ", nayin_element: "Thổ" },
      hour: { stem: "Mậu", branch: "Dần", can_chi: "Mậu Dần", nayin_element: "Thổ" },
    },
  },
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
    day_master_yin_yang: "Dương",
    year_pillar: { stem: "Bính", branch: "Dần", nap_am: "Lư Trung Hỏa" },
    month_pillar: { stem: "Tân", branch: "Sửu", nap_am: "Bích Thượng Thổ" },
    day_pillar: { stem: "Canh", branch: "Ngọ", nap_am: "Lộ Bàng Thổ" },
    hour_pillar: { stem: "Mậu", branch: "Dần", nap_am: "Thành Đầu Thổ" },
  },
  calendar: { solar_term: { name: "Đại Hàn" } },
  feng_shui: {
    cung_phi: "Khảm",
    menh_quai: "Khảm",
    nhom_trach: "Đông Tứ Trạch",
  },
  result_meta: {
    analysis_id: "ana-ui03-0001",
    release_label: "BTE V1.0",
    created_at: "2026-08-29T10:00:00Z",
  },
  score: { confidence: "high" },
} as AnalysisDataDto;

afterEach(cleanup);

function renderLive() {
  return render(
    <CommercialDashboardPage
      analysis={LIVE_ANALYSIS}
      analysisId="ana-ui03-0001"
      resultSource="current"
      layoutMode="live"
    />,
  );
}

describe("UI-03 commercial dashboard", () => {
  it("G1 renders the canonical Commercial Dashboard root", () => {
    const { container } = renderLive();
    expect(container.querySelectorAll('[data-dashboard="commercial-v1"]')).toHaveLength(1);
    expect(container.querySelector('[data-canonical-result="ui03"]')).toBeTruthy();
  });

  it("G2 shows exactly one canonical dashboard body", () => {
    const { container } = renderLive();
    expect(container.querySelectorAll("[data-dashboard-body='canonical-grid']")).toHaveLength(1);
    expect(container.querySelectorAll('[data-dashboard="commercial-v1"]')).toHaveLength(1);
  });

  it("G3 Identity Header exists and is full-width", () => {
    const { container } = renderLive();
    const header = container.querySelector("[data-identity-header='true']");
    expect(header).toBeTruthy();
    expect(header?.classList.contains("bte-id")).toBe(true);
  });

  it("G4 Identity Header contains regions A/B/C/D", () => {
    const { container } = renderLive();
    expect(container.querySelector('[data-region="identity"]')).toBeTruthy();
    expect(container.querySelector('[data-region="pillars"]')).toBeTruthy();
    expect(container.querySelector('[data-region="foundation"]')).toBeTruthy();
    expect(container.querySelector('[data-region="status"]')).toBeTruthy();
  });

  it("G5 Four Pillars has Năm / Tháng / Ngày / Giờ", () => {
    const { container } = renderLive();
    const region = container.querySelector('[data-region="pillars"]')?.textContent || "";
    expect(region).toContain("Năm");
    expect(region).toContain("Tháng");
    expect(region).toContain("Ngày");
    expect(region).toContain("Giờ");
  });

  it("G6 Four Pillars is the Tứ Trụ summary (Can Chi / Nạp âm / Cung Phi)", () => {
    const { container } = renderLive();
    const region = container.querySelector('[data-region="pillars"]')?.textContent || "";
    expect(region).toContain("Trụ");
    expect(region).toContain("Can Chi");
    expect(region).toContain("Nạp âm");
    expect(region).toContain("Cung Phi");
    expect(region).not.toContain("Thiên Can");
    expect(region).not.toContain("Địa Chi");
  });

  it("G7 Day Master is identified on the Bát Tự Ngày trụ column", () => {
    const { container } = renderLive();
    const dayHead = container.querySelector('[data-card="bazi"] thead [data-pillar="day"]');
    expect(dayHead?.getAttribute("data-day-master")).toBe("true");
    expect(dayHead?.textContent).toMatch(/Nhật Chủ/);
    const region = container.querySelector('[data-region="pillars"]')?.textContent || "";
    expect(region).toMatch(/Canh Ngọ/);
  });

  it("G8 Four Nạp Âm values can be rendered", () => {
    const { container } = renderLive();
    const region = container.querySelector('[data-region="pillars"]');
    const cells = [...(region?.querySelectorAll('[data-kind="nap-am"]') ?? [])].map(
      (node) => node.textContent,
    );
    expect(cells).toEqual(["Hỏa", "Thổ", "Thổ", "Thổ"]);
  });

  it("G9 Cung Phi / Mệnh Quái / Nhóm Trạch bind when present", () => {
    renderLive();
    expect(screen.getAllByText("Cung Phi").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Khảm").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Đông Tứ Trạch")).toBeTruthy();
    expect(screen.getByText("Đại Hàn")).toBeTruthy();
  });

  it("G10 canonical Vietnamese card titles exist", () => {
    renderLive();
    for (const card of DASHBOARD_CARDS) {
      expect(screen.getByText(card.title)).toBeTruthy();
    }
    const body = document.body.textContent || "";
    expect(body).not.toMatch(/\bOverview\b/);
    expect(body).not.toMatch(/\bPattern\b/);
    expect(body).not.toMatch(/\bShenSha\b/);
    expect(body).not.toMatch(/\bLuck\b/);
  });

  it("G11 desktop spans follow 4/8, 4/4/4, 6/6, 12, 12", () => {
    const { container } = renderLive();
    const spans = [...container.querySelectorAll("[data-card]")].map((node) =>
      Number(node.getAttribute("data-span")),
    );
    expect(spans).toEqual([4, 8, 4, 4, 4, 6, 6, 12, 12]);
  });

  it("G12 does not duplicate the legacy result dashboard", () => {
    const { container } = renderLive();
    expect(container.querySelector(".cd-root")).toBeNull();
    expect(container.querySelector(".rp-result-page")).toBeNull();
    expect(container.querySelector(".cd-sidebar")).toBeNull();
    expect(container.querySelector('[data-zone="summary"]')).toBeNull();
  });

  it("G13 mobile semantic card order is preserved in the DOM", () => {
    const { container } = renderLive();
    const order = [...container.querySelectorAll("[data-card]")].map((node) =>
      node.getAttribute("data-card"),
    );
    expect(order).toEqual([
      "overview",
      "bazi",
      "five-elements",
      "ten-gods",
      "pattern",
      "shensha",
      "luck",
      "interpretation",
      "action-plan",
    ]);
  });

  it("G14 keeps technical IDs out of the identity and card titles", () => {
    const { container } = renderLive();
    const identity = container.querySelector("[data-identity-header='true']")?.textContent || "";
    expect(identity).not.toMatch(/Thân vượng|Dụng thần|Hỷ thần|Kỵ thần|Mệnh cục/i);
    expect(identity).not.toMatch(/useful_god|GATE_CORE|day_master_yin_yang/);
    expect(screen.getByText("KẾT QUẢ LUẬN GIẢI BÁT TỰ")).toBeTruthy();
  });

  it("G15 ResultStore boot still maps stored analysis onto /result", () => {
    const boot = resolveResultBoot({
      input: { year: 1987, month: 1, day: 21, hour: 4, minute: 30, gender: "male" },
      data: {
        ...LIVE_ANALYSIS,
        useful_god_source: { contract: "analysis_result.UsefulGodView@1.5" },
        useful_god: { useful_display: "Thổ" },
      },
    });
    expect(boot.resultSource).toBe("current");
    expect(boot.analysis?.identity).toBeTruthy();
    expect(boot.layoutMode).toBe("live");
    expect(resolveResultBoot(null, "?layout=skeleton").layoutMode).toBe("skeleton");
  });

  it("does not hard-code CASE-0001 inside the production adapter", () => {
    const root = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
    const adapter = readFileSync(resolve(root, "adapter.ts"), "utf8");
    expect(adapter).not.toContain("Nguyễn Tiến Sơn");
    expect(adapter).not.toContain("1987-01-21");
    expect(adapter).not.toContain("CASE-0001");
    const rebound = adaptIdentityHeader({
      identity: { person: { full_name: "Lê Thị B" }, four_pillars: { day: { stem: "Ất" } } },
      bazi: { day_master: "Ất" },
    });
    expect(rebound.person.fullName).toBe("Lê Thị B");
    expect(rebound.dayMaster.stem).toBe("Ất");
  });

  it("skeleton layout renders the grid without a customer-facing mode control", () => {
    const { container } = render(
      <CommercialDashboardPage layoutMode="skeleton" resultSource="preview" />,
    );
    expect(container.querySelector('[data-layout="skeleton"]')).toBeTruthy();
    expect(container.querySelectorAll("[data-card][data-skeleton='true']")).toHaveLength(9);
    expect(container.textContent).not.toMatch(/Skeleton mode|Chế độ khung/i);
  });
});
