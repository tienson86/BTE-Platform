import type { ReactNode } from "react";

import { CanonicalWorkspaceCard } from "./cards/CanonicalWorkspaceCard";
import {
  WorkspaceHeader,
  WorkspaceSidebar,
  WorkspaceTopNav,
} from "./chrome/WorkspaceChrome";
import { WORKSPACE_GRID_COLUMNS, WORKSPACE_PANELS } from "./layout";

export type ResultWorkspaceProps = {
  /** Isolated visual fixture only. Production stays empty until BZ-UI-03. */
  readonly preview?: boolean;
};

/**
 * BaZi Result Workspace V2 — frozen grid + canonical panel shells.
 * Presentation only. Does not bind engine, API, or stored analysis payload.
 */
export function ResultWorkspace({ preview = false }: ResultWorkspaceProps = {}): ReactNode {
  return (
    <div
      className="bte-rw"
      data-workspace="bazi-result-v2"
      data-sprint="BZ-UI-01"
      data-panels="BZ-UI-02"
      data-grid={WORKSPACE_GRID_COLUMNS}
      data-binding="none"
      data-preview={preview ? "fixture" : "off"}
      data-architecture="zones-rows-grid-cards"
    >
      <WorkspaceSidebar />
      <WorkspaceTopNav />
      <main className="bte-rw__main" id="rw-main" data-workspace-region="result">
        <WorkspaceHeader />
        <section
          className="bte-rw__grid"
          aria-label="Result Workspace"
          data-grid={WORKSPACE_GRID_COLUMNS}
        >
          {WORKSPACE_PANELS.map((panel) => (
            <CanonicalWorkspaceCard key={panel.id} panel={panel} preview={preview} />
          ))}
        </section>
      </main>
    </div>
  );
}
