import { maskVnDate, parseVnDate } from "../date_selection/vnDate";
import { FIELD_ERROR, occupationLabel } from "./labels";
import type { CreateBusinessConsultationBody, PersonRequestBody } from "./api";
import type { PersonFormValue } from "../marriage_consulting/types";

export const EMPTY_PERSON: PersonFormValue = {
  full_name: "",
  gender: "",
  birth_date: "",
  birth_time: "",
  birth_place: "",
};

export const DEFAULT_PERSON_A: PersonFormValue = { ...EMPTY_PERSON };
export const DEFAULT_PERSON_B: PersonFormValue = { ...EMPTY_PERSON };

export type PersonFieldErrors = Partial<Record<keyof PersonFormValue, string>>;

export function maskBirthDate(raw: string): string {
  return maskVnDate(raw);
}

export function validatePerson(value: PersonFormValue): PersonFieldErrors {
  const errors: PersonFieldErrors = {};
  if (!value.gender) errors.gender = FIELD_ERROR.gender;
  if (!parseVnDate(value.birth_date)) errors.birth_date = FIELD_ERROR.birth_date;
  if (value.birth_time && !/^([01]\d|2[0-3]):[0-5]\d$/.test(value.birth_time)) {
    errors.birth_time = "Giờ sinh chưa hợp lệ.";
  }
  return errors;
}

export function toPersonRequest(value: PersonFormValue): PersonRequestBody | null {
  const parsed = parseVnDate(value.birth_date);
  if (!parsed || (value.gender !== "male" && value.gender !== "female")) {
    return null;
  }
  const body: PersonRequestBody = {
    gender: value.gender,
    birth_date: parsed.iso,
  };
  if (value.full_name.trim()) body.full_name = value.full_name.trim();
  if (value.birth_time) body.birth_time = value.birth_time;
  if (value.birth_place.trim()) {
    body.birth_place = { display_name: value.birth_place.trim() };
  }
  return body;
}

export function validateOccupation(value: string): string {
  return occupationLabel(value) ? "" : FIELD_ERROR.occupation;
}

export function toConsultationBody(
  personA: PersonFormValue,
  personB: PersonFormValue,
  occupation: string,
): CreateBusinessConsultationBody | null {
  const a = toPersonRequest(personA);
  const b = toPersonRequest(personB);
  const label = occupationLabel(occupation);
  if (!a || !b || !label) return null;
  return {
    person_a: a,
    person_b: b,
    options: {
      language: "vi",
      audience: "customer",
      expert_mode: false,
      include_score: true,
    },
    request_meta: {
      client: `business_consulting;occupation=${occupation};occupation_label=${label}`,
    },
  };
}
