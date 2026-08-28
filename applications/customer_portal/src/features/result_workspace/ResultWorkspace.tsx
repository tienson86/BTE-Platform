import { useEffect, type ReactNode } from "react";

import type { BaziWorkspaceViewModel } from "./adapter/types";
import { CanonicalWorkspaceCard } from "./cards/CanonicalWorkspaceCard";
import {
  WorkspaceHeader,
  WorkspaceSidebar,
  WorkspaceTopNav,
} from "./chrome/WorkspaceChrome";
import { WORKSPACE_GRID_COLUMNS, WORKSPACE_PANELS } from "./layout";

export type ResultWorkspaceProps = {
  /** Isolated visual fixture only. Never used for production current-result. */
  readonly preview?: boolean;
  /** Canonical presentation view model from BaziWorkspaceAdapter. */
  readonly viewModel?: BaziWorkspaceViewModel | null;
  /** True when there is no current structured analysis to display. */
  readonly noResult?: boolean;
};

/**
 * BaZi Result Workspace V2 — frozen grid + canonical panels.
 * Displays analytical truth from the view model. Does not calculate it.
 */
export function ResultWorkspace({
  preview = false,
  viewModel = null,
  noResult = false,
}: ResultWorkspaceProps = {}): ReactNode {
  useEffect(() => {
    const root = document.querySelector("[data-workspace='bazi-result-v2']");
    const toggle = root?.querySelector("[data-rw-toggle='sidebar']");
    if (!root || !toggle) return undefined;
    const onClick = () => {
      if (root.getAttribute("data-sidebar") === "open") {
        root.removeAttribute("data-sidebar");
      } else {
        root.setAttribute("data-sidebar", "open");
      }
    };
    toggle.addEventListener("click", onClick);
    return () => toggle.removeEventListener("click", onClick);
  }, []);

  const binding = preview ? "preview" : viewModel ? "canonical" : "none";
  return (
    <div
      className="bte-rw"
      data-workspace="bazi-result-v2"
      data-sprint="BZ-UI-01"
      data-panels="BZ-UI-02"
      data-binding={binding}
      data-grid={WORKSPACE_GRID_COLUMNS}
      data-preview={preview ? "fixture" : "off"}
      data-architecture="zones-rows-grid-cards"
      data-analysis-id={viewModel?.analysisId || ""}
    >
      <WorkspaceSidebar />
      <WorkspaceTopNav />
      <main className="bte-rw__main" id="rw-main" data-workspace-region="result">
        <WorkspaceHeader person={viewModel?.person} preview={preview} noResult={noResult && !preview} />
        <section
          className="bte-rw__grid"
          aria-label="Result Workspace"
          data-grid={WORKSPACE_GRID_COLUMNS}
        >
          {WORKSPACE_PANELS.map((panel) => (
            <CanonicalWorkspaceCard
              key={panel.id}
              panel={panel}
              preview={preview}
              viewModel={preview ? null : viewModel}
            />
          ))}
        </section>
      </main>
    </div>
  );
}
