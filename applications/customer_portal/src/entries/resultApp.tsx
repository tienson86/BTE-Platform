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
import { NarrativeV2ShadowPage } from "../screens/narrative_v2_shadow";
import { historyIdFromSearch } from "../resultState/currentResult";
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

function readStoredResult(search: string): {
  current: StoredResult | null;
  historyView: StoredResult | null;
} {
  const store = window.BtePortal?.ResultStore;
  const historyId = historyIdFromSearch(search);
  const fromHistory = Boolean(historyId);
  if (store?.resolveForDisplay) {
    const resolved = store.resolveForDisplay(fromHistory, historyId);
    return {
      current: fromHistory ? store.loadCurrent?.() ?? store.load?.() ?? null : resolved,
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

function mount(): void {
  const host = document.getElementById("canonical-desktop-root");
  if (!host) {
    throw new Error("Missing #canonical-desktop-root mount node.");
  }

  const search = window.location.search;
  const stored = readStoredResult(search);
  const boot = resolveResultBoot(stored.current, search, stored.historyView);
  const commercial = isCanonicalResultPath(window.location.pathname);
  const surface = resolveResultSurface(search, window.location.pathname);

  createRoot(host).render(
    <StrictMode>
      {commercial && surface !== "production" ? (
        <NarrativeV2ShadowPage analysis={boot.analysis} mode={surface} />
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
