import type { ReactNode } from "react";
import {
  InformationBox,
  SectionHeader,
  StatusBadge,
} from "../shared";
import type {
  ExecutiveHeroViewModel,
  PresentationStatus,
} from "../../view_models/executive_summary";
import { cx } from "../../utils";
import { HeroActions } from "./HeroActions";
import { HeroBackground } from "./HeroBackground";
import { renderPresentationGate } from "./presentationGate";

export type ExecutiveHeroProps = {
  data: ExecutiveHeroViewModel;
  status?: PresentationStatus;
  actions?: ReactNode;
  className?: string;
};

/** Executive Hero — identity and overall verdict at a glance. */
export function ExecutiveHero({
  data,
  status = "ready",
  actions,
  className,
}: ExecutiveHeroProps) {
  const { identity, verdict } = data;
  const title = identity.chartTitle ?? identity.dayMasterLabel ?? identity.dayMaster;

  return (
    <section className={cx("cui-biz-hero", className)} aria-label={title}>
      {renderPresentationGate(
        status,
        {
          loadingTitle: "Loading executive hero",
          emptyTitle: "No identity available",
          unavailableTitle: "Hero unavailable",
          errorTitle: "Unable to load hero",
        },
        <HeroBackground>
          <SectionHeader
            title={title}
            subtitle={identity.subtitle ?? `Day Master · ${identity.dayMaster}`}
            level={2}
            actions={
              <StatusBadge status={verdict.tone ?? "info"}>{verdict.label}</StatusBadge>
            }
          />
          {verdict.summary ? (
            <InformationBox title="Overall Verdict">{verdict.summary}</InformationBox>
          ) : null}
          {actions ? <HeroActions>{actions}</HeroActions> : null}
        </HeroBackground>,
      )}
    </section>
  );
}
