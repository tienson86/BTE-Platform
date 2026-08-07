/**
 * Result Page screenshot harness — mounts PortalPage with mock preview.
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { PortalPage } from "../screens/canonical_desktop";

const host = document.getElementById("root");
if (!host) {
  throw new Error("Missing #root");
}

createRoot(host).render(
  <StrictMode>
    <PortalPage previewFallback enabled />
  </StrictMode>,
);
