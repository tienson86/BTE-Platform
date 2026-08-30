/**
 * Interpretation Card — LUẬN GIẢI TỔNG THỂ. Published narrative only.
 */

import { useState, type ReactNode } from "react";
import { INTERPRETATION_CLOSE_LABEL, INTERPRETATION_LEAD_LABEL } from "./cards";
import type { DashboardCardSpec, InterpretationView, InterpretationZoneView } from "./types";
import { visualCardDom } from "./visualHierarchy";

type InterpretationCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: InterpretationView;
};

function Zone({ zone }: { readonly zone: InterpretationZoneView }): ReactNode {
  if (!zone.body) return null;
  return (
    <section className="bte-int__zone" data-int-zone={zone.id} data-int-source={zone.source}>
      <h3 className="bte-int__zone-title">{zone.label}</h3>
      <p className="bte-int__zone-body">{zone.body}</p>
    </section>
  );
}

function canReveal(model: InterpretationView): boolean {
  if (model.leadExtra || model.closing) return true;
  return model.zones.some((zone) => Boolean(zone.extra));
}

/**
 * Full-width synthesis card. Renders adapter-prepared narrative blocks only.
 */
export function InterpretationCard({ card, model }: InterpretationCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const reveal = canReveal(model);
  const visibleZones = model.zones.filter((zone) => zone.body);

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-int`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="interpretation"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
    >
      <header className="bte-int__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {reveal ? (
          <button
            type="button"
            className="bte-int__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem luận giải đầy đủ"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-int__empty" data-int-empty="true">
          {model.emptyMessage}
        </p>
      ) : (
        <>
          {model.lead ? (
            <section className="bte-int__lead-block" data-int-lead="true">
              <h3 className="bte-int__zone-title">{INTERPRETATION_LEAD_LABEL}</h3>
              <p className="bte-int__lead">
                {model.lead}
                {expanded && model.leadExtra ? ` ${model.leadExtra}` : ""}
              </p>
            </section>
          ) : null}
          <div className="bte-int__zones">
            {visibleZones.map((zone) => (
              <Zone key={zone.id} zone={zone} />
            ))}
          </div>
          {expanded
            ? visibleZones
                .filter((zone) => zone.extra)
                .map((zone) => (
                  <p key={`${zone.id}-extra`} className="bte-int__extra" data-int-extra={zone.id}>
                    {zone.extra}
                  </p>
                ))
            : null}
          {expanded && model.closing ? (
            <section className="bte-int__closing-block" data-int-closing="true">
              <h3 className="bte-int__zone-title">{INTERPRETATION_CLOSE_LABEL}</h3>
              <p className="bte-int__closing">{model.closing}</p>
            </section>
          ) : null}
        </>
      )}
    </article>
  );
}
