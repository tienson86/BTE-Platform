/**
 * ShenSha Card — THẦN SÁT. Customer items from the presentation adapter.
 */

import { useState, type ReactNode } from "react";
import { SHENSHA_FALLBACK_HEADING } from "./cards";
import type {
  DashboardCardSpec,
  ShenShaClusterView,
  ShenShaEcosystemView,
  ShenShaItemView,
  ShenShaView,
} from "./types";
import { visualCardDom } from "./visualHierarchy";
import { vizDom } from "./vizCatalog";
import { MobileToggle, useMobileOpen } from "./mobile/MobileToggle";
import { mobileCardDom } from "./mobile/mobileOrder";

const FEATURED_LIMIT = 4;

type ShenShaCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: ShenShaView;
};

function ItemBlock({ item }: { readonly item: ShenShaItemView }): ReactNode {
  return (
    <li className="bte-ss__item" data-ss-name={item.name}>
      <p className="bte-ss__name">{item.name}</p>
      {item.placement ? (
        <p className="bte-ss__meta" data-ss-placement="true">
          {item.placement}
        </p>
      ) : null}
      {item.meaning ? (
        <p className="bte-ss__meaning" data-ss-meaning="true">
          {item.meaning}
        </p>
      ) : null}
      {item.evidence ? (
        <p className="bte-ss__evidence" data-ss-evidence="true">
          {item.evidence}
        </p>
      ) : null}
    </li>
  );
}

function Pack07Star({
  item,
  open,
  onToggle,
}: {
  readonly item: ShenShaItemView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article
      className="bte-ss__star"
      data-ss-name={item.name}
      data-ss-open={open ? "true" : "false"}
    >
      <button type="button" className="bte-ss__star-toggle" aria-expanded={open} onClick={onToggle}>
        <span className="bte-ss__name">{item.name}</span>
        {item.stateLabel ? (
          <span className="bte-ss__chip" data-ss-state="true">
            {item.stateLabel}
          </span>
        ) : null}
      </button>
      {item.placement ? (
        <p className="bte-ss__meta" data-ss-placement="true">
          {item.placement}
        </p>
      ) : null}
      {item.category ? (
        <p className="bte-ss__meta" data-ss-category="true">
          {item.category}
        </p>
      ) : null}
      <div className="bte-ss__star-body" hidden={!open} data-ss-star-detail="true">
        {item.explanation ? (
          <p className="bte-ss__meaning" data-ss-meaning="true">
            {item.explanation}
          </p>
        ) : null}
      </div>
    </article>
  );
}

function ClusterRow({
  item,
  open,
  onToggle,
}: {
  readonly item: ShenShaClusterView;
  readonly open: boolean;
  readonly onToggle: () => void;
}): ReactNode {
  return (
    <article
      className="bte-ss__cluster"
      data-ss-cluster={item.name}
      data-ss-open={open ? "true" : "false"}
    >
      <button type="button" className="bte-ss__star-toggle" aria-expanded={open} onClick={onToggle}>
        <span className="bte-ss__name">{item.name}</span>
        {item.stateLabel ? <span className="bte-ss__chip">{item.stateLabel}</span> : null}
      </button>
      <div className="bte-ss__star-body" hidden={!open} data-ss-cluster-detail="true">
        {item.explanation ? <p className="bte-ss__meaning">{item.explanation}</p> : null}
      </div>
    </article>
  );
}

function EcosystemBlock({ model }: { readonly model: ShenShaEcosystemView }): ReactNode {
  const [openCluster, setOpenCluster] = useState<string | null>(null);
  return (
    <section className="bte-ss__section" data-ss-section="ecosystem">
      <h3 className="bte-ss__heading">Hệ Thần Sát</h3>
      <dl className="bte-ss__eco-grid">
        <div>
          <dt>Nhóm nổi bật</dt>
          <dd data-ss-dominant="true">
            {model.dominantUnresolved ? "Chưa đủ dữ liệu" : model.dominant || "Chưa đủ dữ liệu"}
          </dd>
        </div>
        <div>
          <dt>Nhóm hỗ trợ</dt>
          <dd data-ss-supporting="true">{model.supporting || "—"}</dd>
        </div>
        <div>
          <dt>Nhóm cảnh báo</dt>
          <dd data-ss-warning-group="true">{model.warning || "—"}</dd>
        </div>
        <div>
          <dt>Nhóm chưa đủ điều kiện</dt>
          <dd data-ss-unresolved-group="true">{model.unresolvedLabel || "—"}</dd>
        </div>
      </dl>
      {model.clusters.length ? (
        <div className="bte-ss__cluster-list" data-ss-clusters="true">
          {model.clusters.map((item) => (
            <ClusterRow
              key={item.name}
              item={item}
              open={openCluster === item.name}
              onToggle={() =>
                setOpenCluster((current) => (current === item.name ? null : item.name))
              }
            />
          ))}
        </div>
      ) : null}
    </section>
  );
}

/**
 * Supporting ShenSha card. Renders adapter-prepared customer items only.
 */
export function ShenShaCard({ card, model }: ShenShaCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const [openStar, setOpenStar] = useState<string | null>(null);
  const mobile = useMobileOpen();
  const extraItems = model.items.length > FEATURED_LIMIT;
  const canExpand = extraItems && !model.usePack07;
  const fallbackItems = expanded || model.grouped ? model.items : model.items.slice(0, FEATURED_LIMIT);

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-ss`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="shensha"
      data-expanded={expanded ? "true" : "false"}
      data-grouped={model.grouped ? "true" : "false"}
      data-ss-pack07={model.usePack07 ? "true" : undefined}
      data-mobile-open={mobile.open ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...vizDom(card.id)}
      {...mobileCardDom(card.id)}
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
        {model.available ? (
          <MobileToggle open={mobile.open} label="Xem chi tiết" onToggle={mobile.toggle} />
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-ss__empty" data-ss-empty="true">
          Chưa có dữ liệu Thần Sát.
        </p>
      ) : (
        <div data-mobile-body="true">
          {model.usePack07 ? (
            <>
              <section className="bte-ss__section" data-ss-section="stars">
                <h3 className="bte-ss__heading">Thần Sát hiện</h3>
                <div className="bte-ss__star-list" data-viz-chart="grouped-chips">
                  {model.items.map((item) => (
                    <Pack07Star
                      key={item.name}
                      item={item}
                      open={openStar === item.name}
                      onToggle={() =>
                        setOpenStar((current) => (current === item.name ? null : item.name))
                      }
                    />
                  ))}
                </div>
              </section>
              {model.ecosystem ? <EcosystemBlock model={model.ecosystem} /> : null}
            </>
          ) : model.grouped ? (
            <div className="bte-ss__groups" data-ss-section="groups">
              {model.groups.map((group) => (
                <section key={group.heading} className="bte-ss__group" data-ss-group={group.heading}>
                  <h3 className="bte-ss__heading">{group.heading}</h3>
                  <ul className="bte-ss__list" data-viz-chart="grouped-chips">
                    {group.items.map((item) => (
                      <ItemBlock key={item.name} item={item} />
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          ) : (
            <section className="bte-ss__section" data-ss-section="featured">
              <h3 className="bte-ss__heading">{SHENSHA_FALLBACK_HEADING}</h3>
              <ul className="bte-ss__list" data-viz-chart="grouped-chips">
                {fallbackItems.map((item) => (
                  <ItemBlock key={item.name} item={item} />
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
        </div>
      )}
    </article>
  );
}
