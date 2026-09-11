import { useState, type FormEvent, type ReactNode } from "react";

import { analyzeNumberEnergy } from "./api";
import {
  EMPTY_HINT,
  INTRO,
  LOADING_LABEL,
  PRODUCT_TITLE,
  PURPOSE_LABELS,
  RETRY_LABEL,
  SERVER_FALLBACK,
  SUBMIT_LABEL,
  SYSTEM_NAME,
} from "./labels";
import { NumberEnergyResultView } from "./ResultView";
import { PURPOSE_CONTEXTS, type NumberEnergyData, type PurposeContext } from "./types";
import { validateNumberEnergyForm } from "./validate";

type PageStatus = "idle" | "loading" | "success" | "error";

export function NumberEnergyPage(): ReactNode {
  const [number, setNumber] = useState("");
  const [purposeContext, setPurposeContext] = useState<PurposeContext>("generic_number");
  const [status, setStatus] = useState<PageStatus>("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [fieldErrors, setFieldErrors] = useState<{ number?: string; purpose_context?: string }>({});
  const [data, setData] = useState<NumberEnergyData | null>(null);
  const [lastPayload, setLastPayload] = useState<{
    number: string;
    purpose_context: PurposeContext;
  } | null>(null);

  async function run(payload: { number: string; purpose_context: PurposeContext }): Promise<void> {
    setStatus("loading");
    setErrorMessage("");
    try {
      const result = await analyzeNumberEnergy(payload.number, payload.purpose_context);
      if (!result.ok || !result.envelope.data) {
        setStatus("error");
        setErrorMessage(result.errorMessage);
        setData(null);
        return;
      }
      setData(result.envelope.data);
      setStatus("success");
    } catch {
      setStatus("error");
      setErrorMessage(SERVER_FALLBACK);
      setData(null);
    }
  }

  function onSubmit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const errors = validateNumberEnergyForm(number, purposeContext);
    setFieldErrors(errors);
    if (errors.number || errors.purpose_context) {
      setStatus("error");
      setErrorMessage(errors.number || errors.purpose_context || "");
      setData(null);
      return;
    }
    const payload = { number: number.trim(), purpose_context: purposeContext };
    setLastPayload(payload);
    void run(payload);
  }

  return (
    <div className="ds-page ne-page" data-screen="number-energy">
      <header className="ne-intro">
        <p className="muted">{SYSTEM_NAME}</p>
        <h1 data-testid="number-energy-title">{PRODUCT_TITLE}</h1>
        <p className="muted">{INTRO}</p>
      </header>

      <form
        className="bte-card ds-form ne-form"
        data-testid="number-energy-form"
        onSubmit={onSubmit}
        noValidate
        aria-busy={status === "loading"}
      >
        <h2>Thông tin dãy số</h2>
        <div className="ds-form-grid">
          <label className="full">
            Dãy số
            <input
              id="number-energy-input"
              name="number"
              type="text"
              inputMode="numeric"
              autoComplete="off"
              value={number}
              aria-invalid={Boolean(fieldErrors.number) || undefined}
              aria-describedby="number-energy-input-error"
              onChange={(event) => setNumber(event.target.value)}
            />
            {fieldErrors.number ? (
              <span className="field-error" id="number-energy-input-error">
                {fieldErrors.number}
              </span>
            ) : (
              <span id="number-energy-input-error" className="field-error" hidden />
            )}
          </label>
          <label className="full">
            Ngữ cảnh sử dụng
            <select
              id="number-energy-context"
              name="purpose_context"
              value={purposeContext}
              aria-invalid={Boolean(fieldErrors.purpose_context) || undefined}
              onChange={(event) => setPurposeContext(event.target.value as PurposeContext)}
            >
              {PURPOSE_CONTEXTS.map((item) => (
                <option key={item} value={item}>
                  {PURPOSE_LABELS[item]}
                </option>
              ))}
            </select>
            {fieldErrors.purpose_context ? (
              <span className="field-error">{fieldErrors.purpose_context}</span>
            ) : null}
          </label>
        </div>
        <div className="toolbar">
          <button type="submit" data-testid="submit-number-energy" disabled={status === "loading"}>
            {SUBMIT_LABEL}
          </button>
        </div>
      </form>

      {status === "idle" && !data ? (
        <p className="muted" data-testid="empty-state">
          {EMPTY_HINT}
        </p>
      ) : null}

      {status === "loading" ? (
        <p className="muted" data-testid="loading-state" role="status">
          {LOADING_LABEL}
        </p>
      ) : null}

      {status === "error" ? (
        <div className="bte-card ne-error" data-testid="error-state" role="alert">
          <p>{errorMessage}</p>
          {lastPayload ? (
            <button
              type="button"
              className="secondary"
              data-testid="retry-analysis"
              onClick={() => void run(lastPayload)}
            >
              {RETRY_LABEL}
            </button>
          ) : null}
        </div>
      ) : null}

      {status === "success" && data ? <NumberEnergyResultView data={data} /> : null}
    </div>
  );
}
