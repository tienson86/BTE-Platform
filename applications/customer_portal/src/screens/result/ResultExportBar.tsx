/**
 * Customer export actions — official PDF/DOCX vs convenience print.
 * Layout of frozen Result cards is unchanged.
 */

import { useState, type ReactNode } from "react";
import { apiErrorUserMessage, isApiError } from "../../api/errors";
import {
  downloadOfficialExport,
  selectedExportFromResultStore,
} from "../../export/customerExport";

type ExportBusy = "pdf" | "docx" | null;

export function ResultExportBar(): ReactNode {
  const [busy, setBusy] = useState<ExportBusy>(null);
  const [message, setMessage] = useState("");

  async function onOfficial(format: "pdf" | "docx"): Promise<void> {
    const payload = selectedExportFromResultStore();
    if (!payload) {
      setMessage("Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.");
      return;
    }
    setBusy(format);
    setMessage("");
    try {
      await downloadOfficialExport(format, payload);
    } catch (error) {
      setMessage(isApiError(error) ? apiErrorUserMessage(error) : "Không thể tạo file xuất. Vui lòng thử lại.");
    } finally {
      setBusy(null);
    }
  }

  return (
    <section className="rp-export-bar" id="xuat" aria-labelledby="rp-export-title">
      <div className="rp-export-bar__head">
        <h2 id="rp-export-title">Xuất báo cáo</h2>
        <p className="rp-export-bar__hint">
          <strong>Tải PDF</strong> là bản báo cáo chính thức. In trang kết quả chỉ là bản in trình duyệt.
        </p>
      </div>
      <div className="rp-export-bar__actions">
        <a className="rp-export-bar__btn rp-export-bar__btn--secondary" href="/reports">
          Xem báo cáo
        </a>
        <button
          type="button"
          className="rp-export-bar__btn rp-export-bar__btn--secondary"
          onClick={() => window.print()}
        >
          In trang kết quả
        </button>
        <button
          type="button"
          className="rp-export-bar__btn"
          disabled={busy !== null}
          onClick={() => void onOfficial("pdf")}
        >
          {busy === "pdf" ? "Đang tạo PDF…" : "Tải PDF"}
        </button>
        <button
          type="button"
          className="rp-export-bar__btn"
          disabled={busy !== null}
          onClick={() => void onOfficial("docx")}
        >
          {busy === "docx" ? "Đang tạo DOCX…" : "Tải DOCX"}
        </button>
      </div>
      {message ? (
        <p className="rp-export-bar__error" role="alert">
          {message}
        </p>
      ) : null}
    </section>
  );
}
