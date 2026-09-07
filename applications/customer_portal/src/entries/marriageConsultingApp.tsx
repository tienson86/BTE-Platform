/**
 * Customer Portal entry for TV-01 Marriage Consulting.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { MarriageConsultingPage } from "../features/marriage_consulting/MarriageConsultingPage";

function mount(): void {
  const host = document.getElementById("marriage-consulting-root");
  if (!host) {
    throw new Error("Missing #marriage-consulting-root mount node.");
  }
  createRoot(host).render(
    <StrictMode>
      <MarriageConsultingPage />
    </StrictMode>,
  );
}

mount();
