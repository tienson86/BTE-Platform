import { SectionDivider, SectionSurface } from "../shared";
import type { PillarViewModel } from "../../view_models/four_pillars";
import type { PresentationStatus } from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { EarthlyBranchCell } from "./EarthlyBranchCell";
import { HeavenlyStemCell } from "./HeavenlyStemCell";
import { HiddenStemGroup } from "./HiddenStemGroup";
import { LifeStagePanel } from "./LifeStagePanel";
import { NaYinPanel } from "./NaYinPanel";
import { PillarHeader } from "./PillarHeader";
import { renderPresentationGate } from "./presentationGate";

export type PillarColumnProps = {
  data: PillarViewModel;
  status?: PresentationStatus;
  className?: string;
};

/** Single pillar column — Year / Month / Day / Hour. */
export function PillarColumn({
  data,
  status = "ready",
  className,
}: PillarColumnProps) {
  return (
    <article
      className={cx("cui-biz-pillar-column", className)}
      data-pillar={data.kind}
      data-day-master={data.isDayMaster ? "true" : undefined}
      aria-label={data.isDayMaster ? `${data.title} (Day Master)` : data.title}
      tabIndex={0}
    >
      {renderPresentationGate(
        status,
        {
          loadingTitle: `Loading ${data.title}`,
          emptyTitle: `${data.title} unavailable`,
          unavailableTitle: `${data.title} unavailable`,
          errorTitle: `Unable to load ${data.title}`,
        },
        <SectionSurface gap="list" variant={data.isDayMaster ? "section" : "paper"}>
          <PillarHeader
            title={data.title}
            isDayMaster={data.isDayMaster}
            tenGodLabels={data.tenGodLabels}
          />
          <SectionDivider />
          <HeavenlyStemCell data={data.stem} />
          <EarthlyBranchCell data={data.branch} />
          <HiddenStemGroup items={data.hiddenStems} />
          <NaYinPanel value={data.naYin} />
          <LifeStagePanel value={data.lifeStage} />
        </SectionSurface>,
      )}
    </article>
  );
}
