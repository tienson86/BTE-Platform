import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { ResultPageV2 } from "../../src/features/result_v2/pages/ResultPageV2";
import { resultV2ReadyReport } from "./result_v2_fixture";

afterEach(() => {
  cleanup();
});

describe("ResultPageV2", () => {
  it("renders PX-1 reading order in Vietnamese", () => {
    render(<ResultPageV2 report={resultV2ReadyReport} />);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toContain("ổn định");
    expect(screen.getAllByText("Tóm tắt tư vấn").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Định hướng chính").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Lưu ý quan trọng").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Sự nghiệp").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Tài chính").length).toBeGreaterThan(0);
    // Unavailable domains are hidden (no empty shells).
    expect(screen.queryByText("Quan hệ")).toBeNull();
    expect(screen.queryByText("Sức khỏe")).toBeNull();
    expect(screen.queryByText("Vận trình")).toBeNull();
    expect(screen.getAllByText("Biểu đồ minh họa").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Chi tiết kỹ thuật").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Kiến thức bổ sung").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Phụ lục").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Vì sao").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Kết quả kỳ vọng").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Việc cần làm").length).toBeGreaterThan(0);
    expect(screen.getAllByRole("button", { name: "Bắt đầu theo định hướng này" })).toHaveLength(1);
    expect(screen.queryByText("Hero")).toBeNull();
    expect(screen.queryByText("Summary")).toBeNull();
    expect(screen.queryByText("<html>must-not-render</html>")).toBeNull();
    // Technical is secondary (collapsed) but fully accessible via expand.
    expect(document.querySelector('[data-chart-fundamentals="true"]')).toBeTruthy();
    expect(screen.queryByText("Dương lịch")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Xem chi tiết kỹ thuật" }));
    expect(screen.getByText("Dương lịch")).toBeTruthy();
    expect(screen.getByText("Giáp Tý · Ất Sửu · Bính Dần · Đinh Mão")).toBeTruthy();
  });

  it("shows loading chrome in Vietnamese", () => {
    render(<ResultPageV2 loading />);
    expect(screen.getByText("Đang chuẩn bị tư vấn")).toBeTruthy();
  });
});
