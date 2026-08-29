import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { APP_NAV_ITEMS, PrimaryNav, resolveActiveNavId } from "../../src/layouts/Navigation";

afterEach(() => {
  cleanup();
});

const PRODUCT_LABELS = ["Trang chủ", "Chọn ngày tốt", "Xem lá số"] as const;
const FORBIDDEN_LABELS = ["Báo cáo", "Lịch sử", "Tài khoản", "Hướng dẫn", "Luận giải", "Kết quả"] as const;

describe("UI-01 customer primary navigation", () => {
  it("N1 exposes exactly three product items", () => {
    expect(APP_NAV_ITEMS.map((item) => item.label)).toEqual([...PRODUCT_LABELS]);
    render(<PrimaryNav activeId="home" />);
    const nav = screen.getByRole("navigation", { name: "Điều hướng chính" });
    const links = nav.querySelectorAll("a");
    expect(Array.from(links).map((link) => link.textContent)).toEqual([...PRODUCT_LABELS]);
  });

  it("N2–N3 hide reports, history, and other legacy primary items", () => {
    render(<PrimaryNav />);
    for (const label of FORBIDDEN_LABELS) {
      expect(screen.queryByText(label)).toBeNull();
    }
  });

  it("N4–N7 resolve canonical customer routes", () => {
    expect(resolveActiveNavId("/")).toBe("home");
    expect(resolveActiveNavId("/good-date")).toBe("home");
    expect(resolveActiveNavId("/choose-date")).toBe("choose-date");
    expect(resolveActiveNavId("/analyze")).toBe("analyze");
  });

  it("N8–N9 keep result on the Xem lá số journey without a Kết quả menu", () => {
    expect(resolveActiveNavId("/result")).toBe("analyze");
    expect(APP_NAV_ITEMS.some((item) => item.href === "/result")).toBe(false);
    render(<PrimaryNav activeId="analyze" />);
    expect(screen.queryByText("Kết quả")).toBeNull();
    expect(screen.getByText("Xem lá số").getAttribute("aria-current")).toBe("page");
  });

  it("N10 does not treat Welcome Dashboard as the home destination", () => {
    expect(APP_NAV_ITEMS[0]?.href).toBe("/good-date");
    expect(resolveActiveNavId("/dashboard")).toBeUndefined();
  });
});

describe("UI-01A result shell contract", () => {
  it("A1–A2 keep /result on the three-item customer product nav", () => {
    expect(APP_NAV_ITEMS.map((item) => item.label)).toEqual([...PRODUCT_LABELS]);
    expect(APP_NAV_ITEMS.some((item) => item.href === "/result")).toBe(false);
    expect(resolveActiveNavId("/result")).toBe("analyze");
    render(<PrimaryNav activeId="analyze" />);
    const nav = screen.getByRole("navigation", { name: "Điều hướng chính" });
    expect(Array.from(nav.querySelectorAll("a")).map((link) => link.textContent)).toEqual([
      ...PRODUCT_LABELS,
    ]);
    for (const label of ["Kết quả", "Báo cáo", "Lịch sử"] as const) {
      expect(screen.queryByText(label)).toBeNull();
    }
  });

  it("A8 does not add a competing customer nav list", () => {
    expect(APP_NAV_ITEMS).toHaveLength(3);
    expect(APP_NAV_ITEMS.map((item) => item.href)).toEqual([
      "/good-date",
      "/choose-date",
      "/analyze",
    ]);
  });
});
