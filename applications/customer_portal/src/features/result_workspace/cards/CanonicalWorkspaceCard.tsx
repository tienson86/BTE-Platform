import type { ReactNode } from "react";

import { Card } from "../../../components/base/Card";
import { TuTruPanel } from "../../../components/canonical";
import type { BaziWorkspaceViewModel } from "../adapter/types";
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

function panelBody(
  panel: WorkspacePanelSpec,
  preview: boolean,
  viewModel?: BaziWorkspaceViewModel | null,
): ReactNode {
  const pillars = preview
    ? PREVIEW_TU_TRU
    : viewModel?.fourPillars ?? {
        year: EMPTY_TU_TRU_PILLAR,
        month: EMPTY_TU_TRU_PILLAR,
        day: EMPTY_TU_TRU_PILLAR,
        hour: EMPTY_TU_TRU_PILLAR,
      };
  switch (panel.id) {
    case "tu-tru":
      return (
        <TuTruPanel
          year={pillars.year}
          month={pillars.month}
          day={pillars.day}
          hour={pillars.hour}
        />
      );
    case "overview":
      return <OverviewPanel preview={preview} model={viewModel?.overview} />;
    case "five-elements":
      return <FiveElementsPanel preview={preview} model={viewModel?.fiveElements} />;
    case "ten-gods":
      return <TenGodsPanel preview={preview} model={viewModel?.tenGods} />;
    case "destiny":
      return <DestinyPanel preview={preview} model={viewModel?.pattern} />;
    case "shen-sha":
      return <ShenShaPanel preview={preview} model={viewModel?.shenSha} />;
    case "bone-weight":
      return <BoneWeightPanel preview={preview} model={viewModel?.boneWeight} />;
    case "luck-cycles":
      return <LuckCyclesPanel preview={preview} model={viewModel?.luck} />;
    case "interpretation":
      return <InterpretationPanel preview={preview} model={viewModel?.interpretation} />;
    case "conclusion":
      return <ConclusionPanel preview={preview} model={viewModel?.conclusion} />;
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
  viewModel,
}: {
  panel: WorkspacePanelSpec;
  preview?: boolean;
  viewModel?: BaziWorkspaceViewModel | null;
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
        {panelBody(panel, preview, viewModel)}
      </Card>
    </article>
  );
}
