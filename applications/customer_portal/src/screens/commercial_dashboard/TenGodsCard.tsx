/**
 * Ten Gods Card — THẬP THẦN. Visible consulting first. Hidden stays support.
 * P-003C layout only. Copy and calculation stay in the adapters.
 */

import { useState, type ReactNode } from "react";
import type {
  DashboardCardSpec,
  TenGodCombinationView,
  TenGodCommercialView,
  TenGodDetailedView,
  TenGodEcosystemView,
  TenGodRelationView,
  TenGodsPlacementView,
  TenGodsView,
} from "./types";
import { visualCardDom } from "./visualHierarchy";
import { vizDom } from "./vizCatalog";
import { MobileToggle, useMobileOpen } from "./mobile/MobileToggle";
import { mobileCardDom } from "./mobile/mobileOrder";

type TenGodsCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: TenGodsView;
};

const COMBO_DETAIL: readonly {
  readonly key: "capability" | "income" | "career" | "leadership" | "growth" | "risk" | "recommendation";
  readonly label: string;
}[] = [
  { key: "capability", label: "Năng lực" },
  { key: "income", label: "Thu nhập" },
  { key: "career", label: "Công việc" },
  { key: "leadership", label: "Cầm việc" },
  { key: "growth", label: "Tăng trưởng" },
  { key: "risk", label: "Rủi ro" },
  { key: "recommendation", label: "Hướng đi" },
];

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

function CombinationCard({
  item,
  open,
  onToggle,
}: {
  readonly item: TenGodCombinationView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article
      className="bte-tg__combo"
      data-tg-combination="true"
      data-tg-hero="combination"
      data-tg-combo-open={open ? "true" : "false"}
    >
      <header className="bte-tg__consult-head">
        <h4 className="bte-tg__combo-title">{item.title}</h4>
      </header>
      {item.members.length ? (
        <ul className="bte-tg__badges" data-tg-combo-members="true">
          {item.members.map((name) => (
            <li key={name} className="bte-tg__badge">
              {name}
            </li>
          ))}
        </ul>
      ) : null}
      <p className="bte-tg__consult-insight" data-tg-field="insight">
        {item.insight}
      </p>
      <button
        type="button"
        className="bte-tg__more"
        aria-expanded={open}
        onClick={onToggle}
      >
        {open ? "Thu gọn mô hình" : "Xem mô hình chi tiết"}
      </button>
      <dl className="bte-tg__consult-grid" data-tg-combo-detail="true" hidden={!open}>
        {COMBO_DETAIL.map((field) => (
          <div key={field.key} data-tg-field={field.key}>
            <dt>{field.label}</dt>
            <dd>{item[field.key]}</dd>
          </div>
        ))}
      </dl>
    </article>
  );
}

function RelationCard({
  item,
  open,
  onToggle,
}: {
  readonly item: TenGodRelationView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article
      className="bte-tg__relation"
      data-tg-relation={item.name}
      data-tg-open={open ? "true" : "false"}
      data-tg-unresolved={item.unresolved ? "true" : undefined}
    >
      <button type="button" className="bte-tg__detail-toggle" aria-expanded={open} onClick={onToggle}>
        <span className="bte-tg__consult-name">{item.name}</span>
        <span className="bte-tg__meta">{item.stateLabel}</span>
      </button>
      <div className="bte-tg__detail-body" hidden={!open}>
        {item.unresolved ? (
          <p className="bte-tg__summary">{item.fallback}</p>
        ) : (
          <>
            {item.mechanism ? (
              <p className="bte-tg__summary" data-tg-field="mechanism">
                {item.mechanism}
              </p>
            ) : null}
            {item.condition ? (
              <p className="bte-tg__summary" data-tg-field="condition">
                {item.condition}
              </p>
            ) : null}
          </>
        )}
      </div>
    </article>
  );
}

