/**
 * Canonical 12-column dashboard body. UI-12: all cards implemented.
 */

import type { ReactNode } from "react";
import { BaziCard } from "./BaziCard";
import { DASHBOARD_CARDS } from "./cards";
import { FiveElementsCard } from "./FiveElementsCard";
import { ActionPlanCard } from "./ActionPlanCard";
import { InterpretationCard } from "./InterpretationCard";
import { LuckCard } from "./LuckCard";
import { OverviewCard } from "./OverviewCard";
import { PatternCard } from "./PatternCard";
import { ShenShaCard } from "./ShenShaCard";
import { SkeletonCard } from "./SkeletonCard";
import { TenGodsCard } from "./TenGodsCard";
import { LifeConsultingSection } from "./LifeConsultingSection";
import type {
  ActionPlanView,
  BaziStructureView,
  FiveElementsView,
  InterpretationView,
  LifeConsultingView,
  LuckView,
  OverviewView,
  PatternView,
  ShenShaView,
  TenGodsView,
} from "./types";

type DashboardGridProps = {
  readonly overview?: OverviewView | null;
  readonly bazi?: BaziStructureView | null;
  readonly fiveElements?: FiveElementsView | null;
  readonly tenGods?: TenGodsView | null;
  readonly pattern?: PatternView | null;
  readonly shenSha?: ShenShaView | null;
  readonly luck?: LuckView | null;
  readonly interpretation?: InterpretationView | null;
  readonly actionPlan?: ActionPlanView | null;
  readonly lifeConsulting?: LifeConsultingView | null;
};

/**
 * Frozen card geometry in semantic source order.
 */
export function DashboardGrid({
  overview = null,
  bazi = null,
  fiveElements = null,
  tenGods = null,
  pattern = null,
  shenSha = null,
  luck = null,
  interpretation = null,
  actionPlan = null,
  lifeConsulting = null,
}: DashboardGridProps): ReactNode {
  return (
    <section className="bte-cdash__grid" data-dashboard-body="canonical-grid">
      {DASHBOARD_CARDS.map((card) => {
        if (card.id === "overview" && overview) {
          return (
            <OverviewCard
              key={card.id}
              card={card}
              model={overview}
              priorityTitle={actionPlan?.priority?.title ?? ""}
            />
          );
        }
        if (card.id === "bazi" && bazi) {
          return <BaziCard key={card.id} card={card} model={bazi} />;
        }
        if (card.id === "five-elements" && fiveElements) {
          return <FiveElementsCard key={card.id} card={card} model={fiveElements} />;
        }
        if (card.id === "ten-gods" && tenGods) {
          return <TenGodsCard key={card.id} card={card} model={tenGods} />;
        }
        if (card.id === "pattern" && pattern) {
          return <PatternCard key={card.id} card={card} model={pattern} />;
        }
        if (card.id === "shensha" && shenSha) {
          return <ShenShaCard key={card.id} card={card} model={shenSha} />;
        }
        if (card.id === "luck" && luck) {
          return <LuckCard key={card.id} card={card} model={luck} />;
        }
        if (card.id === "interpretation" && interpretation) {
          return <InterpretationCard key={card.id} card={card} model={interpretation} />;
        }
        if (card.id === "action-plan" && actionPlan) {
          return <ActionPlanCard key={card.id} card={card} model={actionPlan} />;
        }
        return <SkeletonCard key={card.id} card={card} />;
      })}
      {lifeConsulting ? <LifeConsultingSection model={lifeConsulting} /> : null}
    </section>
  );
}
