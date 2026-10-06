import { useEffect, useMemo, useState, type FormEvent, type ReactNode } from "react";

import { customerErrorMessage, envelopeErrors } from "../marriage_consulting/adapter";
import { adaptBusinessView } from "./adapter";
import { createBusinessConsultation, downloadBusinessExport, getBusinessConsultation, getBusinessHistory, getBusinessReport, saveBusinessProfile } from "./api";
import type { BusinessHistoryItem } from "./api";
import { BusinessHistoryPanel } from "./HistoryPanel";
import { IconExport, IconFolder } from "../../screens/canonical_desktop/icons";
import {
  FAMILY_LABEL,
  OCCUPATION_OPTIONS,
  PERSON_A_LABEL,
  PERSON_B_LABEL,
  PRODUCT_TITLE,
  SUBMIT_LABEL,
  occupationLabel,
} from "./labels";
import { PersonPanel } from "./PersonPanel";
import { ResultView } from "./ResultView";
import {
  DEFAULT_PERSON_A,
  DEFAULT_PERSON_B,
  toConsultationBody,
  validateOccupation,
  validatePerson,
} from "./request";
import type { PersonFormValue } from "../marriage_consulting/types";
import type { PersonFieldErrors } from "./request";
import type { BusinessViewModel } from "./types";

type PageStatus = "idle" | "loading" | "success" | "error";

