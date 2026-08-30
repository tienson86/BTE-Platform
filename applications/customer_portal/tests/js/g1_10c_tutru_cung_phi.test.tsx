/**
 * G1-10C — Tứ Trụ Cung Phi binds published BaZi / routing values, not Hạ Nguyên leftovers.
 */

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";

import { CommercialDashboardPage, adaptIdentityHeader } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

afterEach(() => {
  cleanup();
});

const CANONICAL_1966 = {
  calendar: {
    tam_nguyen: "Trung Nguyên",
    calendar_rule_version: "G1-10C",
    ganzhi_routing: {
      year: { cung_phi: "Đoài", source_nguyen: "Trung Nguyên", ganzhi: "Bính Ngọ" },
      month: { cung_phi: "Đoài", source_nguyen: "Trung Nguyên", ganzhi: "Đinh Dậu" },
      day: { cung_phi: "Chấn", source_nguyen: "Hạ Nguyên", ganzhi: "Bính Tuất" },
      hour: { cung_phi: "Cấn", source_nguyen: "Hạ Nguyên", ganzhi: "Canh Dần" },
    },
  },
  identity: {
    four_pillars: {
      year: {
        stem: "Bính",
        branch: "Ngọ",
        can_chi: "Bính Ngọ",
        nayin_element: "Thủy",
        cung_phi: "Đoài",
      },
      month: {
        stem: "Đinh",
        branch: "Dậu",
        can_chi: "Đinh Dậu",
        nayin_element: "Hỏa",
        cung_phi: "Đoài",
      },
      day: {
        stem: "Bính",
        branch: "Tuất",
        can_chi: "Bính Tuất",
        nayin_element: "Thổ",
        cung_phi: "Chấn",
      },
      hour: {
        stem: "Canh",
        branch: "Dần",
        can_chi: "Canh Dần",
        nayin_element: "Mộc",
        cung_phi: "Cấn",
      },
    },
  },
  bazi: {
    year_pillar: { stem: "Bính", branch: "Ngọ", nap_am: "Thiên Hà Thủy", cung_phi: "Đoài" },
    month_pillar: { stem: "Đinh", branch: "Dậu", nap_am: "Sơn Hạ Hỏa", cung_phi: "Đoài" },
    day_pillar: { stem: "Bính", branch: "Tuất", nap_am: "Ốc Thượng Thổ", cung_phi: "Chấn" },
    hour_pillar: { stem: "Canh", branch: "Dần", nap_am: "Tùng Bách Mộc", cung_phi: "Cấn" },
  },
} as AnalysisDataDto;

const STALE_HA_NGUYEN_IDENTITY = {
  ...CANONICAL_1966,
  identity: {
    four_pillars: {
      year: { stem: "Bính", branch: "Ngọ", can_chi: "Bính Ngọ", nayin_element: "Thủy", cung_phi: "Khảm" },
      month: { stem: "Đinh", branch: "Dậu", can_chi: "Đinh Dậu", nayin_element: "Hỏa", cung_phi: "Khảm" },
      day: { stem: "Bính", branch: "Tuất", can_chi: "Bính Tuất", nayin_element: "Thổ", cung_phi: "Chấn" },
      hour: { stem: "Canh", branch: "Dần", can_chi: "Canh Dần", nayin_element: "Mộc", cung_phi: "Cấn" },
    },
  },
} as AnalysisDataDto;

function rowText(container: HTMLElement, pillar: string): string {
  return container.querySelector(`[data-region="pillars"] [data-pillar="${pillar}"]`)?.textContent || "";
}

describe("G1-10C Tứ Trụ Cung Phi live binding", () => {
  it("renders 1966 Year/Month Đoài and Day/Hour Hạ Nguyên palaces", () => {
    const bound = adaptIdentityHeader(CANONICAL_1966);
    expect(bound.pillars.year.canChi).toBe("Bính Ngọ");
    expect(bound.pillars.year.cungPhi).toBe("Đoài");
    expect(bound.pillars.month.canChi).toBe("Đinh Dậu");
    expect(bound.pillars.month.cungPhi).toBe("Đoài");
    expect(bound.pillars.day.canChi).toBe("Bính Tuất");
    expect(bound.pillars.day.cungPhi).toBe("Chấn");
    expect(bound.pillars.hour.canChi).toBe("Canh Dần");
    expect(bound.pillars.hour.cungPhi).toBe("Cấn");

    const { container } = render(
      <CommercialDashboardPage analysis={CANONICAL_1966} resultSource="current" layoutMode="live" />,
    );
    expect(rowText(container, "year")).toContain("Bính Ngọ");
    expect(rowText(container, "year")).toContain("Đoài");
    expect(rowText(container, "month")).toContain("Đinh Dậu");
    expect(rowText(container, "month")).toContain("Đoài");
    expect(rowText(container, "day")).toContain("Bính Tuất");
    expect(rowText(container, "day")).toContain("Chấn");
    expect(rowText(container, "hour")).toContain("Canh Dần");
    expect(rowText(container, "hour")).toContain("Cấn");
    expect(rowText(container, "year")).not.toContain("Khảm");
    expect(rowText(container, "month")).not.toContain("Khảm");
  });

  it("does not keep stale Hạ Nguyên identity Cung when BaZi routing Cung is published", () => {
    const bound = adaptIdentityHeader(STALE_HA_NGUYEN_IDENTITY);
    expect(bound.pillars.year.cungPhi).toBe("Đoài");
    expect(bound.pillars.month.cungPhi).toBe("Đoài");
    const { container } = render(
      <CommercialDashboardPage
        analysis={STALE_HA_NGUYEN_IDENTITY}
        resultSource="current"
        layoutMode="live"
      />,
    );
    expect(rowText(container, "year")).toContain("Đoài");
    expect(rowText(container, "month")).toContain("Đoài");
    expect(rowText(container, "year")).not.toContain("Khảm");
    expect(rowText(container, "month")).not.toContain("Khảm");
  });
});
