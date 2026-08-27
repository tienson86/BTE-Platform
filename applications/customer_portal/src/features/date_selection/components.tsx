import { useState, type FormEvent, type ReactNode } from "react";
import {
  CLOCK_NUMBERS,
  DATE_SELECTION_NAV,
  HOUR_BRANCHES,
  type CalendarCellVm,
  type DayVm,
  type HourVm,
  type PersonVm,
  type RankedDateVm,
} from "./types";

export function DateSelectionNav({ activeHref }: { activeHref?: string }): ReactNode {
  return (
    <div className="nav-dropdown" data-testid="date-selection-nav">
      <button type="button" className="nav-link nav-dropdown__toggle">
        Ngày tốt
      </button>
      <div className="nav-dropdown__menu" role="menu">
        {DATE_SELECTION_NAV.map((item) => (
          <a
            key={item.id}
            href={item.href}
            className="nav-dropdown__link"
            data-active={activeHref === item.href || undefined}
            role="menuitem"
          >
            {item.label}
          </a>
        ))}
      </div>
    </div>
  );
}

export function AnalogClockFace(): ReactNode {
  return (
    <div className="ds-clock" data-testid="analog-clock" aria-label="Đồng hồ analog">
      {CLOCK_NUMBERS.map((num, index) => (
        <span key={num} className="ds-clock__num" style={{ ["--deg" as string]: `${index * 30}deg` }}>
          {num}
        </span>
      ))}
      <div className="ds-clock__hand ds-clock__hand--hour" data-testid="clock-hour-hand" />
      <div className="ds-clock__hand ds-clock__hand--minute" data-testid="clock-minute-hand" />
      <div className="ds-clock__hand ds-clock__hand--second" data-testid="clock-second-hand" />
    </div>
  );
}

export function MonthCalendarGrid({
  cells,
  selectedDay,
  onSelect,
}: {
  cells: CalendarCellVm[];
  selectedDay: number;
  onSelect: (day: number) => void;
}): ReactNode {
  const leading = cells[0]?.weekday ?? 0;
  const placeholders = Array.from({ length: leading }, (_, index) => index);
  return (
    <div className="ds-calendar" data-testid="month-calendar" role="grid">
      {placeholders.map((index) => (
        <div key={`pad-${index}`} className="ds-day" hidden />
      ))}
      {cells.map((cell) => (
        <button
          key={cell.solar_day}
          type="button"
          className="ds-day"
          data-selected={cell.solar_day === selectedDay || undefined}
          data-day={cell.solar_day}
          onClick={() => onSelect(cell.solar_day)}
        >
          <span className="ds-day__solar">{cell.solar_day}</span>
          <span className="ds-day__lunar">
            {cell.lunar_day === 1 || cell.solar_day === 1
              ? `${cell.lunar_day}/${cell.lunar_month}`
              : cell.lunar_day}
          </span>
          <span className="ds-day__state">{cell.six_state.label}</span>
        </button>
      ))}
    </div>
  );
}

export function DayDetailPanel({ day }: { day: DayVm }): ReactNode {
  return (
    <dl className="ds-kv" data-testid="day-detail">
      <dt>Ngày dương</dt>
      <dd>{day.calendar.solar_label}</dd>
      <dt>Ngày âm</dt>
      <dd>{day.calendar.lunar_label}</dd>
      <dt>Can Chi năm</dt>
      <dd>{day.calendar.year_ganzhi}</dd>
      <dt>Can Chi ngày</dt>
      <dd>{day.calendar.day_ganzhi}</dd>
      <dt>Kết quả ngày</dt>
      <dd>{day.six_state.label}</dd>
      <dt>Cung Phi</dt>
      <dd>{day.trach.cung}</dd>
      <dt>Ngũ hành</dt>
      <dd>{day.trach.element_label}</dd>
      <dt>Nhóm</dt>
      <dd>{day.trach.trach_group_label}</dd>
    </dl>
  );
}

export function HourSelector({
  value,
  hours,
  onChange,
}: {
  value: string;
  hours: HourVm[];
  onChange: (branch: string) => void;
}): ReactNode {
  const selected = hours.find((item) => item.window.branch === value) ?? hours[0];
  return (
    <div data-testid="hour-selector">
      <select
        aria-label="Chọn giờ"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        {HOUR_BRANCHES.map((branch) => (
          <option key={branch} value={branch}>
            {branch}
          </option>
        ))}
      </select>
      {selected ? (
        <div data-testid="hour-detail">
          {selected.window.branch} · {selected.window.time_range} · {selected.ganzhi} · {selected.six_state.label} ·{" "}
          {selected.trach.cung} · {selected.trach.element_label} · {selected.trach.trach_group_label}
        </div>
      ) : null}
      <div data-testid="ke-panel">
        {selected?.ke_slots.map((slot) => (
          <div key={slot.ke_index} className="ds-ke-row">
            {slot.time_range} | Khắc {slot.ke_index} | {slot.six_state.label}
          </div>
        ))}
      </div>
    </div>
  );
}

