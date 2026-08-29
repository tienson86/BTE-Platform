/**
 * Canonical 12-column dashboard body. UI-05: Overview + BaZi implemented.
 */

import type { ReactNode } from "react";
import { BaziCard } from "./BaziCard";
import { DASHBOARD_CARDS } from "./cards";
import { OverviewCard } from "./OverviewCard";
import { SkeletonCard } from "./SkeletonCard";
import type { BaziStructureView, OverviewView } from "./types";

type DashboardGridProps = {
  readonly overview?: OverviewView | null;
  readonly bazi?: BaziStructureView | null;
};

/**
 * Frozen card geometry in semantic source order.
 */
export function DashboardGrid({ overview = null, bazi = null }: DashboardGridProps): ReactNode {
  return (
    <section className="bte-cdash__grid" data-dashboard-body="canonical-grid">
      {DASHBOARD_CARDS.map((card) => {
        if (card.id === "overview" && overview) {
          return <OverviewCard key={card.id} card={card} model={overview} />;
        }
        if (card.id === "bazi" && bazi) {
          return <BaziCard key={card.id} card={card} model={bazi} />;
        }
        return <SkeletonCard key={card.id} card={card} />;
      })}
    </section>
  );
}
