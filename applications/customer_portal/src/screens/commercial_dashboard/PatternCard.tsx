/**
 * Pattern Card — MỆNH CỤC. Structural classification only. No inference.
 */

import { useState, type ReactNode } from "react";
import type { DashboardCardSpec, PatternView } from "./types";
import { visualCardDom } from "./visualHierarchy";
import { vizDom } from "./vizCatalog";

type PatternCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: PatternView;
};

function FormationFlow({
  steps,
}: {
  readonly steps: readonly string[];
}): ReactNode {
  if (!steps.length) return null;
  return (
    <ol className="bte-pat__flow" data-viz-chart="formation-flow">
      {steps.map((step, index) => (
        <li key={`${step}-${index}`} className="bte-pat__step">
          {index > 0 ? (
            <span className="bte-pat__arrow" aria-hidden="true" />
          ) : null}
          <span className="bte-pat__step-text">{step}</span>
        </li>
      ))}
    </ol>
  );
}

/**
 * Compact Pattern evidence card with progressive Formation disclosure.
 */
export function PatternCard({ card, model }: PatternCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const canExpand = model.formation.length > 1;
  const formationSteps = expanded || !canExpand ? model.formation : model.formation.slice(0, 1);

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-pat`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="pattern"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...vizDom(card.id)}
    >
      <header className="bte-pat__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {canExpand ? (
          <button
            type="button"
            className="bte-pat__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem quá trình hình thành"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-pat__empty" data-pat-empty="true">
          Chưa đủ dữ liệu Mệnh Cục.
        </p>
      ) : (
        <>
          <section className="bte-pat__section" data-pat-section="primary">
            <h3 className="bte-pat__heading">Mệnh Cục chính</h3>
            <p className="bte-pat__primary" data-pat-primary="true">
              {model.primary}
            </p>
          </section>
          {model.status ? (
            <section className="bte-pat__section" data-pat-section="status">
              <h3 className="bte-pat__heading">Trạng thái</h3>
              <p className="bte-pat__status" data-pat-status="true">
                {model.status}
              </p>
            </section>
          ) : null}
          {model.secondary ? (
            <section className="bte-pat__section" data-pat-section="secondary">
              <h3 className="bte-pat__heading">Phụ cách</h3>
              <p className="bte-pat__secondary" data-pat-secondary="true">
                {model.secondary}
              </p>
            </section>
          ) : null}
          {formationSteps.length ? (
            <section className="bte-pat__section" data-pat-section="formation">
              <h3 className="bte-pat__heading">Quá trình hình thành</h3>
              <FormationFlow steps={formationSteps} />
            </section>
          ) : null}
          {model.summary ? (
            <section className="bte-pat__section" data-pat-section="summary">
              <h3 className="bte-pat__heading">Tóm tắt</h3>
              <p className="bte-pat__summary" data-pat-summary="true">
                {model.summary}
              </p>
            </section>
          ) : null}
        </>
      )}
    </article>
  );
}
