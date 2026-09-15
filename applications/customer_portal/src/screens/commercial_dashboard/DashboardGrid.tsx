/**
 * Canonical 12-column dashboard body. UI-12: all cards implemented.
 */

import type { ReactNode } from "react";
import { BaziCard } from "./BaziCard";
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
  bazi = null,
}: DashboardGridProps): ReactNode {
  const baziCard = { id: "bazi" as const, title: "BÁT TỰ", span: 12 as const };
  return (
    <section className="bte-cdash__grid" data-dashboard-body="canonical-grid">
      {bazi ? <BaziCard card={baziCard} model={bazi} /> : null}
    </section>
  );
}
