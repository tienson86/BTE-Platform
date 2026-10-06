/**
 * Marriage Public API client. HTTP only. No Decision imports.
 */

import type {
  MarriageConsultationDto,
  MarriageEnvelope,
  MarriageHistoryPageDto,
  MarriageReportDto,
} from "./types";

export const DEFAULT_MARRIAGE_API_BASE = "/backend/api/v1/consulting/marriage";
export const MARRIAGE_FETCH_TIMEOUT_MS = 120_000;

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
    include_score?: boolean;
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

export async function getMarriageHistory(
  limit = 100,
): Promise<MarriageEnvelope<MarriageHistoryPageDto>> {
  return request("GET", `${marriageApiBase()}/history?limit=${limit}`);
}

export async function downloadMarriageExport(
  consultationId: string,
  format: "pdf" | "docx",
): Promise<void> {
  const response = await fetch(
    resolvedUrl(`${marriageApiBase()}/${encodeURIComponent(consultationId)}/export/${format}`),
    { headers: { Accept: format === "pdf" ? "application/pdf" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document" } },
  );
  if (!response.ok) throw new Error("Không tạo được tệp xuất. Vui lòng thử lại.");
  const blob = await response.blob();
  const fallback = format === "pdf" ? "BTE_TuVanHonNhan.pdf" : "BTE_TuVanHonNhan.docx";
  const filename = downloadFilename(response.headers.get("Content-Disposition")) || fallback;
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.rel = "noopener";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadFilename(disposition: string | null): string | null {
  if (!disposition) return null;
  const utf8 = disposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8?.[1]) return decodeURIComponent(utf8[1].replace(/^"|"$/g, ""));
  const plain = disposition.match(/filename="?([^";]+)"?/i);
  return plain?.[1] || null;
}

function resolvedUrl(url: string): string {
  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }
  if (typeof window !== "undefined" && window.location?.origin) {
    return `${window.location.origin}${url}`;
  }
  return url;
}

function transportFailure<T>(): MarriageEnvelope<T> {
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

async function request<T>(
  method: string,
  url: string,
  body?: unknown,
): Promise<MarriageEnvelope<T>> {
  const headers: Record<string, string> = { Accept: "application/json" };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), MARRIAGE_FETCH_TIMEOUT_MS);
  try {
    const response = await fetch(resolvedUrl(url), {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
    });
    const text = await response.text();
    let payload: MarriageEnvelope<T> | null = null;
    try {
      payload = text ? (JSON.parse(text) as MarriageEnvelope<T>) : null;
    } catch {
      payload = null;
    }
    if (!payload) {
      return transportFailure<T>();
    }
    return payload;
  } catch {
    return transportFailure<T>();
  } finally {
    clearTimeout(timer);
  }
}
