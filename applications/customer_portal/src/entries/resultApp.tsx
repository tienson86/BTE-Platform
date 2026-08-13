/**
 * Production Result entry — mounts Canonical Desktop V2 on /result.
 *
 * Birth Input (/analyze) → ResultStore → this entry → PortalPage.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { PortalPage } from "../screens/canonical_desktop";
import { isHistoryViewSearch } from "../resultState/currentResult";
import { resolveResultBoot, type StoredResult } from "./resultBoot";

declare global {
  interface Window {
    BtePortal?: {
      ResultStore?: {
        load: () => StoredResult | null;
        loadCurrent?: () => StoredResult | null;
        peekView?: () => StoredResult | null;
        loadForView: () => StoredResult | null;
        resolveForDisplay?: (fromHistory: boolean) => StoredResult | null;
      };
    };
  }
}

function readStoredResult(search: string): {
  current: StoredResult | null;
  historyView: StoredResult | null;
} {
  const store = window.BtePortal?.ResultStore;
  const fromHistory = isHistoryViewSearch(search);
  if (store?.resolveForDisplay) {
    const resolved = store.resolveForDisplay(fromHistory);
    return {
      current: fromHistory ? store.loadCurrent?.() ?? store.load?.() ?? null : resolved,
      historyView: fromHistory ? resolved : store.peekView?.() ?? null,
    };
  }
  return {
    current: store?.loadCurrent?.() ?? store?.load?.() ?? null,
    historyView: store?.peekView?.() ?? store?.loadForView?.() ?? null,
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
      />
    </StrictMode>,
  );
}

mount();
