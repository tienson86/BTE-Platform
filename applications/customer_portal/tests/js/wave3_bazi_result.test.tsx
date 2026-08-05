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
    expect(screen.getByText(BAZI_RESULT_MOCK.profile.fullName)).toBeTruthy();
    expect(screen.getByLabelText("Tứ Trụ")).toBeTruthy();
    expect(screen.getByLabelText("Ngũ Hành")).toBeTruthy();
    expect(screen.getByLabelText("Thập Thần")).toBeTruthy();
    expect(screen.getByLabelText("Thân Vượng Nhược")).toBeTruthy();
  });

  it("keeps unavailable quick actions visible but disabled", () => {
    render(<BaZiResultScreen /> as ReactElement);

    const pdf = screen.getByRole("button", { name: /Xuất PDF/i });
    const print = screen.getByRole("button", { name: /^In/i });
    expect(pdf).toBeDisabled();
    expect(print).toBeDisabled();
  });

  it("supports loading gate without crashing", () => {
    render(<BaZiResultScreen status="loading" /> as ReactElement);
    expect(screen.getAllByLabelText(/Đang tải/i).length).toBeGreaterThan(0);
  });
});
