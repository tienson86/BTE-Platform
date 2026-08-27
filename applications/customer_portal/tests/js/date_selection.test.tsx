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
  formatVnMonth,
  hourOptionLabel,
  parseVnDate,
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
  year_ganzhi: "Canh Ngọ",
  nayin: "Thổ",
  cung: "Đoài",
  cung_element: "Kim",
  trach,
};

const westHour = {
  branch: "Tỵ",
  time_range: "09:41–10:00",
  classification: "Đại An",
  primary: true,
  full_time_range: "09:01–11:00",
  ganzhi: "Canh Tỵ",
  nayin: "Thổ",
  cung: "Càn",
  cung_element: "Kim",
  trach_group: "tay",
  trach_group_label: "Tây Tứ Trạch",
  ke_result: "Đại An",
  ke_time_range: "09:41–10:00",
};

const mauDanHour = {
  branch: "Dần",
  time_range: "03:01–03:20",
  classification: "Đại An",
  primary: true,
  full_time_range: "03:01–05:00",
  ganzhi: "Mậu Dần",
  nayin: "Thổ",
  cung: "Khôn",
  cung_element: "Thổ",
  trach_group: "tay",
  trach_group_label: "Tây Tứ Trạch",
  ke_result: "Đại An",
  ke_time_range: "03:01–03:20",
};

