/**
 * Interpretation Card — LUẬN GIẢI TỔNG THỂ plus compact Domain pillars.
 */

import { useState, type ReactNode } from "react";
import { INTERPRETATION_CLOSE_LABEL, INTERPRETATION_LEAD_LABEL } from "./cards";
import type {
  DashboardCardSpec,
  DomainPillarView,
  InterpretationView,
  InterpretationZoneView,
} from "./types";
import { visualCardDom } from "./visualHierarchy";
import { MobileToggle, useMobileOpen } from "./mobile/MobileToggle";
import { mobileCardDom } from "./mobile/mobileOrder";

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

function DomainRow({
  label,
  value,
}: {
  readonly label: string;
  readonly value: string;
}): ReactNode {
  if (!value) return null;
  return (
    <div className="bte-dom__row">
      <span className="bte-dom__label">{label}</span>
      <span className="bte-dom__value">{value}</span>
    </div>
  );
}

function DomainPillars({
  title,
  items,
}: {
  readonly title: string;
  readonly items: readonly DomainPillarView[];
}): ReactNode {
  const [openId, setOpenId] = useState("");
  if (!items.length) return null;
  return (
    <section className="bte-dom" data-domain-section="pillars" aria-label={title}>
      <h3 className="bte-int__zone-title">{title}</h3>
      <div className="bte-dom__list">
        {items.map((item) => {
          const open = openId === item.id;
          return (
            <article
              key={item.id}
              className="bte-dom__card"
              data-domain-id={item.id}
              data-domain-open={open ? "true" : "false"}
            >
              <button
                type="button"
                className="bte-dom__summary"
                aria-expanded={open}
                onClick={() => setOpenId(open ? "" : item.id)}
              >
                <span className="bte-dom__title">{item.title}</span>
                <span className="bte-dom__state">{item.stateLabel}</span>
              </button>
              <div className="bte-dom__preview">
                <DomainRow label="Động lực" value={item.unresolved ? "" : item.driver} />
                <DomainRow label="Điểm nghẽn" value={item.unresolved ? "" : item.bottleneck} />
                <DomainRow label="Cơ hội" value={item.unresolved ? "" : item.opportunity} />
                <DomainRow label="Lưu ý" value={item.unresolved ? "" : item.caution} />
                {item.unresolved ? <p className="bte-dom__empty">{item.summary}</p> : null}
              </div>
              {open ? (
                <div className="bte-dom__detail" data-domain-detail={item.id}>
                  {item.summary && !item.unresolved ? <p className="bte-dom__copy">{item.summary}</p> : null}
                  <DomainRow label="Hỗ trợ" value={item.support} />
                  <DomainRow label="Điều kiện" value={item.condition} />
                  <DomainRow label="Độ tin cậy" value={item.confidence} />
                  {item.dimensions.length ? (
                    <div className="bte-dom__dims">
                      {item.dimensions.map((dimension) => (
                        <div key={dimension.label} className="bte-dom__dim">
                          <span>{dimension.label}</span>
                          <strong>{dimension.value}</strong>
                        </div>
                      ))}
                    </div>
                  ) : null}
                </div>
              ) : null}
            </article>
          );
        })}
      </div>
    </section>
  );
}

function canReveal(model: InterpretationView): boolean {
  if (model.leadExtra || model.closing) return true;
  return model.zones.some((zone) => Boolean(zone.extra));
}

/**
 * Full-width synthesis card. Renders adapter-prepared narrative and domain labels.
 */
export function InterpretationCard({ card, model }: InterpretationCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const mobile = useMobileOpen();
  const reveal = canReveal(model);
  const visibleZones = model.zones.filter((zone) => zone.body);
  const hasDomains = model.domains.length > 0;

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-int`}
      id="bte-card-interpretation"
      data-card={card.id}
      data-span={card.span}
      data-implemented="interpretation"
      data-expanded={expanded ? "true" : "false"}
      data-mobile-open={mobile.open ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...mobileCardDom(card.id)}
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
        {model.available ? (
          <MobileToggle open={mobile.open} label="Xem chi tiết" onToggle={mobile.toggle} />
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-int__empty" data-int-empty="true">
          {model.emptyMessage}
        </p>
      ) : (
        <>
          <DomainPillars title={model.domainTitle} items={model.domains} />
          {model.lead ? (
            <section className="bte-int__lead-block" data-int-lead="true" data-motion-reveal="lead">
              <h3 className="bte-int__zone-title">{INTERPRETATION_LEAD_LABEL}</h3>
              <p className="bte-int__lead">
                {model.lead}
                {expanded && model.leadExtra ? ` ${model.leadExtra}` : ""}
              </p>
            </section>
          ) : null}
          <div className="bte-int__zones" data-mobile-body="true">
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
          {!hasDomains && !model.lead && !visibleZones.length && !model.closing ? (
            <p className="bte-int__empty" data-int-empty="true">
              {model.emptyMessage}
            </p>
          ) : null}
        </>
      )}
    </article>
  );
}