function EcosystemSummary({ model }: { readonly model: TenGodEcosystemView }): ReactNode {
  const rows: readonly { readonly key: string; readonly title: string; readonly value: string }[] = [
    { key: "driver", title: "Động lực chính", value: model.driver.label },
    { key: "support", title: "Hỗ trợ", value: model.support.label },
    { key: "bottleneck", title: "Điểm nghẽn", value: model.bottleneck.label },
    { key: "blocked", title: "Lực bị chặn", value: model.blocked.label },
    { key: "excessive", title: "Lực dư", value: model.excessive.label },
    { key: "deficient", title: "Lực thiếu", value: model.deficient.label },
    { key: "missing", title: "Không hiện chức năng", value: model.missing.label },
    { key: "flow", title: "Dòng vận hành", value: model.flow },
    { key: "flow-quality", title: "Chất lượng dòng", value: model.flowQuality },
  ];
  return (
    <dl className="bte-tg__eco-grid" data-tg-ecosystem="true">
      {rows.map((row) => (
        <div key={row.key} data-tg-eco={row.key}>
          <dt>{row.title}</dt>
          <dd>{row.value}</dd>
        </div>
      ))}
    </dl>
  );
}

function DetailedCard({
  item,
  open,
  onToggle,
}: {
  readonly item: TenGodDetailedView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article
      className="bte-tg__detail"
      data-tg-detailed={item.name}
      data-tg-open={open ? "true" : "false"}
      data-tg-unresolved={item.unresolved ? "true" : undefined}
    >
      <button type="button" className="bte-tg__detail-toggle" aria-expanded={open} onClick={onToggle}>
        <span className="bte-tg__consult-name">{item.name}</span>
        <span className="bte-tg__meta">{item.statusLabel}</span>
      </button>
      <div className="bte-tg__detail-body" hidden={!open}>
        {item.unresolved ? (
          <p className="bte-tg__summary">{item.fallback}</p>
        ) : (
          <>
            {item.roleLabel ? (
              <p className="bte-tg__summary" data-tg-field="role">
                Vai trò: {item.roleLabel}
              </p>
            ) : null}
            {item.positives.length ? (
              <ul className="bte-tg__points" data-tg-field="positives">
                {item.positives.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            ) : null}
            {item.risks.length ? (
              <ul className="bte-tg__points" data-tg-field="risks">
                {item.risks.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            ) : null}
            {item.conditions.length ? (
              <p className="bte-tg__summary" data-tg-field="conditions">
                {item.conditions.join(" · ")}
              </p>
            ) : null}
          </>
        )}
      </div>
    </article>
  );
}

function CommercialCard({
  item,
  open,
  onToggle,
}: {
  readonly item: TenGodCommercialView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article
      className="bte-tg__consult"
      data-tg-commercial={item.name}
      data-tg-open={open ? "true" : "false"}
    >
      <header className="bte-tg__consult-head">
        <h4 className="bte-tg__consult-name">{item.name}</h4>
        {item.pillarLabel ? <span className="bte-tg__meta">{item.pillarLabel}</span> : null}
      </header>
      <p className="bte-tg__consult-insight" data-tg-field="insight">
        {item.insight}
      </p>
      <dl className="bte-tg__consult-grid" data-tg-compact="true">
        <div data-tg-field="capability">
          <dt>Năng lực</dt>
          <dd>{item.capability}</dd>
        </div>
        <div data-tg-field="income">
          <dt>Thu nhập</dt>
          <dd>{item.income}</dd>
        </div>
      </dl>
      <button
        type="button"
        className="bte-tg__more"
        aria-expanded={open}
        onClick={onToggle}
      >
        {open ? "Thu gọn" : "Xem phân tích đầy đủ"}
      </button>
      <dl className="bte-tg__consult-grid" data-tg-detail="true" hidden={!open}>
        <div data-tg-field="career">
          <dt>Công việc</dt>
          <dd>{item.career}</dd>
        </div>
        <div data-tg-field="risk">
          <dt>Rủi ro</dt>
          <dd>{item.risk}</dd>
        </div>
        <div data-tg-field="recommendation">
          <dt>Hướng đi</dt>
          <dd>{item.recommendation}</dd>
        </div>
      </dl>
    </article>
  );
}

/**
 * Visible Ten Gods get consulting cards. Hidden names stay secondary.
 */
export function TenGodsCard({ card, model }: TenGodsCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const [comboOpen, setComboOpen] = useState(false);
  const [openGod, setOpenGod] = useState<string | null>(null);
  const [openRelation, setOpenRelation] = useState<string | null>(null);
  const mobile = useMobileOpen();
  const canExpand = model.hidden.length > 0 || model.distribution.length > 0;

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-tg`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="ten-gods"
      data-expanded={expanded ? "true" : "false"}
      data-mobile-open={mobile.open ? "true" : "false"}
      data-tg-layout="consulting-v1"
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...vizDom(card.id)}
      {...mobileCardDom(card.id)}
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
        {model.available ? (
          <MobileToggle open={mobile.open} label="Xem chi tiết" onToggle={mobile.toggle} />
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-tg__empty" data-tg-empty="true">
          Chưa đủ dữ liệu Thập Thần.
        </p>
      ) : (
        <div data-mobile-body="true">
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
          {model.detailed.length ? (
            <section className="bte-tg__section" data-tg-section="detailed" data-viz-layer="visible">
              <h3 className="bte-tg__heading">Luận giải chi tiết</h3>
              <div className="bte-tg__detail-grid" data-tg-count={String(model.detailed.length)}>
                {model.detailed.map((item) => (
                  <DetailedCard
                    key={item.name}
                    item={item}
                    open={openGod === item.name}
                    onToggle={() =>
                      setOpenGod((current) => (current === item.name ? null : item.name))
                    }
                  />
                ))}
              </div>
            </section>
          ) : null}
          {model.relations.length ? (
            <section className="bte-tg__section" data-tg-section="relations" data-viz-layer="visible">
              <h3 className="bte-tg__heading">Quan hệ Thập Thần</h3>
              <div className="bte-tg__relation-list" data-tg-count={String(model.relations.length)}>
                {model.relations.map((item) => (
                  <RelationCard
                    key={item.name}
                    item={item}
                    open={openRelation === item.name}
                    onToggle={() =>
                      setOpenRelation((current) => (current === item.name ? null : item.name))
                    }
                  />
                ))}
              </div>
            </section>
          ) : null}
          {model.ecosystem ? (
            <section className="bte-tg__section" data-tg-section="ecosystem" data-viz-layer="visible">
              <h3 className="bte-tg__heading">Hệ Thập Thần</h3>
              <EcosystemSummary model={model.ecosystem} />
            </section>
          ) : null}
          {model.combination ? (
            <section className="bte-tg__section" data-tg-section="combination" data-viz-layer="visible">
              <h3 className="bte-tg__heading">Mô hình tạo giá trị</h3>
              <CombinationCard
                item={model.combination}
                open={comboOpen}
                onToggle={() => setComboOpen((value) => !value)}
              />
            </section>
          ) : null}
          {model.commercial.length ? (
            <section className="bte-tg__section" data-tg-section="commercial" data-viz-layer="visible">
              <h3 className="bte-tg__heading">Lộ rõ — giá trị thương mại</h3>
              <div className="bte-tg__consult-list" data-tg-count={String(model.commercial.length)}>
                {model.commercial.map((item) => (
                  <CommercialCard
                    key={item.name}
                    item={item}
                    open={openGod === item.name}
                    onToggle={() =>
                      setOpenGod((current) => (current === item.name ? null : item.name))
                    }
                  />
                ))}
              </div>
            </section>
          ) : null}
          <section className="bte-tg__section" data-tg-section="visible" data-viz-layer="visible">
            <h3 className="bte-tg__heading">Lộ rõ</h3>
            <PlacementList items={model.visible} showStem={expanded} />
          </section>
          {!expanded && model.hiddenNames.length ? (
            <section className="bte-tg__section" data-tg-section="hidden-summary" data-viz-layer="hidden">
              <h3 className="bte-tg__heading">Tàng Can hỗ trợ</h3>
              <p className="bte-tg__summary" data-tg-hidden-names="true">
                {model.hiddenNames.join(" · ")}
              </p>
              {model.hiddenSupport ? (
                <p className="bte-tg__summary" data-tg-combo-hidden="true">
                  {model.hiddenSupport}
                </p>
              ) : null}
            </section>
          ) : null}
          {expanded && model.hidden.length ? (
            <section className="bte-tg__section" data-tg-section="hidden" data-viz-layer="hidden">
              <h3 className="bte-tg__heading">Tàng Can hỗ trợ</h3>
              <PlacementList items={model.hidden} showStem />
              {model.hiddenSupport ? (
                <p className="bte-tg__summary" data-tg-combo-hidden="true">
                  {model.hiddenSupport}
                </p>
              ) : null}
            </section>
          ) : null}
          {expanded && model.distribution.length ? (
            <section className="bte-tg__section" data-tg-section="distribution" data-viz-layer="relation">
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
        </div>
      )}
    </article>
  );
}
