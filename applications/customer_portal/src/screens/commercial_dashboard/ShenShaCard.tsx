/**
 * ShenSha Card — THẦN SÁT. Supporting evidence only. No invented meaning.
 */

import { useState, type ReactNode } from "react";
import { SHENSHA_FALLBACK_HEADING } from "./cards";
import type { DashboardCardSpec, ShenShaItemView, ShenShaView } from "./types";

const FEATURED_LIMIT = 4;

type ShenShaCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: ShenShaView;
};

function ItemRow({
  item,
  showPlacement,
}: {
  readonly item: ShenShaItemView;
  readonly showPlacement: boolean;
}): ReactNode {
  return (
    <li className="bte-ss__item" data-ss-name={item.name}>
      <span className="bte-ss__chip">{item.name}</span>
      {showPlacement && item.placement ? (
        <span className="bte-ss__meta" data-ss-placement="true">
          {item.placement}
        </span>
      ) : null}
      {item.meaning ? (
        <span className="bte-ss__meaning" data-ss-meaning="true">
          {item.meaning}
        </span>
      ) : null}
    </li>
  );
}

/**
 * Compact ShenSha supporting card with progressive disclosure.
 */
export function ShenShaCard({ card, model }: ShenShaCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const canExpand =
    model.items.length > FEATURED_LIMIT ||
    model.items.some((item) => Boolean(item.placement || item.meaning)) ||
    model.groups.some((group) => group.items.some((item) => Boolean(item.placement || item.meaning)));
  const fallbackItems = expanded ? model.items : model.items.slice(0, FEATURED_LIMIT);

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-ss`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="shensha"
      data-expanded={expanded ? "true" : "false"}
      data-grouped={model.grouped ? "true" : "false"}
      aria-label={model.title}
    >
      <header className="bte-ss__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {canExpand ? (
          <button
            type="button"
            className="bte-ss__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem chi tiết"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-ss__empty" data-ss-empty="true">
          Chưa có dữ liệu Thần Sát.
        </p>
      ) : (
        <>
          {model.grouped ? (
            <div className="bte-ss__groups" data-ss-section="groups">
              {model.groups.map((group) => (
                <section key={group.heading} className="bte-ss__group" data-ss-group={group.heading}>
                  <h3 className="bte-ss__heading">{group.heading}</h3>
                  <ul className="bte-ss__list">
                    {group.items.map((item) => (
                      <ItemRow key={item.name} item={item} showPlacement={expanded} />
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          ) : (
            <section className="bte-ss__section" data-ss-section="featured">
              <h3 className="bte-ss__heading">{SHENSHA_FALLBACK_HEADING}</h3>
              <ul className="bte-ss__list">
                {fallbackItems.map((item) => (
                  <ItemRow key={item.name} item={item} showPlacement={expanded} />
                ))}
              </ul>
            </section>
          )}
          {model.summary ? (
            <p className="bte-ss__summary" data-ss-summary="true">
              {model.summary}
            </p>
          ) : null}
          {model.note ? (
            <p className="bte-ss__note" data-ss-note="true">
              {model.note}
            </p>
          ) : null}
        </>
      )}
    </article>
  );
}
