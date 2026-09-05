/**
 * Action Plan Card — KẾ HOẠCH HÀNH ĐỘNG. Published actions only.
 */

import { useState, type ReactNode } from "react";
import { ACTION_PLAN_LABELS, OPTIMIZATION_LABELS } from "./cards";
import type {
  ActionItemView,
  ActionPlanView,
  DashboardCardSpec,
  OptimizationActionView,
  OptimizationDomainView,
  OptimizationPlanView,
} from "./types";
import { visualCardDom } from "./visualHierarchy";
import { mobileCardDom } from "./mobile/mobileOrder";

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

function OptItem({ item }: { readonly item: OptimizationActionView }): ReactNode {
  return (
    <li className="bte-ap__item">
      <span className="bte-ap__marker bte-ap__marker--action" aria-hidden="true" />
      <div className="bte-ap__copy">
        {item.domain ? <p className="bte-ap__domain">{item.domain}</p> : null}
        <p className="bte-ap__item-title">{item.title}</p>
        {item.reason ? <p className="bte-ap__item-detail">{item.reason}</p> : null}
      </div>
    </li>
  );
}

function DomainDetail({
  domain,
  open,
  onToggle,
}: {
  readonly domain: OptimizationDomainView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article className="bte-ap__domain-card" data-ap-domain={domain.id} data-open={open ? "true" : "false"}>
      <button type="button" className="bte-ap__domain-btn" aria-expanded={open} onClick={onToggle}>
        {domain.title}
      </button>
      {open ? (
        <dl className="bte-ap__domain-detail">
          <div>
            <dt>{OPTIMIZATION_LABELS.target}</dt>
            <dd>{domain.target || domain.action}</dd>
          </div>
          <div>
            <dt>{OPTIMIZATION_LABELS.why}</dt>
            <dd>{domain.why}</dd>
          </div>
          <div>
            <dt>{OPTIMIZATION_LABELS.action}</dt>
            <dd>{domain.action}</dd>
          </div>
          <div>
            <dt>{OPTIMIZATION_LABELS.condition}</dt>
            <dd>{domain.condition}</dd>
          </div>
          <div>
            <dt>{OPTIMIZATION_LABELS.caution}</dt>
            <dd>{domain.caution || domain.temporal}</dd>
          </div>
        </dl>
      ) : null}
    </article>
  );
}

