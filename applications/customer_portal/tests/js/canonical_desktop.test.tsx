/**
 * Result Page Sprint A — zone architecture smoke test (PACK_06 / PACK_07).
 */

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { PortalPage, CANONICAL_DESKTOP_MOCK } from "../../src/screens/canonical_desktop";

describe("PortalPage — Result architecture Sprint A", () => {
  it("renders shell and official zones without direct card composition on page root", () => {
    const { container } = render(<PortalPage />);

    expect(container.querySelector('[data-result-architecture="pack07"]')).toBeTruthy();
    expect(container.querySelector('[data-sprint="A"]')).toBeTruthy();
    expect(container.querySelector(".rp-result-page")).toBeTruthy();

    expect(screen.getByText("BTE Portal")).toBeTruthy();
    expect(screen.getByText("Kết quả")).toBeTruthy();

    // Zone / row markers
    expect(container.querySelector('[data-zone="context"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="summary"][data-pattern="LP-001"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="analysis"][data-pattern="LP-003"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="visualization"][data-pattern="LP-004"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="recommendation"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="interpretation"]')).toBeTruthy();
    expect(container.querySelector('[data-zone="knowledge"]')).toBeTruthy();

    // LP-001 cards
    expect(screen.getByText("TÓM TẮT ĐIỀU HÀNH")).toBeTruthy();
    expect(screen.getByText("CHỈ SỐ CỐT LÕI")).toBeTruthy();
    expect(screen.getByText("ĐỊNH HƯỚNG MỆNH VẬN")).toBeTruthy();

    // LP-003 cards
    expect(screen.getByText("NGŨ HÀNH")).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s05.title)).toBeTruthy();
    expect(screen.getByText("THẬP THẦN")).toBeTruthy();

    // LP-004 cards
    expect(screen.getByText("BIỂU ĐỒ RADAR NGŨ HÀNH")).toBeTruthy();
    expect(screen.getByText("DÒNG THỜI GIAN VẬN")).toBeTruthy();

    // Equal-height rows for Sprint A implemented zones
    expect(container.querySelectorAll('[data-equal-height="true"]').length).toBeGreaterThanOrEqual(4);

    expect(screen.getAllByText("Nguyễn Văn A").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.footer)).toBeTruthy();
  });
});
