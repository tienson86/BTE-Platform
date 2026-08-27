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
  nayin: "Thổ",
  cung: "Ly",
  cung_element: "Hỏa",
  trach_group_label: "Đông Tứ Trạch",
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
    month_ganzhi: "Giáp Thân",
    day_ganzhi: "Quý Dậu",
  },
  six_state: { remainder: 5, code: "tieu_cat", label: "Tiểu Cát" },
  trach,
  nayin: "Kim",
  cung: "Đoài",
  cung_element: "Kim",
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
    const frame = screen.getByTestId("mobile-frame");
    expect(frame.querySelector('[data-testid="ds-calendar-card"]')).toBeTruthy();
    expect(frame.querySelector('[data-testid="ds-day-card"]')).toBeTruthy();
    expect(frame.querySelector('[data-testid="ds-clock-card"]')).toBeTruthy();
    expect(frame.querySelector('[data-testid="ds-hour-card"]')).toBeTruthy();
    expect(frame.querySelector('[data-testid="ds-ke-card"]')).toBeTruthy();
  });

  it("renders Can Chi tháng and keeps Nạp âm separate from Hành Cung", () => {
    render(<LookupScreen cells={cells} day={day} />);
    const detail = screen.getByTestId("day-detail").textContent || "";
    expect(detail).toContain("Can Chi tháng");
    expect(detail).toContain("Giáp Thân");
    expect(detail).toContain("Nạp âm");
    expect(detail).toContain("Hành Cung");
    expect(detail).toContain("Nhóm Trạch");
    expect(detail).not.toContain("Ngũ hành");
    expect(screen.getByTestId("hour-detail").textContent).toContain("Nạp âm giờ");
    expect(screen.getByTestId("hour-detail").textContent).toContain("Hành Cung giờ");
  });

  it("renders Mậu Thìn Nạp âm as Mộc", () => {
    const mauThin: DayVm = {
      ...day,
      calendar: { ...day.calendar, day_ganzhi: "Mậu Thìn" },
      ganzhi: "Mậu Thìn",
      nayin: "Mộc",
      cung: "Chấn",
      cung_element: "Mộc",
      trach: {
        cung: "Chấn",
        element_code: "moc",
        element_label: "Mộc",
        trach_group_code: "dong",
        trach_group_label: "Đông Tứ Trạch",
      },
    };
    render(<LookupScreen cells={cells} day={mauThin} />);
    const detail = screen.getByTestId("day-detail").textContent || "";
    expect(detail).toContain("Mậu Thìn");
    expect(detail).toContain("Nạp âm");
    expect(detail).toContain("Mộc");
    expect(detail).toContain("Chấn");
    expect(detail).toContain("Đông Tứ Trạch");
  });

  it("renders Canh Thìn with Nạp âm Kim and Hành Cung Hỏa", () => {
    const canhThin: DayVm = {
      ...day,
      calendar: { ...day.calendar, day_ganzhi: "Canh Thìn" },
      ganzhi: "Canh Thìn",
      nayin: "Kim",
      cung: "Ly",
      cung_element: "Hỏa",
      trach: {
        cung: "Ly",
        element_code: "hoa",
        element_label: "Hỏa",
        trach_group_code: "dong",
        trach_group_label: "Đông Tứ Trạch",
      },
    };
    render(<LookupScreen cells={cells} day={canhThin} />);
    const detail = screen.getByTestId("day-detail");
    expect(detail.textContent).toContain("Canh Thìn");
    expect(detail.textContent).toContain("Nạp âm");
    expect(detail.textContent).toContain("Kim");
    expect(detail.textContent).toContain("Ly");
    expect(detail.textContent).toContain("Hành Cung");
    expect(detail.textContent).toContain("Hỏa");
    const nayinDd = Array.from(detail.querySelectorAll("dt")).find((el) => el.textContent === "Nạp âm")
      ?.nextElementSibling?.textContent;
    const hanhDd = Array.from(detail.querySelectorAll("dt")).find((el) => el.textContent === "Hành Cung")
      ?.nextElementSibling?.textContent;
    expect(nayinDd).toBe("Kim");
    expect(hanhDd).toBe("Hỏa");
    expect(nayinDd).not.toBe(hanhDd);
  });

  it("places the clock below the calendar on desktop and hour/ke on the right", () => {
    render(<LookupScreen cells={cells} day={day} />);
    const left = screen.getByTestId("ds-left");
    const right = screen.getByTestId("ds-right");
    expect(left.children[0].getAttribute("data-testid")).toBe("ds-calendar-card");
    expect(left.children[1].getAttribute("data-testid")).toBe("ds-clock-card");
    expect(right.children[0].getAttribute("data-testid")).toBe("ds-day-card");
    expect(right.children[1].getAttribute("data-testid")).toBe("ds-hour-card");
    expect(right.children[2].getAttribute("data-testid")).toBe("ds-ke-card");
    expect(screen.getByTestId("ds-hour-card").textContent).toContain("Chọn giờ");
    expect(screen.getByTestId("ds-ke-card").textContent).toContain("Sáu khắc");
  });
});
