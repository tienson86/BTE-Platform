import { useEffect, useState, type ReactNode } from "react";

import { InputSection } from "./InputSection";
import { ResultSection } from "./ResultSection";
import {
  GOLDEN_PREVIEW_INPUT,
  GOLDEN_PREVIEW_TYPE,
  type AnalysisType,
  type GoldenPreviewState,
} from "./formModel";
import { useNumberEnergyRuntime } from "./runtimeController";

export const NUMBER_ENERGY_STATIC_PHASE = "sb16";
export const NUMBER_ENERGY_STATIC_UI_V1 = "NUMBER_ENERGY_STATIC_UI_V1";

export type NumberEnergyPageProps = {
  /** Explicit flag. Public `/number-energy` mounts this as true; component default stays false. */
  runtimeMode?: boolean;
};

export function NumberEnergyPage({ runtimeMode = false }: NumberEnergyPageProps = {}): ReactNode {
  const [analysisType, setAnalysisType] = useState<AnalysisType>(GOLDEN_PREVIEW_TYPE);
  const [inputValue, setInputValue] = useState(GOLDEN_PREVIEW_INPUT);
  const [errorMessage, setErrorMessage] = useState("");
  const [goldenPreview, setGoldenPreview] = useState<GoldenPreviewState | null>(null);
  const runtime = useNumberEnergyRuntime();

  function handleAnalysisTypeChange(nextType: AnalysisType): void {
    setAnalysisType(nextType);
    setInputValue("");
    setErrorMessage("");
    setGoldenPreview(null);
    if (runtimeMode) {
      runtime.reset();
    }
  }

  function handleRevealGoldenPreview(preview: GoldenPreviewState | null): void {
    setGoldenPreview(preview);
    if (!runtimeMode) {
      return;
    }
    if (!preview) {
      runtime.reset();
      return;
    }
    setErrorMessage("");
    void runtime.submit({
      purpose_context: preview.analysisType,
      input: preview.originalInput,
    });
  }

  const resultPreview =
    runtimeMode && runtime.status !== "success" ? null : goldenPreview;
  const runtimeView =
    runtimeMode && runtime.status === "success" ? runtime.view : null;
  const runtimeSlotSource =
    runtimeMode && runtime.status === "success" ? runtime.slotSource : null;

  useEffect(() => {
    if (!goldenPreview && !(runtimeMode && runtime.status === "success")) {
      return;
    }
    if (runtimeMode && runtime.status !== "success") {
      return;
    }
    const heading = document.querySelector<HTMLElement>("[data-testid='result-hero'] h2");
    heading?.focus();
  }, [goldenPreview, runtimeMode, runtime.status]);

  useEffect(() => {
    if (!runtimeMode || runtime.status !== "error" || !runtime.error) {
      return;
    }
    setErrorMessage(runtime.error.message);
    setGoldenPreview(null);
  }, [runtimeMode, runtime.status, runtime.error]);

  let statusText = "";
  if (runtimeMode && runtime.status === "loading") {
    statusText = "Đang phân tích dãy số…";
  } else if (resultPreview) {
    statusText = "Đã hiện kết quả minh họa.";
  }

  return (
    <div
      className="ds-page ne-page"
      data-screen="number-energy"
      data-testid="number-energy-page"
      data-static-phase={NUMBER_ENERGY_STATIC_PHASE}
      data-static-freeze={NUMBER_ENERGY_STATIC_UI_V1}
      data-runtime-mode={runtimeMode ? "on" : "off"}
    >
      <header className="ne-intro" data-testid="page-title-area">
        <p className="muted">Bát Cực Linh Số</p>
        <h1 data-testid="number-energy-title">Tư vấn năng lượng số</h1>
        <p className="muted">
          Phân tích cấu trúc trường khí của số điện thoại, biển số xe hoặc số định danh theo Bát Cực Linh Số.
        </p>
      </header>
      <p className="ne-sr-only" aria-live="polite" data-testid="form-status">
        {statusText}
      </p>
      <InputSection
        analysisType={analysisType}
        inputValue={inputValue}
        errorMessage={errorMessage}
        runtimeMode={runtimeMode}
        onAnalysisTypeChange={handleAnalysisTypeChange}
        onInputChange={(value) => {
          setInputValue(value);
          if (errorMessage) {
            setErrorMessage("");
          }
        }}
        onErrorMessageChange={setErrorMessage}
        onRevealGoldenPreview={handleRevealGoldenPreview}
      />
      <ResultSection
        goldenPreview={resultPreview}
        runtimeView={runtimeView}
        slotSource={runtimeSlotSource}
      />
    </div>
  );
}
