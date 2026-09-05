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
  Pack07NarrativeComposerView,
  Pack07NarrativeDomainView,
  Pack07NarrativeItemView,
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

function ComposerList({
  id,
  title,
  items,
}: {
  readonly id: string;
  readonly title: string;
  readonly items: readonly Pack07NarrativeItemView[];
}): ReactNode {
  if (!items.length) return null;
  return (
    <section className="bte-int__composer-section" data-int-section={id}>
      <h3 className="bte-int__zone-title">{title}</h3>
      <ul className="bte-int__composer-list">
        {items.map((entry, index) => (
          <li key={`${id}-${index}`} className="bte-int__composer-item">
            {entry.title ? <strong className="bte-int__composer-item-title">{entry.title}</strong> : null}
            {entry.summary ? <p className="bte-int__zone-body">{entry.summary}</p> : null}
          </li>
        ))}
      </ul>
    </section>
  );
}

function ComposerDomains({
  title,
  items,
  fields,
}: {
  readonly title: string;
  readonly items: readonly Pack07NarrativeDomainView[];
  readonly fields: Pack07NarrativeComposerView["labels"]["fields"];
}): ReactNode {
  if (!items.length) return null;
  return (
    <section className="bte-int__composer-section" data-int-section="domains">
      <h3 className="bte-int__zone-title">{title}</h3>
      <div className="bte-int__composer-domains">
        {items.map((entry) => (
          <article key={entry.id || entry.title} className="bte-dom__card" data-int-domain={entry.id}>
            <div className="bte-dom__summary">
              <span className="bte-dom__title">{entry.title}</span>
              <span className="bte-dom__state">{entry.state}</span>
            </div>
            <DomainRow label={fields.state} value={entry.state} />
            <DomainRow label={fields.driver} value={entry.driver} />
            <DomainRow label={fields.bottleneck} value={entry.bottleneck} />
            <DomainRow label={fields.opportunity} value={entry.opportunity} />
            <DomainRow label={fields.caution} value={entry.caution} />
            <DomainRow label={fields.condition} value={entry.condition} />
          </article>
        ))}
      </div>
    </section>
  );
}

function ComposerBody({ composer }: { readonly composer: Pack07NarrativeComposerView }): ReactNode {
  return (
    <div className="bte-int__composer" data-int-composer="true">
      {composer.executive ? (
        <section className="bte-int__lead-block" data-int-section="executive" data-int-lead="true">
          <h3 className="bte-int__zone-title">{composer.labels.executive}</h3>
          <p className="bte-int__lead">{composer.executive}</p>
        </section>
      ) : null}
      <div className="bte-int__composer-body" data-mobile-body="true">
        <ComposerList id="strengths" title={composer.labels.strengths} items={composer.strengths} />
        <ComposerList id="risks" title={composer.labels.risks} items={composer.risks} />
        <ComposerList id="opportunities" title={composer.labels.opportunities} items={composer.opportunities} />
        <ComposerDomains title={composer.labels.domains} items={composer.domains} fields={composer.labels.fields} />
        <ComposerList id="luck" title={composer.labels.luck} items={composer.luck} />
        <ComposerList id="actions" title={composer.labels.actions} items={composer.actions} />
        {composer.closing ? (
          <section className="bte-int__closing-block" data-int-section="closing" data-int-closing="true">
            <h3 className="bte-int__zone-title">{composer.labels.closing}</h3>
            <p className="bte-int__closing">{composer.closing}</p>
          </section>
        ) : null}
      </div>
    </div>
  );
}

function canReveal(model: InterpretationView): boolean {
  if (model.composer) return false;
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
      ) : model.composer ? (
        <ComposerBody composer={model.composer} />
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
