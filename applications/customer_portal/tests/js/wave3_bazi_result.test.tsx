import type { ReactElement } from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { BaZiResultScreen } from "../../src/screens/bazi";
import { BAZI_RESULT_MOCK } from "../../src/screens/bazi/mockData";

describe("Wave 3 BaZi Result UI", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders header, pillars, elements, ten gods, and strength", () => {
    render(<BaZiResultScreen /> as ReactElement);

    expect(screen.getByRole("heading", { level: 1, name: /Kết Quả Bát Tự/i })).toBeTruthy();
    expect(screen.getAllByText(BAZI_RESULT_MOCK.profile.fullName).length).toBeGreaterThan(0);
    expect(screen.getByLabelText("Tứ Trụ")).toBeTruthy();
    expect(screen.getByLabelText("Phân bố Ngũ hành")).toBeTruthy();
    expect(screen.getByLabelText("Thập Thần")).toBeTruthy();
    expect(screen.getAllByLabelText("Thân Vượng Nhược").length).toBeGreaterThan(0);
    expect(screen.getByText("Chính Quan")).toBeTruthy();
    expect(screen.getByText("THÂN VƯỢNG")).toBeTruthy();
  });

  it("keeps unavailable quick actions visible but disabled", () => {
    render(<BaZiResultScreen /> as ReactElement);

    const pdf = screen.getByRole("button", { name: /Xuất PDF/i });
    const printBtn = screen.getByRole("button", { name: /In — chưa khả dụng/i });
    expect((pdf as HTMLButtonElement).disabled).toBe(true);
    expect((printBtn as HTMLButtonElement).disabled).toBe(true);
  });

  it("supports loading gate without crashing", () => {
    render(<BaZiResultScreen status="loading" /> as ReactElement);
    expect(screen.getAllByLabelText(/Đang tải/i).length).toBeGreaterThan(0);
  });
});
