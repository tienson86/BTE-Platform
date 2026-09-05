/**
 * Luck Card — ĐẠI VẬN. Timeline only. No tốt/xấu inference.
 */

import { useState, type ReactNode } from "react";
import type {
  DashboardCardSpec,
  LuckActivationItemView,
  LuckCycleView,
  LuckInteractionEdgeView,
  LuckView,
} from "./types";
import { visualCardDom } from "./visualHierarchy";
import { vizDom } from "./vizCatalog";
import { mobileCardDom } from "./mobile/mobileOrder";

const COMPACT_LIMIT = 5;

function publishTrend(value: string): string {
  const next = value.trim();
  if (!next || next.includes("{") || next.includes("}")) return "";
  return next;
}

type LuckCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: LuckView;
};

function windowCycles(cycles: readonly LuckCycleView[], expanded: boolean): readonly LuckCycleView[] {
  if (expanded || cycles.length <= COMPACT_LIMIT) return cycles;
  const current = cycles.findIndex((cycle) => cycle.isCurrent);
  const idx = current >= 0 ? current : 0;
  let start = Math.max(0, idx - 2);
  const end = Math.min(cycles.length, start + COMPACT_LIMIT);
  start = Math.max(0, end - COMPACT_LIMIT);
  return cycles.slice(start, end);
}

function CycleBadge({
  cycle,
  detail,
}: {
  readonly cycle: LuckCycleView;
  readonly detail: boolean;
}): ReactNode {
  return (
    <li
      className="bte-luck__badge"
      data-luck-cycle={cycle.ganZhi}
      data-luck-current={cycle.isCurrent ? "true" : undefined}
    >
      <span className="bte-luck__node" aria-hidden="true" />
      <span className="bte-luck__badge-name">{cycle.ganZhi}</span>
      {cycle.isCurrent ? (
        <span className="bte-luck__now" data-luck-now="true">
          Hiện tại
        </span>
      ) : null}
      {cycle.yearRange ? <span className="bte-luck__badge-meta">{cycle.yearRange}</span> : null}
      {detail && cycle.ageRange ? <span className="bte-luck__badge-meta">{cycle.ageRange}</span> : null}
    </li>
  );
}

/**
 * Compact Luck timeline card with progressive disclosure.
 */
