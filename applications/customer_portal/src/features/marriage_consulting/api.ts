/**
 * Marriage Public API client. HTTP only. No Decision imports.
 */

import type {
  MarriageConsultationDto,
  MarriageEnvelope,
  MarriageReportDto,
} from "./types";

export const DEFAULT_MARRIAGE_API_BASE = "/backend/api/v1/consulting/marriage";

export type PersonRequestBody = {
  full_name?: string;
  gender: "male" | "female";
  birth_date: string;
  birth_time?: string;
  birth_place?: { display_name: string };
};

export type CreateConsultationBody = {
  person_a: PersonRequestBody;
  person_b: PersonRequestBody;
  options?: {
    language?: string;
    audience?: string;
    expert_mode?: boolean;
  };
};

export function marriageApiBase(): string {
  const fromWindow =
    typeof window !== "undefined"
      ? (window as Window & { __BTE_MARRIAGE_API_BASE__?: string }).__BTE_MARRIAGE_API_BASE__
      : undefined;
  return fromWindow || DEFAULT_MARRIAGE_API_BASE;
}

export async function createConsultation(
  body: CreateConsultationBody,
  expert = false,
): Promise<MarriageEnvelope<MarriageConsultationDto>> {
  const url = expert ? `${marriageApiBase()}?expert=true` : marriageApiBase();
  return request("POST", url, body);
}

export async function getConsultation(
  consultationId: string,
  expert = false,
): Promise<MarriageEnvelope<MarriageConsultationDto>> {
  const suffix = expert ? "?expert=true" : "";
  return request("GET", `${marriageApiBase()}/${consultationId}${suffix}`);
}

export async function getReport(
  consultationId: string,
  expert = false,
): Promise<MarriageEnvelope<MarriageReportDto>> {
  const suffix = expert ? "?expert=true" : "";
  return request("GET", `${marriageApiBase()}/${consultationId}/report${suffix}`);
}

function resolvedUrl(url: string): string {
  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }
  return `http://127.0.0.1${url}`;
}

async function request<T>(
  method: string,
  url: string,
  body?: unknown,
): Promise<MarriageEnvelope<T>> {
  const headers: Record<string, string> = { Accept: "application/json" };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const response = await fetch(resolvedUrl(url), {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let payload: MarriageEnvelope<T> | null = null;
  try {
    payload = text ? (JSON.parse(text) as MarriageEnvelope<T>) : null;
  } catch {
    payload = null;
  }
  if (!payload) {
    return {
      status: "FAILED",
      data: null,
      warnings: [],
      errors: [
        {
          code: "INTERNAL_ERROR",
          stage: "transport",
          message: "Không thể hoàn tất phân tích lúc này.",
          retryable: true,
          consultation_id: null,
        },
      ],
    };
  }
  return payload;
}
