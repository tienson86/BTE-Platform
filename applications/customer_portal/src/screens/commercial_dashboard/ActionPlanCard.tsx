/**
 * Action Plan Card — KẾ HOẠCH HÀNH ĐỘNG. Published actions only.
 */

import { useState, type ReactNode } from "react";
import { ACTION_PLAN_LABELS } from "./cards";
import type { ActionItemView, ActionPlanView, DashboardCardSpec } from "./types";
import { visualCardDom } from "./visualHierarchy";

type ActionPlanCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: ActionPlanView;
};

type ActionMarker = "priority" | "action" | "warning" | "watch";

function Item({
  item,
  marker,
}: {
  readonly item: ActionItemView;
  readonly marker: ActionMarker;
}): ReactNode {
  return (
    <li className="bte-ap__item" data-ap-source={item.source}>
      <span className={`bte-ap__marker bte-ap__marker--${marker}`} aria-hidden="true" />
      <div className="bte-ap__copy">
        {item.domain ? <p className="bte-ap__domain">{item.domain}</p> : null}
        <p className="bte-ap__item-title">{item.title}</p>
        {item.detail ? <p className="bte-ap__item-detail">{item.detail}</p> : null}
      </div>
    </li>
  );
}

/**
 * Closing decision card. Renders adapter-prepared actions only.
 */
export function ActionPlanCard({ card, model }: ActionPlanCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const canExpand = model.extraActions.length > 0;
  const actions = expanded ? [...model.actions, ...model.extraActions] : model.actions;

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-ap`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="action-plan"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
    >
      <header className="bte-ap__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {canExpand ? (
          <button
            type="button"
            className="bte-ap__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem đầy đủ kế hoạch"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-ap__empty" data-ap-empty="true">
          {model.emptyMessage}
        </p>
      ) : (
        <>
          {model.priority ? (
            <section className="bte-ap__priority" data-ap-section="priority">
              <h3 className="bte-ap__heading">{ACTION_PLAN_LABELS.priority}</h3>
              <ul className="bte-ap__list bte-ap__list--priority">
                <Item item={model.priority} marker="priority" />
              </ul>
            </section>
          ) : null}
          {actions.length ? (
            <section className="bte-ap__actions" data-ap-section="actions">
              <h3 className="bte-ap__heading">{ACTION_PLAN_LABELS.actions}</h3>
              <ul className="bte-ap__list bte-ap__list--tiles">
                {actions.map((item) => (
                  <Item key={`${item.source}-${item.title}`} item={item} marker="action" />
                ))}
              </ul>
            </section>
          ) : null}
          {model.warnings.length ? (
            <section className="bte-ap__warnings" data-ap-section="warnings">
              <h3 className="bte-ap__heading">{ACTION_PLAN_LABELS.warnings}</h3>
              <ul className="bte-ap__list">
                {model.warnings.map((item) => (
                  <Item key={`${item.source}-${item.title}`} item={item} marker="warning" />
                ))}
              </ul>
            </section>
          ) : null}
          {model.watch.length ? (
            <section className="bte-ap__watch" data-ap-section="watch">
              <h3 className="bte-ap__heading">{ACTION_PLAN_LABELS.watch}</h3>
              <ul className="bte-ap__list">
                {model.watch.map((item) => (
                  <Item key={`${item.source}-${item.title}`} item={item} marker="watch" />
                ))}
              </ul>
            </section>
          ) : null}
        </>
      )}
    </article>
  );
}
