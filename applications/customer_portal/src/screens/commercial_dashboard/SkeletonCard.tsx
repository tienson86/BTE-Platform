/**
 * Skeleton Card placeholder — title only, no analysis content.
 */

import type { ReactNode } from "react";
import type { DashboardCardSpec } from "./types";

type SkeletonCardProps = {
  readonly card: DashboardCardSpec;
};

/**
 * Structural placeholder for an unimplemented Commercial Dashboard card.
 */
export function SkeletonCard({ card }: SkeletonCardProps): ReactNode {
  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span}`}
      data-card={card.id}
      data-span={card.span}
      data-skeleton="true"
      aria-label={card.title}
    >
      <h2 className="bte-cdash__card-title">{card.title}</h2>
      <div className="bte-cdash__skel" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>
    </article>
  );
}
