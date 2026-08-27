import { Fragment, useState, type FormEvent, type ReactNode } from "react";
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
import { maskVnDate, maskVnMonth, parseVnDate, parseVnMonth } from "./vnDate";

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

const ELEMENT_TOKEN: Record<string, string> = {
  Mộc: "moc",
  Hỏa: "hoa",
  Thổ: "tho",
  Kim: "kim",
  Thủy: "thuy",
};

function ElementBadge({ value }: { value?: string | null }): ReactNode {
  if (!value) return "—";
  const token = ELEMENT_TOKEN[value] ?? "kim";
  return <span className={`ds-badge ds-badge--${token}`}>{value}</span>;
}

function CungBadge({ value }: { value?: string | null }): ReactNode {
  if (!value) return "—";
  return <span className="ds-badge ds-badge--cung">{value}</span>;
}

function CompactResult({
  rows,
  testId,
}: {
  rows: Array<[string, ReactNode]>;
  testId: string;
}): ReactNode {
  return (
    <dl className="ds-kv" data-testid={testId}>
      {rows.map(([label, value]) => (
        <Fragment key={label}>
          <dt>{label}</dt>
          <dd>{value}</dd>
        </Fragment>
      ))}
    </dl>
  );
}

function HoaGiapStrip({
  ganzhi,
  nayin,
  cung,
  hanhCung,
}: {
  ganzhi: string;
  nayin: string;
  cung: string;
  hanhCung: string;
}): ReactNode {
  return (
    <div className="ds-identity" role="group" aria-label="Can Chi Nạp âm Cung Phi Hành Cung">
      <div className="ds-identity__cell">
        <span className="ds-identity__label">Can Chi</span>
        <span className="ds-identity__value">{ganzhi || "—"}</span>
      </div>
      <div className="ds-identity__cell">
        <span className="ds-identity__label">Nạp âm</span>
        <ElementBadge value={nayin} />
      </div>
      <div className="ds-identity__cell">
        <span className="ds-identity__label">Cung Phi</span>
        <CungBadge value={cung} />
      </div>
      <div className="ds-identity__cell">
        <span className="ds-identity__label">Hành Cung</span>
        <ElementBadge value={hanhCung} />
      </div>
    </div>
  );
}

function dayIdentity(day: DayVm): { ganzhi: string; nayin: string; cung: string; hanhCung: string; trach: string } {
  return {
    ganzhi: day.ganzhi || day.calendar.day_ganzhi,
    nayin: day.nayin || day.nayin_element || "",
    cung: day.cung || day.trach?.cung || "",
    hanhCung: day.cung_element || day.trach?.element_label || "",
    trach: day.trach_group_label || day.trach?.trach_group_label || "—",
  };
}

function hourIdentity(hour: HourVm): { ganzhi: string; nayin: string; cung: string; hanhCung: string; trach: string } {
  return {
    ganzhi: hour.ganzhi,
    nayin: hour.nayin || hour.nayin_element || "",
    cung: hour.cung || hour.trach?.cung || "",
    hanhCung: hour.cung_element || hour.trach?.element_label || "",
    trach: hour.trach_group_label || hour.trach?.trach_group_label || "—",
  };
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
  const identity = dayIdentity(day);
  return (
    <div data-testid="day-result-card">
      <HoaGiapStrip
        ganzhi={identity.ganzhi}
        nayin={identity.nayin}
        cung={identity.cung}
        hanhCung={identity.hanhCung}
      />
      <CompactResult
        testId="day-detail"
        rows={[
          ["Ngày dương", day.calendar.solar_label],
          ["Ngày âm", day.calendar.lunar_label],
          ["Can Chi năm", day.calendar.year_ganzhi],
          ["Can Chi tháng", day.calendar.month_ganzhi || day.month_ganzhi || "—"],
          ["Can Chi ngày", day.calendar.day_ganzhi],
          ["Kết quả ngày", day.six_state.label],
          ["Nạp âm", <ElementBadge key="nayin" value={identity.nayin} />],
          ["Cung Phi", <CungBadge key="cung" value={identity.cung} />],
          ["Hành Cung", <ElementBadge key="hanh" value={identity.hanhCung} />],
          ["Nhóm Trạch", identity.trach],
        ]}
      />
    </div>
  );
}

