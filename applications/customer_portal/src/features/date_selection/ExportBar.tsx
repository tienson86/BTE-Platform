/**
 * Date Selection PDF/DOCX export actions for /choose-date.
 * Uses the SearchResult currently on screen. Does not rerun search.
 */

import { useState, type ReactNode } from "react";

export type DateSelectionExportFormat = "pdf" | "docx";

export const EXPORT_PDF_LABEL = "📄 Xuất PDF";
export const EXPORT_DOCX_LABEL = "📝 Xuất DOCX";
export const EXPORT_PDF_LOADING = "Đang tạo PDF...";
export const EXPORT_DOCX_LOADING = "Đang tạo DOCX...";
export const EXPORT_FAILED_MESSAGE = "Không tạo được báo cáo. Vui lòng thử lại.";

export type DateSelectionExportFn = (
  searchResult: unknown,
  format: DateSelectionExportFormat,
) => Promise<void>;

export type DateSelectionExportBarProps = {
  readonly searchResult: unknown | null;
  readonly hasRecommendations: boolean;
  readonly exportFile?: DateSelectionExportFn;
};

function filenameFromDisposition(header: string | null, fallback: string): string {
  const value = header || "";
  const utf = /filename\*=UTF-8''([^;]+)/i.exec(value);
  if (utf?.[1]) {
    try {
      return decodeURIComponent(utf[1]);
    } catch {
      return utf[1];
    }
  }
  const ascii = /filename="([^"]+)"/i.exec(value);
  return ascii?.[1] || fallback;
}

function safeExportMessage(message: string): string {
  const text = message.trim();
    if (!text || /\.py:|Traceback/i.test(text)) return EXPORT_FAILED_MESSAGE;
  return text;
}

export function triggerDateSelectionDownload(blob: Blob, filename: string): void {
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

export async function downloadDateSelectionExport(
  searchResult: unknown,
  format: DateSelectionExportFormat,
): Promise<void> {
  const path =
    format === "docx"
      ? "/backend/api/v1/date-selection/report/docx"
      : "/backend/api/v1/date-selection/report/pdf";
  const response = await fetch(path, {
    method: "POST",
    headers: {
      Accept:
        "application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ search_result: searchResult }),
  });
  if (!response.ok) {
    let message = EXPORT_FAILED_MESSAGE;
    try {
      const payload = (await response.json()) as { message?: unknown };
      if (typeof payload.message === "string") message = safeExportMessage(payload.message);
    } catch {
      message = EXPORT_FAILED_MESSAGE;
    }
    throw new Error(message);
  }
  const blob = await response.blob();
  if (!blob.size) throw new Error(EXPORT_FAILED_MESSAGE);
  triggerDateSelectionDownload(
    blob,
    filenameFromDisposition(
      response.headers.get("Content-Disposition"),
      format === "docx" ? "bao-cao-chon-ngay-tot.docx" : "bao-cao-chon-ngay-tot.pdf",
    ),
  );
}

export function DateSelectionExportBar({
  searchResult,
  hasRecommendations,
  exportFile = downloadDateSelectionExport,
}: DateSelectionExportBarProps): ReactNode {
  const [busy, setBusy] = useState<DateSelectionExportFormat | null>(null);
  const [notice, setNotice] = useState("");
  if (!searchResult || !hasRecommendations) return null;

  async function onExport(format: DateSelectionExportFormat): Promise<void> {
    setBusy(format);
    setNotice("");
    try {
      await exportFile(searchResult, format);
      setNotice("");
    } catch (error) {
      const message = error instanceof Error ? error.message : EXPORT_FAILED_MESSAGE;
      setNotice(safeExportMessage(message));
    } finally {
      setBusy(null);
    }
  }

  return (
    <section className="ds-export" data-testid="ds-export" aria-label="Xuất báo cáo">
      <div className="ds-export__actions">
        <button
          type="button"
          disabled={busy !== null}
          onClick={() => void onExport("pdf")}
        >
          {busy === "pdf" ? EXPORT_PDF_LOADING : EXPORT_PDF_LABEL}
        </button>
        <button
          type="button"
          disabled={busy !== null}
          onClick={() => void onExport("docx")}
        >
          {busy === "docx" ? EXPORT_DOCX_LOADING : EXPORT_DOCX_LABEL}
        </button>
      </div>
      {notice ? (
        <p
          className="ds-export__status"
          data-tone={busy ? undefined : "error"}
          role="status"
        >
          {notice}
        </p>
      ) : null}
    </section>
  );
}
