import { CommercialRail, type ReportMode } from "../components/CommercialRail";
import { ResultPageV2 } from "../../result_v2/pages/ResultPageV2";
import { PvError } from "../components/states";
import { portalDemoReport } from "../fixtures/demoReport";
import { adaptLiveAnalysisResult } from "../liveAnalysisResultAdapter";
import type { AnalysisDataDto } from "../../../models";
import type { CanonicalReportInput } from "../../result_v2/adapter/reportInput";

export type ResultViewerPageProps = {
  mode?: ReportMode;
  saved?: boolean;
  /** Real analysis identifier from POST /api/v1/analyze (LAUNCH-02). */
  analysisId?: string | null;
  /** Raw analyze payload retained for Result V2 mapping (LAUNCH-03). */
  analysisResult?: AnalysisDataDto | null;
  onSave?: () => void;
  onPdf?: () => void;
  onPrint?: () => void;
  onShare?: () => void;
  onKnowledge?: () => void;
  onPremium?: () => void;
};

type LiveViewModel =
  | { kind: "demo"; report: CanonicalReportInput }
  | { kind: "api"; report: CanonicalReportInput }
  | { kind: "error"; error_code: string; error_message: string };

function resolveViewModel(
  analysisId: string | null,
  analysisResult: AnalysisDataDto | null,
): LiveViewModel {
  const hasLiveAnalysis = Boolean(analysisId);
  if (!hasLiveAnalysis) {
    return { kind: "demo", report: portalDemoReport };
  }

  const mapped = adaptLiveAnalysisResult(analysisResult, {
    analysis_id: analysisId,
  });
  if (!mapped.ok) {
    return {
      kind: "error",
      error_code: mapped.error_code,
      error_message: mapped.error_message,
    };
  }
  return { kind: "api", report: mapped.report };
}

/**
 * Result viewer shell.
 * Live sessions map analysisResult → CanonicalReportInput → Result V2.
 * Demo report remains only for preview routes without a live analysis id.
 */
export default function ResultViewerPage({
  mode = "reading",
  saved = false,
  analysisId = null,
  analysisResult = null,
  onSave,
  onPdf,
  onPrint,
  onShare,
  onKnowledge,
  onPremium,
}: ResultViewerPageProps) {
  const view = resolveViewModel(analysisId, analysisResult ?? null);
  const hasLiveAnalysis = Boolean(analysisId);

  return (
    <div
      className="pv-result-viewer"
      data-report-mode={mode}
      data-analysis-id={analysisId ?? undefined}
      data-analysis-source={hasLiveAnalysis ? "api" : "demo"}
      data-has-analysis-result={analysisResult ? "true" : "false"}
      data-result-map={view.kind}
    >
      {view.kind === "error" ? (
        <PvError
          title="Không thể hiển thị kết quả"
          body={view.error_message}
        />
      ) : (
        <ResultPageV2 report={view.report} />
      )}
      <CommercialRail
        saved={saved}
        onSave={() => onSave?.()}
        onPdf={() => onPdf?.()}
        onPrint={() => onPrint?.()}
        onShare={() => onShare?.()}
        onKnowledge={() => onKnowledge?.()}
        onPremium={() => onPremium?.()}
      />
    </div>
  );
}