export function KePanel({
  slots,
  currentIndex = 0,
}: {
  slots: HourVm["ke_slots"];
  currentIndex?: number;
}): ReactNode {
  return (
    <div data-testid="ke-panel">
      {slots.map((slot) => {
        const current = slot.ke_index === currentIndex;
        const positive = !current && ["dai_an", "tieu_cat", "toc_hy"].includes(slot.six_state.code);
        return (
          <div
            key={slot.ke_index}
            className="ds-ke-row"
            data-current={current || undefined}
            data-tone={positive ? "positive" : undefined}
          >
            <span className="ds-ke-row__time">{slot.time_range}</span>
            <span className="ds-ke-row__label">Khắc {slot.ke_index}</span>
            <span className="ds-ke-row__result">{slot.six_state.label}</span>
          </div>
        );
      })}
    </div>
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
  const identity = selected ? hourIdentity(selected) : null;
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
      {selected && identity ? (
        <div data-testid="hour-detail">
          <HoaGiapStrip
            ganzhi={identity.ganzhi}
            nayin={identity.nayin}
            cung={identity.cung}
            hanhCung={identity.hanhCung}
          />
          <CompactResult
            testId="hour-detail-kv"
            rows={[
              ["Giờ", selected.window.branch],
              ["Khung giờ", selected.window.time_range],
              ["Can Chi giờ", selected.ganzhi],
              ["Kết quả giờ", selected.six_state.label],
              ["Nạp âm giờ", <ElementBadge key="hnayin" value={identity.nayin} />],
              ["Cung Phi giờ", <CungBadge key="hcung" value={identity.cung} />],
              ["Hành Cung giờ", <ElementBadge key="hhanh" value={identity.hanhCung} />],
              ["Nhóm Trạch giờ", identity.trach],
            ]}
          />
        </div>
      ) : null}
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
  const selectedHour = day.hours.find((item) => item.window.branch === branch) ?? day.hours[0];
  return (
    <div className="ds-page" data-testid="lookup-screen">
      <div className="ds-layout">
        <div className="ds-left" data-testid="ds-left">
          <section className="bte-card ds-calendar-card" data-testid="ds-calendar-card">
            <MonthCalendarGrid cells={cells} selectedDay={selectedDay} onSelect={setSelectedDay} />
          </section>
          <section className="bte-card ds-clock-card" data-testid="ds-clock-card">
            <AnalogClockFace />
          </section>
        </div>
        <div className="ds-right" data-testid="ds-right">
          <section className="bte-card ds-detail" data-testid="ds-day-card">
            <h2>Kết quả ngày</h2>
            <DayDetailPanel day={day} />
          </section>
          <section className="bte-card ds-hour" data-testid="ds-hour-card">
            <h2>Chọn giờ</h2>
            <HourSelector value={branch} hours={day.hours} onChange={setBranch} />
          </section>
          <section className="bte-card ds-ke" data-testid="ds-ke-card">
            <h2>Sáu khắc</h2>
            <KePanel slots={selectedHour?.ke_slots ?? []} />
          </section>
        </div>
      </div>
    </div>
  );
}

export function SearchForm({
  onSubmit,
}: {
  onSubmit: (payload: {
    full_name: string;
    gender: string;
    birth: string;
    target_month: string;
  }) => void;
}): ReactNode {
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [birth, setBirth] = useState("");
  const now = new Date();
  const [targetMonth, setTargetMonth] = useState(
    `${String(now.getMonth() + 1).padStart(2, "0")}/${now.getFullYear()}`,
  );
  const handleSubmit = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const fullName = String(form.get("full_name") || "").trim();
    const gender = String(form.get("gender") || "");
    const parsedBirth = parseVnDate(birth);
    const parsedMonth = parseVnMonth(targetMonth);
    const next: Record<string, string> = {};
    if (!fullName) next.full_name = "Vui lòng nhập họ và tên.";
    if (!gender) next.gender = "Vui lòng chọn giới tính.";
    if (!birth.trim()) next.birth = "Vui lòng nhập ngày sinh dương lịch.";
    else if (!parsedBirth) next.birth = "Ngày không hợp lệ.";
    if (!parsedMonth) next.target_month = "Tháng không hợp lệ.";
    setErrors(next);
    if (Object.keys(next).length || !parsedBirth || !parsedMonth) return;
    onSubmit({
      full_name: fullName,
      gender,
      birth: parsedBirth.iso,
      target_month: parsedMonth.iso,
    });
  };
  return (
    <form className="ds-form" onSubmit={handleSubmit} data-testid="search-form" noValidate>
      <div className="ds-form-grid">
        <label className="full">
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
          <input
            name="birth"
            type="text"
            inputMode="numeric"
            placeholder="DD/MM/YYYY"
            value={birth}
            onChange={(event) => setBirth(maskVnDate(event.target.value))}
          />
          {errors.birth ? <span className="field-error">{errors.birth}</span> : null}
        </label>
        <label className="full">
          Tháng cần tìm ngày tốt
          <div
            className="ds-month-input"
            data-testid="target-month"
            data-display={parseVnMonth(targetMonth)?.display ?? ""}
          >
            <span className="ds-month-input__prefix">Tháng</span>
            <input
              name="target_month"
              type="text"
              inputMode="numeric"
              placeholder="09/2026"
              aria-label="Tháng cần tìm ngày tốt"
              value={targetMonth}
              onChange={(event) => setTargetMonth(maskVnMonth(event.target.value))}
            />
          </div>
          {errors.target_month ? <span className="field-error">{errors.target_month}</span> : null}
        </label>
      </div>
      <button type="submit">TÌM NGÀY TỐT</button>
    </form>
  );
}