function OptimizationBody({ model }: { readonly model: OptimizationPlanView }): ReactNode {
  const [openId, setOpenId] = useState(model.domains[0]?.id ?? "");
  return (
    <div className="bte-ap__opt" data-ap-opt="true">
      <p className="bte-ap__subtitle">{model.subtitle}</p>
      {model.topPriorities.length ? (
        <section className="bte-ap__priority" data-ap-section="top-priorities">
          <ol className="bte-ap__top">
            {model.topPriorities.map((item) => (
              <li key={item.label} className="bte-ap__top-item" data-ap-rank={item.rank}>
                <p className="bte-ap__top-label">{item.label}</p>
                <p className="bte-ap__item-title">{item.title}</p>
                <p className="bte-ap__item-detail">
                  {item.domain}
                  {item.reason ? ` · ${item.reason}` : ""}
                </p>
              </li>
            ))}
          </ol>
        </section>
      ) : null}
      {(["develop", "improve", "control", "avoid", "temporal"] as const).map((key) =>
        model.groups[key].length ? (
          <section key={key} className="bte-ap__actions" data-ap-section={key === "temporal" ? "current" : key}>
            <h3 className="bte-ap__heading">{OPTIMIZATION_LABELS[key]}</h3>
            <ul className="bte-ap__list bte-ap__list--tiles">
              {model.groups[key].map((item) => (
                <OptItem key={`${key}-${item.domain}-${item.title}`} item={item} />
              ))}
            </ul>
          </section>
        ) : null,
      )}
      <div className="bte-ap__scopes">
        <section className="bte-ap__scope" data-ap-section="natal" data-ap-scope="natal">
          <h3 className="bte-ap__heading">{model.natal.title}</h3>
          <ul className="bte-ap__list">
            {model.natal.items.map((item) => (
              <OptItem key={`natal-${item.domain}-${item.title}`} item={item} />
            ))}
          </ul>
        </section>
        <section className="bte-ap__scope" data-ap-section="temporal" data-ap-scope="temporal">
          <h3 className="bte-ap__heading">{model.temporal.title}</h3>
          <ul className="bte-ap__list">
            {model.temporal.items.map((item) => (
              <OptItem key={`temporal-${item.domain}-${item.title}`} item={item} />
            ))}
          </ul>
        </section>
      </div>
      {model.conflicts.length ? (
        <section className="bte-ap__warnings" data-ap-section="conflicts">
          <h3 className="bte-ap__heading">{OPTIMIZATION_LABELS.conflicts}</h3>
          <ul className="bte-ap__list">
            {model.conflicts.map((item) => (
              <li key={item.title} className="bte-ap__item" data-ap-conflict="true">
                <span className="bte-ap__marker bte-ap__marker--warning" aria-hidden="true" />
                <div className="bte-ap__copy">
                  <p className="bte-ap__domain">{item.domains}</p>
                  <p className="bte-ap__item-title">{item.title}</p>
                  <p className="bte-ap__item-detail">{item.resolution}</p>
                </div>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
      {model.domains.length ? (
        <section className="bte-ap__domains" data-ap-section="domains">
          <h3 className="bte-ap__heading">{OPTIMIZATION_LABELS.domains}</h3>
          {model.domains.map((domain) => (
            <DomainDetail
              key={domain.id}
              domain={domain}
              open={openId === domain.id}
              onToggle={() => setOpenId((current) => (current === domain.id ? "" : domain.id))}
            />
          ))}
        </section>
      ) : null}
      {model.usefulGod || model.elements.length ? (
        <div className="bte-ap__function-plan" data-ap-section="function-plan">
          {model.usefulGod ? (
            <section className="bte-ap__elements" data-ap-section="useful-god">
              <h3 className="bte-ap__heading">{OPTIMIZATION_LABELS.usefulGod}</h3>
              <ul className="bte-ap__list">
                <li className="bte-ap__item">
                  <span className="bte-ap__marker bte-ap__marker--watch" aria-hidden="true" />
                  <div className="bte-ap__copy">
                    <p className="bte-ap__domain">{model.usefulGod.element}</p>
                    <p className="bte-ap__item-title">{model.usefulGod.functions}</p>
                    <p className="bte-ap__item-detail">{model.usefulGod.reason}</p>
                  </div>
                </li>
              </ul>
            </section>
          ) : null}
          {model.elements.length ? (
            <section className="bte-ap__elements" data-ap-section="elements">
              <h3 className="bte-ap__heading">{OPTIMIZATION_LABELS.elements}</h3>
              <ul className="bte-ap__list">
                {model.elements.map((item) => (
                  <li key={item.element} className="bte-ap__item">
                    <span className="bte-ap__marker bte-ap__marker--watch" aria-hidden="true" />
                    <div className="bte-ap__copy">
                      <p className="bte-ap__domain">{item.element}</p>
                      <p className="bte-ap__item-title">{item.direction}</p>
                      <p className="bte-ap__item-detail">
                        {item.function}
                        {item.domains ? ` · ${item.domains}` : ""}
                        {item.reason ? ` · ${item.reason}` : ""}
                      </p>
                    </div>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

/**
 * Closing decision card. Renders adapter-prepared actions only.
 */
export function ActionPlanCard({ card, model }: ActionPlanCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const canExpand = model.extraActions.length > 0;
  const actions = expanded ? [...model.actions, ...model.extraActions] : model.actions;
  const optimization = model.optimization;

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-ap`}
      id="bte-card-action-plan"
      data-card={card.id}
      data-span={card.span}
      data-implemented="action-plan"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...mobileCardDom(card.id)}
    >
      <header className="bte-ap__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {!optimization && canExpand ? (
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
      ) : optimization ? (
        <OptimizationBody model={optimization} />
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
