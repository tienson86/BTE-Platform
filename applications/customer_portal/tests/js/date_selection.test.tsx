import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { APP_NAV_ITEMS, PrimaryNav, resolveActiveNavId } from "../../src/layouts/Navigation";
import {
  AnalogClockFace,
  DateSelectionMobileFrame,
  DateSelectionNav,
  LookupScreen,
  SearchForm,
  SearchScreen,
} from "../../src/features/date_selection";
import type { CalendarCellVm, DayVm, HourVm, PersonVm, RankedDateVm } from "../../src/features/date_selection";

afterEach(() => {
  cleanup();
});

const trach = {
  cung: "Đoài",
  element_code: "kim",
  element_label: "Kim",
  trach_group_code: "tay",
  trach_group_label: "Tây Tứ Trạch",
};

const hour = (branch: string, label: string): HourVm => ({
  window: { branch, time_range: "07:01–09:00" },
  ganzhi: "Bính Thìn",
  six_state: { remainder: 4, code: "xich_khau", label },
  trach,
  ke_slots: [
    { ke_index: 1, time_range: "07:01–07:20", six_state: { remainder: 5, code: "tieu_cat", label: "Tiểu Cát" } },
    { ke_index: 2, time_range: "07:21–07:40", six_state: { remainder: 0, code: "khong_vong", label: "Không Vong" } },
    { ke_index: 3, time_range: "07:41–08:00", six_state: { remainder: 1, code: "dai_an", label: "Đại An" } },
    { ke_index: 4, time_range: "08:01–08:20", six_state: { remainder: 2, code: "luu_lien", label: "Lưu Liên" } },
    { ke_index: 5, time_range: "08:21–08:40", six_state: { remainder: 3, code: "toc_hy", label: "Tốc Hỷ" } },
    { ke_index: 6, time_range: "08:41–09:00", six_state: { remainder: 4, code: "xich_khau", label: "Xích Khẩu" } },
  ],
});

const day: DayVm = {
  calendar: {
    solar_label: "27/08/2026",
    lunar_label: "15/07/2026",
    year_ganzhi: "Bính Ngọ",
    day_ganzhi: "Quý Dậu",
  },
  six_state: { remainder: 5, code: "tieu_cat", label: "Tiểu Cát" },
  trach,
  hours: [hour("Thìn", "Xích Khẩu"), hour("Tỵ", "Tiểu Cát")],
};

const cells: CalendarCellVm[] = Array.from({ length: 31 }, (_, index) => ({
  solar_year: 2026,
  solar_month: 8,
  solar_day: index + 1,
  lunar_day: index + 1,
  lunar_month: 7,
  weekday: index === 0 ? 5 : 0,
  six_state: { remainder: 5, code: "tieu_cat", label: "Tiểu Cát" },
}));

const person: PersonVm = {
  full_name: "Nguyễn Văn A",
  gender_label: "Nam",
  solar_label: "15/05/1990",
  lunar_label: "21/04/1990",
  ganzhi: "Canh Ngọ",
  trach,
};

const ranked: RankedDateVm[] = [
  {
    day,
    recommendations: [{ time_range: "09:41–10:00", primary: true }],
  },
];

describe("Date Selection frontend", () => {
  it("exposes Ngày tốt dropdown with exactly two items", () => {
    const item = APP_NAV_ITEMS.find((entry) => entry.id === "date-selection");
    expect(item?.label).toBe("Ngày tốt");
    expect(item?.children?.map((child) => child.label)).toEqual([
      "Xem ngày tốt/xấu",
      "Chọn ngày tốt",
    ]);
    render(<PrimaryNav activeId="date-selection" />);
    expect(screen.getByText("Ngày tốt")).toBeTruthy();
    expect(screen.getByText("Xem ngày tốt/xấu")).toBeTruthy();
    expect(screen.getByText("Chọn ngày tốt")).toBeTruthy();
    cleanup();
    render(<DateSelectionNav activeHref="/good-date" />);
    expect(screen.getAllByRole("menuitem")).toHaveLength(2);
  });

  it("resolves new routes", () => {
    expect(resolveActiveNavId("/good-date")).toBe("date-selection");
    expect(resolveActiveNavId("/choose-date")).toBe("date-selection");
    expect(resolveActiveNavId("/result")).toBe("result");
  });

  it("renders calendar selection, hour selector, and detail changes", () => {
    render(<LookupScreen cells={cells} day={day} />);
    expect(screen.getByTestId("month-calendar")).toBeTruthy();
    expect(screen.getAllByText("27").length).toBeGreaterThan(0);
    expect(screen.getByTestId("day-detail").textContent).toContain("Tiểu Cát");
    fireEvent.click(document.querySelector('[data-day="15"]') as HTMLElement);
    expect(document.querySelector('[data-day="15"]')?.getAttribute("data-selected")).toBe("true");
    fireEvent.change(screen.getByLabelText("Chọn giờ"), { target: { value: "Tỵ" } });
    expect(screen.getByTestId("hour-detail").textContent).toContain("Tỵ");
    expect(screen.getByTestId("ke-panel").textContent).toContain("Khắc 1");
    expect(screen.getByTestId("ke-panel").textContent).toContain("07:01–07:20");
  });

  it("renders analog clock with numbers 1-12", () => {
    render(<AnalogClockFace />);
    for (let num = 1; num <= 12; num += 1) {
      expect(screen.getByText(String(num))).toBeTruthy();
    }
    expect(screen.queryByText("Tý")).toBeNull();
  });

  it("validates the customer form and shows lunar verification + top results", () => {
    render(<SearchForm onSubmit={() => undefined} />);
    fireEvent.click(screen.getByText("TÌM NGÀY TỐT"));
    expect(screen.getByText("Vui lòng nhập họ và tên.")).toBeTruthy();
    expect(screen.getByText("Vui lòng chọn giới tính.")).toBeTruthy();
    render(<SearchScreen person={person} dates={ranked} />);
    expect(screen.getByTestId("person-block").textContent).toContain("21/04/1990");
    expect(screen.getByTestId("person-block").textContent).toContain("Cung Phi");
    expect(screen.getByTestId("top-results").textContent).toContain("27/08/2026");
    expect(screen.getByTestId("top-results").textContent).toContain("09:41–10:00");
  });

  it("has a mobile layout frame", () => {
    render(
      <DateSelectionMobileFrame>
        <LookupScreen cells={cells} day={day} />
      </DateSelectionMobileFrame>,
    );
    expect(screen.getByTestId("mobile-frame").getAttribute("style")).toContain("375");
  });
});
