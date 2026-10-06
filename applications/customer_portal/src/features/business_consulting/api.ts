import type {
  MarriageConsultationDto,
  MarriageEnvelope,
} from "../marriage_consulting/types";
import { triggerBrowserDownload } from "../../export/customerExport";
import type { BusinessReportDto, BusinessScoreAudit } from "./types";

export type BusinessHistoryItem = {
  consultation_id: string;
  display_identity: string;
  created_at: string;
  saved_at: string | null;
  occupation: string;
  occupation_label: string;
};

export type BusinessHistoryPage = { items: BusinessHistoryItem[]; next_cursor: string | null };
export type BusinessConsultationDto = MarriageConsultationDto & {
  business_context?: BusinessHistoryItem;
  business_score?: BusinessScoreAudit | null;
  input?: { person_a: PersonRequestBody; person_b: PersonRequestBody };
};

export const DEFAULT_BUSINESS_API_BASE = "/backend/api/v1/consulting/marriage";
export const BUSINESS_FETCH_TIMEOUT_MS = 120_000;

export type PersonRequestBody = {
  full_name?: string;
  gender: "male" | "female";
  birth_date: string;
  birth_time?: string;
  birth_place?: { display_name: string };
};

export type CreateBusinessConsultationBody = {
  person_a: PersonRequestBody;
  person_b: PersonRequestBody;
  options?: {
    language?: string;
    audience?: string;
    expert_mode?: boolean;
    include_score?: boolean;
  };
  request_meta?: {
    client?: string;
  };
};

export function businessApiBase(): string {
  const fromWindow =
    typeof window !== "undefined"
      ? (window as Window & { __BTE_BUSINESS_API_BASE__?: string }).__BTE_BUSINESS_API_BASE__
      : undefined;
  return fromWindow || DEFAULT_BUSINESS_API_BASE;
}

export async function createBusinessConsultation(
  body: CreateBusinessConsultationBody,
): Promise<MarriageEnvelope<MarriageConsultationDto>> {
  return request("POST", businessApiBase(), body);
}

export async function getBusinessConsultation(
  consultationId: string,
): Promise<MarriageEnvelope<BusinessConsultationDto>> {
  return request("GET", `${businessApiBase()}/business/${encodeURIComponent(consultationId)}`);
}

export async function getBusinessReport(
  consultationId: string,
): Promise<MarriageEnvelope<BusinessReportDto>> {
  return request("GET", `${businessApiBase()}/business/${encodeURIComponent(consultationId)}/report`);
}

export function getBusinessHistory(cursor?: string): Promise<MarriageEnvelope<BusinessHistoryPage>> {
  const query = new URLSearchParams({ limit: "100" });
  if (cursor) query.set("cursor", cursor);
  return request("GET", `${businessApiBase()}/business/history?${query}`);
}

export function saveBusinessProfile(id: string): Promise<MarriageEnvelope<BusinessHistoryItem>> {
  return request("POST", `${businessApiBase()}/business/${encodeURIComponent(id)}/save`);
}

export async function downloadBusinessExport(id: string, format: "pdf" | "docx"): Promise<void> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), BUSINESS_FETCH_TIMEOUT_MS);
  try {
    const mediaType = format === "pdf" ? "application/pdf" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
    const response = await fetch(resolvedUrl(`${businessApiBase()}/business/${encodeURIComponent(id)}/export/${format}`), { headers: { Accept: mediaType }, signal: controller.signal });
    if (!response.ok || !response.headers.get("Content-Type")?.includes(mediaType)) {
      throw new Error("Không tạo được báo cáo hợp tác. Vui lòng thử lại.");
    }
    const disposition = response.headers.get("Content-Disposition");
    const encoded = disposition?.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
    const plain = disposition?.match(/filename="?([^";]+)"?/i)?.[1];
    const filename = encoded ? decodeURIComponent(encoded.replace(/^"|"$/g, "")) : plain || `BTE_TuVanHopTac.${format}`;
    triggerBrowserDownload(await response.blob(), filename);
  } finally {
    clearTimeout(timer);
  }
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
  const timer = setTimeout(() => controller.abort(), BUSINESS_FETCH_TIMEOUT_MS);
  try {
    const response = await fetch(resolvedUrl(url), {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
    });
    const text = await response.text();
    try {
      return text ? (JSON.parse(text) as MarriageEnvelope<T>) : transportFailure<T>();
    } catch {
      return transportFailure<T>();
    }
  } catch {
    return transportFailure<T>();
  } finally {
    clearTimeout(timer);
  }
}
