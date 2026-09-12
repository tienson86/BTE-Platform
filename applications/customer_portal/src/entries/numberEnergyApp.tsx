/**
 * Customer Portal entry for Number Energy V1.
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
