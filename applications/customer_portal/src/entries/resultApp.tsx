/**
 * Production Result entry — mounts Canonical Desktop V2 on /result.
 *
 * Birth Input (/analyze) → ResultStore → this entry → PortalPage.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { PortalPage } from "../screens/canonical_desktop";
import { historyIdFromSearch } from "../resultState/currentResult";
import { resolveResultBoot, type StoredResult } from "./resultBoot";

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

function mount(): void {
  const host = document.getElementById("canonical-desktop-root");
  if (!host) {
    throw new Error("Missing #canonical-desktop-root mount node.");
  }

  const search = window.location.search;
  const stored = readStoredResult(search);
  const boot = resolveResultBoot(stored.current, search, stored.historyView);

  createRoot(host).render(
    <StrictMode>
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
    </StrictMode>,
  );
}

mount();
