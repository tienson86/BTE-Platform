/**
 * RB07 Number Energy runtime API client boundary.
 *
 * HTTP only. Does not adapt presentation, does not score, does not bind UI.
 * Do not import this module into NumberEnergyPage, ResultSection,
 * numberEnergyApp, or leftover analyze helpers.
 * Freeze: NUMBER_ENERGY_STATIC_UI_V1
 */

import type { NumberEnergyRuntimePayload } from "./presentationContract";

export const DEFAULT_NUMBER_ENERGY_RUNTIME_API = "/api/v1/number-energy/analyze";

export const NUMBER_ENERGY_RUNTIME_ERROR_CODE = {
  INVALID_INPUT: "INVALID_INPUT",
  HTTP_ERROR: "HTTP_ERROR",
  INVALID_JSON: "INVALID_JSON",
  MISSING_DATA: "MISSING_DATA",
  NETWORK_ERROR: "NETWORK_ERROR",
  API_ERROR: "API_ERROR",
} as const;

export type NumberEnergyRuntimeErrorCode =
  (typeof NUMBER_ENERGY_RUNTIME_ERROR_CODE)[keyof typeof NUMBER_ENERGY_RUNTIME_ERROR_CODE];

export type NumberEnergyRuntimeAnalyzeInput = {
  purpose_context: string;
  input: string;
  apiUrl?: string;
};

export type NumberEnergyRuntimeClientError = {
  code: NumberEnergyRuntimeErrorCode;
  message: string;
  status?: number;
};

export type NumberEnergyRuntimeResult =
  | { ok: true; data: NumberEnergyRuntimePayload }
  | { ok: false; error: NumberEnergyRuntimeClientError };

type NumberEnergyApiWindow = Window & {
  __BTE_NUMBER_ENERGY_API__?: string;
};

const SAFE_INPUT_MESSAGE = "Dữ liệu phân tích chưa hợp lệ.";
const SAFE_HTTP_MESSAGE = "Không thể hoàn tất phân tích lúc này.";
const SAFE_JSON_MESSAGE = "Không thể đọc kết quả phân tích.";
const SAFE_MISSING_DATA_MESSAGE = "Kết quả phân tích chưa đầy đủ.";
const SAFE_NETWORK_MESSAGE = "Không thể kết nối dịch vụ phân tích.";

/**
 * Resolve the live analyze URL: override, then window config, then default.
 */
export function numberEnergyRuntimeApiUrl(override?: string): string {
  const explicit = override?.trim();
  if (explicit) {
    return explicit;
  }
  if (typeof window !== "undefined") {
    const fromWindow = (window as NumberEnergyApiWindow).__BTE_NUMBER_ENERGY_API__?.trim();
    if (fromWindow) {
      return fromWindow;
    }
  }
  return DEFAULT_NUMBER_ENERGY_RUNTIME_API;
}

/**
 * Call POST /api/v1/number-energy/analyze and return runtime `data` or a safe error.
 */
export async function analyzeNumberEnergyRuntime(
  request: NumberEnergyRuntimeAnalyzeInput,
): Promise<NumberEnergyRuntimeResult> {
  const purpose = request.purpose_context.trim();
  const number = request.input.trim();
  if (!purpose || !number) {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.INVALID_INPUT, SAFE_INPUT_MESSAGE);
  }
  const url = numberEnergyRuntimeApiUrl(request.apiUrl);
  let response: Response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        number,
        purpose_context: toApiPurpose(purpose),
      }),
    });
  } catch {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.NETWORK_ERROR, SAFE_NETWORK_MESSAGE);
  }
  let text: string;
  try {
    text = await response.text();
  } catch {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.NETWORK_ERROR, SAFE_NETWORK_MESSAGE, response.status);
  }
  let parsed: unknown;
  try {
    parsed = text ? JSON.parse(text) : null;
  } catch {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.INVALID_JSON, SAFE_JSON_MESSAGE, response.status);
  }
  if (!response.ok) {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.HTTP_ERROR, httpMessage(response.status), response.status);
  }
  if (!isRecord(parsed)) {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.INVALID_JSON, SAFE_JSON_MESSAGE, response.status);
  }
  if (parsed.success === false) {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.API_ERROR, SAFE_HTTP_MESSAGE, response.status);
  }
  if (!isRecord(parsed.data)) {
    return fail(NUMBER_ENERGY_RUNTIME_ERROR_CODE.MISSING_DATA, SAFE_MISSING_DATA_MESSAGE, response.status);
  }
  return { ok: true, data: parsed.data as NumberEnergyRuntimePayload };
}

function toApiPurpose(purpose: string): string {
  return purpose === "motorcycle_plate" ? "motorbike_plate" : purpose;
}

function httpMessage(status: number): string {
  return status === 422 ? SAFE_INPUT_MESSAGE : SAFE_HTTP_MESSAGE;
}

function fail(
  code: NumberEnergyRuntimeErrorCode,
  message: string,
  status?: number,
): NumberEnergyRuntimeResult {
  return status === undefined ? { ok: false, error: { code, message } } : { ok: false, error: { code, message, status } };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
