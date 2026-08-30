/**
 * Overview Card — TỔNG QUAN LÁ SỐ. Presentation only.
 */

import type { ReactNode } from "react";
import type { DashboardCardSpec, OverviewEvidenceView, OverviewView } from "./types";
import { visualCardDom } from "./visualHierarchy";
import { mobileCardDom } from "./mobile/mobileOrder";

type OverviewCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: OverviewView;
  readonly priorityTitle?: string;
};

function EvidenceGroup({
  region,
  items,
}: {
  readonly region: "identity" | "balance";
  readonly items: readonly OverviewEvidenceView[];
}): ReactNode {
  if (!items.length) return null;
  return (
    <div className="bte-ov__group" data-overview-section={region}>
      {items.map((item) => (
        <div key={item.key} className="bte-ov__badge" data-evidence={item.key}>
          <span className="bte-ov__badge-label">{item.label}</span>
          <span className="bte-ov__badge-value">{item.value}</span>
        </div>
      ))}
    </div>
  );
}

/**
 * Hero Overview card: Top Priority → Insight → identity → balance → quick conclusion.
 */
export function OverviewCard({ card, model, priorityTitle = "" }: OverviewCardProps): ReactNode {
  const empty = !model.insight && !model.conclusion && !model.identity.length && !model.balance.length;
  const topPriority = priorityTitle.trim();
  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-ov`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="overview"
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...mobileCardDom(card.id)}
    >
      <header className="bte-ov__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {model.subtitle ? <p className="bte-ov__subtitle">{model.subtitle}</p> : null}
      </header>
      {topPriority ? (
        <p className="bte-ov__priority" data-overview-section="top-priority">
          <span className="bte-cdash__badge bte-cdash__badge--accent">Ưu tiên</span>
          <span className="bte-ov__priority-title">{topPriority}</span>
        </p>
      ) : null}
      {model.insight ? (
        <p className="bte-ov__insight" data-overview-section="insight">
          {model.insight}
        </p>
      ) : null}
      <EvidenceGroup region="identity" items={model.identity} />
      <EvidenceGroup region="balance" items={model.balance} />
      {model.conclusion ? (
        <p className="bte-ov__conclusion" data-overview-section="conclusion">
          {model.conclusion}
        </p>
      ) : null}
      {empty ? (
        <p className="bte-ov__empty" data-overview-empty="true">
          Chưa đủ dữ liệu
        </p>
      ) : null}
    </article>
  );
}
