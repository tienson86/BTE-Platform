/**
 * PortalPage / ResultPage — BTE Result Page (Design System V1.0).
 *
 * Architecture (PACK_06 / PACK_07) — FROZEN:
 *   ResultPage → Zones → Rows → Grid → Cards → ViewModels → Presentation Adapter
 *
 * Sprint C: quality, responsive, accessibility, performance (Phases 09–13).
 * Data: AnalyzeService → canonicalDesktopAdapter → resultPresentationAdapter.
 */

import { useMemo, type ReactNode } from "react";
import type { CanonicalDesktopViewModel } from "../../adapters";
import type { FullReportViewModel } from "../../report/fullReportViewModel";
import { useCanonicalDesktopResult } from "../../hooks";
import type { AnalyzeChartRequest } from "../../models";
import { CanonicalDesktopProvider } from "./CanonicalDesktopContext";
import { PortalFooter, PortalHeader, PortalSidebar } from "./shell/PortalChrome";
import {
  ResultPageBody,
  ResultPageProvider,
  ResultPageStatusGate,
  adaptResultPageViewModel,
} from "../result";
import type { CustomerExportPayload } from "../../export/customerExport";
import { ResultExportBar } from "../result/ResultExportBar";
import "../../styles/canonical-desktop.css";
import "../../styles/presentation.css";
import "../../styles/result-page.css";
import "../../styles/result-page-visual-v2.css";

export type PortalPageProps = {
  /** Birth request for POST /analyze. Omit to keep fixture preview. */
  readonly request?: AnalyzeChartRequest | null;
  /** Injected ViewModel (tests / ResultStore-adapted engine payload). */
  readonly initialData?: CanonicalDesktopViewModel;
  readonly enabled?: boolean;
  /**
   * When no request/initialData: use fixture (preview) vs empty gate.
   * Production host passes false when expecting engine data.
   */
  readonly previewFallback?: boolean;
  readonly fullReport?: FullReportViewModel | null;
  readonly analysisId?: string | null;
  readonly resultSource?: "current" | "history" | "empty" | "preview" | "contract";
  readonly exportPayload?: CustomerExportPayload | null;
};

/**
 * Result Page host — shell + zone architecture (no direct cards).
 */
export function PortalPage({
  request = null,
  initialData,
  enabled = true,
  previewFallback = false,
  fullReport = null,
  analysisId = null,
  resultSource = "current",
  exportPayload = null,
}: PortalPageProps = {}): ReactNode {
  const { viewModel } = useCanonicalDesktopResult({
    request,
    initialData,
    enabled,
    previewFallback,
  });

  const resultModel = useMemo(
    () => adaptResultPageViewModel(viewModel, fullReport),
    [viewModel, fullReport],
  );

  const boundAnalysisId = fullReport?.analysisId || analysisId || resultModel.analysisId || "";
  const mode =
    viewModel.status !== "ready"
      ? viewModel.status
      : viewModel.source === "api"
        ? "engine-live"
        : "dashboard-preview";

  return (
    <CanonicalDesktopProvider value={viewModel}>
      <ResultPageProvider value={resultModel}>
        <div
          className="cd-root"
          data-canonical="desktop-v2"
          data-result-architecture="pack07"
          data-presentation="pack04"
          data-mode={mode}
          data-status={viewModel.status}
          data-analysis-id={boundAnalysisId}
          data-result-source={resultSource}
          data-sprint="D"
        >
          <PortalSidebar />
          <PortalHeader />
          <main className="cd-content" data-page="result" id="rp-main">
            {resultSource === "history" && viewModel.status === "ready" ? (
              <p className="rp-history-banner" role="status">
                Đang xem kết quả đã lưu. Kết quả phân tích hiện tại không đổi.
              </p>
            ) : null}
            {viewModel.status !== "ready" ? (
              <ResultPageStatusGate
                status={viewModel.status}
                message={viewModel.statusMessage}
              />
            ) : (
              <>
                <ResultPageBody />
                <ResultExportBar payload={exportPayload} />
              </>
            )}
          </main>
          <PortalFooter />
        </div>
      </ResultPageProvider>
    </CanonicalDesktopProvider>
  );
}

/** Official Result Page alias (PACK_07). */
export const ResultPage = PortalPage;