const ranked: RankedDateVm[] = [
  {
    day,
    recommendations: [westHour],
    compatible_hours: [
      {
        branch: "Dần",
        full_time_range: "03:01–05:00",
        ganzhi: "Mậu Dần",
        nayin: "Thổ",
        cung: "Khôn",
        cung_element: "Thổ",
        trach_group: "tay",
        trach_group_label: "Tây Tứ Trạch",
        positive_ke: [{ index: 1, time_range: "03:01–03:20", result: "Đại An" }],
      },
      {
        branch: "Tỵ",
        full_time_range: "09:01–11:00",
        ganzhi: "Canh Tỵ",
        nayin: "Thổ",
        cung: "Càn",
        cung_element: "Kim",
        trach_group: "tay",
        trach_group_label: "Tây Tứ Trạch",
        positive_ke: [{ index: 3, time_range: "09:41–10:00", result: "Đại An" }],
      },
      {
        branch: "Mão",
        full_time_range: "05:01–07:00",
        ganzhi: "Kỷ Mão",
        nayin: "Thổ",
        cung: "Cấn",
        cung_element: "Thổ",
        trach_group: "tay",
        trach_group_label: "Tây Tứ Trạch",
        positive_ke: [
          { index: 2, time_range: "05:21–05:40", result: "Tốc Hỷ" },
          { index: 5, time_range: "06:21–06:40", result: "Tiểu Cát" },
        ],
      },
    ],
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

  it("shows full traditional hour labels in the selector", () => {
    render(<LookupScreen cells={cells} day={day} />);
    const select = screen.getByLabelText("Chọn giờ") as HTMLSelectElement;
    const labels = Array.from(select.options).map((option) => option.textContent);
    expect(labels).toEqual([
      "Giờ Tý (23:01–01:00)",
      "Giờ Sửu (01:01–03:00)",
      "Giờ Dần (03:01–05:00)",
      "Giờ Mão (05:01–07:00)",
      "Giờ Thìn (07:01–09:00)",
      "Giờ Tỵ (09:01–11:00)",
      "Giờ Ngọ (11:01–13:00)",
      "Giờ Mùi (13:01–15:00)",
      "Giờ Thân (15:01–17:00)",
      "Giờ Dậu (17:01–19:00)",
      "Giờ Tuất (19:01–21:00)",
      "Giờ Hợi (21:01–23:00)",
    ]);
    expect(Array.from(select.options).map((option) => option.value)).toEqual([
      "Tý",
      "Sửu",
      "Dần",
      "Mão",
      "Thìn",
      "Tỵ",
      "Ngọ",
      "Mùi",
      "Thân",
      "Dậu",
      "Tuất",
      "Hợi",
    ]);
    expect(select.value).toBe("Thìn");
    expect(select.selectedOptions[0].textContent).toBe("Giờ Thìn (07:01–09:00)");
    fireEvent.change(select, { target: { value: "Tỵ" } });
    expect(select.selectedOptions[0].textContent).toBe("Giờ Tỵ (09:01–11:00)");
    expect(screen.getByTestId("hour-detail").textContent).toContain("Can Chi giờ");
    expect(screen.getByTestId("hour-detail").textContent).toContain("Tỵ");
    expect(screen.getByTestId("ke-panel").textContent).toContain("Khắc 1");
    expect(hourOptionLabel("Tý")).toBe("Giờ Tý (23:01–01:00)");
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
    expect(screen.queryByText("Vui lòng chọn giới tính.")).toBeNull();
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
    expect(screen.getByTestId("hour-detail").textContent).not.toContain("Kết quả giờ");
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

  it("parses Vietnamese birth dates and rejects impossible days", () => {
    expect(parseVnDate("21/01/1987")).toEqual({
      year: 1987,
      month: 1,
      day: 21,
      iso: "1987-01-21",
      display: "21/01/1987",
    });
    expect(parseVnDate("29/02/2024")?.iso).toBe("2024-02-29");
    expect(parseVnDate("31/02/2026")).toBeNull();
    expect(parseVnDate("32/01/2026")).toBeNull();
    expect(parseVnDate("21/13/1987")).toBeNull();
    expect(formatVnMonth(2026, 9)).toBe("Tháng 09/2026");
    expect(formatVnMonth(2026, 9)).not.toContain("September");
  });

  it("accepts DD/MM/YYYY on the search form and keeps the visible value", () => {
    const submitted: Array<{ birth: string; target_month: string }> = [];
    render(
      <SearchForm
        onSubmit={(payload) => submitted.push({ birth: payload.birth, target_month: payload.target_month })}
      />,
    );
    fireEvent.change(screen.getByLabelText("Họ và tên"), { target: { value: "Nguyễn Tiến Sơn" } });
    expect((screen.getByRole("radio", { name: "Nam" }) as HTMLInputElement).checked).toBe(true);
    fireEvent.change(screen.getByPlaceholderText("DD/MM/YYYY"), { target: { value: "21011987" } });
    expect((screen.getByPlaceholderText("DD/MM/YYYY") as HTMLInputElement).value).toBe("21/01/1987");
    fireEvent.change(screen.getByPlaceholderText("09/2026"), { target: { value: "092026" } });
    expect(screen.getByTestId("target-month").getAttribute("data-display")).toBe("Tháng 09/2026");
    fireEvent.click(screen.getByText("TÌM NGÀY TỐT"));
    expect(submitted).toEqual([{ birth: "1987-01-21", target_month: "2026-09" }]);
  });

  it("rejects 31/02/2026 without submitting", () => {
    const submitted: unknown[] = [];
    render(<SearchForm onSubmit={(payload) => submitted.push(payload)} />);
    fireEvent.change(screen.getByLabelText("Họ và tên"), { target: { value: "A" } });
    fireEvent.change(screen.getByPlaceholderText("DD/MM/YYYY"), { target: { value: "31022026" } });
    fireEvent.click(screen.getByText("TÌM NGÀY TỐT"));
    expect(screen.getByText("Ngày không hợp lệ.")).toBeTruthy();
    expect(submitted).toHaveLength(0);
  });

  it("renders personal information with explicit semantic labels", () => {
    render(<SearchScreen person={person} dates={ranked} />);
    const block = screen.getByTestId("person-block").textContent || "";
    expect(block).toContain("Ngày sinh dương");
    expect(block).toContain("15/05/1990");
    expect(block).toContain("Ngày sinh âm");
    expect(block).toContain("21/04/1990");
    expect(block).toContain("Can Chi năm");
    expect(block).toContain("Nạp âm");
    expect(block).toContain("Thổ");
    expect(block).toContain("Cung Phi");
    expect(block).toContain("Hành Cung");
    expect(block).toContain("Kim");
    expect(block).toContain("Nhóm Trạch");
    expect(block).not.toContain("Ngũ hành");
    const canChi = Array.from(screen.getByTestId("person-detail").querySelectorAll("dt")).map(
      (el) => el.textContent,
    );
    expect(canChi).not.toContain("Can Chi");
    expect(screen.getByTestId("top-results").textContent).toContain("27/08/2026");
    expect(screen.getByTestId("top-results").textContent).not.toContain("September");
    expect(screen.getByTestId("top-results").textContent).not.toMatch(/\d{4}-\d{2}-\d{2}/);
  });

  it("keeps search inputs usable on a mobile frame", () => {
    render(
      <DateSelectionMobileFrame>
        <SearchForm onSubmit={() => undefined} />
      </DateSelectionMobileFrame>,
    );
    const birth = screen.getByPlaceholderText("DD/MM/YYYY");
    expect(birth.getAttribute("type")).toBe("text");
    expect(screen.getByTestId("target-month")).toBeTruthy();
    expect(screen.queryByText("Ngũ hành")).toBeNull();
  });

  it("renders complete Top-5 day identity including year and month Ganzhi", () => {
    render(<SearchScreen person={person} dates={ranked} />);
    const card = screen.getByTestId("ranked-card").textContent || "";
    expect(card).toContain("Can Chi năm");
    expect(card).toContain("Bính Ngọ");
    expect(card).toContain("Can Chi tháng");
    expect(card).toContain("Giáp Thân");
    expect(card).toContain("Can Chi ngày");
    expect(card).toContain("Quý Dậu");
    expect(card).toContain("Nạp âm");
    expect(card).toContain("Cung Phi");
    expect(card).toContain("Đoài (Kim)");
    expect(card).not.toContain("Hành Cung");
    expect(card).toContain("Nhóm Trạch");
    expect(card).toContain("Tây Tứ Trạch");
    expect(card).not.toContain("Ngũ hành");
  });

  it("renders recommended hour evidence for Mậu Dần including Trạch", () => {
    render(
      <SearchScreen
        person={person}
        dates={[
          {
            day,
            recommendations: [mauDanHour],
            compatible_hours: [
              {
                branch: "Dần",
                full_time_range: "03:01–05:00",
                ganzhi: "Mậu Dần",
                nayin: "Thổ",
                cung: "Khôn",
                cung_element: "Thổ",
                trach_group: "tay",
                trach_group_label: "Tây Tứ Trạch",
                positive_ke: [{ index: 1, time_range: "03:01–03:20", result: "Đại An" }],
              },
            ],
          },
        ]}
      />,
    );
    const hours = screen.getByTestId("compatible-hours").textContent || "";
    expect(hours).toContain("Giờ Dần (03:01–05:00) · Khôn (Thổ)");
    expect(hours).toContain("Giờ phù hợp Nhóm Trạch của bạn");
    expect(hours).not.toContain("✓ Phù hợp Nhóm Trạch của bạn");
    expect(screen.queryByTestId("trach-match")).toBeNull();
    expect(screen.getByTestId("positive-ke").textContent).toContain("Đại An");
    expect(screen.getByTestId("positive-ke").textContent).toContain("03:01–03:20");
    expect(hours).not.toContain("Ngũ hành");
    expect(hours).not.toContain("Kết quả giờ");
    expect(hours).not.toContain("Giờ đề xuất");
    expect(hours).not.toContain("Thời điểm đẹp nhất");
  });

  it("keeps additional khắc structured with traditional hour identity", () => {
    render(<SearchScreen person={person} dates={ranked} />);
    const ke = screen.getByTestId("positive-ke").textContent || "";
    expect(ke).toContain("Các thời điểm đẹp");
    expect(ke).toContain("Đại An");
    expect(ke).toContain("Tốc Hỷ");
    expect(ke).toContain("Tiểu Cát");
    expect(ke).toContain("Giờ Mão");
    expect(ke).toContain("05:21–05:40");
    expect(screen.getByTestId("top-results").textContent).not.toContain("Thời điểm đẹp nhất");
    expect(screen.getByTestId("top-results").textContent).not.toContain(
      "05:21–05:40, 03:41–04:00",
    );
  });

  it("never renders an opposite-trạch hour as recommended", () => {
    render(
      <SearchScreen
        person={person}
        dates={[
          {
            day,
            recommendations: [],
            compatible_hours: [
              {
                ...mauDanHour,
                branch: "Thìn",
                full_time_range: "07:01–09:00",
                ganzhi: "Bính Thìn",
                cung: "Ly",
                cung_element: "Hỏa",
                trach_group: "dong",
                trach_group_label: "Đông Tứ Trạch",
                positive_ke: [{ index: 1, time_range: "07:01–07:20", result: "Đại An" }],
              },
            ],
          },
        ]}
      />,
    );
    expect(screen.queryByTestId("compatible-hours")).toBeNull();
    expect(screen.queryByTestId("positive-ke")).toBeNull();
  });

  it("never renders an opposite-trạch day card", () => {
    const eastDay: DayVm = {
      ...day,
      trach_group: "dong",
      trach: {
        cung: "Ly",
        element_code: "hoa",
        element_label: "Hỏa",
        trach_group_code: "dong",
        trach_group_label: "Đông Tứ Trạch",
      },
    };
    render(
      <SearchScreen
        person={person}
        dates={[{ day: eastDay, recommendations: [], compatible_hours: [] }]}
      />,
    );
    expect(screen.queryByTestId("ranked-card")).toBeNull();
  });

  it("keeps Top-5 evidence readable inside a mobile frame", () => {
    render(
      <DateSelectionMobileFrame>
        <SearchScreen person={person} dates={ranked} />
      </DateSelectionMobileFrame>,
    );
    const card = screen.getByTestId("ranked-card");
    expect(card.querySelector("table")).toBeNull();
    expect(card.textContent).toContain("Can Chi năm");
    expect(card.textContent).toContain("Nạp âm");
    expect(card.textContent).toContain("Cung Phi");
    expect(card.textContent).toContain("Nhóm Trạch");
    expect(card.textContent).toContain("Các thời điểm đẹp");
    expect(card.textContent).toContain("Giờ phù hợp Nhóm Trạch của bạn");
    expect(card.textContent).not.toContain("Kết quả giờ");
    expect(card.textContent).not.toContain("Giờ đề xuất");
    expect(card.textContent).not.toContain("Thời điểm đẹp nhất");
    expect(screen.getByTestId("mobile-frame").getAttribute("style")).toContain("375");
  });

  it("never shows Kết quả giờ on lookup or search surfaces", () => {
    render(<LookupScreen cells={cells} day={day} />);
    expect(screen.getByTestId("hour-detail").textContent).not.toContain("Kết quả giờ");
    expect(screen.getByTestId("hour-detail-kv").textContent).toContain("Can Chi giờ");
    expect(screen.getByTestId("ke-panel").textContent).toContain("Tiểu Cát");
    cleanup();
    render(<SearchScreen person={person} dates={ranked} />);
    const results = screen.getByTestId("top-results").textContent || "";
    expect(results).not.toContain("Kết quả giờ");
    expect(results).toContain("Các thời điểm đẹp");
    expect(results).toContain("Giờ phù hợp Nhóm Trạch của bạn");
    expect(results).not.toContain("Thời điểm đẹp nhất");
  });

  it("uses gender radios with Nam selected by default", () => {
    render(<SearchForm onSubmit={() => undefined} />);
    const radios = screen.getAllByRole("radio");
    expect(radios).toHaveLength(2);
    expect((screen.getByRole("radio", { name: "Nam" }) as HTMLInputElement).checked).toBe(true);
    expect((screen.getByRole("radio", { name: "Nữ" }) as HTMLInputElement).checked).toBe(false);
    expect(screen.queryByRole("combobox")).toBeNull();
  });

  it("places input and person panels in the same desktop row", () => {
    render(<SearchScreen person={person} dates={ranked} />);
    const row = screen.getByTestId("search-row");
    expect(row.className).toContain("ds-search-row");
    expect(row.querySelector('[data-testid="search-form"]')).toBeTruthy();
    expect(row.querySelector('[data-testid="person-block"]')).toBeTruthy();
    expect(row.compareDocumentPosition(screen.getByTestId("top-results")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it("does not duplicate Trach confirmation on recommended hours", () => {
    render(<SearchScreen person={person} dates={ranked} />);
    const hours = screen.getByTestId("compatible-hours").textContent || "";
    expect(hours).toContain("Giờ phù hợp Nhóm Trạch của bạn");
    expect(hours).not.toContain("✓ Phù hợp Nhóm Trạch của bạn");
    expect(screen.getByTestId("ranked-card").textContent).toContain("Đoài (Kim)");
    expect(screen.getByTestId("compatible-hours").textContent).toContain("Càn (Kim)");
  });
});
