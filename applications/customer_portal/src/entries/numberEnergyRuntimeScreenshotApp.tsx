/**
 * RB16 review-only harness. Mounts NumberEnergyPage with explicit runtimeMode.
 * Not used by public `/number-energy` (numberEnergyApp.tsx stays static).
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { NumberEnergyPage } from "../features/number_energy/NumberEnergyPage";

function mount(): void {
  const host = document.getElementById("number-energy-root");
  if (!host) {
    throw new Error("Missing #number-energy-root mount node.");
  }
  createRoot(host).render(
    <StrictMode>
      <NumberEnergyPage runtimeMode />
    </StrictMode>,
  );
}

mount();
