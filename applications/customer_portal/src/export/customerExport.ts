/**
 * Official customer PDF/DOCX download from the selected stored analysis.
 * Presentation only — does not re-analyze.
 */

import { getApiRuntimeConfig } from "../config/api";
import { ApiError, kindFromStatus } from "../api/errors";
import type { ApiErrorPayload } from "../api/errors";

export type CustomerExportSource = "current" | "history";

export type CustomerExportPayload = {
  readonly analysis_id: string;
  readonly source: CustomerExportSource;
  readonly data: Record<string, unknown>;
  readonly input?: Record<string, unknown> | null;
};

export const EXPORT_EMPTY_MESSAGE =
  "Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.";

const EXPORT_TIMEOUT_MS = 120_000;

function joinUrl(baseUrl: string, path: string): string {
  const base = baseUrl.replace(/\/+$/, "");
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${base}${suffix}`;
}

function filenameFromDisposition(header: string | null, fallback: string): string {
  if (!header) return fallback;
  const utf = /filename\*=UTF-8''([^;]+)/i.exec(header);
  if (utf?.[1]) {
    try {
      return decodeURIComponent(utf[1]);
    } catch {
      return utf[1];
    }
  }
  const ascii = /filename="?([^";]+)"?/i.exec(header);
  return ascii?.[1] || fallback;
}

function jsonErrorMessage(payload: ApiErrorPayload | null, fallback: string): string {
  if (!payload) return fallback;
  if (typeof payload.message === "string" && payload.message) return payload.message;
  if (typeof payload.detail === "string" && payload.detail) return payload.detail;
  return fallback;
}

/**
 * POST official PDF or DOCX and trigger a browser download.
 */
export async function downloadOfficialExport(
  format: "pdf" | "docx",
  payload: CustomerExportPayload,
): Promise<void> {
  const analysisId = payload.analysis_id.trim();
  if (!analysisId || !payload.data) {
    throw new ApiError(EXPORT_EMPTY_MESSAGE, {
      kind: "validation",
      status: 422,
      code: "export_empty",
    });
  }
  const runtime = getApiRuntimeConfig();
  const path = format === "pdf" ? "/export/pdf" : "/export/docx";
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), EXPORT_TIMEOUT_MS);
  let response: Response;
  try {
    response = await fetch(joinUrl(runtime.baseUrl, path), {
      method: "POST",
      headers: {
        Accept: format === "pdf"
          ? "application/pdf"
          : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        analysis_id: analysisId,
        source: payload.source,
        data: payload.data,
        input: payload.input ?? {},
      }),
      signal: controller.signal,
    });
  } catch (error) {
    window.clearTimeout(timer);
    const aborted =
      (error instanceof DOMException && error.name === "AbortError") ||
      (error instanceof Error && error.name === "AbortError");
    throw new ApiError(aborted ? "Yêu cầu hết thời gian chờ. Vui lòng thử lại." : "Không kết nối được máy chủ.", {
      kind: aborted ? "timeout" : "network",
      status: aborted ? 408 : null,
      cause: error,
    });
  }
  window.clearTimeout(timer);

  if (!response.ok) {
    const text = await response.text();
    let parsed: ApiErrorPayload | null = null;
    try {
      parsed = text ? (JSON.parse(text) as ApiErrorPayload) : null;
    } catch {
      parsed = null;
    }
    throw new ApiError(
      jsonErrorMessage(parsed, "Không thể tạo file xuất. Vui lòng thử lại."),
      {
        kind: kindFromStatus(response.status),
        status: response.status,
        code: parsed?.code ?? kindFromStatus(response.status),
        payload: parsed,
      },
    );
  }

  const blob = await response.blob();
  if (!blob.size) {
    throw new ApiError("Không thể tạo file xuất. Vui lòng thử lại.", {
      kind: "server",
      status: 500,
      code: "export_renderer_failed",
    });
  }
  const fallback = format === "pdf" ? "BTE_BaoCao_V1.pdf" : "BTE_BaoCao_V1.docx";
  const filename = filenameFromDisposition(
    response.headers.get("Content-Disposition"),
    fallback,
  );
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/**
 * Resolve the selected ResultStore record for export (current vs History).
 */
export function selectedExportFromResultStore(): CustomerExportPayload | null {
  const store = window.BtePortal?.ResultStore;
  if (!store) return null;
  const search = window.location.search;
  const params = new URLSearchParams(search.startsWith("?") ? search.slice(1) : search);
  const fromHistory = params.get("from") === "history";
  const historyId = (params.get("id") || "").trim();
  const record = store.resolveForDisplay
    ? store.resolveForDisplay(fromHistory, historyId || null)
    : fromHistory
      ? store.loadForView()
      : store.loadCurrent?.() ?? store.load();
  if (!record?.data) return null;
  const analysisId = String(
    record.analysis_id ||
      record.id ||
      (record.data as { analysis_id?: string }).analysis_id ||
      "",
  ).trim();
  if (!analysisId) return null;
  return {
    analysis_id: analysisId,
    source: fromHistory ? "history" : "current",
    data: record.data as Record<string, unknown>,
    input: (record.input as Record<string, unknown> | null) ?? {},
  };
}

declare global {
  interface Window {
    BtePortal?: {
      ResultStore?: {
        load: () => { analysis_id?: string; id?: string; data?: unknown; input?: unknown } | null;
        loadCurrent?: () => { analysis_id?: string; id?: string; data?: unknown; input?: unknown } | null;
        loadForView: () => { analysis_id?: string; id?: string; data?: unknown; input?: unknown } | null;
        resolveForDisplay?: (
          fromHistory: boolean,
          expectedId?: string | null,
        ) => { analysis_id?: string; id?: string; data?: unknown; input?: unknown } | null;
      };
    };
  }
}
