/**
 * G1-11 — Cân Xương header populated vs empty states.
 */

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";

import { CommercialDashboardPage, adaptIdentityHeader } from "../../src/screens/commercial_dashboard";
import { CAN_XUONG_EMPTY_COPY } from "../../src/adapters/canonicalCanXuong";
import type { AnalysisDataDto } from "../../src/models";

afterEach(() => {
  cleanup();
});

const POPULATED = {
  can_xuong: {
    total_weight: 47,
    liang: 4,
    chi: 7,
    display_weight: "X lượng Y chỉ",
    classification: "Thượng cách",
    rating: "Khá",
    summary: "Tài lộc khá · hậu vận thuận",
    interpretation: "Luận giải chi tiết canonical.",
    source: "yuan_tian_gang_can_xuong",
    version: "G1-11",
  },
  identity: {
    four_pillars: {
      year: { stem: "Bính", branch: "Ngọ", can_chi: "Bính Ngọ", nayin_element: "Thủy", cung_phi: "Đoài" },
    },
  },
  bazi: {
    year_pillar: { stem: "Bính", branch: "Ngọ" },
  },
} as AnalysisDataDto;

const EMPTY = {
  identity: {
    four_pillars: {
      year: { stem: "Bính", branch: "Ngọ", can_chi: "Bính Ngọ" },
    },
  },
} as AnalysisDataDto;

describe("G1-11 Cân Xương header", () => {
  it("A populated state shows weight, classification, summary and no dash rows", () => {
    const bound = adaptIdentityHeader(POPULATED);
    expect(bound.foundation.available).toBe(true);
    expect(bound.foundation.displayWeight).toBe("X lượng Y chỉ");
    expect(bound.foundation.classification).toBe("Thượng cách");
    expect(bound.foundation.summary).toBe("Tài lộc khá · hậu vận thuận");

    const { container } = render(
      <CommercialDashboardPage analysis={POPULATED} resultSource="current" layoutMode="live" />,
    );
    const summary = container.querySelector('[data-can-xuong="summary"]');
    expect(summary?.textContent).toContain("X lượng Y chỉ");
    expect(summary?.textContent).toContain("Thượng cách");
    expect(summary?.textContent).toContain("Tài lộc khá · hậu vận thuận");
    expect(container.textContent).not.toContain("Cân lượng —");
    expect(container.textContent).not.toContain("Phân loại —");
    expect(container.textContent).not.toContain("Đánh giá —");
    expect(container.textContent).not.toContain("Tóm tắt —");
    expect(container.querySelector("#sec-can-xuong")?.textContent).toContain("Luận giải chi tiết canonical.");
  });

  it("B empty state shows one restrained copy and no four dash placeholders", () => {
    const bound = adaptIdentityHeader(EMPTY);
    expect(bound.foundation.available).toBe(false);

    const { container } = render(
      <CommercialDashboardPage analysis={EMPTY} resultSource="current" layoutMode="live" />,
    );
    const empty = container.querySelector('[data-can-xuong="empty"]');
    expect(empty?.textContent).toContain(CAN_XUONG_EMPTY_COPY);
    expect(container.textContent).not.toContain("Cân lượng —");
    expect(container.textContent).not.toContain("Phân loại —");
    expect(container.textContent).not.toContain("Đánh giá —");
    expect(container.textContent).not.toContain("Tóm tắt —");
  });
});
