import { useEffect, useMemo, useState, type FormEvent, type ReactNode } from "react";

import { adaptMarriageView, customerErrorMessage, envelopeErrors } from "./adapter";
import {
  createConsultation,
  downloadMarriageExport,
  getConsultation,
  getMarriageHistory,
  getReport,
} from "./api";
import { MarriageHistoryPanel } from "./HistoryPanel";
import {
  FAMILY_LABEL,
  PERSON_A_LABEL,
  PERSON_B_LABEL,
  PRODUCT_TITLE,
  SUBMIT_LABEL,
} from "./labels";
import { PersonPanel } from "./PersonPanel";
import { ResultView } from "./ResultView";
import { DEFAULT_PERSON_A, DEFAULT_PERSON_B, toConsultationBody, validatePerson } from "./request";
import type { MarriageHistoryItemDto, PersonFormValue } from "./types";
import type { PersonFieldErrors } from "./request";
import type { MarriageViewModel } from "./types";

type PageStatus = "idle" | "loading" | "success" | "error";

export function MarriageConsultingPage(): ReactNode {
  const [personA, setPersonA] = useState<PersonFormValue>(DEFAULT_PERSON_A);
  const [personB, setPersonB] = useState<PersonFormValue>(DEFAULT_PERSON_B);
  const [errorsA, setErrorsA] = useState<PersonFieldErrors>({});
  const [errorsB, setErrorsB] = useState<PersonFieldErrors>({});
  const [status, setStatus] = useState<PageStatus>("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [retryable, setRetryable] = useState(false);
  const [view, setView] = useState<MarriageViewModel | null>(null);
  const [lastBody, setLastBody] = useState<ReturnType<typeof toConsultationBody>>(null);
  const [activeConsultationId, setActiveConsultationId] = useState<string | null>(null);
  const [history, setHistory] = useState<MarriageHistoryItemDto[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [historyError, setHistoryError] = useState("");
  const [exporting, setExporting] = useState<"pdf" | "docx" | null>(null);
  const [exportError, setExportError] = useState("");

  const layout = useMemo(() => "customer-dashboard", []);

  useEffect(() => {
    void refreshHistory();
  }, []);

  async function refreshHistory(): Promise<void> {
    setHistoryLoading(true);
    setHistoryError("");
    const envelope = await getMarriageHistory();
    if (!envelope.data) {
      setHistoryError("Chưa tải được danh sách hồ sơ. Vui lòng thử lại sau.");
      setHistoryLoading(false);
      return;
    }
    setHistory(envelope.data.items);
    setHistoryLoading(false);
  }

  async function loadResult(id: string): Promise<void> {
    try {
      const reportEnvelope = await getReport(id);
      const report = reportEnvelope.data;
      if (!report) {
        setStatus("error");
        setErrorMessage(customerErrorMessage(envelopeErrors(reportEnvelope)[0]));
        setRetryable(true);
        return;
      }
      const consultationEnvelope = await getConsultation(id);
      const consultation = consultationEnvelope.data;
      if (!consultation) {
        setStatus("error");
        setErrorMessage(customerErrorMessage(envelopeErrors(consultationEnvelope)[0]));
        setRetryable(true);
        return;
      }
      setView(adaptMarriageView(
        consultation,
        report,
        [...(consultationEnvelope.warnings || []), ...(reportEnvelope.warnings || [])],
      ));
      setActiveConsultationId(id);
      setStatus("success");
    } catch {
      setStatus("error");
      setErrorMessage(customerErrorMessage(undefined));
      setRetryable(true);
    }
  }

  async function run(body = lastBody): Promise<void> {
    if (!body) return;
    setStatus("loading");
    setErrorMessage("");
    setRetryable(false);
    try {
      const created = await createConsultation(body);
      const createErrors = envelopeErrors(created);
      if (!created.data || created.status !== "SUCCESS") {
        const err = createErrors[0];
        setStatus("error");
        setErrorMessage(customerErrorMessage(err));
        setRetryable(Boolean(err?.retryable));
        return;
      }
      await loadResult(created.data.consultation_id);
      await refreshHistory();
    } catch {
      setStatus("error");
      setErrorMessage(customerErrorMessage(undefined));
      setRetryable(true);
    }
  }

  async function onExport(format: "pdf" | "docx"): Promise<void> {
    if (!activeConsultationId || exporting) return;
    setExporting(format);
    setExportError("");
    try {
      await downloadMarriageExport(activeConsultationId, format);
    } catch (error) {
      setExportError(error instanceof Error ? error.message : "Không tạo được tệp xuất. Vui lòng thử lại.");
    } finally {
      setExporting(null);
    }
  }

  function startNewConsultation(): void {
    setPersonA(DEFAULT_PERSON_A);
    setPersonB(DEFAULT_PERSON_B);
    setErrorsA({});
    setErrorsB({});
    setView(null);
    setActiveConsultationId(null);
    setLastBody(null);
    setErrorMessage("");
    setExportError("");
    setStatus("idle");
  }

  function onSubmit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const nextA = validatePerson(personA);
    const nextB = validatePerson(personB);
    setErrorsA(nextA);
    setErrorsB(nextB);
    if (Object.keys(nextA).length || Object.keys(nextB).length) {
      setStatus("error");
      setErrorMessage("Thiếu thông tin bắt buộc.");
      setRetryable(false);
      return;
    }
    const body = toConsultationBody(personA, personB, false);
    setLastBody(body);
    void run(body);
  }

  return (
    <div className="ds-page mc-page" data-screen="marriage-consulting" data-layout={layout}>
      <header className="mc-intro">
        <p className="muted" data-testid="consulting-family">
          {FAMILY_LABEL} → {PRODUCT_TITLE}
        </p>
        <h1 data-testid="marriage-title">{PRODUCT_TITLE}</h1>
        <p className="muted">
          Hai người sẽ nhận bản tư vấn hôn nhân: nên tiến tới thế nào, điểm mạnh nhất,
          và điều cần lưu ý nhất.
        </p>
      </header>

      {view && status !== "loading" ? null : (
        <form className="mc-form" data-testid="marriage-form" onSubmit={onSubmit} noValidate>
          <div className="mc-people" data-testid="people-layout">
            <PersonPanel side="a" value={personA} errors={errorsA} onChange={setPersonA} />
            <PersonPanel side="b" value={personB} errors={errorsB} onChange={setPersonB} />
          </div>
          <div className="mc-cta">
            <button type="submit" id="btnMarriageAnalyze" data-testid="submit-marriage" disabled={status === "loading"}>
              {SUBMIT_LABEL}
            </button>
          </div>
        </form>
      )}

      {status === "idle" && !view ? (
        <p className="muted" data-testid="empty-state">
          Nhập thông tin {PERSON_A_LABEL} và {PERSON_B_LABEL} rồi chọn {SUBMIT_LABEL}.
        </p>
      ) : null}

      {status === "loading" ? (
        <div className="bte-card mc-loading" data-testid="loading-state" role="status" aria-live="polite">
          <p>Đang phân tích hôn nhân...</p>
          <div className="skeleton-card" />
          <div className="skeleton-card" />
        </div>
      ) : null}

      {status === "error" ? (
        <div className="bte-card mc-error" data-testid="error-state" role="alert">
          <p>{errorMessage}</p>
          {retryable ? (
            <button type="button" className="secondary" data-testid="retry-analysis" onClick={() => void run()}>
              Thử lại
            </button>
          ) : null}
        </div>
      ) : null}

      {view && status !== "loading" ? (
        <>
          <div className="mc-result-toolbar" data-testid="marriage-result-toolbar">
            <button type="button" className="secondary" onClick={startNewConsultation}>
              Tư vấn cặp mới
            </button>
            <div className="mc-result-toolbar__exports" aria-label="Xuất bản luận giải">
              <button
                type="button"
                className="secondary"
                disabled={Boolean(exporting)}
                onClick={() => void onExport("pdf")}
              >
                {exporting === "pdf" ? "Đang tạo PDF..." : "Xuất PDF"}
              </button>
              <button
                type="button"
                className="secondary"
                disabled={Boolean(exporting)}
                onClick={() => void onExport("docx")}
              >
                {exporting === "docx" ? "Đang tạo DOCX..." : "Xuất DOCX"}
              </button>
            </div>
          </div>
          {exportError ? <p className="mc-export-error" role="alert">{exportError}</p> : null}
          <ResultView view={view} />
        </>
      ) : null}

      <MarriageHistoryPanel
        items={history}
        loading={historyLoading}
        error={historyError}
        activeId={activeConsultationId}
        onOpen={(id) => {
          setStatus("loading");
          void loadResult(id);
        }}
      />
    </div>
  );
}
