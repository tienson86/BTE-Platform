import {
  INVALID_CONTEXT_ERROR,
  NON_DIGIT_ERROR,
  EMPTY_NUMBER_ERROR,
  MAX_NUMBER_DIGITS,
  TOO_LONG_ERROR,
} from "./labels";
import { PURPOSE_CONTEXTS, type PurposeContext } from "./types";

export type NumberEnergyFieldErrors = {
  number?: string;
  purpose_context?: string;
};

export function isPurposeContext(value: string): value is PurposeContext {
  return (PURPOSE_CONTEXTS as readonly string[]).includes(value);
}

export function isAsciiDigitString(value: string): boolean {
  return /^[0-9]+$/.test(value);
}

export function validateNumberEnergyForm(
  number: string,
  purposeContext: string,
): NumberEnergyFieldErrors {
  const errors: NumberEnergyFieldErrors = {};
  const trimmed = number.trim();
  if (!trimmed) {
    errors.number = EMPTY_NUMBER_ERROR;
  } else if (!isAsciiDigitString(trimmed)) {
    errors.number = NON_DIGIT_ERROR;
  } else if (trimmed.length > MAX_NUMBER_DIGITS) {
    errors.number = TOO_LONG_ERROR;
  }
  if (!isPurposeContext(purposeContext)) {
    errors.purpose_context = INVALID_CONTEXT_ERROR;
  }
  return errors;
}
