/**
 * Customer export actions for /result.
 * Official PDF/DOCX vs convenience Print view — labels match behavior.
 */

import { useState, type ReactNode } from "react";
import {
  OFFICIAL_DOCX_LABEL,
  OFFICIAL_PDF_HINT,
  OFFICIAL_PDF_LABEL,
  PRINT_VIEW_HINT,
  PRINT_VIEW_LABEL,
  VIEW_REPORT_LABEL,
  customerExportBlockMessage,
  customerExportErrorMessage,
  customerExportReady,
  downloadOfficialExport,
  type CustomerExportPayload,
} from "../../export/customerExport";

export type ResultExportBarProps = {
  readonly payload: CustomerExportPayload | null;
};

export function ResultExportBar({ payload }: ResultExportBarProps): ReactNode {
  const [busy, setBusy] = useState<"pdf" | "docx" | null>(null);
  const [notice, setNotice] = useState("");
  const ready = customerExportReady(payload);
  const block = customerExportBlockMessage(payload);

  async function onDownload(format: "pdf" | "docx"): Promise<void> {
    if (!payload) {
      setNotice(block);
      return;
    }
    setBusy(format);
    setNotice("");
    try {
      await downloadOfficialExport(payload, format);
    } catch (error) {
      setNotice(customerExportErrorMessage(error));
    } finally {
      setBusy(null);
    }
  }

  return (
    <section
      id="xuat"
      className="rp-export-bar"
      data-export="customer-v1"
      aria-label="Xuất báo cáo"
    >
      <div className="rp-export-bar__copy">
        <h2 className="rp-export-bar__title">Xuất báo cáo</h2>
        <p className="rp-export-bar__hint">
          {OFFICIAL_PDF_HINT} {PRINT_VIEW_HINT}
        </p>
      </div>
      <div className="rp-export-bar__actions">
        <a className="rp-card__cta rp-card__cta--secondary" href="/reports">
          {VIEW_REPORT_LABEL}
        </a>
        <button
          type="button"
          className="rp-card__cta rp-card__cta--secondary"
          onClick={() => window.print()}
        >
          {PRINT_VIEW_LABEL}
        </button>
        <button
          type="button"
          className="rp-card__cta rp-card__cta--primary"
          disabled={!ready || busy !== null}
          onClick={() => void onDownload("pdf")}
        >
          {busy === "pdf" ? "Đang tạo PDF…" : OFFICIAL_PDF_LABEL}
        </button>
        <button
          type="button"
          className="rp-card__cta rp-card__cta--primary"
          disabled={!ready || busy !== null}
          onClick={() => void onDownload("docx")}
        >
          {busy === "docx" ? "Đang tạo DOCX…" : OFFICIAL_DOCX_LABEL}
        </button>
      </div>
      {notice || (!ready && block) ? (
        <p className="rp-export-bar__status" role="status">
          {notice || block}
        </p>
      ) : null}
    </section>
  );
}
