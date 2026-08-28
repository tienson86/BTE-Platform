import type { ReactNode } from "react";

import { Card } from "../../../components/base/Card";
import { TuTruPanel } from "../../../components/canonical";
import { EMPTY_TU_TRU_PILLAR, WORKSPACE_PANELS } from "../layout";
import {
  BoneWeightPanel,
  ConclusionPanel,
  DestinyPanel,
  FiveElementsPanel,
  InterpretationPanel,
  LuckCyclesPanel,
  OverviewPanel,
  ShenShaPanel,
  TenGodsPanel,
} from "../panels";
import { PREVIEW_TU_TRU } from "../previewFixture";
import type { WorkspacePanelSpec } from "../types";

function panelBody(panel: WorkspacePanelSpec, preview: boolean): ReactNode {
  switch (panel.id) {
    case "tu-tru":
      return (
        <TuTruPanel
          year={preview ? PREVIEW_TU_TRU.year : EMPTY_TU_TRU_PILLAR}
          month={preview ? PREVIEW_TU_TRU.month : EMPTY_TU_TRU_PILLAR}
          day={preview ? PREVIEW_TU_TRU.day : EMPTY_TU_TRU_PILLAR}
          hour={preview ? PREVIEW_TU_TRU.hour : EMPTY_TU_TRU_PILLAR}
        />
      );
    case "overview":
      return <OverviewPanel preview={preview} />;
    case "five-elements":
      return <FiveElementsPanel preview={preview} />;
    case "ten-gods":
      return <TenGodsPanel preview={preview} />;
    case "destiny":
      return <DestinyPanel preview={preview} />;
    case "shen-sha":
      return <ShenShaPanel preview={preview} />;
    case "bone-weight":
      return <BoneWeightPanel preview={preview} />;
    case "luck-cycles":
      return <LuckCyclesPanel preview={preview} />;
    case "interpretation":
      return <InterpretationPanel preview={preview} />;
    case "conclusion":
      return <ConclusionPanel preview={preview} />;
    default:
      return null;
  }
}

/**
 * Canonical card cell on the frozen 10-column workspace grid.
 */
export function CanonicalWorkspaceCard({
  panel,
  preview = false,
}: {
  panel: WorkspacePanelSpec;
  preview?: boolean;
}): ReactNode {
  const index = WORKSPACE_PANELS.findIndex((item) => item.id === panel.id) + 1;
  const isTuTru = panel.id === "tu-tru";
  return (
    <article
      id={`panel-${panel.id}`}
      className={`bte-rw__cell bte-rw__cell--${panel.span}`}
      data-panel={panel.id}
      data-span={panel.span}
      data-row={panel.row}
      data-kind={panel.kind}
      data-index={String(index).padStart(2, "0")}
    >
      <Card
        className="bte-rw-card"
        title={
          <>
            <span className="bte-rw-card__index">{String(index).padStart(2, "0")}</span>
            {isTuTru ? null : panel.title}
          </>
        }
        data-canonical-card="true"
      >
        {panelBody(panel, preview)}
      </Card>
    </article>
  );
}