function personIdentity(person: PersonVm): {
  ganzhi: string;
  nayin: string;
  cung: string;
  hanhCung: string;
  trach: string;
} {
  return {
    ganzhi: person.year_ganzhi || person.ganzhi,
    nayin: person.nayin || person.nayin_element || "",
    cung: person.cung_phi || person.cung || person.trach.cung,
    hanhCung: person.cung_element || person.trach.element_label,
    trach: person.trach_group_label || person.trach.trach_group_label,
  };
}

export function PersonBlock({ person }: { person: PersonVm }): ReactNode {
  const identity = personIdentity(person);
  return (
    <section data-testid="person-block">
      <h2>Thông tin của bạn</h2>
      <CompactResult
        testId="person-detail"
        rows={[
          ["Họ và tên", person.full_name],
          ["Giới tính", person.gender_label],
          ["Ngày sinh dương", person.solar_label],
          ["Ngày sinh âm", person.lunar_label],
          ["Can Chi năm", identity.ganzhi],
          ["Nạp âm", <ElementBadge key="pnayin" value={identity.nayin} />],
          ["Cung Phi", <CungBadge key="pcung" value={identity.cung} />],
          ["Hành Cung", <ElementBadge key="phanh" value={identity.hanhCung} />],
          ["Nhóm Trạch", identity.trach],
        ]}
      />
    </section>
  );
}

export function TopResults({ dates }: { dates: RankedDateVm[] }): ReactNode {
  return (
    <div className="ds-cards" data-testid="top-results">
      {dates.map((item) => {
        const identity = dayIdentity(item.day);
        return (
          <article key={item.day.calendar.solar_label} className="bte-card">
            <div className="ds-card-date">{item.day.calendar.solar_label}</div>
            <div className="ds-card-lunar">{item.day.calendar.lunar_label} âm</div>
            <div className="ds-card-state">{item.day.six_state.label}</div>
            <div>Can Chi ngày: {identity.ganzhi}</div>
            <div>Nạp âm: {identity.nayin || "—"}</div>
            <div>Cung Phi: {identity.cung || "—"}</div>
            <div>Hành Cung: {identity.hanhCung || "—"}</div>
            <div>Nhóm: {identity.trach}</div>
            <div>Giờ đề xuất: {item.recommendations[0]?.time_range}</div>
          </article>
        );
      })}
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
