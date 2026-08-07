/**
 * Result Page Sprint A+B — zone architecture + content zones smoke test.
 */

import { describe, expect, it } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { PortalPage, CANONICAL_DESKTOP_MOCK } from "../../src/screens/canonical_desktop";

describe("PortalPage — Result architecture Sprint B", () => {
  it("preserves Sprint A zones and renders LP-005/006/007 content zones", () => {
    const { container } = render(<PortalPage />);

    expect(container.querySelector('[data-result-architecture="pack07"]')).toBeTruthy();
    expect(container.querySelector('[data-sprint="B"]')).toBeTruthy();
    expect(container.querySelector(".rp-result-page")).toBeTruthy();

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

    // Reading order: recommendation before interpretation before knowledge
    const zones = [...container.querySelectorAll("[data-zone]")].map(
      (node) => node.getAttribute("data-zone"),
    );
    expect(zones.indexOf("recommendation")).toBeLessThan(zones.indexOf("interpretation"));
    expect(zones.indexOf("interpretation")).toBeLessThan(zones.indexOf("knowledge"));

    // LP-005
    expect(screen.getByText("KHUYẾN NGHỊ")).toBeTruthy();
    expect(screen.getByText("Critical")).toBeTruthy();
    expect(container.querySelectorAll(".rp-rec-item").length).toBeGreaterThan(0);
    expect(container.querySelectorAll(".rp-rec-item").length).toBeLessThanOrEqual(5);

    // LP-006 preview default + expand
    expect(screen.getByText("LUẬN GIẢI")).toBeTruthy();
    expect(screen.getAllByText("Observation").length).toBeGreaterThan(0);
    const expandButtons = screen.getAllByRole("button", { name: "Mở rộng luận giải" });
    expect(expandButtons.length).toBeGreaterThan(0);
    fireEvent.click(expandButtons[0]!);
    expect(screen.getAllByText("Impact").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Suggestion").length).toBeGreaterThan(0);

    // LP-007
    expect(screen.getByText("KIẾN THỨC")).toBeTruthy();
    expect(screen.getByText("Thuật ngữ")).toBeTruthy();
    expect(screen.getByText("Tài liệu tham chiếu")).toBeTruthy();
    expect(screen.getByText("Lý thuyết truyền thống")).toBeTruthy();
    expect(screen.getByText("Phụ lục")).toBeTruthy();

    expect(screen.getAllByText("Nguyễn Văn A").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.footer)).toBeTruthy();
  });
});
