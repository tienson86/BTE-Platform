/**
 * Result Page Sprint A+B+C — architecture, content, quality smoke test.
 */

import { describe, expect, it } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { PortalPage, CANONICAL_DESKTOP_MOCK } from "../../src/screens/canonical_desktop";
import { createCanonicalDesktopGateViewModel } from "../../src/adapters";

describe("PortalPage — Result architecture Sprint D / UI V1", () => {
  it("preserves zones, content, and accessible expand controls", () => {
    const { container } = render(<PortalPage />);

    expect(container.querySelector('[data-result-architecture="pack07"]')).toBeTruthy();
    expect(container.querySelector('[data-sprint="D"]')).toBeTruthy();
    expect(container.querySelector('[data-visual="v2"]')).toBeTruthy();
    expect(container.querySelector(".rp-result-page")).toBeTruthy();
    expect(container.querySelector("#rp-main")).toBeTruthy();

    expect(screen.getByText("BTE Portal")).toBeTruthy();
    expect(screen.getByText("Kết quả")).toBeTruthy();

    // Frozen Sprint A patterns
    expect(container.querySelector('[data-zone="summary"][data-pattern="LP-001"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="analysis"][data-pattern="LP-003"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="visualization"][data-pattern="LP-004"]')).toBeTruthy();

    // Sprint B patterns
    expect(container.querySelector('[data-zone="recommendation"][data-pattern="LP-005"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="interpretation"][data-pattern="LP-006"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="knowledge"][data-pattern="LP-007"]')).toBeTruthy();

    // Reading order
    const zones = [...container.querySelectorAll("[data-zone]")].map(
      (node) => node.getAttribute("data-zone"),
    );
    expect(zones.indexOf("recommendation")).toBeLessThan(zones.indexOf("interpretation"));
    expect(zones.indexOf("interpretation")).toBeLessThan(zones.indexOf("knowledge"));

    // LP-005 — Frozen customer priority copy (not English "Critical")
    expect(screen.getByText("KHUYẾN NGHỊ")).toBeTruthy();
    expect(screen.getByText("Ưu tiên cao")).toBeTruthy();
    expect(container.querySelectorAll(".rp-rec-item").length).toBeGreaterThan(0);
    expect(container.querySelectorAll(".rp-rec-item").length).toBeLessThanOrEqual(5);

    // LP-006 preview default + expand (accessible name includes title)
    expect(screen.getByText("LUẬN GIẢI")).toBeTruthy();
    expect(screen.getAllByText("Quan sát").length).toBeGreaterThan(0);
    const expandButtons = screen.getAllByRole("button", {
      name: /Mở rộng luận giải/i,
    });
    expect(expandButtons.length).toBeGreaterThan(0);
    expect(expandButtons[0]!.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(expandButtons[0]!);
    expect(expandButtons[0]!.getAttribute("aria-expanded")).toBe("true");
    expect(screen.getAllByText("Tác động").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Gợi ý").length).toBeGreaterThan(0);

    // LP-007 accordion controls
    expect(screen.getByText("KIẾN THỨC")).toBeTruthy();
    const terminology = screen.getByRole("button", { name: /Thuật ngữ/i });
    expect(terminology.getAttribute("aria-expanded")).toBeTruthy();

    expect(screen.getAllByText("Nguyễn Văn A").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.footer)).toBeTruthy();
  });

  it("renders accessible loading / empty / error gates", () => {
    const { rerender, container } = render(
      <PortalPage initialData={createCanonicalDesktopGateViewModel("loading")} />,
    );
    expect(container.querySelector('[data-status="loading"]')).toBeTruthy();
    expect(screen.getByRole("status")).toBeTruthy();

    rerender(
      <PortalPage
        initialData={createCanonicalDesktopGateViewModel("empty", "Chưa có dữ liệu")}
      />,
    );
    expect(container.querySelector('[data-status="empty"]')).toBeTruthy();
    expect(screen.getByText("Chưa có kết quả")).toBeTruthy();

    rerender(
      <PortalPage
        initialData={createCanonicalDesktopGateViewModel("error", "Lỗi mạng")}
      />,
    );
    expect(container.querySelector('[data-status="error"]')).toBeTruthy();
    expect(screen.getByRole("alert")).toBeTruthy();
    expect(screen.getByText("Không tải được kết quả")).toBeTruthy();
  });
});
