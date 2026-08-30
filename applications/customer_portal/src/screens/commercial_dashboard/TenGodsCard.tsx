/**
 * Ten Gods Card — THẬP THẦN. Structural placement only. No interpretation.
 */

import { useState, type ReactNode } from "react";
import type { DashboardCardSpec, TenGodsPlacementView, TenGodsView } from "./types";
import { visualCardDom } from "./visualHierarchy";

type TenGodsCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: TenGodsView;
};

function PlacementList({
  items,
  showStem,
}: {
  readonly items: readonly TenGodsPlacementView[];
  readonly showStem: boolean;
}): ReactNode {
  if (!items.length) return null;
  return (
    <ul className="bte-tg__list">
      {items.map((item, index) => (
        <li
          key={`${item.pillar}-${item.tenGod}-${item.stem}-${index}`}
          className="bte-tg__item"
          data-pillar={item.pillar}
          data-ten-god={item.tenGod}
          data-day-master={item.isDayMaster ? "true" : undefined}
        >
          <span className="bte-tg__pillar">{item.pillarLabel}</span>
          <span className="bte-tg__god">
            {item.tenGod}
            {showStem && item.stem ? <span className="bte-tg__meta">{item.stem}</span> : null}
          </span>
        </li>
      ))}
    </ul>
  );
}

function presenceLabel(visible: boolean, hidden: boolean): string {
  if (visible && hidden) return "Lộ · Ẩn";
  if (visible) return "Lộ";
  return "Ẩn";
}

/**
 * Compact Ten Gods evidence card with progressive disclosure.
 */
export function TenGodsCard({ card, model }: TenGodsCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const canExpand = model.hidden.length > 0 || model.distribution.length > 0;

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-tg`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="ten-gods"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
    >
      <header className="bte-tg__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {canExpand ? (
          <button
            type="button"
            className="bte-tg__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem chi tiết"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-tg__empty" data-tg-empty="true">
          Chưa đủ dữ liệu Thập Thần.
        </p>
      ) : (
        <>
          {model.featured.length ? (
            <section className="bte-tg__section" data-tg-section="featured">
              <h3 className="bte-tg__heading">Nổi bật</h3>
              <ul className="bte-tg__badges">
                {model.featured.map((name) => (
                  <li key={name} className="bte-tg__badge">
                    {name}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
          <section className="bte-tg__section" data-tg-section="visible">
            <h3 className="bte-tg__heading">Lộ rõ</h3>
            <PlacementList items={model.visible} showStem={expanded} />
          </section>
          {!expanded && model.hiddenNames.length ? (
            <section className="bte-tg__section" data-tg-section="hidden-summary">
              <h3 className="bte-tg__heading">Tàng Can</h3>
              <p className="bte-tg__summary" data-tg-hidden-names="true">
                {model.hiddenNames.join(" · ")}
              </p>
            </section>
          ) : null}
          {expanded && model.hidden.length ? (
            <section className="bte-tg__section" data-tg-section="hidden">
              <h3 className="bte-tg__heading">Tàng Can</h3>
              <PlacementList items={model.hidden} showStem />
            </section>
          ) : null}
          {expanded && model.distribution.length ? (
            <section className="bte-tg__section" data-tg-section="distribution">
              <h3 className="bte-tg__heading">Phân bố</h3>
              <ul className="bte-tg__dist">
                {model.distribution.map((row) => (
                  <li key={row.name} className="bte-tg__dist-row" data-tg-dist={row.name}>
                    <span>{row.name}</span>
                    <span className="bte-tg__meta">{presenceLabel(row.visible, row.hidden)}</span>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
          {model.summary ? (
            <p className="bte-tg__comment" data-tg-summary="true">
              {model.summary}
            </p>
          ) : null}
        </>
      )}
    </article>
  );
}
