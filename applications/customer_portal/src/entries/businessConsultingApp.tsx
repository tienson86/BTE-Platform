import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { BusinessConsultingPage } from "../features/business_consulting/BusinessConsultingPage";

function mount(): void {
  const host = document.getElementById("business-consulting-root");
  if (!host) {
    throw new Error("Missing #business-consulting-root mount node.");
  }
  createRoot(host).render(
    <StrictMode>
      <BusinessConsultingPage />
    </StrictMode>,
  );
}

mount();
