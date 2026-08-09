import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { PortalApp } from "../../src/features/portal/PortalApp";

afterEach(() => {
  cleanup();
});

describe("Portal PX-5", () => {
  it("renders Vietnamese shell and home", () => {
    render(<PortalApp initialRoute="home" />);
    expect(screen.getAllByText("Trang chủ").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Tổng quan").length).toBeGreaterThan(0);
    expect(screen.getByRole("button", { name: "Bắt đầu phân tích mới" })).toBeTruthy();
    expect(screen.queryByText("Dashboard")).toBeNull();
    expect(screen.queryByText("Skip to content")).toBeNull();
    expect(screen.queryByText("Primary")).toBeNull();
  });

  it("renders consultant dashboard without admin metrics", () => {
    render(<PortalApp initialRoute="dashboard" />);
    expect(screen.getByText("Bạn nên hoàn tất một định hướng đang dở.")).toBeTruthy();
    expect(screen.getByText("Tiếp tục tư vấn")).toBeTruthy();
    expect(screen.queryByText("Tổng số lá số")).toBeNull();
    expect(screen.queryByText("Mock")).toBeNull();
  });

  it("renders analysis wizard steps in Vietnamese", () => {
    render(<PortalApp initialRoute="analyze-birth" />);
    expect(screen.getByLabelText("Các bước phân tích")).toBeTruthy();
    expect(screen.getByLabelText("Họ và tên")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Tiếp tục" })).toBeTruthy();
  });
});
