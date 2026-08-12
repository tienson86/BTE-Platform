/**
 * Map Portal wizard draft → existing POST /api/v1/analyze BirthRequest fields.
 * No new domain model; reuses AnalyzeChartRequest from models/dto.
 */

import type { AnalyzeChartRequest } from "../../models";
import type { WizardDraft } from "./pages/AnalysisWizard";

const DEFAULT_TIMEZONE = "Asia/Ho_Chi_Minh";

/**
 * Validate wizard draft and build the API birth payload.
 * Returns null when required birth fields are missing or out of range.
 */
export function draftToAnalyzeRequest(draft: WizardDraft): AnalyzeChartRequest | null {
  if (draft.name.trim().length < 2 || draft.place.trim().length < 2) {
    return null;
  }

  const year = Number(draft.year);
  const month = Number(draft.month);
  const day = Number(draft.day);
  const hourRaw = draft.hour.trim() === "" ? 0 : Number(draft.hour);
  const minuteRaw = draft.minute.trim() === "" ? 0 : Number(draft.minute);

  if (!Number.isInteger(year) || year < 1 || year > 9999) return null;
  if (!Number.isInteger(month) || month < 1 || month > 12) return null;
  if (!Number.isInteger(day) || day < 1 || day > 31) return null;
  if (!Number.isInteger(hourRaw) || hourRaw < 0 || hourRaw > 23) return null;
  if (!Number.isInteger(minuteRaw) || minuteRaw < 0 || minuteRaw > 59) return null;

  const gender = draft.gender.trim();
  return {
    year,
    month,
    day,
    hour: hourRaw,
    minute: minuteRaw,
    gender: gender ? gender : null,
    timezone: DEFAULT_TIMEZONE,
    full_name: draft.name.trim(),
    birth_place: draft.place.trim(),
  };
}
