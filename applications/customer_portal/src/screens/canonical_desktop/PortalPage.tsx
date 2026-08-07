/**
 * PortalPage / ResultPage — Desktop Dashboard (CANONICAL_PORTAL_UI_DESKTOP_V2).
 *
 * Data: AnalyzeService → canonicalDesktopAdapter → CanonicalDesktopProvider.
 * Layout frozen — see DESKTOP_V2_FREEZE.md.
 */

import type { ReactNode } from "react";
import type { CanonicalDesktopViewModel } from "../../adapters";
import { useCanonicalDesktopResult } from "../../hooks";
import type { AnalyzeChartRequest } from "../../models";
import { CanonicalDesktopProvider } from "./CanonicalDesktopContext";
import { PortalFooter, PortalHeader, PortalSidebar } from "./shell/PortalChrome";
import { Row01, Row02, Row03, Row04 } from "./rows";
import "../../styles/canonical-desktop.css";

export type PortalPageProps = {
  /** Birth request for POST /analyze. Omit to keep fixture preview. */
  readonly request?: AnalyzeChartRequest | null;
  /** Injected ViewModel (tests / story). */
  readonly initialData?: CanonicalDesktopViewModel;
  readonly enabled?: boolean;
};

/**
 * Canonical Desktop Dashboard — engine-backed when `request` is provided.
 */
export function PortalPage({
  request = null,
  initialData,
  enabled = true,
}: PortalPageProps = {}): ReactNode {
  const { viewModel } = useCanonicalDesktopResult({
    request,
    initialData,
    enabled,
    previewFallback: true,
  });

  const mode = viewModel.source === "api" ? "engine-live" : "dashboard-preview";

  return (
    <CanonicalDesktopProvider value={viewModel}>
      <div
        className="cd-root"
        data-canonical="desktop-v2"
        data-mode={mode}
        data-status={viewModel.status}
      >
        <PortalSidebar />
        <PortalHeader />
        <main className="cd-content" data-page="result">
          <div
            className="cd-result-page"
            data-architecture="independent-row-containers"
          >
            <Row01 />
            <Row02 />
            <Row03 />
            <Row04 />
          </div>
        </main>
        <PortalFooter />
      </div>
    </CanonicalDesktopProvider>
  );
}

/** Alias matching DESKTOP_COMPONENT_MAPPING naming. */
export const ResultPage = PortalPage;
