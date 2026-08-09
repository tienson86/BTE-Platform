/**
 * Result Page V2 screenshot harness — PX-4.
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ResultPageV2 } from "../features/result_v2/pages/ResultPageV2";
import { resultV2ReadyReport } from "../../tests/js/result_v2_fixture";

const host = document.getElementById("root");
if (!host) {
  throw new Error("Missing #root");
}

createRoot(host).render(
  <StrictMode>
    <ResultPageV2 report={resultV2ReadyReport} />
  </StrictMode>,
);
