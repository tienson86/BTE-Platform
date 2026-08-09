import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { PortalApp } from "../features/portal/PortalApp";

const host = document.getElementById("root");
if (!host) {
  throw new Error("Missing #root");
}

createRoot(host).render(
  <StrictMode>
    <PortalApp />
  </StrictMode>,
);
