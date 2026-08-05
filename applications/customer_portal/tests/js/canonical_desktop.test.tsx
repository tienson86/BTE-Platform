/**
 * Desktop Canonical UI — structural smoke test (TASK_UI_IMPLEMENTATION_001).
 */

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { PortalPage, CANONICAL_DESKTOP_MOCK } from "../../src/screens/canonical_desktop";

describe("PortalPage — Desktop Canonical V1", () => {
  it("renders shell and all sections S00–S11 in Vietnamese", () => {
    const { container } = render(<PortalPage />);

    expect(container.querySelector('[data-canonical="desktop-v1"]')).toBeTruthy();
    expect(screen.getByText("BTE Portal")).toBeTruthy();
    expect(screen.getByText("Kết quả")).toBeTruthy();
    expect(screen.getByText("PHÂN TÍCH LÁ SỐ")).toBeTruthy();
    expect(screen.getByText("TIỆN ÍCH")).toBeTruthy();

    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s00.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s01.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s02.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s03.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s04.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s05.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s06.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s07.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s08.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s09.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s10.title)).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.s11.title)).toBeTruthy();

    expect(screen.getAllByText("Nguyễn Văn A").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Bính Hỏa")).toBeTruthy();
    expect(screen.getByText("4 lượng 8 chỉ")).toBeTruthy();
    expect(screen.getByText(CANONICAL_DESKTOP_MOCK.footer)).toBeTruthy();
  });
});
