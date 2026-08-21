/**
 * Official customer PDF/DOCX download from the selected analysis.
 * Uses the canonical presentation model on the API. Does not recompute engines.
 */

import { API_ENDPOINTS } from "../api/endpoints";
import { ApiError, apiErrorUserMessage } from "../api/errors";
import { getApiClient } from "../api/client";
import {
  CONTRACT_MISMATCH_MESSAGE,
  EMPTY_RESULT_MESSAGE,
  customerContractStatus,
} from "../resultState/customerContract";
import type { AnalysisDataDto } from "../models";

export type CustomerExportSource = "current" | "history";

export type CustomerExportPayload = {
  readonly analysisId: string;
  readonly source: CustomerExportSource;
  readonly data: AnalysisDataDto;
  readonly input?: Record<string, unknown> | null;
};

export type CustomerExportFormat = "pdf" | "docx";

export const OFFICIAL_PDF_LABEL = "Tải PDF";
export const OFFICIAL_DOCX_LABEL = "Tải DOCX";
export const PRINT_VIEW_LABEL = "In";
export const VIEW_REPORT_LABEL = "Xem báo cáo";
export const PRINT_VIEW_HINT = "Bản in trình duyệt — không phải PDF chính thức.";
export const OFFICIAL_PDF_HINT = "PDF chính thức (Report V1).";

export function customerExportReady(payload: CustomerExportPayload | null | undefined): boolean {
  if (!payload?.analysisId || !payload.data) return false;
  return customerContractStatus(payload.data) === "ok";
}

export function customerExportBlockMessage(
  payload: CustomerExportPayload | null | undefined,
): string {
  if (!payload?.analysisId || !payload.data) return EMPTY_RESULT_MESSAGE;
  const status = customerContractStatus(payload.data);
  if (status === "ok") return "";
  return CONTRACT_MISMATCH_MESSAGE;
}

export async function downloadOfficialExport(
  payload: CustomerExportPayload,
  format: CustomerExportFormat,
): Promise<void> {
  const block = customerExportBlockMessage(payload);
  if (block) {
    throw new ApiError(block, { kind: "validation", status: 409, code: "export_contract_mismatch" });
  }
  const path = format === "pdf" ? API_ENDPOINTS.exportPdf : API_ENDPOINTS.exportDocx;
  const fallbackFilename = format === "pdf" ? "BTE_BaoCao_V1.pdf" : "BTE_BaoCao_V1.docx";
  const result = await getApiClient().requestBlob(
    path,
    {
      analysis_id: payload.analysisId,
      source: payload.source,
      data: payload.data,
      input: payload.input ?? null,
    },
    { fallbackFilename, timeoutMs: 120_000 },
  );
  triggerBrowserDownload(result.blob, result.filename);
}

export function customerExportErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message || apiErrorUserMessage(error);
  }
  if (error instanceof Error && error.message) {
    return error.message;
  }
  return "Không tạo được tệp xuất. Vui lòng thử lại.";
}

export function triggerBrowserDownload(blob: Blob, filename: string): void {
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

declare global {
  interface Window {
    BteCustomerExport?: {
      downloadOfficialExport: typeof downloadOfficialExport;
      customerExportReady: typeof customerExportReady;
      customerExportBlockMessage: typeof customerExportBlockMessage;
      customerExportErrorMessage: typeof customerExportErrorMessage;
    };
  }
}

export function attachCustomerExportToWindow(): void {
  if (typeof window === "undefined") return;
  window.BteCustomerExport = {
    downloadOfficialExport,
    customerExportReady,
    customerExportBlockMessage,
    customerExportErrorMessage,
  };
}
