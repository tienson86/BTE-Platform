import type { ChangeEvent, ReactNode } from "react";

import { PERSON_A_LABEL, PERSON_B_LABEL } from "./labels";
import { maskBirthDate, maskBirthTime, type PersonFieldErrors } from "./request";
import type { PersonFormValue } from "./types";

const PLACES = ["Hà Nội", "Bắc Ninh", "Hải Phòng", "TP Hồ Chí Minh", "Đà Nẵng"];

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

  function onTime(event: ChangeEvent<HTMLInputElement>): void {
    update("birth_time", maskBirthTime(event.target.value));
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
      <fieldset className="ds-gender" data-testid={`${prefix}-gender`}>
        <legend>Giới tính</legend>
        <div className="ds-gender__options" role="radiogroup" aria-label={`${title} — giới tính`} aria-describedby={`${prefix}-gender-error`}>
          <label>
            <input
              type="radio"
              name={`${prefix}-gender`}
              value="male"
              checked={value.gender === "male"}
              onChange={() => update("gender", "male")}
            />
            <span>Nam</span>
          </label>
          <label>
            <input
              type="radio"
              name={`${prefix}-gender`}
              value="female"
              checked={value.gender === "female"}
              onChange={() => update("gender", "female")}
            />
            <span>Nữ</span>
          </label>
        </div>
        <span className="field-error" id={`${prefix}-gender-error`} data-testid={`${prefix}-gender-error`} hidden={!errors.gender}>
          {errors.gender}
        </span>
      </fieldset>
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
        <input
          id={`${prefix}-birth-time`}
          name={`${prefix}-birth-time`}
          type="text"
          inputMode="numeric"
          placeholder="HH:mm"
          maxLength={5}
          lang="vi"
          aria-describedby={`${prefix}-time-hint`}
          value={value.birth_time}
          onChange={onTime}
        />
      </label>
      <span className="muted" id={`${prefix}-time-hint`}>
        Không bắt buộc. Để trống nếu chưa rõ giờ sinh.
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
