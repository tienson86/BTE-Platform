import { useState, type ReactNode } from "react";

import { InputSection } from "./InputSection";
import { ResultSection } from "./ResultSection";
import {
  GOLDEN_PREVIEW_INPUT,
  GOLDEN_PREVIEW_TYPE,
  type AnalysisType,
  type GoldenPreviewState,
} from "./formModel";

export function NumberEnergyPage(): ReactNode {
  const [analysisType, setAnalysisType] = useState<AnalysisType>(GOLDEN_PREVIEW_TYPE);
  const [inputValue, setInputValue] = useState(GOLDEN_PREVIEW_INPUT);
  const [errorMessage, setErrorMessage] = useState("");
  const [goldenPreview, setGoldenPreview] = useState<GoldenPreviewState | null>(null);

  function handleAnalysisTypeChange(nextType: AnalysisType): void {
    setAnalysisType(nextType);
    setInputValue("");
    setErrorMessage("");
  }

  return (
    <div
      className="ds-page ne-page"
      data-screen="number-energy"
      data-testid="number-energy-page"
      data-static-phase="sb04"
    >
      <header className="ne-intro" data-testid="page-title-area">
        <p className="muted">Bát Cực Linh Số</p>
        <h1 data-testid="number-energy-title">Tư vấn năng lượng số</h1>
        <p className="muted">
          Phân tích cấu trúc trường khí của số điện thoại hoặc biển số xe theo Bát Cực Linh Số.
        </p>
      </header>
      <InputSection
        analysisType={analysisType}
        inputValue={inputValue}
        errorMessage={errorMessage}
        onAnalysisTypeChange={handleAnalysisTypeChange}
        onInputChange={(value) => {
          setInputValue(value);
          if (errorMessage) {
            setErrorMessage("");
          }
        }}
        onErrorMessageChange={setErrorMessage}
        onRevealGoldenPreview={setGoldenPreview}
      />
      <ResultSection goldenPreview={goldenPreview} />
    </div>
  );
}