export function BusinessConsultingPage(): ReactNode {
  const [personA, setPersonA] = useState<PersonFormValue>(DEFAULT_PERSON_A);
  const [personB, setPersonB] = useState<PersonFormValue>(DEFAULT_PERSON_B);
  const [occupation, setOccupation] = useState("");
  const [lastOccupation, setLastOccupation] = useState("");
  const [occupationError, setOccupationError] = useState("");
  const [errorsA, setErrorsA] = useState<PersonFieldErrors>({});
  const [errorsB, setErrorsB] = useState<PersonFieldErrors>({});
  const [status, setStatus] = useState<PageStatus>("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [retryable, setRetryable] = useState(false);
  const [view, setView] = useState<BusinessViewModel | null>(null);
  const [lastBody, setLastBody] = useState<ReturnType<typeof toConsultationBody>>(null);
  const [history, setHistory] = useState<BusinessHistoryItem[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [exporting, setExporting] = useState<"pdf" | "docx" | null>(null);
  const [actionError, setActionError] = useState("");
  const [retryResultId, setRetryResultId] = useState<string | null>(null);
  const busy = status === "loading" || saving || Boolean(exporting);

  const layout = useMemo(() => "customer-dashboard", []);
  useEffect(() => { void refreshHistory(); }, []);

  async function refreshHistory(cursor?: string): Promise<void> {
    setHistoryLoading(true);
    setHistoryError("");
    try {
      const response = await getBusinessHistory(cursor);
      if (!response.data || !Array.isArray(response.data.items)) throw new Error();
      setHistory((items) => cursor ? [...items, ...response.data!.items.filter((item) => !items.some((current) => current.consultation_id === item.consultation_id))] : response.data!.items);
      setNextCursor(response.data.next_cursor);
    } catch {
      setHistoryError("Chưa tải được hồ sơ hợp tác. Vui lòng làm mới danh sách.");
    } finally { setHistoryLoading(false); }
  }

  async function loadResult(id: string, selectedOccupation = lastOccupation): Promise<void> {
    setRetryResultId(id);
    try {
      const reportEnvelope = await getBusinessReport(id);
      const report = reportEnvelope.data;
      if (!report) {
        setStatus("error");
        setErrorMessage(customerErrorMessage(envelopeErrors(reportEnvelope)[0]));
        setRetryable(true);
        return;
      }
      const consultationEnvelope = await getBusinessConsultation(id);
      const consultation = consultationEnvelope.data;
      if (!consultation) {
        setStatus("error");
        setErrorMessage(customerErrorMessage(envelopeErrors(consultationEnvelope)[0]));
        setRetryable(true);
        return;
      }
      const context = consultation.business_context;
      const resultOccupation = context?.occupation_label || selectedOccupation;
      const nextView = adaptBusinessView(
        consultation,
        report,
        [...(consultationEnvelope.warnings || []), ...(reportEnvelope.warnings || [])],
        resultOccupation,
      );
      setView(nextView);
      setLastOccupation(resultOccupation);
      setSavedAt(context?.saved_at || null);
      if (context) setOccupation(context.occupation);
      setRetryResultId(null);
      setStatus("success");
    } catch {
      setStatus("error");
      setErrorMessage(customerErrorMessage(undefined));
      setRetryable(true);
    }
  }

  async function run(body = lastBody, selectedOccupation = lastOccupation): Promise<void> {
    if (!body) return;
    setStatus("loading");
    setView(null);
    setSavedAt(null);
    setActionError("");
    setRetryResultId(null);
    setErrorMessage("");
    setRetryable(false);
    try {
      const created = await createBusinessConsultation(body);
      const createErrors = envelopeErrors(created);
      if (!created.data || created.status !== "SUCCESS") {
        const err = createErrors[0];
        setStatus("error");
        setErrorMessage(customerErrorMessage(err));
        setRetryable(Boolean(err?.retryable));
        return;
      }
      await loadResult(created.data.consultation_id, selectedOccupation);
    } catch {
      setStatus("error");
      setErrorMessage(customerErrorMessage(undefined));
      setRetryable(true);
    }
  }

  async function onSave(): Promise<void> {
    if (!view || busy || savedAt) return;
    setSaving(true);
    setActionError("");
    try {
      const response = await saveBusinessProfile(view.consultationId);
      if (!response.data?.saved_at) throw new Error();
      setSavedAt(response.data.saved_at);
      await refreshHistory();
    } catch { setActionError("Chưa lưu được hồ sơ hợp tác. Vui lòng thử lại."); }
    finally { setSaving(false); }
  }

  async function onExport(format: "pdf" | "docx"): Promise<void> {
    if (!view || busy) return;
    setExporting(format);
    setActionError("");
    try { await downloadBusinessExport(view.consultationId, format); }
    catch { setActionError("Không tải được báo cáo hợp tác. Vui lòng thử lại."); }
    finally { setExporting(null); }
  }

  function startNew(): void {
    setView(null);
    setPersonA(DEFAULT_PERSON_A);
    setPersonB(DEFAULT_PERSON_B);
    setOccupation("");
    setLastOccupation("");
    setOccupationError("");
    setErrorsA({}); setErrorsB({});
    setLastBody(null); setSavedAt(null); setRetryResultId(null);
    setActionError(""); setErrorMessage(""); setRetryable(false); setStatus("idle");
  }

  function onSubmit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const nextA = validatePerson(personA);
    const nextB = validatePerson(personB);
    const nextOccupation = validateOccupation(occupation);
    setErrorsA(nextA);
    setErrorsB(nextB);
    setOccupationError(nextOccupation);
    if (Object.keys(nextA).length || Object.keys(nextB).length || nextOccupation) {
      setStatus("error");
      setErrorMessage("Thiếu thông tin bắt buộc.");
      setRetryable(false);
      return;
    }
    const body = toConsultationBody(personA, personB, occupation);
    setLastBody(body);
    setLastOccupation(occupationLabel(occupation));
    void run(body, occupationLabel(occupation));
  }

  return (
    <div className="ds-page mc-page bc-page" data-screen="business-consulting" data-layout={layout}>
      <header className="mc-intro">
        <p className="muted" data-testid="consulting-family">
          {FAMILY_LABEL} → {PRODUCT_TITLE}
        </p>
        <h1 data-testid="business-title">{PRODUCT_TITLE}</h1>
        <p className="muted">
          Nhập thông tin hai người, chọn giới tính và ngành/nghề dự định hợp tác để xem mức độ phối hợp,
          điểm nên tận dụng và điều cần thỏa thuận trước khi làm chung.
        </p>
      </header>

      {view && status !== "loading" ? null : (
        <form className="mc-form" data-testid="business-form" onSubmit={onSubmit} noValidate>
          <section className="bte-card bc-context" data-testid="business-context">
            <label htmlFor="business-occupation">
              <span>Ngành/nghề dự định hợp tác</span>
              <select
                id="business-occupation"
                name="business-occupation"
                required
                lang="vi"
                data-testid="occupation-select"
                aria-invalid={Boolean(occupationError) || undefined}
                aria-describedby="business-occupation-error"
                value={occupation}
                onChange={(event) => setOccupation(event.target.value)}
              >
                {OCCUPATION_OPTIONS.map((item) => (
                  <option key={item.value || "empty"} value={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>
              <span className="field-error" id="business-occupation-error" hidden={!occupationError}>
                {occupationError}
              </span>
            </label>
          </section>
          <div className="mc-people" data-testid="people-layout">
            <PersonPanel side="a" value={personA} errors={errorsA} onChange={setPersonA} />
            <PersonPanel side="b" value={personB} errors={errorsB} onChange={setPersonB} />
          </div>
          <div className="mc-cta">
            <button type="submit" id="btnBusinessAnalyze" data-testid="submit-business" disabled={status === "loading"}>
              {SUBMIT_LABEL}
            </button>
          </div>
        </form>
      )}

      {status === "idle" && !view ? (
        <p className="muted" data-testid="empty-state">
          Chọn ngành/nghề, nhập thông tin {PERSON_A_LABEL} và {PERSON_B_LABEL}, rồi chọn {SUBMIT_LABEL}.
        </p>
      ) : null}

      {status === "loading" ? (
        <div className="bte-card mc-loading" data-testid="loading-state" role="status" aria-live="polite">
          <p>Đang phân tích hợp tác...</p>
          <div className="skeleton-card" />
          <div className="skeleton-card" />
        </div>
      ) : null}

      {status === "error" ? (
        <div className="bte-card mc-error" data-testid="error-state" role="alert">
          <p>{errorMessage}</p>
          {retryable ? (
            <button type="button" className="secondary" data-testid="retry-analysis" onClick={() => { setStatus("loading"); void (retryResultId ? loadResult(retryResultId) : run()); }}>
              Thử lại
            </button>
          ) : null}
        </div>
      ) : null}

      {view && status !== "loading" ? (
        <>
          <div className="mc-result-toolbar" data-testid="business-result-toolbar">
            <button type="button" className="secondary" disabled={busy} onClick={startNew}>Tư vấn hợp tác mới</button>
            <div className="mc-result-toolbar__exports" aria-label="Lưu và tải báo cáo hợp tác">
              <button type="button" className="secondary" disabled={busy || Boolean(savedAt)} onClick={() => void onSave()}>
                <IconFolder size={16} /> {saving ? "Đang lưu..." : savedAt ? "Đã lưu hồ sơ" : "Lưu hồ sơ"}
              </button>
              <button type="button" className="secondary" disabled={busy} onClick={() => void onExport("pdf")}>
                <IconExport size={16} /> {exporting === "pdf" ? "Đang tạo PDF..." : "Tải PDF"}
              </button>
              <button type="button" className="secondary" disabled={busy} onClick={() => void onExport("docx")}>
                <IconExport size={16} /> {exporting === "docx" ? "Đang tạo DOCX..." : "Tải DOCX"}
              </button>
            </div>
          </div>
          {actionError ? <p role="alert">{actionError}</p> : null}
          <ResultView view={view} occupation={lastOccupation} />
        </>
      ) : null}
      <BusinessHistoryPanel
        items={history} loading={historyLoading} error={historyError}
        activeId={view?.consultationId || null} disabled={busy} hasMore={Boolean(nextCursor)}
        onRefresh={() => void refreshHistory()}
        onLoadMore={() => { if (nextCursor) void refreshHistory(nextCursor); }}
        onOpen={(id) => { setView(null); setStatus("loading"); setErrorMessage(""); setActionError(""); setRetryable(false); void loadResult(id); }}
      />
    </div>
  );
}