export function LookupScreen({
  cells,
  day,
}: {
  cells: CalendarCellVm[];
  day: DayVm;
}): ReactNode {
  const [selectedDay, setSelectedDay] = useState(day.calendar.solar_label.split("/")[0] ? Number(day.calendar.solar_label.split("/")[0]) : 1);
  const [branch, setBranch] = useState(day.hours[0]?.window.branch ?? "Tý");
  return (
    <div className="ds-page ds-layout" data-testid="lookup-screen">
      <MonthCalendarGrid cells={cells} selectedDay={selectedDay} onSelect={setSelectedDay} />
      <div>
        <DayDetailPanel day={day} />
        <AnalogClockFace />
        <HourSelector value={branch} hours={day.hours} onChange={setBranch} />
      </div>
    </div>
  );
}

export function SearchForm({
  onSubmit,
}: {
  onSubmit: (payload: { full_name: string; gender: string; birth: string }) => void;
}): ReactNode {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const handleSubmit = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const fullName = String(form.get("full_name") || "").trim();
    const gender = String(form.get("gender") || "");
    const birth = String(form.get("birth") || "");
    const next: Record<string, string> = {};
    if (!fullName) next.full_name = "Vui lòng nhập họ và tên.";
    if (!gender) next.gender = "Vui lòng chọn giới tính.";
    if (!birth) next.birth = "Vui lòng nhập ngày sinh dương lịch.";
    setErrors(next);
    if (Object.keys(next).length) return;
    onSubmit({ full_name: fullName, gender, birth });
  };
  return (
    <form className="ds-form" onSubmit={handleSubmit} data-testid="search-form" noValidate>
      <label>
        Họ và tên
        <input name="full_name" />
        {errors.full_name ? <span className="field-error">{errors.full_name}</span> : null}
      </label>
      <label>
        Giới tính
        <select name="gender" defaultValue="">
          <option value="">Chọn giới tính</option>
          <option value="male">Nam</option>
          <option value="female">Nữ</option>
        </select>
        {errors.gender ? <span className="field-error">{errors.gender}</span> : null}
      </label>
      <label>
        Ngày sinh dương lịch
        <input name="birth" type="date" />
        {errors.birth ? <span className="field-error">{errors.birth}</span> : null}
      </label>
      <button type="submit">TÌM NGÀY TỐT</button>
    </form>
  );
}

export function PersonBlock({ person }: { person: PersonVm }): ReactNode {
  return (
    <section data-testid="person-block">
      <h2>Thông tin của bạn</h2>
      <dl>
        <dt>Họ tên</dt>
        <dd>{person.full_name}</dd>
        <dt>Giới tính</dt>
        <dd>{person.gender_label}</dd>
        <dt>Ngày sinh dương</dt>
        <dd>{person.solar_label}</dd>
        <dt>Ngày sinh âm</dt>
        <dd>{person.lunar_label}</dd>
        <dt>Can Chi</dt>
        <dd>{person.ganzhi}</dd>
        <dt>Cung Phi</dt>
        <dd>{person.trach.cung}</dd>
        <dt>Ngũ hành</dt>
        <dd>{person.trach.element_label}</dd>
        <dt>Nhóm</dt>
        <dd>{person.trach.trach_group_label}</dd>
      </dl>
    </section>
  );
}

export function TopResults({ dates }: { dates: RankedDateVm[] }): ReactNode {
  return (
    <div className="ds-cards" data-testid="top-results">
      {dates.map((item) => (
        <article key={item.day.calendar.solar_label} className="bte-card">
          <div className="ds-card-date">{item.day.calendar.solar_label}</div>
          <div className="ds-card-lunar">{item.day.calendar.lunar_label} âm</div>
          <div className="ds-card-state">{item.day.six_state.label}</div>
          <div>
            {item.day.trach.cung} · {item.day.trach.element_label} · {item.day.trach.trach_group_label}
          </div>
          <div>Giờ đề xuất</div>
          <div>{item.recommendations[0]?.time_range}</div>
        </article>
      ))}
    </div>
  );
}

export function SearchScreen({
  person,
  dates,
}: {
  person?: PersonVm;
  dates?: RankedDateVm[];
}): ReactNode {
  const [submitted, setSubmitted] = useState(Boolean(person));
  return (
    <div className="ds-page" data-testid="search-screen">
      <SearchForm onSubmit={() => setSubmitted(true)} />
      {submitted && person ? <PersonBlock person={person} /> : null}
      {submitted && dates ? <TopResults dates={dates} /> : null}
    </div>
  );
}

export function DateSelectionMobileFrame({ children }: { children: ReactNode }): ReactNode {
  return (
    <div className="ds-page" data-testid="mobile-frame" style={{ width: 375 }}>
      {children}
    </div>
  );
}
