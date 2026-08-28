/**
 * Production Result Workspace entry — mounts BaZi Result Workspace V2.
 *
 * Analyze → ResultStore current → this entry → ResultWorkspace.
 * Does not rerun analysis. Preview fixture only when ?preview=1.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ResultWorkspace } from "../features/result_workspace";
import { historyIdFromSearch } from "../resultState/currentResult";
import { resolveWorkspaceBoot, type StoredResult } from "./workspaceBoot";

declare global {
  interface Window {
    BtePortal?: {
      ResultStore?: {
        load: () => StoredResult | null;
        loadCurrent?: () => StoredResult | null;
        peekView?: () => StoredResult | null;
        loadForView: () => StoredResult | null;
        resolveForDisplay?: (
          fromHistory: boolean,
          expectedId?: string | null,
        ) => StoredResult | null;
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
  const host = document.getElementById("result-workspace-root");
  if (!host) {
    throw new Error("Missing #result-workspace-root mount node.");
  }

  const search = window.location.search;
  const stored = readStoredResult(search);
  const boot = resolveWorkspaceBoot(stored.current, search, stored.historyView);

  createRoot(host).render(
    <StrictMode>
      <ResultWorkspace
        preview={boot.preview}
        viewModel={boot.viewModel}
        noResult={boot.noResult}
      />
    </StrictMode>,
  );
}

mount();
