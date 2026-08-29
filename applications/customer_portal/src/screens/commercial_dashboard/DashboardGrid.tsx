/**
 * Canonical 12-column dashboard body. UI-07: through Ten Gods implemented.
 */

import type { ReactNode } from "react";
import { BaziCard } from "./BaziCard";
import { DASHBOARD_CARDS } from "./cards";
import { FiveElementsCard } from "./FiveElementsCard";
import { OverviewCard } from "./OverviewCard";
import { SkeletonCard } from "./SkeletonCard";
import { TenGodsCard } from "./TenGodsCard";
import type { BaziStructureView, FiveElementsView, OverviewView, TenGodsView } from "./types";

type DashboardGridProps = {
  readonly overview?: OverviewView | null;
  readonly bazi?: BaziStructureView | null;
  readonly fiveElements?: FiveElementsView | null;
  readonly tenGods?: TenGodsView | null;
};

/**
 * Frozen card geometry in semantic source order.
 */
export function DashboardGrid({
  overview = null,
  bazi = null,
  fiveElements = null,
  tenGods = null,
}: DashboardGridProps): ReactNode {
  return (
    <section className="bte-cdash__grid" data-dashboard-body="canonical-grid">
      {DASHBOARD_CARDS.map((card) => {
        if (card.id === "overview" && overview) {
          return <OverviewCard key={card.id} card={card} model={overview} />;
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
        return <SkeletonCard key={card.id} card={card} />;
      })}
    </section>
  );
}
