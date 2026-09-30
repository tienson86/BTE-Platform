import type { ChangeEvent, ReactNode } from "react";

import { PERSON_A_LABEL, PERSON_B_LABEL } from "./labels";
import { maskBirthDate, type PersonFieldErrors } from "./request";
import type { PersonFormValue } from "./types";

const PLACES = ["Hà Nội", "Bắc Ninh", "Hải Phòng", "TP Hồ Chí Minh", "Đà Nẵng"];
const BIRTH_HOUR_OPTIONS = [
  { value: "", label: "Không biết" },
  { value: "00:00", label: "Giờ Tý (23:00-00:59)" },
  { value: "02:00", label: "Giờ Sửu (01:00-02:59)" },
  { value: "04:00", label: "Giờ Dần (03:00-04:59)" },
  { value: "06:00", label: "Giờ Mão (05:00-06:59)" },
  { value: "08:00", label: "Giờ Thìn (07:00-08:59)" },
  { value: "10:00", label: "Giờ Tỵ (09:00-10:59)" },
  { value: "12:00", label: "Giờ Ngọ (11:00-12:59)" },
  { value: "14:00", label: "Giờ Mùi (13:00-14:59)" },
  { value: "16:00", label: "Giờ Thân (15:00-16:59)" },
  { value: "18:00", label: "Giờ Dậu (17:00-18:59)" },
  { value: "20:00", label: "Giờ Tuất (19:00-20:59)" },
  { value: "22:00", label: "Giờ Hợi (21:00-22:59)" },
];

type PersonPanelProps = {
  side: "a" | "b";
  value: PersonFormValue;
  errors: PersonFieldErrors;
  onChange: (value: PersonFormValue) => void;
};

export function PersonPanel({ side, value, errors, onChange }: PersonPanelProps): ReactNode {
  const prefix = side === "a" ? "person-a" : "person-b";
  const title = side === "a" ? PERSON_A_LABEL : PERSON_B_LABEL;
  const listId = `${prefix}-places`;

  function update<K extends keyof PersonFormValue>(key: K, next: PersonFormValue[K]): void {
    onChange({ ...value, [key]: next });
  }

  function onDate(event: ChangeEvent<HTMLInputElement>): void {
    update("birth_date", maskBirthDate(event.target.value));
  }

  return (
    <section className="bte-card mc-person" data-person={side} data-testid={`${prefix}-panel`}>
      <h2>{title}</h2>
      <label htmlFor={`${prefix}-full-name`}>
        <span>Họ tên</span>
        <input
          id={`${prefix}-full-name`}
          name={`${prefix}-full-name`}
          type="text"
          autoComplete="name"
          value={value.full_name}
          onChange={(event) => update("full_name", event.target.value)}
        />
      </label>
      <div className="mc-birth-row">
        <label htmlFor={`${prefix}-birth-date`}>
          <span>Ngày sinh dương lịch</span>
          <input
            id={`${prefix}-birth-date`}
            name={`${prefix}-birth-date`}
            type="text"
            inputMode="numeric"
            autoComplete="bday"
            placeholder="DD/MM/YYYY"
            maxLength={10}
            required
            lang="vi"
            aria-invalid={Boolean(errors.birth_date) || undefined}
            aria-describedby={`${prefix}-birth-date-error`}
            value={value.birth_date}
            onChange={onDate}
          />
          <span className="field-error" id={`${prefix}-birth-date-error`} hidden={!errors.birth_date}>
            {errors.birth_date}
          </span>
        </label>
        <label htmlFor={`${prefix}-birth-time`}>
          <span>Giờ sinh</span>
          <select
            id={`${prefix}-birth-time`}
            name={`${prefix}-birth-time`}
            lang="vi"
            aria-describedby={`${prefix}-time-hint`}
            value={value.birth_time}
            onChange={(event) => update("birth_time", event.target.value)}
          >
            {BIRTH_HOUR_OPTIONS.map((item) => (
              <option key={item.label} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </label>
      </div>
      <span className="muted" id={`${prefix}-time-hint`}>
        Chọn theo 12 địa chi. Nếu không nhớ giờ sinh, để Không biết.
      </span>
      <span className="field-error" hidden={!errors.birth_time}>
        {errors.birth_time}
      </span>
      <label htmlFor={`${prefix}-birth-place`}>
        <span>Nơi sinh</span>
        <input
          id={`${prefix}-birth-place`}
          name={`${prefix}-birth-place`}
          type="text"
          autoComplete="address-level2"
          list={listId}
          value={value.birth_place}
          onChange={(event) => update("birth_place", event.target.value)}
        />
      </label>
      <datalist id={listId}>
        {PLACES.map((place) => (
          <option key={place} value={place} />
        ))}
      </datalist>
    </section>
  );
}
