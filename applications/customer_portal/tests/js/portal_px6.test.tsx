import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { PortalApp } from "../../src/features/portal/PortalApp";

afterEach(() => {
  cleanup();
});

describe("Portal PX-6 journey", () => {
  it("offers onboarding from home without removing first analysis CTA", () => {
    render(<PortalApp initialRoute="home" />);
    expect(screen.getByRole("button", { name: "Bắt đầu phân tích mới" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Tìm hiểu BTE trước" })).toBeTruthy();
  });

  it("walks onboarding in Vietnamese", () => {
    render(<PortalApp initialRoute="onboarding" />);
    expect(screen.getByText("Chào mừng")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Tiếp tục" }));
    expect(screen.getByText("BTE làm gì")).toBeTruthy();
  });

  it("shows commercial result actions and knowledge return", async () => {
    render(<PortalApp initialRoute="result" />);
    expect(await screen.findByRole("button", { name: "Lưu báo cáo" }, { timeout: 5000 })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Tải bản PDF" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "In tư vấn" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Chia sẻ" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Mở bài liên quan" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Đặt tư vấn chuyên sâu" })).toBeTruthy();
  });

  it("returns from knowledge article to consultation", () => {
    render(<PortalApp initialRoute="knowledge-article" />);
    expect(screen.getByRole("button", { name: "Quay lại tư vấn" })).toBeTruthy();
    expect(screen.queryByText("No data")).toBeNull();
  });
});
