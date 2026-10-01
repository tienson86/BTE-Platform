import { useMemo, useState, type FormEvent, type ReactNode } from "react";

import { adaptMarriageView, customerErrorMessage, envelopeErrors } from "./adapter";
import { createConsultation, getConsultation, getReport } from "./api";
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
import type { PersonFormValue } from "./types";
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

  const layout = useMemo(() => "customer-dashboard", []);

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
    } catch {
      setStatus("error");
      setErrorMessage(customerErrorMessage(undefined));
      setRetryable(true);
    }
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

      {view && status !== "loading" ? <ResultView view={view} /> : null}
    </div>
  );
}