export function LuckCard({ card, model }: LuckCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const canExpand = model.cycles.length > COMPACT_LIMIT;
  const timeline = windowCycles(model.cycles, expanded);
  const trend = publishTrend(model.trend);

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-luck`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="luck"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...vizDom(card.id)}
      {...mobileCardDom(card.id)}
    >
      <header className="bte-luck__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {canExpand ? (
          <button
            type="button"
            className="bte-luck__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem toàn bộ Đại Vận"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-luck__empty" data-luck-empty="true">
          Chưa đủ dữ liệu Đại Vận.
        </p>
      ) : (
        <>
          {model.current ? (
            <section className="bte-luck__section" data-luck-section="current">
              <h3 className="bte-luck__heading">Đại Vận hiện tại</h3>
              <p className="bte-luck__value-row" data-luck-current-row="true">
                <span className="bte-luck__ganzhi" data-luck-current-name="true">
                  {model.current.ganZhi}
                </span>
                <span className="bte-luck__chronology">
                  {model.current.yearRange ? (
                    <span className="bte-luck__years">
                      {" ("}
                      <span data-luck-current-years="true">{model.current.yearRange}</span>
                      {")"}
                    </span>
                  ) : null}
                  {model.current.yearRange && model.current.ageRange ? (
                    <span className="bte-luck__sep" aria-hidden="true">
                      {" · "}
                    </span>
                  ) : null}
                  {model.current.ageRange ? (
                    <span className="bte-luck__ages" data-luck-current-ages="true">
                      {model.current.ageRange}
                    </span>
                  ) : null}
                </span>
              </p>
            </section>
          ) : null}
          {model.direction || model.startAge ? (
            <section className="bte-luck__section" data-luck-section="start">
              <h3 className="bte-luck__heading">Khởi vận</h3>
              <p className="bte-luck__value-row bte-luck__value-row--meta" data-luck-start-row="true">
                {model.direction ? (
                  <span className="bte-luck__meta" data-luck-direction="true">
                    {model.direction}
                  </span>
                ) : null}
                {model.direction && model.startAge ? (
                  <span className="bte-luck__sep" aria-hidden="true">
                    {" · "}
                  </span>
                ) : null}
                {model.startAge ? (
                  <span className="bte-luck__meta" data-luck-start-age="true">
                    {model.startAge}
                  </span>
                ) : null}
              </p>
            </section>
          ) : null}
          {timeline.length ? (
            <section className="bte-luck__section" data-luck-section="timeline">
              <h3 className="bte-luck__heading">Timeline Đại Vận</h3>
              <ol className="bte-luck__timeline" data-viz-chart="timeline">
                {timeline.map((cycle) => (
                  <CycleBadge key={`${cycle.ganZhi}-${cycle.yearRange}`} cycle={cycle} detail={expanded} />
                ))}
              </ol>
            </section>
          ) : null}
          {model.next ? (
            <section className="bte-luck__section" data-luck-section="next">
              <h3 className="bte-luck__heading">Đại Vận kế tiếp</h3>
              <p className="bte-luck__next" data-luck-next="true">
                {model.next.ganZhi}
                {model.next.yearRange ? ` · ${model.next.yearRange}` : ""}
              </p>
            </section>
          ) : null}
          {model.activation ? <ActivationSummary model={model.activation} /> : null}
          {model.interaction ? <InteractionSummary model={model.interaction} /> : null}
          {trend ? (
            <p className="bte-luck__trend" data-luck-trend="true">
              {trend}
            </p>
          ) : null}
        </>
      )}
    </article>
  );
}

function ActivationSummary({
  model,
}: {
  readonly model: NonNullable<LuckView["activation"]>;
}): ReactNode {
  const [openId, setOpenId] = useState<string | null>(null);
  return (
    <section className="bte-luck__section bte-luck__activation" data-luck-section="activation">
      <h3 className="bte-luck__heading">{model.title}</h3>
      {model.timeWindow ? (
        <p className="bte-luck__activation-window" data-luck-activation-window="true">
          {model.ganZhi ? `${model.ganZhi} · ` : ""}
          {model.timeWindow}
        </p>
      ) : null}
      <ul className="bte-luck__activation-list">
        {model.items.map((item) => (
          <ActivationRow
            key={item.id}
            item={item}
            open={openId === item.id}
            onToggle={() => setOpenId((current) => (current === item.id ? null : item.id))}
          />
        ))}
      </ul>
    </section>
  );
}

function ActivationRow({
  item,
  open,
  onToggle,
}: {
  readonly item: LuckActivationItemView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <li
      className="bte-luck__activation-item"
      data-luck-activation-id={item.id}
      data-luck-activation-open={open ? "true" : undefined}
    >
      <button type="button" className="bte-luck__activation-row" onClick={onToggle}>
        <span className="bte-luck__activation-title">{item.title}</span>
        <span className="bte-luck__activation-state" data-luck-activation-state="true">
          {item.stateLabel}
        </span>
        {item.marker ? (
          <span className="bte-luck__activation-marker" data-luck-activation-marker="true">
            {item.marker}
          </span>
        ) : null}
      </button>
      {open ? (
        <div className="bte-luck__activation-detail" data-luck-activation-detail="true">
          {item.driver ? <p data-luck-activation-driver="true">{item.driver}</p> : null}
          {item.bottleneck ? <p data-luck-activation-bottleneck="true">{item.bottleneck}</p> : null}
          {item.conditions.map((condition) => (
            <p key={condition}>{condition}</p>
          ))}
        </div>
      ) : null}
    </li>
  );
}

function InteractionSummary({
  model,
}: {
  readonly model: NonNullable<LuckView["interaction"]>;
}): ReactNode {
  const [openKey, setOpenKey] = useState<string | null>(null);
  const [showEdges, setShowEdges] = useState(false);
  return (
    <section className="bte-luck__section bte-luck__interaction" data-luck-section="interaction">
      <h3 className="bte-luck__heading">{model.title}</h3>
      <dl className="bte-luck__interaction-summary">
        {model.situation ? (
          <div className="bte-luck__interaction-row">
            <dt>Trạng thái vận</dt>
            <dd data-luck-interaction-situation="true">{model.situation}</dd>
          </div>
        ) : null}
        {model.driver ? (
          <div className="bte-luck__interaction-row">
            <dt>Tương tác chính</dt>
            <dd data-luck-interaction-driver="true">{model.driver}</dd>
          </div>
        ) : null}
        {model.bottleneck ? (
          <div className="bte-luck__interaction-row">
            <dt>Điểm nghẽn</dt>
            <dd data-luck-interaction-bottleneck="true">{model.bottleneck}</dd>
          </div>
        ) : null}
        {model.opportunity ? (
          <div className="bte-luck__interaction-row">
            <dt>Cơ hội</dt>
            <dd data-luck-interaction-opportunity="true">{model.opportunity}</dd>
          </div>
        ) : null}
        {model.risk ? (
          <div className="bte-luck__interaction-row">
            <dt>Đánh đổi</dt>
            <dd data-luck-interaction-risk="true">{model.risk}</dd>
          </div>
        ) : null}
      </dl>
      {model.edges.length ? (
        <>
          <button
            type="button"
            className="bte-luck__toggle"
            aria-expanded={showEdges}
            data-luck-interaction-toggle="true"
            onClick={() => setShowEdges((value) => !value)}
          >
            {showEdges ? "Thu gọn tương tác" : "Chi tiết tương tác"}
          </button>
          {showEdges ? (
            <ul className="bte-luck__interaction-list">
              {model.edges.map((edge) => {
                const key = `${edge.source}-${edge.target}-${edge.type}`;
                return (
                  <InteractionEdge
                    key={key}
                    edge={edge}
                    open={openKey === key}
                    onToggle={() => setOpenKey((current) => (current === key ? null : key))}
                  />
                );
              })}
            </ul>
          ) : null}
        </>
      ) : null}
    </section>
  );
}

function InteractionEdge({
  edge,
  open,
  onToggle,
}: {
  readonly edge: LuckInteractionEdgeView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <li
      className="bte-luck__interaction-item"
      data-luck-interaction-edge="true"
      data-luck-interaction-open={open ? "true" : undefined}
    >
      <button type="button" className="bte-luck__interaction-row-btn" onClick={onToggle}>
        <span className="bte-luck__interaction-pair">
          {edge.source}
          {" ↔ "}
          {edge.target}
        </span>
        <span className="bte-luck__interaction-type">{edge.type}</span>
      </button>
      {open ? (
        <div className="bte-luck__interaction-detail" data-luck-interaction-detail="true">
          {edge.explanation ? <p>{edge.explanation}</p> : null}
          {edge.condition ? <p>{edge.condition}</p> : null}
        </div>
      ) : null}
    </li>
  );
}
