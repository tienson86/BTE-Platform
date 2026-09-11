import { useId, type FormEvent, type ReactNode } from "react";

import {
  ANALYSIS_TYPE_OPTIONS,
  getAnalysisOption,
  type AnalysisType,
  type GoldenPreviewState,
  validateCustomerInput,
} from "./formModel";

type InputSectionProps = {
  analysisType: AnalysisType;
  inputValue: string;
  errorMessage: string;
  onAnalysisTypeChange: (type: AnalysisType) => void;
  onInputChange: (value: string) => void;
  onRevealGoldenPreview: (preview: GoldenPreviewState) => void;
  onErrorMessageChange: (message: string) => void;
};

export function InputSection({
  analysisType,
  inputValue,
  errorMessage,
  onAnalysisTypeChange,
  onInputChange,
  onRevealGoldenPreview,
  onErrorMessageChange,
}: InputSectionProps): ReactNode {
  const errorId = useId();
  const helpId = useId();
  const option = getAnalysisOption(analysisType);
  const isEmpty = inputValue.trim() === "";

  function handleSubmit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const nextError = validateCustomerInput(analysisType, inputValue);
    if (nextError) {
      onErrorMessageChange(nextError);
      return;
    }
    onErrorMessageChange("");
    onRevealGoldenPreview({
      analysisType,
      originalInput: inputValue.trim(),
    });
  }

  return (
    <section className="bte-card ne-shell-section ne-form-card" data-section="NE-INPUT" data-testid="input-section">
      <h2>Nhập số cần phân tích</h2>
      <p className="muted">
        Phân tích cấu trúc trường khí của số điện thoại hoặc biển số xe theo Bát Cực Linh Số.
      </p>
      <form className="ne-form" data-testid="input-form-region" onSubmit={handleSubmit} noValidate>
        <fieldset className="ne-type-fieldset">
          <legend className="ne-field-label">
            Loại số cần phân tích
            <span className="ne-required">Bắt buộc</span>
          </legend>
          <div className="ne-type-grid" role="radiogroup" aria-required="true" data-testid="analysis-type-group">
            {ANALYSIS_TYPE_OPTIONS.map((item) => {
              const selected = item.value === analysisType;
              return (
                <label
                  key={item.value}
                  className="ne-type-card"
                  data-selected={selected ? "true" : "false"}
                  data-testid={`analysis-type-${item.value}`}
                >
                  <input
                    type="radio"
                    name="analysis-type"
                    value={item.value}
                    checked={selected}
                    required
                    onChange={() => onAnalysisTypeChange(item.value)}
                  />
                  <span className="ne-type-card__title">{item.label}</span>
                  <span className="ne-type-card__copy">{item.support}</span>
                </label>
              );
            })}
          </div>
        </fieldset>

        <div className="ne-field">
          <label className="ne-field-label" htmlFor="number-energy-input">
            {option.fieldLabel}
            <span className="ne-required">Bắt buộc</span>
          </label>
          <input
            id="number-energy-input"
            className="ne-number-input"
            data-testid="number-input"
            value={inputValue}
            onChange={(event) => onInputChange(event.target.value)}
            placeholder={option.placeholder}
            required
            aria-required="true"
            aria-invalid={errorMessage ? "true" : "false"}
            aria-describedby={errorMessage ? `${helpId} ${errorId}` : helpId}
            autoComplete={analysisType === "phone_number" ? "tel" : "off"}
            inputMode={analysisType === "phone_number" ? "numeric" : "text"}
            spellCheck={false}
          />
          <p className="muted ne-field-help" id={helpId}>
            {option.help}
            {analysisType === "phone_number"
              ? " Với số điện thoại, hệ thống còn phân tích Tài vận, nguồn Tài, dòng Tài và hậu vận của dãy số."
              : null}
          </p>
          {errorMessage ? (
            <p className="ne-field-error" id={errorId} data-testid="input-error" role="alert">
              {errorMessage}
            </p>
          ) : null}
        </div>

        <div className="ne-form-actions">
          <button type="submit" data-testid="analysis-submit" disabled={isEmpty}>
            {option.cta}
          </button>
        </div>
      </form>
    </section>
  );
}
