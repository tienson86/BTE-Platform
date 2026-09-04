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

function ExecutiveFacts({
  items,
}: {
  readonly items: readonly OverviewEvidenceView[];
}): ReactNode {
  if (!items.length) return null;
  return (
    <div className="bte-ov__facts" data-overview-section="facts">
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
 * Hero Overview card: executive facts → narrative. No new copy.
 */
export function OverviewCard({ card, model, priorityTitle = "" }: OverviewCardProps): ReactNode {
  const facts = [...model.identity, ...model.balance];
  const empty =
    !model.insight &&
    !model.summary &&
    !model.conclusion &&
    !facts.length;
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
      <ExecutiveFacts items={facts} />
      {model.insight ? (
        <p className="bte-ov__insight" data-overview-section="insight" data-motion-reveal="insight">
          {model.insight}
        </p>
      ) : null}
      {model.summary ? (
        <p className="bte-ov__summary" data-overview-section="summary">
          {model.summary}
        </p>
      ) : null}
      {model.conclusion ? (
        <p className="bte-ov__conclusion" data-overview-section="conclusion">
          {model.conclusion}
        </p>
      ) : null}
      {topPriority ? (
        <p className="bte-ov__priority" data-overview-section="top-priority" data-motion-reveal="priority">
          <span className="bte-cdash__badge bte-cdash__badge--accent">Ưu tiên</span>
          <span className="bte-ov__priority-title">{topPriority}</span>
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
