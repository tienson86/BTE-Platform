/**
 * Five Elements Card — NGŨ HÀNH. Structural distribution only.
 */

import type { ReactNode } from "react";
import type { DashboardCardSpec, FiveElementRowView, FiveElementsView } from "./types";
import { visualCardDom } from "./visualHierarchy";
import { vizDom } from "./vizCatalog";
import { MobileToggle, useMobileOpen } from "./mobile/MobileToggle";
import { mobileCardDom } from "./mobile/mobileOrder";

type FiveElementsCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: FiveElementsView;
};

function barPercent(count: number | null, peak: number): number {
  if (count == null || peak <= 0) return 0;
  return Math.max(0, Math.min(100, (count / peak) * 100));
}

function ChartRow({
  row,
  peak,
}: {
  readonly row: FiveElementRowView;
  readonly peak: number;
}): ReactNode {
  const value = row.count == null ? "" : String(row.count);
  const label = row.count == null ? row.label : `${row.label} ${row.count}`;
  return (
    <li className="bte-fe__row" data-element={row.key} data-fe-row={row.label}>
      <span className={`bte-fe__swatch bte-fe__fill--${row.key}`} aria-hidden="true" />
      <span className="bte-fe__name">{row.label}</span>
      <span className="bte-fe__track" aria-hidden="true">
        <span
          className={`bte-fe__fill bte-fe__fill--${row.key}`}
          style={{ width: `${barPercent(row.count, peak)}%` }}
        />
      </span>
      <span className="bte-fe__count" data-fe-count={row.key} aria-label={label}>
        {value}
      </span>
    </li>
  );
}

/**
 * Compact Five Elements distribution card. Chart plus exact counts.
 */
export function FiveElementsCard({ card, model }: FiveElementsCardProps): ReactNode {
  const peak = Math.max(0, ...model.rows.map((row) => row.count ?? 0));
  const mobile = useMobileOpen();
  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-fe`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="five-elements"
      data-mobile-open={mobile.open ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...vizDom(card.id)}
      {...mobileCardDom(card.id)}
    >
      <header className="bte-fe__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {model.balanceStatus ? (
          <p className="bte-fe__status" data-fe-status="true">
            {model.balanceStatus}
          </p>
        ) : model.available ? (
          <p className="bte-fe__heading" data-fe-heading="true">
            {model.sectionHeading}
          </p>
        ) : null}
        {model.available ? (
          <MobileToggle open={mobile.open} label="Xem chi tiết" onToggle={mobile.toggle} />
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-fe__empty" data-fe-empty="true">
          Chưa đủ dữ liệu Ngũ Hành.
        </p>
      ) : (
        <div data-mobile-body="true">
          <ul className="bte-fe__chart" data-fe-chart="bars" data-viz-chart="balance-bars">
            {model.rows.map((row) => (
              <ChartRow key={row.key} row={row} peak={peak} />
            ))}
          </ul>
          {model.comment ? (
            <p className="bte-fe__comment" data-fe-comment="true">
              {model.comment}
            </p>
          ) : null}
        </div>
      )}
    </article>
  );
}
