/**
 * Production Result entry — mounts Commercial Dashboard on /result.
 * PortalPage remains the isolated Result architecture host for regression
 * routes such as /interpretation.
 *
 * Birth Input (/analyze) → ResultStore → this entry → CommercialDashboardPage.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { PortalPage } from "../screens/canonical_desktop";
import { CommercialDashboardPage } from "../screens/commercial_dashboard";
import { ExecutiveReportPage } from "../screens/executive_report";
import { NarrativeV2ShadowPage } from "../screens/narrative_v2_shadow";
import { historyIdFromSearch } from "../resultState/currentResult";
import { resolveNarrativeProvider } from "../resultState/narrativeProvider";
import { resolveResultSurface } from "../resultState/narrativeV2Shadow";
import { resolveResultBoot, toAnalyzeRequest, type StoredResult } from "./resultBoot";

declare global {
  interface Window {
    BtePortal?: {
      ResultStore?: {
        load: () => StoredResult | null;
        loadCurrent?: () => StoredResult | null;
        peekView?: () => StoredResult | null;
        loadForView: () => StoredResult | null;
        resolveForDisplay?: (fromHistory: boolean, expectedId?: string | null) => StoredResult | null;
      };
    };
  }
}

function readStoredResult(
  search: string,
  pathname: string,
): {
  current: StoredResult | null;
  historyView: StoredResult | null;
} {
  const store = window.BtePortal?.ResultStore;
  const historyId = historyIdFromSearch(search);
  const fromHistory = Boolean(historyId);
  const surface = resolveResultSurface(search, pathname);
  if (store?.resolveForDisplay) {
    const resolved = store.resolveForDisplay(fromHistory, historyId);
    const productionCurrent = fromHistory
      ? store.loadCurrent?.() ?? store.load?.() ?? null
      : resolved;
    // Shadow review may inspect stored Presentation even when the production
    // calendar gate withholds loadCurrent.
    const current =
      productionCurrent ??
      (surface !== "production" ? store.load?.() ?? null : null);
    return {
      current,
      historyView: fromHistory ? resolved : null,
    };
  }
  return {
    current: store?.loadCurrent?.() ?? store?.load?.() ?? null,
    historyView: null,
  };
}

function isCanonicalResultPath(pathname: string): boolean {
  return pathname === "/result" || pathname === "/result/";
}

function isReportPreviewPath(pathname: string): boolean {
  return pathname === "/report-preview" || pathname === "/report-preview/";
}

function mount(): void {
  const host = document.getElementById("canonical-desktop-root");
  if (!host) {
    throw new Error("Missing #canonical-desktop-root mount node.");
  }

  const search = window.location.search;
  const stored = readStoredResult(search, window.location.pathname);
  const boot = resolveResultBoot(stored.current, search, stored.historyView);
  const commercial = isCanonicalResultPath(window.location.pathname);
  const reportPreview = isReportPreviewPath(window.location.pathname);
  const surface = resolveResultSurface(search, window.location.pathname);

  createRoot(host).render(
    <StrictMode>
      {reportPreview ? (
        <ExecutiveReportPage
          analysis={boot.analysis ?? stored.current?.data ?? null}
          request={boot.request ?? toAnalyzeRequest(stored.current?.input ?? null)}
        />
      ) : commercial && surface !== "production" ? (
        <NarrativeV2ShadowPage
          analysis={boot.analysis ?? stored.current?.data ?? null}
          mode={surface}
        />
      ) : commercial ? (
        <CommercialDashboardPage
          analysis={boot.analysis}
          request={boot.request ?? toAnalyzeRequest(stored.current?.input ?? null)}
          initialData={boot.initialData}
          analysisId={boot.analysisId}
          resultSource={boot.resultSource}
          reanalyzeHref={boot.reanalyzeHref}
          layoutMode={boot.layoutMode}
          previewFallback={boot.previewFallback}
          narrativeProvider={resolveNarrativeProvider(search)}
        />
      ) : (
        <PortalPage
          request={boot.request}
          initialData={boot.initialData}
          enabled
          previewFallback={boot.previewFallback}
          fullReport={boot.fullReport}
          analysisId={boot.analysisId}
          resultSource={boot.resultSource}
          exportPayload={boot.exportPayload}
          reanalyzeHref={boot.reanalyzeHref}
        />
      )}
    </StrictMode>,
  );
}

mount();
