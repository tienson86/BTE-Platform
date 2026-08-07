/**
 * Production Result entry — mounts Canonical Desktop V2 on /result.
 *
 * Birth Input (/analyze) → ResultStore → this entry → PortalPage.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { PortalPage } from "../screens/canonical_desktop";
import { resolveResultBoot, type StoredResult } from "./resultBoot";

declare global {
  interface Window {
    BtePortal?: {
      ResultStore?: {
        loadForView: () => StoredResult | null;
      };
    };
  }
}

function mount(): void {
  const host = document.getElementById("canonical-desktop-root");
  if (!host) {
    throw new Error("Missing #canonical-desktop-root mount node.");
  }

  const stored = window.BtePortal?.ResultStore?.loadForView?.() ?? null;
  const boot = resolveResultBoot(stored, window.location.search);

  createRoot(host).render(
    <StrictMode>
      <PortalPage
        request={boot.request}
        initialData={boot.initialData}
        enabled
        previewFallback={boot.previewFallback}
      />
    </StrictMode>,
  );
}

mount();
