/**
 * BaZi Structure Card — BÁT TỰ detail. Presentation only. No interpretation.
 */

import type { ReactNode } from "react";
import type { BaziPillarView, BaziStructureView, DashboardCardSpec } from "./types";
import { visualCardDom } from "./visualHierarchy";
import { vizDom } from "./vizCatalog";
import { MobileToggle, useMobileOpen } from "./mobile/MobileToggle";
import { mobileCardDom } from "./mobile/mobileOrder";

type BaziCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: BaziStructureView;
};

function cellMeta(primary: string, secondary: string): ReactNode {
  if (!primary) return null;
  return (
    <>
      <span className="bte-bazi__value">{primary}</span>
      {secondary ? <span className="bte-bazi__meta">{secondary}</span> : null}
    </>
  );
}

function HiddenCell({ items }: { readonly items: BaziPillarView["hiddenStems"] }): ReactNode {
  if (!items.length) return null;
  return (
    <ul className="bte-bazi__hidden">
      {items.map((item) => (
        <li key={item.stem}>
          <span>{item.stem}</span>
          {item.tenGod ? <span className="bte-bazi__meta">{item.tenGod}</span> : null}
        </li>
      ))}
    </ul>
  );
}

function hasRow(pillars: readonly BaziPillarView[], read: (pillar: BaziPillarView) => boolean): boolean {
  return pillars.some(read);
}

/**
 * Four-pillar BaZi evidence table. Detail rows stay visible so it is not a Tứ Trụ summary.
 */
export function BaziCard({ card, model }: BaziCardProps): ReactNode {
  const pillars = model.pillars;
  const showNapAm = hasRow(pillars, (pillar) => Boolean(pillar.napAm));
  const showTenGod = hasRow(pillars, (pillar) => Boolean(pillar.tenGod));
  const showHidden = hasRow(pillars, (pillar) => pillar.hiddenStems.length > 0);
  const showStage = hasRow(pillars, (pillar) => Boolean(pillar.truongSinh));
  const mobile = useMobileOpen();

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-bazi`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="bazi"
      data-bazi-model="detail"
      data-mobile-open={mobile.open ? "true" : "false"}
      aria-label={model.title}
      {...visualCardDom(card.id)}
      {...vizDom(card.id)}
      {...mobileCardDom(card.id)}
    >
      <header className="bte-bazi__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        <MobileToggle open={mobile.open} label="Xem chi tiết" onToggle={mobile.toggle} />
      </header>
      {!model.available ? (
        <p className="bte-bazi__empty" data-bazi-empty="true">
          Chưa đủ dữ liệu Bát Tự.
        </p>
      ) : (
        <div className="bte-bazi__scroll" data-viz-chart="structure" data-mobile-body="true">
          <table className="bte-bazi__table">
            <thead>
              <tr>
                <th scope="col" className="bte-bazi__corner" />
                {pillars.map((pillar) => (
                  <th
                    key={pillar.key}
                    scope="col"
                    data-pillar={pillar.key}
                    data-day-master={pillar.isDayMaster ? "true" : undefined}
                  >
                    <span className="bte-bazi__col-label">{pillar.label}</span>
                    {pillar.isDayMaster ? (
                      <span className="bte-bazi__day-master">Nhật Chủ</span>
                    ) : null}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr data-bazi-row="stem">
                <th scope="row">Thiên Can</th>
                {pillars.map((pillar) => (
                  <td
                    key={`stem-${pillar.key}`}
                    data-pillar={pillar.key}
                    data-bazi-field="stem"
                    data-day-master={pillar.isDayMaster ? "true" : undefined}
                  >
                    {cellMeta(
                      pillar.stem,
                      [pillar.stemElement, pillar.stemYinYang].filter(Boolean).join(" · "),
                    )}
                  </td>
                ))}
              </tr>
              <tr data-bazi-row="branch">
                <th scope="row">Địa Chi</th>
                {pillars.map((pillar) => (
                  <td key={`branch-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="branch">
                    {cellMeta(pillar.branch, pillar.branchElement)}
                  </td>
                ))}
              </tr>
              {showNapAm ? (
                <tr data-bazi-row="nap-am">
                  <th scope="row">Nạp Âm</th>
                  {pillars.map((pillar) => (
                    <td key={`nap-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="nap-am">
                      {pillar.napAm}
                    </td>
                  ))}
                </tr>
              ) : null}
              {showHidden ? (
                <tr data-bazi-row="hidden">
                  <th scope="row">Tàng Can</th>
                  {pillars.map((pillar) => (
                    <td key={`hidden-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="hidden">
                      <HiddenCell items={pillar.hiddenStems} />
                    </td>
                  ))}
                </tr>
              ) : null}
              {showTenGod ? (
                <tr data-bazi-row="ten-god">
                  <th scope="row">Thập Thần</th>
                  {pillars.map((pillar) => (
                    <td key={`god-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="ten-god">
                      {pillar.tenGod}
                    </td>
                  ))}
                </tr>
              ) : null}
              {showStage ? (
                <tr data-bazi-row="stage">
                  <th scope="row">Trường Sinh</th>
                  {pillars.map((pillar) => (
                    <td key={`stage-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="stage">
                      {pillar.truongSinh}
                    </td>
                  ))}
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      )}
    </article>
  );
}
